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
from ..model import Branch,Menu,User,UserBranch
from ..model.counter_work import TELLER_VOLUME_ADJUST,OCR_ORG_RATE_ERROR,OCR_SALE_RATE_ERROR,OCR_FIRST_ERROR,CASH_ERROR_RATE,COUNTER_REASON
import os, time, random,sys
from datetime import datetime,timedelta
from decimal import Decimal

class teller_Ajust_base():
    '''柜员业务调整值'''
    def teller_V_Adjust_save(self,**kwargs):
        nsd =  kwargs.get('newdata')
        org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==nsd["child_org_code"]).all()
        if not org_no_value:
            raise Exception(u"机构号不正确")
        counter_work='''
        select * from teller_volume_adjust where left(DATE_ID,6)=%s and CHILD_ORG_CODE='%s' and TRAN_TELLER_CODE='%s'
        '''%(nsd["date_id"][:6],nsd["child_org_code"],nsd['tran_teller_code']) 
        counter_work_sql=g.db_session.execute(counter_work).fetchone()
        if counter_work_sql :
            raise Exception(u"该机构('%s')此月('%s')已有此柜员业务量调整值,若要修改,请去编辑"%(nsd["child_org_code"],nsd["date_id"][:6]))
        else:
            nsd["date_id"]=int(nsd["date_id"])
            nsd["adj_values"]=Decimal(nsd["adj_values"])
            g.db_session.add(TELLER_VOLUME_ADJUST(**nsd))
        return u"添加成功" 

    def teller_V_Adjust_update(self,**kwargs):
        nsd =  kwargs.get('newdata')
        org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==nsd["child_org_code"]).all()
        if not org_no_value:
            raise Exception(u"机构号不正确")
        g.db_session.query(TELLER_VOLUME_ADJUST).filter(TELLER_VOLUME_ADJUST.id==nsd["id"]).update(nsd)
 
        return u"编辑成功"  

    def teller_V_Adjust_delete(self,**kwargs):
        nsd =  kwargs.get('newdata')
        g.db_session.query(TELLER_VOLUME_ADJUST).filter(TELLER_VOLUME_ADJUST.id==nsd["id"]).delete()
 
        return u"删除成功" 
 
    def teller_V_Adjust_upload(self,filepath,filename):
        try:
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            nrows = sheet.nrows
            if nrows in [0,1,2]:
                raise Exception(u"警告:文件为空")
        except Exception,e:
            return str(e)
        all_msg = []
        souser = []
        for r in range(2,nrows):
            try:
                date_id = str(int(sheet.cell(r,0).value))
                if len(str(sheet.cell(r,1).value)) == 7:
                    child_org_code=str(sheet.cell(r,1).value).replace('.00',"").replace('.0',"").strip()
                else:
                    child_org_code= str(int(sheet.cell(r,1).value))
                child_org_name = str(sheet.cell(r,2).value)
                tran_teller_code =str(sheet.cell(r,3).value).replace('.00',"").replace('.0',"").strip()
                sale_name  =str(sheet.cell(r,4).value)
                adj_values= Decimal(sheet.cell(r,5).value)
                pst_season= str(sheet.cell(r,6).value)
                if date_id =='' or len(date_id)!=8:
                    raise Exception(u'请填写日期,将其格式改为20160630这样的样式')
                else:
                    date_id=int(date_id)
                if child_org_code.strip()=='':
                    raise Exception(u'请填写机构号')
                if tran_teller_code.strip()=="":
                    raise Exception(u'请填写员工号')
                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==child_org_code).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")

                nsd={
                'date_id':date_id,
                'child_org_code':child_org_code,
                'child_org_name':child_org_name,
                'tran_teller_code':tran_teller_code,
                'sale_name':sale_name,
                'adj_values':adj_values,
                'pst_season':pst_season
                }
                nsd['child_org_name']=org_no_value[0].branch_name
                org_user_sql="""
                select * from v_staff_info where  org='%s' and user_name='%s'
                """%(nsd["child_org_code"],nsd["tran_teller_code"])
                org_user_val=g.db_session.execute(org_user_sql).fetchone()
                if not org_user_val:
                    raise Exception(u"柜员号不在所属的机构")
                nsd['sale_name']=org_user_val.name
                key = str(date_id)[:6]+str(child_org_code)+str(tran_teller_code)
                if key in souser:
                    raise Exception ( u'第'+str(r+1)+u'行,'+str(child_org_code)+u'机构号，'+str(tran_teller_code)+'excel中该月已存在，请勿重复导入')
                else:
                    souser.append(key)
                counter_work='''
                select * from teller_volume_adjust where left(DATE_ID,6)=%s and CHILD_ORG_CODE='%s' and TRAN_TELLER_CODE='%s'
                '''%(str(nsd["date_id"])[:6],nsd["child_org_code"],nsd['tran_teller_code']) 
                counter_work_sql=g.db_session.execute(counter_work).fetchone()
                if counter_work_sql :
                    raise Exception(u"该机构('%s')此月('%s')已有此柜员('%s')业务量调整值,若要修改,请去编辑"%(nsd["child_org_code"],str(nsd["date_id"])[:6],nsd['tran_teller_code']))
                else:
                   g.db_session.add(TELLER_VOLUME_ADJUST(**nsd))

            except ValueError, e:
                g.db_session.rollback()
                return u'第'+str(r + 1) + u'行有错误,'+u"请检查该行是否有值为空或包含非法字符"
            except IndexError,e:
                g.db_session.rollback()
                return u'第'+str(r+1)+u'行有错误,请检查列数'
            except Exception,e:
                g.db_session.rollback()
                print Exception,':',e
                if str(e).split(':')[0]=='Invalid literal for Decimal':
                    return u'第'+str(r+1)+u'行有问题:'+'有非法字符'
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        return u"添加成功" 
