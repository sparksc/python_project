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
from ..model.counter_work import COUNTER_EXAM_VOL,OCR_ORG_RATE_ERROR,OCR_SALE_RATE_ERROR,OCR_FIRST_ERROR,CASH_ERROR_RATE,COUNTER_REASON
import os, time, random,sys
from datetime import datetime,timedelta
from decimal import Decimal

class countExamBasevol():
    '''柜员业务量人数考核基础表'''
    def count_exam_base_vol_save(self,**kwargs):
        nsd =  kwargs.get('newdata')
        nsd["date_id"]=int(str(nsd["date_id"])[:6])

        org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==nsd["org_code"]).all()
        if not org_no_value:
            raise Exception(u"机构号不正确")
        counter_work=g.db_session.query(COUNTER_EXAM_VOL).filter(COUNTER_EXAM_VOL.date_id==nsd["date_id"],COUNTER_EXAM_VOL.org_code==nsd["org_code"]).first()
        
        if counter_work :
            raise Exception(u"该机构('%s')此月('%s')已有柜员业务量人数考核,若要修改,请去编辑"%(nsd["org_code"],nsd["date_id"]))
        else:
            g.db_session.add(COUNTER_EXAM_VOL(**nsd))
        return u"添加成功" 

    def count_exam_base_vol_update(self,**kwargs):
        nsd =  kwargs.get('newdata')
        nsd["date_id"]=int(str(nsd["date_id"])[:6])
        current_app.logger.debug(nsd)        
        org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==nsd["org_code"]).all()
        if not org_no_value:
            raise Exception(u"机构号不正确")
        g.db_session.query(COUNTER_EXAM_VOL).filter(COUNTER_EXAM_VOL.id==nsd["id"]).update(nsd)
 
        return u"编辑成功"  

    def count_exam_base_vol_delete(self,**kwargs):
        nsd =  kwargs.get('newdata')
        g.db_session.query(COUNTER_EXAM_VOL).filter(COUNTER_EXAM_VOL.id==nsd["id"]).delete()
 
        return u"删除成功" 
 
    def count_exam_base_vol_upload(self,filepath,filename):
        try:
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            nrows = sheet.nrows
            if nrows in [0,1,2]:
                raise Exception(u"警告:文件为空")
        except Exception,e:
            return str(e)
        souser = []
        for r in range(2,nrows):
            try:
                date_id = str(int(sheet.cell(r,0).value))
                if len(str(sheet.cell(r,1).value)) == 7:
                    org_code=str(sheet.cell(r,1).value)
                else:
                    org_code= str(int(sheet.cell(r,1).value))
                org_name = str(sheet.cell(r,2).value)
                asscount_cnt= Decimal(sheet.cell(r,3).value or 0)
                special_cnt=  Decimal(sheet.cell(r,4).value or 0)
                comcount_cnt= Decimal(sheet.cell(r,5).value or 0)
                discount_cnt= Decimal(sheet.cell(r,6).value or 0)
                mark=sheet.cell(r,7).value
                if date_id =='' or len(date_id)!=6:
                    raise Exception(u'请填写日期,将其格式改为201606这样的样式')
                else:
                    date_id=int(date_id)
                if org_code.strip()=='':
                    raise Exception(u'请填写机构号')
                if org_name.strip()=="":
                    raise Exception(u'请填写机构名称')
                if asscount_cnt< 0 or special_cnt<0 or comcount_cnt<0 or discount_cnt<0:
                    e = u'第'+str(r+1)+u'行人数不能为负数'
                    raise Exception(e)
                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_code).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")

                nsd={
                'date_id':date_id,
                'org_code':org_code,
                'org_name':org_name,
                'asscount_cnt':asscount_cnt,
                'special_cnt':special_cnt,
                'comcount_cnt':comcount_cnt,
                'discount_cnt':discount_cnt,
                'mark':mark
                }
                nsd['org_name']=org_no_value[0].branch_name
                key = str(date_id)+str(org_code)
                if key in souser:
                    raise Exception ( u'第'+str(r+1)+u'行,'+str(org_code)+u'机构号，excel中已存在，请勿重复导入')
                else:
                    souser.append(key)

                counter_work=g.db_session.query(COUNTER_EXAM_VOL).filter(COUNTER_EXAM_VOL.date_id==nsd["date_id"],COUNTER_EXAM_VOL.org_code==nsd["org_code"]).first()
                if counter_work :
                    raise Exception(u"该机构('%s')此月('%s')已有柜员业务量人数考核,若要修改,请去编辑"%(nsd["org_code"],nsd["date_id"]))
                else:
                   g.db_session.add(COUNTER_EXAM_VOL(**nsd))

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
                    return u'第'+str(r+1)+u'行有问题:'+'人数有非法字符'
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        return u"添加成功" 

    "OCR系统差错率机构排名情况"    
    def ocr_org_rate_error_upload(self,filepath,filename):
        try:
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            nrows = sheet.nrows
            if nrows in [0,1,2,3,4]:
                raise Exception(u"警告:文件为空")
        except Exception,e:
            return str(e)
        #sql_date="select distinct date_id from ocr_org_rate_error"
        #distinct_date=[]
        #sql_date=g.db_session.execute(sql_date).fetchall()
        #for i in sql_date:
        #    distinct_date.append(int(i[0]))
        souser = []
        for r in range(4,nrows):
            try:
                date_id = str(sheet.cell(r,0).value).replace(".00","").replace(".0","").strip()
                if len(str(sheet.cell(r,1).value)) == 7:
                    org_code=str(sheet.cell(r,1).value)
                else:
                    org_code= str(int(sheet.cell(r,1).value))
                org_name = str(sheet.cell(r,2).value)
                scan_bus_cnt= Decimal(sheet.cell(r,3).value or 0)
                inform_cnt=  Decimal(sheet.cell(r,4).value or 0)
                adjust_cnt= Decimal(sheet.cell(r,5).value or 0)
                total_cnt= Decimal(sheet.cell(r,6).value or 0)
                rete_error= Decimal(sheet.cell(r,7).value or 0)
                pai_rank= Decimal(sheet.cell(r,8).value or 0)
                if date_id =='' or len(date_id)!=6:
                    raise Exception(u'请填写日期,将其格式改为201606这样的样式')
                else:
                    date_id=int(date_id)
                if org_code.strip()=='':
                    raise Exception(u'请填写机构号')
                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_code).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")

                nsd={
                'date_id':date_id,
                'org_code':org_code,
                'org_name':org_name,
                'scan_bus_cnt':scan_bus_cnt,
                'inform_cnt':inform_cnt,
                'adjust_cnt':adjust_cnt,
                'total_cnt':total_cnt,
                'rete_error':rete_error,
                'pai_rank':pai_rank
                }
                #if nsd['date_id'] in distinct_date:
                #    raise Exception ( u'第'+str(r+1)+u'行,'+str(date_id)+u'月份的数据已存在,,请勿重复导入')
                nsd['org_name']=org_no_value[0].branch_name
                key = str(date_id)+str(org_code)
                if key in souser:
                    raise Exception ( u'第'+str(r+1)+u'行,'+str(org_code)+u'机构号，excel中已存在，请勿重复导入')
                else:
                    souser.append(key)
                counter_work=g.db_session.query(OCR_ORG_RATE_ERROR).filter(OCR_ORG_RATE_ERROR.date_id==nsd["date_id"],OCR_ORG_RATE_ERROR.org_code==nsd["org_code"]).first()
                if counter_work :
                    raise Exception(u"该机构('%s')此月('%s')已有数据"%(nsd["org_code"],nsd["date_id"]))
                else:
                    g.db_session.add(OCR_ORG_RATE_ERROR(**nsd))

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

    "OCR系统差错率柜员排名情况"    
    def ocr_sale_rate_error_upload(self,filepath,filename):
        try:
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            nrows = sheet.nrows
            if nrows in [0,1,2,3,4]:
                raise Exception(u"警告:文件为空")
        except Exception,e:
            return str(e)
        #sql_date="select distinct date_id from ocr_sale_rate_error"
        #distinct_date=[]
        #sql_date=g.db_session.execute(sql_date).fetchall()
        #for i in sql_date:
        #    distinct_date.append(int(i[0]))
        f_user_dict={}
        f_user_sql="""select user_name,NAME from F_USER"""
        f_user_sql=g.db_session.execute(f_user_sql).fetchall()
        for i in f_user_sql:
            f_user_dict[i[0]]=i[1]
        souser = []
        for r in range(4,nrows):
            try:
                date_id = str(sheet.cell(r,0).value).replace(".00","").replace(".0","").strip()
                if len(str(sheet.cell(r,3).value)) == 7:
                    org_code=str(sheet.cell(r,3).value)
                else:
                    org_code= str(int(sheet.cell(r,3).value))
                org_name = str(sheet.cell(r,4).value)
                sale_code= str(sheet.cell(r,1).value).replace(".00","").replace(".0","").strip()
                sale_name= str(sheet.cell(r,2).value)
                scan_bus_cnt= Decimal(sheet.cell(r,5).value or 0)
                inform_cnt=  Decimal(sheet.cell(r,6).value or 0)
                adjust_cnt= Decimal(sheet.cell(r,7).value or 0)
                total_cnt= Decimal(sheet.cell(r,8).value or 0)
                rete_error= Decimal(sheet.cell(r,9).value or 0)
                pai_rank= Decimal(sheet.cell(r,10).value or 0)
                if date_id =='' or len(date_id)!=6:
                    raise Exception(u'请填写日期,将其格式改为201606这样的样式')
                else:
                    date_id=int(date_id)
                if org_code.strip()=='':
                    raise Exception(u'请填写机构号')
                if sale_code.strip()=="":
                    raise Exception(u'请填写员工号')
                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_code).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")
                if sale_code in f_user_dict:
                    sale_name=f_user_dict.get(sale_code)
                else:
                    raise Exception(u'此'+str(sale_code)+"柜员号不存在")
                nsd={
                'date_id':date_id,
                'sale_code':sale_code,
                'sale_name':sale_name,
                'org_code':org_code,
                'org_name':org_name,
                'scan_bus_cnt':scan_bus_cnt,
                'inform_cnt':inform_cnt,
                'adjust_cnt':adjust_cnt,
                'total_cnt':total_cnt,
                'rete_error':rete_error,
                'pai_rank':pai_rank
                }
                #if nsd['date_id'] in distinct_date:
                #    raise Exception ( u'第'+str(r+1)+u'行,'+str(date_id)+u'月份的数据已存在,,请勿重复导入')
                nsd['org_name']=org_no_value[0].branch_name
                key = str(date_id)+str(org_code)+str(sale_code)
                if key in souser:
                    raise Exception ( u'第'+str(r+1)+u'行,'+str(org_code)+u'机构号'+str(sale_code)+'员工号，excel中已存在，请勿重复导入')
                else:
                    souser.append(key)
                counter_work=g.db_session.query(OCR_SALE_RATE_ERROR).filter(OCR_SALE_RATE_ERROR.date_id==nsd["date_id"],OCR_SALE_RATE_ERROR.org_code==nsd["org_code"],OCR_SALE_RATE_ERROR.sale_code==nsd["sale_code"]).first()
                if counter_work :
                    raise Exception(u"该机构('%s')此月('%s')柜员('%s')已有数据"%(nsd["org_code"],nsd["date_id"],nsd["sale_code"]))
                else:
                    g.db_session.add(OCR_SALE_RATE_ERROR(**nsd))

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

    "OCR系统一类差错率机构排名情况"    
    def ocr_first_error_upload(self,filepath,filename):
        try:
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            nrows = sheet.nrows
            if nrows in [0,1,2,3,4]:
                raise Exception(u"警告:文件为空")
        except Exception,e:
            return str(e)
        #sql_date="select distinct date_id from ocr_first_error"
        #distinct_date=[]
        #sql_date=g.db_session.execute(sql_date).fetchall()
        #for i in sql_date:
        #    distinct_date.append(int(i[0]))
        souser = []
        for r in range(4,nrows):
            try:
                date_id = str(sheet.cell(r,0).value).replace(".00","").replace(".0","").strip()
                if len(str(sheet.cell(r,1).value)) == 7:
                    org_code=str(sheet.cell(r,1).value)
                else:
                    org_code= str(int(sheet.cell(r,1).value))
                org_name = str(sheet.cell(r,2).value)
                scan_bus_cnt= Decimal(sheet.cell(r,3).value or 0)
                inform_cnt=  Decimal(sheet.cell(r,4).value or 0)
                rete_error= Decimal(sheet.cell(r,5).value or 0)
                pai_rank= Decimal(sheet.cell(r,6).value or 0)
                if date_id =='' or len(date_id)!=6:
                    raise Exception(u'请填写日期,将其格式改为201606这样的样式')
                else:
                    date_id=int(date_id)
                if org_code.strip()=='':
                    raise Exception(u'请填写机构号')
                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_code).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")

                nsd={
                'date_id':date_id,
                'org_code':org_code,
                'org_name':org_name,
                'scan_bus_cnt':scan_bus_cnt,
                'inform_cnt':inform_cnt,
                'rete_error':rete_error,
                'pai_rank':pai_rank
                }
                #if nsd['date_id'] in distinct_date:
                #    raise Exception ( u'第'+str(r+1)+u'行,'+str(date_id)+u'月份的数据已存在,,请勿重复导入')
                nsd['org_name']=org_no_value[0].branch_name
                key = str(date_id)+str(org_code)
                if key in souser:
                    raise Exception ( u'第'+str(r+1)+u'行,'+str(org_code)+u'机构号，excel中已存在，请勿重复导入')
                else:
                    souser.append(key)

                counter_work=g.db_session.query(OCR_FIRST_ERROR).filter(OCR_FIRST_ERROR.date_id==nsd["date_id"],OCR_FIRST_ERROR.org_code==nsd["org_code"]).first()
                if counter_work :
                    raise Exception(u"该机构('%s')此月('%s')已有数据"%(nsd["org_code"],nsd["date_id"]))
                else: 
                    g.db_session.add(OCR_FIRST_ERROR(**nsd))

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

    "柜员上交清算中心现金清分整点差错情况"    
    def cash_error_rate_upload(self,filepath,filename):
        try:
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            nrows = sheet.nrows
            if nrows in [0,1,2,3,4]:
                raise Exception(u"警告:文件为空")
        except Exception,e:
            return str(e)
        f_user_dict={}
        f_user_sql="""select user_name,NAME from F_USER"""
        f_user_sql=g.db_session.execute(f_user_sql).fetchall()
        for i in f_user_sql:
            f_user_dict[i[0]]=i[1]
        souser = []
        for r in range(4,nrows):
            try:
                date_id = str(sheet.cell(r,0).value).replace(".00","").replace(".0","").strip()
                if len(str(sheet.cell(r,1).value)) == 7:
                    org_code=str(sheet.cell(r,1).value)
                else:
                    org_code= str(int(sheet.cell(r,1).value))
                org_name = str(sheet.cell(r,2).value)
                sale_code= str(sheet.cell(r,3).value).replace(".00","").replace(".0","").strip()
                sale_name= str(sheet.cell(r,4).value)
                long_cny= Decimal(sheet.cell(r,5).value or 0)
                long_cnt=  Decimal(sheet.cell(r,6).value or 0)
                short_cny= Decimal(sheet.cell(r,7).value or 0)
                short_cnt= Decimal(sheet.cell(r,8).value or 0)
                together_cny= Decimal(sheet.cell(r,9).value or 0)
                together_cnt= Decimal(sheet.cell(r,10).value or 0)
                false_cny= Decimal(sheet.cell(r,11).value or 0)
                false_cnt= Decimal(sheet.cell(r,12).value or 0)
                if date_id =='' or len(date_id)!=8:
                    raise Exception(u'请填写日期,将其格式改为20160630这样的样式')
                else:
                    date_id=int(date_id)
                if org_code.strip()=='':
                    raise Exception(u'请填写机构号')
                if sale_code.strip()=='':
                    raise Exception(u'请填写员工号')
                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_code).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")
                if sale_code in f_user_dict:
                    sale_name=f_user_dict.get(sale_code)
                else:
                    raise Exception(u'此'+str(sale_code)+"柜员号不存在")
                nsd={
                'date_id':date_id,
                'sale_code':sale_code,
                'sale_name':sale_name,
                'org_code':org_code,
                'org_name':org_name,
                'long_cny':long_cny,
                'long_cnt':long_cnt,
                'short_cny':short_cny,
                'short_cnt':short_cnt,
                'together_cny':together_cny,
                'together_cnt':together_cnt,
                'false_cny':false_cny,
                'false_cnt':false_cnt
                }
                time_correct=g.db_session.execute("select * from d_date where id =%s"%(nsd['date_id'])).fetchone()
                if not time_correct:
                    raise Exception ("日期错误")
                #if nsd['date_id'] in distinct_date:
                #    raise Exception ( u'第'+str(r+1)+u'行,'+str(date_id)+u'月份的数据已存在,,请勿重复导入')
                nsd['org_name']=org_no_value[0].branch_name
                key = str(date_id)+str(org_code)+str(sale_code)
                if key in souser:
                    raise Exception ( u'第'+str(r+1)+u'行,'+str(org_code)+u'机构号'+str(sale_code)+'员工号，excel中已存在，请勿重复导入')
                else:
                    souser.append(key)
                counter_work=g.db_session.query(CASH_ERROR_RATE).filter(CASH_ERROR_RATE.date_id==nsd["date_id"],CASH_ERROR_RATE.org_code==nsd["org_code"],CASH_ERROR_RATE.sale_code==nsd["sale_code"]).first()
                if counter_work :
                    raise Exception(u"该机构('%s')此月('%s')柜员('%s')已有数据"%(nsd["org_code"],nsd["date_id"],nsd["sale_code"]))
                else:
                    g.db_session.add(CASH_ERROR_RATE(**nsd))

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

    "柜员履职发现（阻止）重大差错或风险事故情况表"    
    def counter_reason_upload(self,filepath,filename):
        try:
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            nrows = sheet.nrows
            if nrows in [0,1,2,3,4]:
                raise Exception(u"警告:文件为空")
        except Exception,e:
            return str(e)
        f_user_dict={}
        f_user_sql="""select user_name,NAME from F_USER"""
        f_user_sql=g.db_session.execute(f_user_sql).fetchall()
        for i in f_user_sql:
            f_user_dict[i[0]]=i[1]
        souser = []
        for r in range(4,nrows):
            try:
                date_id = str(sheet.cell(r,0).value).replace(".00","").replace(".0","").strip()
                if len(str(sheet.cell(r,3).value)) == 7:
                    org_code=str(sheet.cell(r,3).value)
                else:
                    org_code= str(int(sheet.cell(r,3).value))
                org_name = str(sheet.cell(r,4).value)
                sale_code= str(sheet.cell(r,1).value).replace(".00","").replace(".0","").strip()
                sale_name= str(sheet.cell(r,2).value)
                mark= sheet.cell(r,5).value
                if date_id =='' or len(date_id)!=6:
                    raise Exception(u'请填写日期,将其格式改为201606这样的样式')
                else:
                    date_id=int(date_id)
                if org_code.strip()=='':
                    raise Exception(u'请填写机构号')
                if sale_code.strip()=='':
                    raise Exception(u'请填写员工号')
                if mark.strip()=='':
                    raise Exception(u'请填写具体描述事件')
                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_code).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")
                if sale_code in f_user_dict:
                    sale_name=f_user_dict.get(sale_code)
                else:
                    raise Exception(u'此'+str(sale_code)+"柜员号不存在")
                nsd={
                'date_id':date_id,
                'sale_code':sale_code,
                'sale_name':sale_name,
                'org_code':org_code,
                'org_name':org_name,
                'mark':mark
                }
                #if nsd['date_id'] in distinct_date:
                #    raise Exception ( u'第'+str(r+1)+u'行,'+str(date_id)+u'月份的数据已存在,,请勿重复导入')
                nsd['org_name']=org_no_value[0].branch_name
                key = str(date_id)+str(org_code)+str(sale_code)
                if key in souser:
                    raise Exception ( u'第'+str(r+1)+u'行,'+str(org_code)+u'机构号'+str(sale_code)+'员工号，excel中已存在，请勿重复导入')
                else:
                    souser.append(key)

                counter_work=g.db_session.query(COUNTER_REASON).filter(COUNTER_REASON.date_id==nsd["date_id"],COUNTER_REASON.org_code==nsd["org_code"],COUNTER_REASON.sale_code==nsd["sale_code"]).first()
                if counter_work :
                    raise Exception(u"该机构('%s')此月('%s')柜员('%s')已有数据"%(nsd["org_code"],nsd["date_id"],nsd["sale_code"]))
                else:
                    g.db_session.add(COUNTER_REASON(**nsd))

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


