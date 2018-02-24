# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime
from flask import json, g,current_app
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all
import xlrd
from ..base import utils
from ..model import Branch,Menu,User,UserBranch,PUHUI_BRANCH_TARGET_HANDER as hUIPU_bRANCH,REPORT_CREDIT_VILLAGNUM  
import os, time, random,sys
from decimal import Decimal
from datetime import datetime,timedelta

class huiPuBranchTarGetHander():
       
    '''支行目标任务手工'''
    def branchhander_save(self,**kwargs):
        nsd =  kwargs.get('newdata')
        nsd["date_id"]=int(nsd["date_id"])
        
        org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==nsd["org_code"]).all()
        if not org_no_value:
            raise Exception(u"机构号不正确")
        counter_work=g.db_session.query(hUIPU_bRANCH).filter(hUIPU_bRANCH.date_id==nsd["date_id"],hUIPU_bRANCH.org_code==nsd["org_code"]).first()
        
        if counter_work :
            raise Exception(u"该机构('%s')在('%d')年份已有值,若要修改,请去编辑"%(nsd["org_code"],nsd["date_id"]))
        else:
            g.db_session.add(hUIPU_bRANCH(**nsd))
        return u"添加成功" 

    def branchhander_update(self,**kwargs):
        nsd =  kwargs.get('newdata')
        nsd["date_id"]=int(nsd["date_id"])
        
        org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==nsd["org_code"]).all()
        if not org_no_value:
            raise Exception(u"机构号不正确")
        g.db_session.query(hUIPU_bRANCH).filter(hUIPU_bRANCH.id==nsd["id"]).update(nsd)
 
        return u"编辑成功"  
    def branchhander_upload(self,filepath,filename):
        try:
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            nrows = sheet.nrows
            if nrows in [0,1,2]:
                raise Exception(u"警告:文件为空")
        except Exception,e:
            return str(e)
        for r in range(2,nrows):
            try:
                date_id = str(int(sheet.cell(r,0).value))
                if str(sheet.cell(r,1).value)[0]=='M':
                    org_code=str(sheet.cell(r,1).value)
                else:
                    org_code= str(int(sheet.cell(r,1).value))
                org_name = sheet.cell(r,2).value
                farmersfile_targetper= Decimal(str(sheet.cell(r,3).value or 0))
                farmcredit_gradeper= Decimal(str(sheet.cell(r,4).value or 0))
                mincar_cusjudper= Decimal(str(sheet.cell(r,5).value or 0))
                huipu_fastcarper= Decimal(str(sheet.cell(r,6).value or 0))
                paln_objvilnum= int(Decimal(str(sheet.cell(r,7).value or 0)))
                cardcir_offaddnum= int(Decimal(str(sheet.cell(r,8).value or 0)))
                bumbus_addnum= int(Decimal(str(sheet.cell(r,9).value or 0)))
                yearplan_addloannum= int(Decimal(str(sheet.cell(r,10).value or 0)))
                creditloan_blanceper= Decimal(str(sheet.cell(r,11).value or 0))
                creditloan_pernumper= Decimal(str(sheet.cell(r,12).value or 0))
                remark=str(sheet.cell(r,13).value or "")
                if date_id =='' or len(date_id)!=4:
                    raise Exception(u'请填写日期,将其格式改为2016这样的样式')
                else:
                    date_id=int(date_id)
                if org_code.strip()=='':
                    raise Exception(u'请填写机构号')
                if org_name.strip()=="":
                    raise Exception(u'请填写机构名称')
                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_code).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")
                    
                nsd={
                'date_id':date_id,
                'org_code':org_code,
                'org_name':org_name,
                'farmersfile_targetper':farmersfile_targetper,
                'farmcredit_gradeper':farmcredit_gradeper,
                'mincar_cusjudper':mincar_cusjudper,
                'huipu_fastcarper':huipu_fastcarper,
                'paln_objvilnum':paln_objvilnum,
                'cardcir_offaddnum':cardcir_offaddnum,
                'bumbus_addnum':bumbus_addnum,
                'yearplan_addloannum':yearplan_addloannum,
                'creditloan_blanceper':creditloan_blanceper,
                'creditloan_pernumper':creditloan_pernumper,
                'remark':remark
                }
                nsd['org_name']=org_no_value[0].branch_name
                counter_work=g.db_session.query(hUIPU_bRANCH).filter(hUIPU_bRANCH.date_id==nsd["date_id"],hUIPU_bRANCH.org_code==nsd["org_code"]).first()
                if counter_work :
                    raise Exception(u"该机构('%s')在('%d')年份已有值,若要修改,请去编辑"%(nsd["org_code"],nsd["date_id"]))
                else:
                   g.db_session.add(hUIPU_bRANCH(**nsd))
            except Exception,e:
                g.db_session.rollback()
                print Exception,':',e
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        return u"添加成功" 

    '''整村授信手工'''

    def credit_save(self,**kwargs):
        nsd =  kwargs.get('newdata')
        nsd["syear"]=int(nsd["syear"])
        nsd["smonth"]=int(nsd["smonth"])
        org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==nsd["org_code"]).all()
        if not org_no_value:
            raise Exception(u"机构号不正确")
        counter_work=g.db_session.query(REPORT_CREDIT_VILLAGNUM).filter(REPORT_CREDIT_VILLAGNUM.syear==nsd["syear"],REPORT_CREDIT_VILLAGNUM.smonth==nsd["smonth"],REPORT_CREDIT_VILLAGNUM.org_code==nsd["org_code"]).first()
        
        if counter_work :
            raise Exception(u"该机构('%s')在('%d')年('%d')月已有值,若要修改,请去编辑"%(nsd["org_code"],nsd["syear"],nsd['smonth']))
        else:
            g.db_session.add(REPORT_CREDIT_VILLAGNUM(**nsd))
        return u"添加成功" 

    def credit_update(self,**kwargs):
        nsd =  kwargs.get('newdata')
        nsd["syear"]=int(nsd["syear"])
        nsd["smonth"]=int(nsd["smonth"])
        
        org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==nsd["org_code"]).all()
        if not org_no_value:
            raise Exception(u"机构号不正确")
        g.db_session.query(REPORT_CREDIT_VILLAGNUM).filter(REPORT_CREDIT_VILLAGNUM.id==nsd["id"]).update(nsd)
 
        return u"编辑成功"  
    def credit_upload(self,filepath,filename):
        try:
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            nrows = sheet.nrows
            if nrows in [0,1,2]:
                raise Exception(u"警告:文件为空")
        except Exception,e:
            return str(e)
        self.smonth_stand=['1','2','3','4','5','6','7','8','9','10','11',12]
        for r in range(2,nrows):
            try:
                syear= str(int(sheet.cell(r,0).value or 0))
                smonth=str(int(sheet.cell(r,1).value or 0))
                if str(sheet.cell(r,2).value)[0]=='M':
                    org_code=str(sheet.cell(r,2).value)
                else:
                    org_code= str(int(sheet.cell(r,2).value))
                org_name = sheet.cell(r,3).value
                report_creditvill_num= sheet.cell(r,4).value
                remark= str(sheet.cell(r,5).value or "")
                if syear=='' or len(syear)!=4 or syear=='0':
                    raise Exception(u'请填写年份,将其格式改为2016这样的样式')
                else:
                    syear=int(syear)
                if smonth=='' or smonth=='0' or (smonth not in self.smonth_stand):
                    raise Exception(u'月份未输入,或月份输入已错误')
                else:
                    smonth=int(smonth)
                if org_code.strip()=='':
                    raise Exception(u'请填写机构号')
                if org_name.strip()=="":
                    raise Exception(u'请填写机构名称')
                if report_creditvill_num=="" or report_creditvill_num==None:
                    raise Exception(u'请填写报告期已整村授信个数')
                else:
                    report_creditvill_num=int(report_creditvill_num)
                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_code).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")
                    
                nsd={
                'syear':syear,
                'smonth':smonth,
                'org_code':org_code,
                'org_name':org_name,
                'report_creditvill_num':report_creditvill_num,
                'remark':remark
                }
                nsd['org_name']=org_no_value[0].branch_name
                counter_work=g.db_session.query(REPORT_CREDIT_VILLAGNUM).filter(REPORT_CREDIT_VILLAGNUM.syear==nsd["syear"],REPORT_CREDIT_VILLAGNUM.smonth==nsd["smonth"],REPORT_CREDIT_VILLAGNUM.org_code==nsd["org_code"]).first()
                if counter_work :
                    raise Exception(u"该机构('%s')在('%d')年('%d')月已有值,若要修改,请去编辑"%(nsd["org_code"],nsd["syear"],nsd['smonth']))
                else:
                   g.db_session.add(REPORT_CREDIT_VILLAGNUM(**nsd))
            except Exception,e:
                g.db_session.rollback()
                print Exception,':',e
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        return u"添加成功" 
