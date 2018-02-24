# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime,xlrd
from flask import json, g,current_app
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all

from ..base import utils
from ..model import REPORT_MANAGER_DEP,REPORT_MANAGER_LOAN,REPORT_MANAGER_CREDITCARD,REPORT_MANAGER_OTHER,CustHook,Branch,User 
import datetime
from decimal import *

class Staff_sal_inputService():
    """ Target Service  """

    def add_save(self,**kwargs):
        try:
            current_app.logger.debug('qqqq')
            custinfo = kwargs.get('custinfo_add')
            custinfo['DATE_ID']=int(custinfo['DATE_ID'])
            loan=kwargs.get('loan_add')
            ebank=kwargs.get('ebank_add')
            crad=kwargs.get('card_add')
            dep=kwargs.get('dep_add')
            if custinfo['DATE_ID']=='':
                raise Exception(u'请填写日期')
            if custinfo['ORG_CODE'].strip()=='':
                raise Exception(u'请填写机构号')
            if custinfo['ORG_NAME'].strip()=='':
                raise Exception(u'请机构名称')
            if custinfo['SALE_CODE'].strip()=='':
                raise Exception(u'请填写员工编号')
            if custinfo['SALE_NAME'].strip()=='':
                raise Exception(u'请填写员工名')
 

            for i in dep.keys():
                if dep[i].strip()=='' or dep[i]==None:
                    dep[i]=0
                else:
                    dep[i]=int(Decimal(dep[i])*100000000)

            current_app.logger.debug('qqqq')
            for i in loan.keys():
                if loan[i].strip()==''or loan[i]==None:
                    loan[i]=0
                else:
                    loan[i]=int(Decimal(loan[i])*100000000)
            
            for i in crad.keys():
                if crad[i].strip()=='' or crad[i]==None:
                    crad[i]=0
                else:
                    crad[i]=int(Decimal(crad[i]))
            current_app.logger.debug('ebank')
            for i in ebank.keys():
               if ebank[i].strip()=='':
                   ebank[i]=0
               else:
                   ebank[i]=int(Decimal(ebank[i])*100)
            org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==custinfo['ORG_CODE']).all()
            if not org_no_value:
                raise Exception(u"机构号不正确")
            user_value=g.db_session.query(User).filter(User.user_name==custinfo['SALE_CODE']).all()
            if not org_no_value:
                raise Exception(u"柜员号不正确")
            man_dep_value=g.db_session.query(REPORT_MANAGER_DEP).filter(REPORT_MANAGER_DEP.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_DEP.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_DEP.SALE_CODE==custinfo['SALE_CODE']).all()
            if man_dep_value:
                g.db_session.query(REPORT_MANAGER_DEP).filter(REPORT_MANAGER_DEP.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_DEP.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_DEP.SALE_CODE==custinfo['SALE_CODE']).update(dep)
            else:
                dep.update(custinfo)
                g.db_session.add(REPORT_MANAGER_DEP(**dep))

            man_loan_value=g.db_session.query(REPORT_MANAGER_LOAN).filter(REPORT_MANAGER_LOAN.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_LOAN.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_LOAN.SALE_CODE==custinfo['SALE_CODE']).all()
            if man_loan_value:
                g.db_session.query(REPORT_MANAGER_LOAN).filter(REPORT_MANAGER_LOAN.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_LOAN.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_LOAN.SALE_CODE==custinfo['SALE_CODE']).update(loan)
            else:
                loan.update(custinfo)
                g.db_session.add(REPORT_MANAGER_LOAN(**loan))

            man_card_value=g.db_session.query(REPORT_MANAGER_CREDITCARD).filter(REPORT_MANAGER_CREDITCARD.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_CREDITCARD.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_CREDITCARD.SALE_CODE==custinfo['SALE_CODE']).all()
            if man_card_value:
                g.db_session.query(REPORT_MANAGER_CREDITCARD).filter(REPORT_MANAGER_CREDITCARD.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_CREDITCARD.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_CREDITCARD.SALE_CODE==custinfo['SALE_CODE']).update(crad)
            else:
                crad.update(custinfo)
                g.db_session.add(REPORT_MANAGER_CREDITCARD(**crad))

            man_ebank_value=g.db_session.query(REPORT_MANAGER_OTHER).filter(REPORT_MANAGER_OTHER.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_OTHER.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_OTHER.SALE_CODE==custinfo['SALE_CODE']).all()
            if man_ebank_value:
                g.db_session.query(REPORT_MANAGER_OTHER).filter(REPORT_MANAGER_OTHER.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_OTHER.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_OTHER.SALE_CODE==custinfo['SALE_CODE']).update(ebank)
            else:
                ebank.update(custinfo)
                g.db_session.add(REPORT_MANAGER_OTHER(**ebank))



            return u'添加成功'
        except Exception,e:
            print type(e),Exception,'1111111111111111111111111111111111111111111111'
            return str(e)

    def edit_save(self,**kwargs):
        try:
            custinfo = kwargs.get('custinfo')
            custinfo['DATE_ID']=int(custinfo['DATE_ID'])
            loan=kwargs.get('loan')
            ebank=kwargs.get('ebank')
            crad=kwargs.get('card')
            dep=kwargs.get('dep')
            current_app.logger.debug(custinfo)
            for i in dep.keys():
                if dep[i].strip()=='':
                    dep[i]=0
                else:
                    dep[i]=int(Decimal(dep[i])*100000000)

            current_app.logger.debug('qqqq')
            for i in loan.keys():
                if loan[i].strip()=='':
                    loan[i]=0
                else:
                    loan[i]=int(Decimal(loan[i])*100000000)

            for i in crad.keys():
                if crad[i].strip()=='':
                    crad[i]=0
                else:
                    crad[i]=int(Decimal(crad[i]))
            current_app.logger.debug('ebank')

            for i in ebank.keys():
                if ebank[i].strip()=='':
                    ebank[i]=0
                else:
                    ebank[i]=int(Decimal(ebank[i])*100)

            org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==custinfo['ORG_CODE']).all()
            if not org_no_value:
                raise Exception(u"机构号不正确")
            user_value=g.db_session.query(User).filter(User.user_name==custinfo['SALE_CODE']).all()
            if not org_no_value:  
                raise Exception(u"柜员号不正确")


            man_dep_value=g.db_session.query(REPORT_MANAGER_DEP).filter(REPORT_MANAGER_DEP.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_DEP.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_DEP.SALE_CODE==custinfo['SALE_CODE']).all()
            if man_dep_value:
                g.db_session.query(REPORT_MANAGER_DEP).filter(REPORT_MANAGER_DEP.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_DEP.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_DEP.SALE_CODE==custinfo['SALE_CODE']).update(dep)
            else:
                dep.update(custinfo)
                g.db_session.add(REPORT_MANAGER_DEP(**dep))

            man_loan_value=g.db_session.query(REPORT_MANAGER_LOAN).filter(REPORT_MANAGER_LOAN.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_LOAN.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_LOAN.SALE_CODE==custinfo['SALE_CODE']).all()
            if man_loan_value:
                g.db_session.query(REPORT_MANAGER_LOAN).filter(REPORT_MANAGER_LOAN.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_LOAN.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_LOAN.SALE_CODE==custinfo['SALE_CODE']).update(loan)
            else:
                loan.update(custinfo)
                g.db_session.add(REPORT_MANAGER_LOAN(**loan))

            man_card_value=g.db_session.query(REPORT_MANAGER_CREDITCARD).filter(REPORT_MANAGER_CREDITCARD.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_CREDITCARD.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_CREDITCARD.SALE_CODE==custinfo['SALE_CODE']).all()
            if man_card_value:
                g.db_session.query(REPORT_MANAGER_CREDITCARD).filter(REPORT_MANAGER_CREDITCARD.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_CREDITCARD.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_CREDITCARD.SALE_CODE==custinfo['SALE_CODE']).update(crad)
            else:
                crad.update(custinfo)
                g.db_session.add(REPORT_MANAGER_CREDITCARD(**crad))

            man_ebank_value=g.db_session.query(REPORT_MANAGER_OTHER).filter(REPORT_MANAGER_OTHER.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_OTHER.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_OTHER.SALE_CODE==custinfo['SALE_CODE']).all()
            if man_ebank_value:
                g.db_session.query(REPORT_MANAGER_OTHER).filter(REPORT_MANAGER_OTHER.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_OTHER.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_OTHER.SALE_CODE==custinfo['SALE_CODE']).update(ebank)
            else:
                ebank.update(custinfo)
                g.db_session.add(REPORT_MANAGER_OTHER(**ebank))

            return u'修改成功'
        except Exception,e:
            return str(e)

    def sdelete(self,**kwargs):
        newdata =  kwargs.get('newdata')
        DATE_ID=int(newdata.get('DATE_ID'))
        ORG_CODE=newdata['ORG_CODE']
        SALE_CODE=newdata['SALE_CODE']
        current_app.logger.debug(newdata)
        g.db_session.query(REPORT_MANAGER_DEP).filter(REPORT_MANAGER_DEP.DATE_ID==DATE_ID,REPORT_MANAGER_DEP.ORG_CODE==ORG_CODE,REPORT_MANAGER_DEP.SALE_CODE==SALE_CODE).delete()
        g.db_session.query(REPORT_MANAGER_LOAN).filter(REPORT_MANAGER_LOAN.DATE_ID==DATE_ID,REPORT_MANAGER_LOAN.ORG_CODE==ORG_CODE,REPORT_MANAGER_LOAN.SALE_CODE==SALE_CODE).delete()
        g.db_session.query(REPORT_MANAGER_CREDITCARD).filter(REPORT_MANAGER_CREDITCARD.DATE_ID==DATE_ID,REPORT_MANAGER_CREDITCARD.ORG_CODE==ORG_CODE,REPORT_MANAGER_CREDITCARD.SALE_CODE==SALE_CODE).delete()
        g.db_session.query(REPORT_MANAGER_OTHER).filter(REPORT_MANAGER_OTHER.DATE_ID==DATE_ID,REPORT_MANAGER_OTHER.ORG_CODE==ORG_CODE,REPORT_MANAGER_OTHER.SALE_CODE==SALE_CODE).delete()
        return(u'删除成功')
 

    def upload(self, filepath,filename):
        """
            批量录入
        """
        print '导入开始'
        try:

            current_app.logger.debug('aaaaaa')
            today=datetime.date.today()
            data = xlrd.open_workbook(filepath)
            current_app.logger.debug('11aaaaaa')
            sheet = data.sheet_by_index(0)
            current_app.logger.debug('22aaaaaa')
            #行
            nrows = sheet.nrows
            current_app.logger.debug('qqqqaaaaaa')
            current_app.logger.debug(nrows)
            if nrows in [0,1,2]:
                raise Exception(u"警告:文件为空")
            bill_type_sign = ""
            list = []
        except Exception,e:
            return str(e)
        for r in range(2,nrows):
            try:
                DATE_ID= sheet.cell(r,0).value
                ORG_CODE= sheet.cell(r,1).value
                ORG_NAME= sheet.cell(r,2).value
                SALE_CODE= sheet.cell(r,3).value
                SALE_NAME= sheet.cell(r,4).value
                '''存款'''
                LAST_AVG_SAL= sheet.cell(r,15).value
                ADD_AVG_SAL= sheet.cell(r,16).value
                '''贷款'''
                TOTAL_NUM_SAL= sheet.cell(r,18).value
                AVG_SAL= sheet.cell(r,19).value
                PRI_ADD_NUM_SAL= sheet.cell(r,20).value
                PUB_ADD_NUM_SAL= sheet.cell(r,21).value
                ADD_AVG_ASL= sheet.cell(r,22).value
                TWO_CARD_LOANRATE_SAL= sheet.cell(r,23).value
                ELEC_FILE_INFO_SAL= sheet.cell(r,24).value
                '''信用卡'''
                salary= sheet.cell(r,31).value
                '''电子银行'''
                MB_ADD_NUM_SAL= sheet.cell(r,36).value
                CB_ADD_NUM_SAL = sheet.cell(r,37).value
                EPAY_ADD_NUM_SAL= sheet.cell(r,28).value
                ADD_HIGH_POS_SAL= sheet.cell(r,29).value
                ADD_LOW_POS_SAL= sheet.cell(r,30).value
                FARM_SERV_SAL= sheet.cell(r,39).value
                ADD_THIRD_DEPO_SAL= sheet.cell(r,33).value
                ADD_ETC_NUM_SAL= sheet.cell(r,34).value
                BASE_PAY= sheet.cell(r,5).value
                POSITION_PAY= sheet.cell(r,6).value
                BRANCH_NET_SAL= sheet.cell(r,7).value
                MANAGE_BUS_SAL= sheet.cell(r,8).value
                WORK_QUALITY_SAL= sheet.cell(r,9).value
                HIG_CIV_QUAL_SAL= sheet.cell(r,10).value
                JOB_SAT_SAL= sheet.cell(r,11).value
                DAY_DEP_COMP_PER= sheet.cell(r,12).value
                DAY_DEP_SAL= sheet.cell(r,13).value
                DAY_DEP_SEC_FEN= sheet.cell(r,14).value
                CREDIT_POOL= sheet.cell(r,17).value
                INTER_SET_SAL= sheet.cell(r,25).value
                SALE_VOC_SAL= sheet.cell(r,26).value
                ADD_EFC_CURSAL= sheet.cell(r,27).value
                ADD_FUNON_SAL= sheet.cell(r,32).value
                PER_CAR_DANERSAL= sheet.cell(r,35).value
                BUM_HOM_SAL= sheet.cell(r,38).value
                OTHER_ACHI_SAL= sheet.cell(r,41).value
                COMPRE_SAL= sheet.cell(r,42).value
                LABOR_COMP_SAL= sheet.cell(r,43).value
                PROV_FUND_SAL= sheet.cell(r,44).value
                SAFE_FAN_SAL= sheet.cell(r,45).value
                ALL_RISK_SAL= sheet.cell(r,46).value
                BAD_LOAN_PERSAL= sheet.cell(r,47).value
                FTP_ACH_SAL= sheet.cell(r,48).value
                COUNT_COMPLE_SAL= sheet.cell(r,49).value
                COUNT_COP_SSAL= sheet.cell(r,50).value
                HP_FINA_SAL= sheet.cell(r,51).value
                OTHER_SPEC_SAL1= sheet.cell(r,52).value
                OTHER_SPEC_SAL2= sheet.cell(r,53).value
                OTHER_SPEC_SAL3= sheet.cell(r,54).value
                OTHER_SPEC_SAL4= sheet.cell(r,55).value
                OTHER_SPEC_SAL5= sheet.cell(r,56).value
                BRANCH_SECO_FEN1= sheet.cell(r,57).value
                BRANCH_SECO_FEN2= sheet.cell(r,58).value
                BRANCH_SECO_FEN3= sheet.cell(r,59).value
                BRANCH_SECO_FEN4= sheet.cell(r,60).value
                OTHER_ACH_WAGES= sheet.cell(r,61).value
                OVER_WORK_SAL= sheet.cell(r,62).value
                OTHER_SAL1_DUAN= sheet.cell(r,63).value
                OTHER_SAL2= sheet.cell(r,64).value
                OTHER_SAL3_WEI= sheet.cell(r,65).value
                OTHER_SAL4_KE= sheet.cell(r,66).value
                OTHER_SAL5_GE= sheet.cell(r,67).value
                OTHER_SAL6= sheet.cell(r,68).value
                OTHER_SAL7= sheet.cell(r,69).value
                OTHER_SAL8= sheet.cell(r,70).value
                QJ_BAD_LOAN_SAL= sheet.cell(r,40).value
                if DATE_ID.strip()=='' or len(DATE_ID)!=8:
                    raise Exception(u'请填写日期,将其格式改为20160630这样的样式')
                else:
                    DATE_ID=int(DATE_ID)
                if ORG_CODE.strip()=='':
                    raise Exception(u'请填写机构号')
                if ORG_NAME.strip()=='':
                    raise Exception(u'请机构名称')
                if SALE_CODE.strip()=='':
                    raise Exception(u'请填写员工编号')
                if SALE_NAME.strip()=='':
                    raise Exception(u'请填写员工名')
                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==ORG_CODE).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")
                user_value=g.db_session.query(User).filter(User.user_name==SALE_CODE).all()
                if not org_no_value:
                    raise Exception(u"柜员号不正确")

                custinfo={
                'DATE_ID':DATE_ID,
                'ORG_CODE':ORG_CODE,
                'ORG_NAME':ORG_NAME,
                'SALE_CODE':SALE_CODE,
                'SALE_NAME':SALE_NAME
                }

                
                dep={ 'LAST_AVG_SAL': LAST_AVG_SAL,
                      'ADD_AVG_SAL': ADD_AVG_SAL
                }
                loan={
                        'TOTAL_NUM_SAL':TOTAL_NUM_SAL,
                        'AVG_SAL':AVG_SAL,
                        'PRI_ADD_NUM_SAL':PRI_ADD_NUM_SAL,
                        'PUB_ADD_NUM_SAL':PUB_ADD_NUM_SAL,
                        'ADD_AVG_ASL':ADD_AVG_ASL,
                        'TWO_CARD_LOANRATE_SAL':TWO_CARD_LOANRATE_SAL,
                        'ELEC_FILE_INFO_SAL':ELEC_FILE_INFO_SAL
                }

                crad={
                       'SALARY':salary,
                }
                ebank={
                
                        'MB_ADD_NUM_SAL':MB_ADD_NUM_SAL,
                        'CB_ADD_NUM_SAL':CB_ADD_NUM_SAL,
                        'EPAY_ADD_NUM_SAL':EPAY_ADD_NUM_SAL,
                        'ADD_HIGH_POS_SAL':ADD_HIGH_POS_SAL,
                        'ADD_LOW_POS_SAL':ADD_LOW_POS_SAL,
                        'FARM_SERV_SAL':FARM_SERV_SAL,
                        'ADD_THIRD_DEPO_SAL':ADD_THIRD_DEPO_SAL,
                        'ADD_ETC_NUM_SAL':ADD_ETC_NUM_SAL,
                        'BASE_PAY':BASE_PAY,
                        'POSITION_PAY':POSITION_PAY,
                        'BRANCH_NET_SAL':BRANCH_NET_SAL,
                        'MANAGE_BUS_SAL':MANAGE_BUS_SAL,
                        'WORK_QUALITY_SAL':WORK_QUALITY_SAL,
                        'HIG_CIV_QUAL_SAL':HIG_CIV_QUAL_SAL,
                        'JOB_SAT_SAL':JOB_SAT_SAL,
                        'DAY_DEP_COMP_PER':DAY_DEP_COMP_PER,
                        'DAY_DEP_SAL':DAY_DEP_SAL,
                        'DAY_DEP_SEC_FEN':DAY_DEP_SEC_FEN,
                        'CREDIT_POOL':CREDIT_POOL,
                        'INTER_SET_SAL':INTER_SET_SAL,
                        'SALE_VOC_SAL':SALE_VOC_SAL,
                        'ADD_EFC_CURSAL':ADD_EFC_CURSAL,
                        'ADD_FUNON_SAL':ADD_FUNON_SAL,
                        'PER_CAR_DANERSAL':PER_CAR_DANERSAL,
                        'BUM_HOM_SAL':BUM_HOM_SAL,
                        'OTHER_ACHI_SAL':OTHER_ACHI_SAL,
                        'COMPRE_SAL':COMPRE_SAL,
                        'LABOR_COMP_SAL':LABOR_COMP_SAL,
                        'PROV_FUND_SAL':PROV_FUND_SAL,
                        'SAFE_FAN_SAL':SAFE_FAN_SAL,
                        'ALL_RISK_SAL':ALL_RISK_SAL,
                        'BAD_LOAN_PERSAL':BAD_LOAN_PERSAL,
                        'FTP_ACH_SAL':FTP_ACH_SAL,
                        'COUNT_COMPLE_SAL':COUNT_COMPLE_SAL,
                        'COUNT_COP_SSAL':COUNT_COP_SSAL,
                        'HP_FINA_SAL':HP_FINA_SAL,
                        'OTHER_SPEC_SAL1':OTHER_SPEC_SAL1,
                        'OTHER_SPEC_SAL2':OTHER_SPEC_SAL2,
                        'OTHER_SPEC_SAL3':OTHER_SPEC_SAL3,
                        'OTHER_SPEC_SAL4':OTHER_SPEC_SAL4,
                        'OTHER_SPEC_SAL5':OTHER_SPEC_SAL5,
                        'BRANCH_SECO_FEN1':BRANCH_SECO_FEN1,
                        'BRANCH_SECO_FEN2':BRANCH_SECO_FEN2,
                        'BRANCH_SECO_FEN3':BRANCH_SECO_FEN3,
                        'BRANCH_SECO_FEN4':BRANCH_SECO_FEN4,
                        'OTHER_ACH_WAGES':OTHER_ACH_WAGES,
                        'OVER_WORK_SAL':OVER_WORK_SAL,
                        'OTHER_SAL1_DUAN':OTHER_SAL1_DUAN,
                        'OTHER_SAL2':OTHER_SAL2,
                        'OTHER_SAL3_WEI':OTHER_SAL3_WEI,
                        'OTHER_SAL4_KE':OTHER_SAL4_KE,
                        'OTHER_SAL5_GE':OTHER_SAL5_GE,
                        'OTHER_SAL6':OTHER_SAL6,
                        'OTHER_SAL7':OTHER_SAL7,
                        'OTHER_SAL8':OTHER_SAL8,
                        'QJ_BAD_LOAN_SAL':QJ_BAD_LOAN_SAL
                }
                current_app.logger.debug('qqqq')
                for i in dep.keys():
                    if dep[i].strip()=='':
                        dep[i]=0
                    else:
                        dep[i]=int(Decimal(dep[i])*100000000)

                current_app.logger.debug('qqqq')
                for i in loan.keys():
                    if loan[i].strip()=='':
                        loan[i]=0
                    else:
                        loan[i]=int(Decimal(loan[i])*100000000)

                for i in crad.keys():
                    if crad[i].strip()=='':
                        crad[i]=0
                    else:
                        crad[i]=int(Decimal(crad[i]))
                current_app.logger.debug('ebank')

                for i in ebank.keys():
                    if ebank[i].strip()=='':
                        ebank[i]=0
                    else:
                        ebank[i]=int(Decimal(ebank[i])*100)
                current_app.logger.debug('qqqqaaaa')
                #print temp
                man_dep_value=g.db_session.query(REPORT_MANAGER_DEP).filter(REPORT_MANAGER_DEP.DATE_ID==DATE_ID,REPORT_MANAGER_DEP.ORG_CODE==ORG_CODE,REPORT_MANAGER_DEP.SALE_CODE==SALE_CODE).all()
                if man_dep_value:
                    g.db_session.query(REPORT_MANAGER_DEP).filter(REPORT_MANAGER_DEP.DATE_ID==DATE_ID,REPORT_MANAGER_DEP.ORG_CODE==ORG_CODE,REPORT_MANAGER_DEP.SALE_CODE==SALE_CODE).update(dep)
                else :
                    dep.update(custinfo)
                    g.db_session.add(REPORT_MANAGER_DEP(**dep))

                man_loan_value=g.db_session.query(REPORT_MANAGER_LOAN).filter(REPORT_MANAGER_LOAN.DATE_ID==DATE_ID,REPORT_MANAGER_LOAN.ORG_CODE==ORG_CODE,REPORT_MANAGER_LOAN.SALE_CODE==SALE_CODE).all()
                if man_loan_value:
                    g.db_session.query(REPORT_MANAGER_LOAN).filter(REPORT_MANAGER_LOAN.DATE_ID==DATE_ID,REPORT_MANAGER_LOAN.ORG_CODE==ORG_CODE,REPORT_MANAGER_LOAN.SALE_CODE==SALE_CODE).update(loan)

                else:
                    loan.update(custinfo)
                    g.db_session.add(REPORT_MANAGER_LOAN(**loan))

                man_card_value=g.db_session.query(REPORT_MANAGER_CREDITCARD).filter(REPORT_MANAGER_CREDITCARD.DATE_ID==DATE_ID,REPORT_MANAGER_CREDITCARD.ORG_CODE==ORG_CODE,REPORT_MANAGER_CREDITCARD.SALE_CODE==SALE_CODE).all()

                if man_card_value:
                    g.db_session.query(REPORT_MANAGER_CREDITCARD).filter(REPORT_MANAGER_CREDITCARD.DATE_ID==DATE_ID,REPORT_MANAGER_CREDITCARD.ORG_CODE==ORG_CODE,REPORT_MANAGER_CREDITCARD.SALE_CODE==SALE_CODE).update(crad)
                else:
                    crad.update(custinfo)
                    g.db_session.add(REPORT_MANAGER_CREDITCARD(**crad))
    
                man_ebank_value=g.db_session.query(REPORT_MANAGER_OTHER).filter(REPORT_MANAGER_OTHER.DATE_ID==DATE_ID,REPORT_MANAGER_OTHER.ORG_CODE==ORG_CODE,REPORT_MANAGER_OTHER.SALE_CODE==SALE_CODE).all()
                if man_ebank_value:
                    g.db_session.query(REPORT_MANAGER_OTHER).filter(REPORT_MANAGER_OTHER.DATE_ID==DATE_ID,REPORT_MANAGER_OTHER.ORG_CODE==ORG_CODE,REPORT_MANAGER_OTHER.SALE_CODE==SALE_CODE).update(ebank)
                else:
                    ebank.update(custinfo)
                    g.db_session.add(REPORT_MANAGER_OTHER(**ebank))

            except Exception,e:    
                g.db_session.rollback()
                print Exception,':',e
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        return u'导入成功'

            
