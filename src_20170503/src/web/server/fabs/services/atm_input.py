# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime,xlrd
from flask import json, g
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all

from ..base import utils
from ..model import D_ATM,CustHook,Branch 
import datetime


class Atm_inputService():
    """ Target Service  """

    def add_save(self,**kwargs):
        try:
            org_no = kwargs.get('org_no')
            addr = kwargs.get('addr')
            atm_no = kwargs.get('atm_no')
            typ = kwargs.get('typ')
            sub_typ = kwargs.get('sub_typ')
            status = kwargs.get('status')
            org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_no).all()
            print("org_no_value----%s")%org_no_value
            if not org_no_value:
                raise Exception(u"机构号不正确")
            atm_value=g.db_session.query(D_ATM).filter(D_ATM.atm_no==atm_no).all()
            today=datetime.date.today()
            if atm_value:
                raise Exception(u"机具编号已存在,不能添加")
            else:
                g.db_session.add(D_ATM(org_no=org_no,addr=addr,atm_no=atm_no,typ=typ,sub_typ=sub_typ,status=status))
                if typ in ('存取','取'):
                    typ='ATM'
                else:
                    pass

                g.db_session.add(CustHook(manager_no=org_no,org_no=org_no,percentage=100,hook_type='管户',start_date=today.strftime('%Y%m%d'),end_date=20991231,status='待手工',etl_date=today.strftime('%Y%m%d'),src='存量导入',typ='机具',cust_no=atm_no,cust_in_no=atm_no,note=addr,sub_typ=typ))
                return u'添加成功'
        except Exception,e:
            print "Exception",e
            return str(e)

    def edit_save(self,**kwargs):
        try:
            item_id = kwargs.get('item_id')
            org_no = kwargs.get('org_no')
            addr = kwargs.get('addr')
            atm_no = kwargs.get('atm_no')
            typ = kwargs.get('typ')
            sub_typ = kwargs.get('sub_typ')
            status = kwargs.get('status')
            end_date = kwargs.get('end_date')
            today=datetime.date.today()
            org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_no).all()
            if not org_no_value:
                raise Exception(u"机构号不正确")
            g.db_session.query(D_ATM).filter(D_ATM.id==item_id).update({D_ATM.org_no:org_no,D_ATM.addr:addr,D_ATM.atm_no:atm_no,D_ATM.typ:typ,D_ATM.sub_typ:sub_typ,D_ATM.status:status,D_ATM.end_date:end_date})

            if typ in('存取','取'):
                typ='ATM'
            else:
                pass
            g.db_session.query(CustHook).filter(CustHook.cust_no==atm_no).update({CustHook.manager_no:org_no,CustHook.org_no:org_no,CustHook.start_date:today.strftime('%Y%m%d'),CustHook.end_date:end_date,CustHook.etl_date:today.strftime('%Y%m%d'),CustHook.note:addr,CustHook.sub_typ:typ})

            return u'修改成功'
        except Exception,e:
            print "Exception",e
            return str(e)




    def upload(self, filepath):
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
             if nrows in [0,1]:
                raise Exception(u"警告:文件为空")
        except Exception,e:
            return str(e)

        for r in range(1,nrows):
            try:
                atm_no = str(sheet.cell(r,1).value)
                typ = str(sheet.cell(r,2).value)
                sub_typ = str(sheet.cell(r,3).value)
                addr = str(sheet.cell(r,4).value)
                org_no = str(sheet.cell(r,0).value)
                if org_no.strip()=='':
                    raise Exception(u'请填写认定机构')
                if atm_no.strip()=='':
                    raise Exception(u'请填写机具编号')
                if addr.strip()=='':
                    raise Exception(u'请填写地址')
                if typ.strip()=='':
                    raise Exception(u'请填写机具类型')
                if sub_typ.strip()=='':
                    raise Exception(u'请填写附离')
                if org_no[-2:]=='.0':
                    org_no=org_no[:-2]
                if atm_no[-2:]=='.0':
                    atm_no=atm_no[:-2]
                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_no).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")
                atm_value=g.db_session.query(D_ATM).filter(D_ATM.atm_no==atm_no).all()
                if atm_value:
                    raise Exception(u"机具编号已存在,不能添加")
                temp = {'atm_no':atm_no, 
                        'typ':typ, 
                        'sub_typ':sub_typ, 
                        'addr':addr, 
                        'org_no':org_no,
                        'status':'正常'
                }                
                if typ in ('存取','取'):
                    typ='ATM'
                temp2 = {
                    'manager_no':org_no,
                    'org_no':org_no,
                    'percentage':100,
                    'hook_type':'管户',
                    'start_date':today.strftime('%Y%m%d'),
                    'end_date':20991231,
                    'status':'待手工',
                    'etl_date':today.strftime('%Y%m%d'),
                    'src':'excel导入',
                    'typ':'机具',
                    'cust_no':atm_no,
                    'cust_in_no':atm_no,
                    'note':addr,
                    'sub_typ':typ
                }
                #print temp
                g.db_session.add(D_ATM(**temp))        
                g.db_session.add(CustHook(**temp2))        
            except Exception,e:    
                g.db_session.rollback()
                print Exception,':',e
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        return u'导入成功'
