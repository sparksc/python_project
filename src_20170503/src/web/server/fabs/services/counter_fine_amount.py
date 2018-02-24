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
from ..model import Branch,Menu,User,UserBranch,UserGroup,Group,D_DATE
from ..model.counter_work import REPORT_MANAGER_WORKQUALITY_HANDER as REPORT_HANDER
import os, time, random,sys
from datetime import datetime,timedelta

class CounterFineAmountService():
    '''柜员参与考核人数的手工维护'''
    def exam_save(self,**kwargs):
        nsd =  kwargs.get('newdata')
        nsd["date_id"]=int(nsd["date_id"])
        sql="""
         select MONTHEND_ID from d_date where id=%s
        """%(nsd["date_id"])
        aa=g.db_session.execute(sql).fetchone()
        if nsd["date_id"] != int(aa[0]):
            raise Exception(u"未到月末,不能添加")
        

        org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==nsd["org_code"]).all()
        if not org_no_value:
            raise Exception(u"机构号不正确")

        counter_work=g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"]).first()
        
        if counter_work :
            if counter_work.assess_man_num:
                raise Exception(u"该机构('%s')此刻已有参与考核人数(%s),若要修改,请去编辑"%(nsd["org_code"],counter_work.assess_man_num))

        exam_amount=g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"]).all()
        if exam_amount:
            g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"]).update({'assess_man_num':float(nsd["assess_man_num"])})
        else:
            g.db_session.add(REPORT_HANDER(**nsd))
        return u"添加成功" 

    def exam_update(self,**kwargs):
        nsd =  kwargs.get('newdata')
        nsd["date_id"]=int(nsd["date_id"])
        sql="""
         select MONTHEND_ID from d_date where id=%s
        """%(nsd["date_id"])
        aa=g.db_session.execute(sql).fetchone()
        if nsd["date_id"] != int(aa[0]):
            raise Exception(u"未到月末,不能添加")
        
        
        org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==nsd["org_code"]).all()
        if not org_no_value:
            raise Exception(u"机构号不正确")
        g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"]).update({'assess_man_num':float(nsd["assess_man_num"])})
 
        return u"编辑成功"  
    def exam_upload(self,filepath,filename):
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
                    org_code=str(sheet.cell(r,1).value)
                else:
                    org_code= str(int(sheet.cell(r,1).value))
                org_name = str(sheet.cell(r,2).value)
                assess_man_num= sheet.cell(r,3).value
                if date_id =='' or len(date_id)!=8:
                    raise Exception(u'请填写日期,将其格式改为20160630这样的样式')
                else:
                    date_id=int(date_id)
                if org_code.strip()=='':
                    raise Exception(u'请填写机构号')
                if org_name.strip()=="":
                    raise Exception(u'请填写机构名称')
                if assess_man_num ==None or assess_man_num=="":
                    raise Exception(u'请填写参与考核人数')
                if float(assess_man_num) < 0:
                    e = u'第'+str(r+1)+u'行参与考核人数不能为负数'
                    raise Exception(e)
                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_code).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")

                d = g.db_session.query(D_DATE).filter(D_DATE.ID == int(date_id)).first()
                if not d:
                    raise Exception(u'日期有误')

                sql="""
                select MONTHEND_ID from d_date where id=%s
                """%(date_id)
                bb=g.db_session.execute(sql).fetchone()
                if date_id!=int(bb[0]):
                    raise Exception(u"请保证日期都是月末")

                nsd={
                'date_id':date_id,
                'org_code':org_code,
                'org_name':org_name,
                'assess_man_num':float(assess_man_num)
                }
                nsd['org_name']=org_no_value[0].branch_name

                all_msg.append(nsd)
                key = str(date_id)+str(org_code)
                if key in souser:
                    raise Exception (u'第'+str(r+1)+u'行,'+str(org_code)+u'机构号，excel中已存在，请勿重复导入')
                else:
                    souser.append(key)

                counter_work=g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"]).first()
                if nsd['assess_man_num']<0:
                    raise Exception(u"考核人数不能为负")
                if counter_work :
                    if counter_work.assess_man_num:
                        raise Exception(u"第'%s'行该机构('%s')此刻已有参与考核人数(%s),若要修改,请去编辑"%(str(r+1),nsd["org_code"],counter_work.assess_man_num))
                
                exam_amount=g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"]).all()
                if exam_amount:
                   g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"]).update({'assess_man_num':nsd["assess_man_num"]})
                else:
                   g.db_session.add(REPORT_HANDER(**nsd))
            except ValueError, e:
                g.db_session.rollback()
                return u'第'+str(r + 1) + u'行有错误,'+u"请检查该行是否有值为空或包含非法字符"
            except IndexError,e:
                g.db_session.rollback()
                return u'第'+str(r+1)+u'行有错误,请检查列数'
            except Exception,e:
                g.db_session.rollback()
                print Exception,':',e
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        return u"添加成功" 
 
    '''柜员担任其他工作天数的手工维护'''
    def other_save(self,**kwargs):
        nsd =  kwargs.get('newdata')
        nsd["date_id"]=int(nsd["date_id"])
        sql="""
         select MONTHEND_ID from d_date where id=%s
        """%(nsd["date_id"])
        aa=g.db_session.execute(sql).fetchone()
        if nsd["date_id"] != int(aa[0]):
            raise Exception(u"未到月末,不能添加")
        

        org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==nsd["org_code"]).all()
        if not org_no_value:
            raise Exception(u"机构号不正确")
        user_value=g.db_session.query(User).filter(User.user_name==nsd["sale_code"]).all()
        if not user_value:
            raise Exception(u"柜员号不正确")

        org_user_sql="""
        select * from v_staff_info where  org='%s' and user_name='%s'
        """%(nsd["org_code"],nsd["sale_code"])
        
        org_user_val=g.db_session.execute(org_user_sql).fetchone()
        if not org_user_val:
            raise Exception(u"柜员号不在所属的机构")
        counter_work=g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"],REPORT_HANDER.sale_code==nsd["sale_code"]).first()
        
        if counter_work :
            if counter_work.work_days or counter_work.server_days:
                raise Exception(u"该柜员('%s')在此月已有工作日('%s')或担任天数('%s'),若要修改,请去编辑"%(nsd["sale_code"],float(counter_work.work_days) or 0,float(counter_work.server_days) or 0))

        nsd["work_days"]=float(nsd["work_days"])
        nsd["server_days"]=float(nsd["server_days"])
        other_amount=g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"],REPORT_HANDER.sale_code==nsd["sale_code"]).all()
        if other_amount:
            g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"],REPORT_HANDER.sale_code==nsd["sale_code"]).update({'work_days':nsd["work_days"],'server_days':nsd["server_days"]})
        else:
            g.db_session.add(REPORT_HANDER(**nsd))
        return u"添加成功" 

    def other_update(self,**kwargs):
        nsd =  kwargs.get('newdata')
        nsd["date_id"]=int(nsd["date_id"])
        sql="""
         select MONTHEND_ID from d_date where id=%s
        """%(nsd["date_id"])
        aa=g.db_session.execute(sql).fetchone()
        if nsd["date_id"] != int(aa[0]):
            raise Exception(u"未到月末,不能添加")
        
        org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==nsd["org_code"]).all()
        if not org_no_value:
            raise Exception(u"机构号不正确")
        user_value=g.db_session.query(User).filter(User.user_name==nsd["sale_code"]).all()
        if not user_value:
            raise Exception(u"柜员号不正确")
        nsd["work_days"]=float(nsd["work_days"])
        nsd["server_days"]=float(nsd["server_days"])
        g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.id==nsd["id"]).update({'work_days':nsd["work_days"],'server_days':nsd["server_days"]})
 
        return u"编辑成功"  
    def other_upload(self,filepath,filename):
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
                    org_code=str(sheet.cell(r,1).value)
                else:
                    org_code= str(int(sheet.cell(r,1).value))
                org_name = str(sheet.cell(r,2).value)
                sale_code = str(int(sheet.cell(r,3).value))
                sale_name = str(sheet.cell(r,4).value)
                work_days=  ''.join(str( sheet.cell(r,5).value).split(','))
                server_days=''.join(str( sheet.cell(r,6).value).split(','))
                if date_id =='' or len(date_id)!=8:
                    raise Exception(u'请填写日期,将其格式改为20160630这样的样式')
                else:
                    date_id=int(date_id)
                if org_code.strip()=='':
                    raise Exception(u'请填写机构号')
                if org_name.strip()=="":
                    raise Exception(u'请填写机构名称')
                if sale_code.strip()=="":
                    raise Exception(u'请填写员工编号')
                if sale_name.strip()=="":
                    raise Exception(u'请填写员工名')
                if work_days=="" or work_days==None:
                    raise Exception(u"请填写工作日")
                if server_days=="" or server_days==None:
                    raise Exception(u"请填写担任天数")
                if float(work_days) < 0:
                    e = u'第'+str(r+1)+u'行工作日不能为负数'
                    raise Exception(e)
                if float(server_days) < 0:
                    e = u'第'+str(r+1)+u'行担任天数不能为负数'
                    raise Exception(e)

                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_code).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")

                user_value=g.db_session.query(User).filter(User.user_name==sale_code).all()
                if not user_value:
                    raise Exception(u"柜员号不正确")

                d = g.db_session.query(D_DATE).filter(D_DATE.ID == int(date_id)).first()
                if not d:
                    raise Exception(u'日期有误')

                sql="""
                select MONTHEND_ID from d_date where id=%s
                """%(int(date_id))
                bb=g.db_session.execute(sql).fetchone()
                if date_id!=int(bb[0]):
                    raise Exception(u"请保证日期都是月末")

                nsd={
                'date_id':date_id,
                'org_code':org_code,
                'org_name':org_name,
                'sale_code':sale_code,
                'sale_name':sale_name,
                'work_days':float(work_days),
                'server_days':float(server_days)
                }

                all_msg.append(nsd)
                key = str(date_id)+str(org_code)+str(sale_code)
                if key in souser:
                    raise Exception ( u'第'+str(r+1)+u'行,'+str(sale_code)+u'柜员号，excel中已存在，请勿重复导入')
                else:
                    souser.append(key)

                org_user_sql="""
                select * from v_staff_info where  org='%s' and user_name='%s'
                """%(nsd["org_code"],nsd["sale_code"])
                
                org_user_val=g.db_session.execute(org_user_sql).fetchone()
                if not org_user_val:
                    raise Exception(u"柜员号不在所属的机构")
                nsd['org_name']=org_user_val.branch_name
                nsd['sale_name']=org_user_val.name
                if nsd['work_days']<0:
                    raise Exception(u"工作日不能为负")
                if nsd['server_days']<0:
                    raise Exception(u"担任天数不能为负")
 
                counter_work=g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"],REPORT_HANDER.sale_code==nsd["sale_code"]).first()
               
                if counter_work :
                    if counter_work.work_days or counter_work.server_days:
                        raise Exception(u"第'%s'行该柜员('%s')在此月已有工作日(%s)或担任天数(%s),若要修改,请去编辑"%(str(r+1),nsd["sale_code"],counter_work.work_days or 0,counter_work.server_days or 0))


                other_amount=g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"],REPORT_HANDER.sale_code==nsd["sale_code"]).all()
                if other_amount:
                   g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"],REPORT_HANDER.sale_code==nsd["sale_code"]).update({'work_days':nsd["work_days"],'server_days':nsd["server_days"]})
                else:
                   g.db_session.add(REPORT_HANDER(**nsd))
            except ValueError, e:
                g.db_session.rollback()
                return u'第'+str(r + 1) + u'行有错误,'+u"请检查该行是否有值为空或包含非法字符"
            except IndexError,e:
                g.db_session.rollback()
                return u'第'+str(r+1)+u'行有错误,请检查列数'
            except Exception,e:
                g.db_session.rollback()
                print Exception,':',e
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        return u"添加成功" 

    '''员工请假天数'''
    def lieve_save(self,**kwargs):
        nsd =  kwargs.get('newdata')
        nsd["date_id"]=int(nsd["date_id"])
        sql="""
         select MONTHEND_ID from d_date where id=%s
        """%(nsd["date_id"])
        aa=g.db_session.execute(sql).fetchone()
        if nsd["date_id"] != int(aa[0]):
            raise Exception(u"未到月末,不能添加")
        

        org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==nsd["org_code"]).all()
        if not org_no_value:
            raise Exception(u"机构号不正确")
        user_value=g.db_session.query(User).filter(User.user_name==nsd["sale_code"]).all()
        if not user_value:
            raise Exception(u"柜员号不正确")
        org_user_sql="""
        select * from v_staff_info where  org='%s' and user_name='%s'
        """%(nsd["org_code"],nsd["sale_code"])
        
        org_user_val=g.db_session.execute(org_user_sql).fetchone()
        if not org_user_val:
            raise Exception(u"柜员号不在所属的机构")
        counter_work=g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"],REPORT_HANDER.sale_code==nsd["sale_code"]).first()
        
        if counter_work :
            if counter_work.counter_lieve_days:
                raise Exception(u"该柜员('%s')在此月已有员工请假天数('%s'),若要修改,请去编辑"%(nsd["sale_code"],float(counter_work.counter_lieve_days)))


        nsd["counter_lieve_days"]=float(nsd["counter_lieve_days"])
        lieve_amount=g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"],REPORT_HANDER.sale_code==nsd["sale_code"]).all()
        if lieve_amount:
            g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"],REPORT_HANDER.sale_code==nsd["sale_code"]).update({'counter_lieve_days':nsd["counter_lieve_days"]})
        else:
            g.db_session.add(REPORT_HANDER(**nsd))
        return u"添加成功" 

    def lieve_update(self,**kwargs):
        nsd =  kwargs.get('newdata')
        nsd["date_id"]=int(nsd["date_id"])
        sql="""
         select MONTHEND_ID from d_date where id=%s
        """%(nsd["date_id"])
        aa=g.db_session.execute(sql).fetchone()
        if nsd["date_id"] != int(aa[0]):
            raise Exception(u"未到月末,不能添加")
        
        
        org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==nsd["org_code"]).all()
        if not org_no_value:
            raise Exception(u"机构号不正确")
        user_value=g.db_session.query(User).filter(User.user_name==nsd["sale_code"]).all()
        if not user_value:
            raise Exception(u"柜员号不正确")
        nsd["counter_lieve_days"]=float(nsd["counter_lieve_days"])
        g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.id==nsd["id"]).update({'counter_lieve_days':nsd["counter_lieve_days"]})
 
        return u"编辑成功"  
    def lieve_upload(self,filepath,filename):
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
                    org_code=str(sheet.cell(r,1).value)
                else:
                    org_code= str(int(sheet.cell(r,1).value))
                org_name = str(sheet.cell(r,2).value)
                sale_code = str(int(sheet.cell(r,3).value))
                sale_name = str(sheet.cell(r,4).value)
                counter_lieve_days=  ''.join(str( sheet.cell(r,5).value).split(','))
                if date_id =='' or len(date_id)!=8:
                    raise Exception(u'请填写日期,将其格式改为20160630这样的样式')
                else:
                    date_id=int(date_id)
                if org_code.strip()=='':
                    raise Exception(u'请填写机构号')
                if org_name.strip()=="":
                    raise Exception(u'请填写机构名称')
                if sale_code.strip()=="":
                    raise Exception(u'请填写员工编号')
                if sale_name.strip()=="":
                    raise Exception(u'请填写员工名')
                if counter_lieve_days=="" or counter_lieve_days==None:
                    raise Exception(u"请填写柜员请假天数")
                if float(counter_lieve_days) < 0:
                    e = u'第'+str(r+1)+u'行柜员请假天数不能为负数'
                    raise Exception(e)


                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_code).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")

                user_value=g.db_session.query(User).filter(User.user_name==sale_code).all()
                if not user_value:
                    raise Exception(u"柜员号不正确")

                d = g.db_session.query(D_DATE).filter(D_DATE.ID == int(date_id)).first()
                if not d:
                    raise Exception(u'日期有误')

                sql="""
                select MONTHEND_ID from d_date where id=%s
                """%(int(date_id))
                bb=g.db_session.execute(sql).fetchone()
                if date_id!=int(bb[0]):
                    raise Exception(u"请保证日期都是月末")

                nsd={
                'date_id':date_id,
                'org_code':org_code,
                'org_name':org_name,
                'sale_code':sale_code,
                'sale_name':sale_name,
                'counter_lieve_days':float(counter_lieve_days)
                }


                all_msg.append(nsd)
                key = str(date_id)+str(org_code)+str(sale_code)
                if key in souser:
                    raise Exception ( u'第'+str(r+1)+u'行,'+str(sale_code)+u'柜员号，excel中已存在，请勿重复导入')
                else:
                    souser.append(key)

                if nsd['counter_lieve_days']<0:
                    raise Exception(u"员工请假天数不能为负")

                org_user_sql="""
                select * from v_staff_info where  org='%s' and user_name='%s'
                """%(nsd["org_code"],nsd["sale_code"])
                
                org_user_val=g.db_session.execute(org_user_sql).fetchone()
                if not org_user_val:
                    raise Exception(u"柜员号不在所属的机构")
                nsd['org_name']=org_user_val.branch_name
                nsd['sale_name']=org_user_val.name
                counter_work=g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"],REPORT_HANDER.sale_code==nsd["sale_code"]).first()
                
                if counter_work :
                    if counter_work.counter_lieve_days:
                        raise Exception(u"第'%s'行该柜员('%s')在此月已有柜员请假天数('%s'),若要修改,请去编辑"%(str(r+1),nsd["sale_code"],counter_work.counter_lieve_days))
                 
                lieve_amount=g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"],REPORT_HANDER.sale_code==nsd["sale_code"]).all()
                if lieve_amount:
                   g.db_session.query(REPORT_HANDER).filter(REPORT_HANDER.date_id==nsd["date_id"],REPORT_HANDER.org_code==nsd["org_code"],REPORT_HANDER.sale_code==nsd["sale_code"]).update({'counter_lieve_days':nsd["counter_lieve_days"]})
                else:
                   g.db_session.add(REPORT_HANDER(**nsd))
            except ValueError, e:
                g.db_session.rollback()
                return u'第'+str(r + 1) + u'行有错误,'+u"请检查该行是否有值为空或包含非法字符"
            except IndexError,e:
                g.db_session.rollback()
                return u'第'+str(r+1)+u'行有错误,请检查列数'
            except Exception,e:
                g.db_session.rollback()
                print Exception,':',e
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        return u"添加成功" 
 
