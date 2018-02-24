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
from ..model import REPORT_MANAGER_DEP,REPORT_MANAGER_LOAN,REPORT_MANAGER_CREDITCARD,REPORT_MANAGER_OTHER,REPORT_MANAGER_HZSAL,CustHook,Branch 
import datetime
from decimal import *

class Staff_sal_hzinputService():
    """ Target Service  """

    def add_save(self,**kwargs):
        try:
            current_app.logger.debug('qqqq')
            custinfo = kwargs.get('custinfo_add')
            custinfo['DATE_ID']=int(custinfo['DATE_ID'])
            sql="""
            select MONTHEND_ID from d_date where id=%s
            """%(custinfo['DATE_ID'])
            aa=g.db_session.execute(sql).fetchone()
            if custinfo['DATE_ID']!=int(aa[0]):
                raise Exception(u"未到月末,不能添加")
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
 
            org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==custinfo['ORG_CODE']).all()
            if not org_no_value:
                raise Exception(u"机构号不正确")
            for i in custinfo.keys():
                if i=='DATE_ID' or i=='ORG_CODE' or i=='SALE_CODE' or i=='ORG_NAME' or i=='SALE_NAME':
                    pass
                elif custinfo[i].strip()=='':
                    custinfo[i]=0
                else:
                    custinfo[i]=int(Decimal(custinfo[i])*100)
            current_app.logger.debug('qqqqaaaa')
            #print temp
            man_dep_value=g.db_session.query(REPORT_MANAGER_HZSAL).filter(REPORT_MANAGER_HZSAL.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_HZSAL.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_HZSAL.SALE_CODE==custinfo['SALE_CODE']).all()
            if man_dep_value:
                g.db_session.query(REPORT_MANAGER_HZSAL).filter(REPORT_MANAGER_HZSAL.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_HZSAL.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_HZSAL.SALE_CODE==custinfo['SALE_CODE']).update(custinfo)
            else :
                g.db_session.add(REPORT_MANAGER_HZSAL(**custinfo))

            return u'添加成功'
        except Exception,e:
            print type(e),Exception,'1111111111111111111111111111111111111111111111'
            return str(e)

    def edit_save(self,**kwargs):
        try:
            custinfo = kwargs.get('custinfo')
            custinfo['DATE_ID']=int(custinfo['DATE_ID'])

            org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==custinfo['ORG_CODE']).all()
            if not org_no_value:
                raise Exception(u"机构号不正确")
            for i in custinfo.keys():
                if i=='DATE_ID' or i=='ORG_CODE' or i=='SALE_CODE' or i=='ORG_NAME' or i=='SALE_NAME':
                    pass
                elif custinfo[i].strip()=='':
                    custinfo[i]=0
                else:
                    custinfo[i]=int(Decimal(custinfo[i])*100)
            current_app.logger.debug('qqqqaaaa')
            #print temp
            man_dep_value=g.db_session.query(REPORT_MANAGER_HZSAL).filter(REPORT_MANAGER_HZSAL.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_HZSAL.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_HZSAL.SALE_CODE==custinfo['SALE_CODE']).all()
            if man_dep_value:
                g.db_session.query(REPORT_MANAGER_HZSAL).filter(REPORT_MANAGER_HZSAL.DATE_ID==custinfo['DATE_ID'],REPORT_MANAGER_HZSAL.ORG_CODE==custinfo['ORG_CODE'],REPORT_MANAGER_HZSAL.SALE_CODE==custinfo['SALE_CODE']).update(custinfo)
            else :
                g.db_session.add(REPORT_MANAGER_HZSAL(**custinfo))


            return u'修改成功'
        except Exception,e:
            return str(e)

    def sdelete(self,**kwargs):
        newdata =  kwargs.get('newdata')
        DATE_ID=int(newdata.get('DATE_ID'))
        ORG_CODE=newdata['ORG_CODE']
        SALE_CODE=newdata['SALE_CODE']
        current_app.logger.debug(newdata)
        g.db_session.query(REPORT_MANAGER_HZSAL).filter(REPORT_MANAGER_HZSAL.DATE_ID==DATE_ID,REPORT_MANAGER_HZSAL.ORG_CODE==ORG_CODE,REPORT_MANAGER_HZSAL.SALE_CODE==SALE_CODE).delete()
        return(u'删除成功')
 

    def upload(self, filepath,filename):
        """
            批量录入
        """
        print '导入开始'
        try:

            today=datetime.date.today()
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            #行
            nrows = sheet.nrows
            current_app.logger.debug(nrows)
            if nrows in [0,1,2]:
                raise Exception(u"警告:文件为空")
            bill_type_sign = ""
            list = []
        except Exception,e:
            return str(e)
        for r in range(2,nrows):
            try:
                DATE_ID= str(int(sheet.cell(r,0).value))
                if str(sheet.cell(r,1).value)[0]=='M':
                    ORG_CODE=str(sheet.cell(r,1).value)
                else:
                    ORG_CODE= str(int(sheet.cell(r,1).value))
                ORG_NAME= sheet.cell(r,2).value
                SALE_CODE= str(int(sheet.cell(r,3).value))
                SALE_NAME= sheet.cell(r,4).value
                HZ_BASE_PAY= ''.join(str( sheet.cell(r,7).value).split(','))
                HZ_POSITION_PAY= ''.join(str( sheet.cell(r,8).value).split(','))
                HZ_NET_BUS_SAL= ''.join(str( sheet.cell(r,9).value).split(','))
                HZ_COMPRE_SAL= ''.join(str( sheet.cell(r,10).value).split(','))
                HZ_LABOR_COMP_SAL= ''.join(str( sheet.cell(r,11).value).split(','))
                HZ_PROV_FUND_SAL= ''.join(str( sheet.cell(r,12).value).split(','))
                HZ_SAFE_FAN_SAL= ''.join(str( sheet.cell(r,13).value).split(','))
                HZ_ALL_RISK_SAL= ''.join(str( sheet.cell(r,14).value).split(','))
                HZ_BAD_LOAN_PERSAL= ''.join(str( sheet.cell(r,15).value).split(','))
                HZ_FTP_ACH_SAL= ''.join(str( sheet.cell(r,16).value).split(','))
                HZ_COUNT_COMPLE_SAL= ''.join(str( sheet.cell(r,17).value).split(','))
                HZ_OTHER_SPEC_SAL1= ''.join(str( sheet.cell(r,18).value).split(','))
                HZ_OTHER_SPEC_SAL2= ''.join(str( sheet.cell(r,19).value).split(','))
                HZ_OTHER_SPEC_SAL3= ''.join(str( sheet.cell(r,20).value).split(','))
                HZ_OTHER_SPEC_SAL4= ''.join(str( sheet.cell(r,21).value).split(','))
                HZ_OTHER_SPEC_SAL5= ''.join(str( sheet.cell(r,22).value).split(','))
                HZ_OTHER_SAL1= ''.join(str( sheet.cell(r,23).value).split(','))
                HZ_OTHER_SAL2= ''.join(str( sheet.cell(r,24).value).split(','))
                HZ_OTHER_SAL3= ''.join(str( sheet.cell(r,25).value).split(','))
                HZ_OTHER_SAL4= ''.join(str( sheet.cell(r,26).value).split(','))
                HZ_OTHER_SAL5= ''.join(str( sheet.cell(r,27).value).split(','))


                current_app.logger.debug(DATE_ID)
                if DATE_ID.strip()=='' or len(DATE_ID)!=8:
                    raise Exception(u'请填写日期,将其格式改为20160630这样的样式')
                else:
                    DATE_ID=int(DATE_ID)
                sql="""
                select MONTHEND_ID from d_date where id=%s
                """%(DATE_ID)
                bb=g.db_session.execute(sql).fetchone()
                if DATE_ID!=int(bb[0]):
                    raise Exception(u"请保证日期都是月末")
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
                custinfo={
                'DATE_ID':DATE_ID,
                'ORG_CODE':ORG_CODE,
                'ORG_NAME':ORG_NAME,
                'SALE_CODE':SALE_CODE,
                'SALE_NAME':SALE_NAME,
                'HZ_BASE_PAY':HZ_BASE_PAY,
                'HZ_POSITION_PAY':HZ_POSITION_PAY,
                'HZ_NET_BUS_SAL':HZ_NET_BUS_SAL,
                'HZ_COMPRE_SAL':HZ_COMPRE_SAL,
                'HZ_LABOR_COMP_SAL':HZ_LABOR_COMP_SAL,
                'HZ_PROV_FUND_SAL':HZ_PROV_FUND_SAL,
                'HZ_SAFE_FAN_SAL':HZ_SAFE_FAN_SAL,
                'HZ_ALL_RISK_SAL':HZ_ALL_RISK_SAL,
                'HZ_BAD_LOAN_PERSAL':HZ_BAD_LOAN_PERSAL,
                'HZ_FTP_ACH_SAL':HZ_FTP_ACH_SAL,
                'HZ_COUNT_COMPLE_SAL':HZ_COUNT_COMPLE_SAL,
                'HZ_OTHER_SPEC_SAL1':HZ_OTHER_SPEC_SAL1,
                'HZ_OTHER_SPEC_SAL2':HZ_OTHER_SPEC_SAL2,
                'HZ_OTHER_SPEC_SAL3':HZ_OTHER_SPEC_SAL3,
                'HZ_OTHER_SPEC_SAL4':HZ_OTHER_SPEC_SAL4,
                'HZ_OTHER_SPEC_SAL5':HZ_OTHER_SPEC_SAL5,
                'HZ_OTHER_SAL1':HZ_OTHER_SAL1,
                'HZ_OTHER_SAL2':HZ_OTHER_SAL2,
                'HZ_OTHER_SAL3':HZ_OTHER_SAL3,
                'HZ_OTHER_SAL4':HZ_OTHER_SAL4,
                'HZ_OTHER_SAL5':HZ_OTHER_SAL5
                }

                for i in custinfo.keys():
                    if i=='DATE_ID' or i=='ORG_CODE' or i=='SALE_CODE' or i=='ORG_NAME' or i=='SALE_NAME':
                        pass
                    elif custinfo[i].strip()=='':
                        custinfo[i]=0
                    else:
                        custinfo[i]=int(Decimal(custinfo[i])*100)
                current_app.logger.debug('qqqqaaaa')
                #print temp
                man_dep_value=g.db_session.query(REPORT_MANAGER_HZSAL).filter(REPORT_MANAGER_HZSAL.DATE_ID==DATE_ID,REPORT_MANAGER_HZSAL.ORG_CODE==ORG_CODE,REPORT_MANAGER_HZSAL.SALE_CODE==SALE_CODE).all()
                if man_dep_value:
                    g.db_session.query(REPORT_MANAGER_HZSAL).filter(REPORT_MANAGER_HZSAL.DATE_ID==DATE_ID,REPORT_MANAGER_HZSAL.ORG_CODE==ORG_CODE,REPORT_MANAGER_HZSAL.SALE_CODE==SALE_CODE).update(custinfo)
                else :
                    g.db_session.add(REPORT_MANAGER_HZSAL(**custinfo))


            except Exception,e:    
                g.db_session.rollback()
                print Exception,':',e
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        return u'导入成功'
