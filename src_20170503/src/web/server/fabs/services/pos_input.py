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
from ..model import D_POS,CustHook,Branch 
import datetime


class Pos_inputService():
    """ Target Service  """

    def add_save(self,**kwargs):
        try:
            org_no = kwargs.get('org_no')
            merchant_name = kwargs.get('merchant_name')
            merchant_no = kwargs.get('merchant_no').strip()
            pos_no = kwargs.get('pos_no').strip()
            merchant_addr  = kwargs.get('merchant_addr')
            merchant_contract = kwargs.get('merchant_contract')
            merchant_tel = kwargs.get('merchant_tel')
            merchant_mob = kwargs.get('merchant_mob')
            install_date = kwargs.get('install_date')
            typ = kwargs.get('typ')
            status = kwargs.get('status')

            org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_no).all()
            if not org_no_value:
                raise Exception(u"机构号不正确")
                
            pos_value=g.db_session.query(D_POS).filter(D_POS.merchant_no==merchant_no,D_POS.pos_no==pos_no).all()
            if pos_value:
                raise Exception(u"POS已存在,不能添加")
            else:
                g.db_session.add(D_POS(org_no=org_no,merchant_name=merchant_name,merchant_no=merchant_no,pos_no=pos_no,\
                merchant_addr=merchant_addr,merchant_contract=merchant_contract,merchant_tel=merchant_tel,\
                merchant_mob=merchant_mob,install_date=install_date,typ=typ,status=status))
                g.db_session.add(CustHook(manager_no=org_no,org_no=org_no,percentage=100,hook_type='管户',start_date=install_date,end_date=20991231,\
                status='待手工',etl_date=install_date,src='存量导入',typ='POS',cust_no=merchant_no,cust_in_no=pos_no,note=merchant_addr,sub_typ=typ))
            return u'添加成功'
        except Exception,e:
            print type(e),Exception,'1111111111111111111111111111111111111111111111'
            return str(e)

    def edit_save(self,**kwargs):
        try:
            item_id = kwargs.get('item_id')
            org_no = kwargs.get('org_no')
            merchant_name = kwargs.get('merchant_name')
            merchant_no = kwargs.get('merchant_no')
            pos_no = kwargs.get('pos_no')
            merchant_addr  = kwargs.get('merchant_addr')
            merchant_contract = kwargs.get('merchant_contract')
            merchant_tel = kwargs.get('merchant_tel')
            merchant_mob = kwargs.get('merchant_mob')
            install_date = kwargs.get('install_date')
            typ = kwargs.get('typ')
            status = kwargs.get('status')
            end_date = kwargs.get('end_date')
            org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_no).all()
            if not org_no_value:
                raise Exception(u"机构号不正确")
            g.db_session.query(D_POS).filter(D_POS.id==item_id).update({D_POS.org_no:org_no,D_POS.merchant_name:merchant_name,\
                D_POS.merchant_no:merchant_no,D_POS.pos_no:pos_no,D_POS.merchant_addr:merchant_addr,D_POS.merchant_contract:merchant_contract,\
                D_POS.merchant_tel:merchant_tel,D_POS.merchant_mob:merchant_mob,D_POS.install_date:install_date,D_POS.typ:typ,D_POS.status:status,D_POS.end_date:end_date})
            return u'修改成功'
        except Exception,e:
            return str(e)




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
            if nrows in [0,1]:
                raise Exception(u"警告:文件为空")
            bill_type_sign = ""
            list = []
        except Exception,e:
            return str(e)
        for r in range(1,nrows):
            try:
                merchant_name = sheet.cell(r,0).value
                merchant_no = str(sheet.cell(r,1).value).replace('.0','')
                if (sheet.cell(r,2).value):
                    pos_no = str(sheet.cell(r,2).value).replace('.0','')
                else:
                    pos_no = ''
                merchant_addr = sheet.cell(r,3).value
                merchant_contract = sheet.cell(r,4).value
                merchant_tel = str(sheet.cell(r,5).value).replace('.0','')
                if isinstance((sheet.cell(r,6).value),float):
                    merchant_mob = str(int(sheet.cell(r,6).value))
                    print merchant_mob
                else :
                    merchant_mob = str(sheet.cell(r,6).value)

                if str(sheet.cell(r,9).value)[0]=='M':
                    org_no = str(sheet.cell(r,9).value)
                else:
                    org_no = str(int(sheet.cell(r,9).value))
                if (sheet.cell(r,7).value):
                    install_date = str(int(sheet.cell(r,7).value))
                else :
                    install_date = ''
                typ =sheet.cell(r,8).value 
                if org_no.strip()=='':
                    raise Exception(u'请填写认定机构')
                if pos_no.strip()=='':
                    raise Exception(u'请填写终端号')
                if merchant_no.strip()=='':
                    raise Exception(u'请填写商户编号')
                if merchant_addr.strip()=='':
                    raise Exception(u'请填写地址')
                if typ.strip()=='':
                    raise Exception(u'请填写机具类型')
                org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_no).all()
                if not org_no_value:
                    raise Exception(u"机构号不正确")

                temp = {'merchant_name':merchant_name, 
                        'merchant_no':merchant_no.strip(), 
                        'pos_no':pos_no.strip(), 
                        'merchant_addr':merchant_addr, 
                        'merchant_contract':merchant_contract, 
                        'merchant_tel':merchant_tel, 
                        'merchant_mob':merchant_mob, 
                        'org_no':org_no, 
                        'install_date':install_date,
                        'typ':typ,
                        'status':'正常'
                }
                temp2 = {
                    'manager_no':org_no,
                    'org_no':org_no,
                    'percentage':100,
                    'hook_type':'管户',
                    'start_date':install_date,
                    'end_date':20991231,
                    'status':'待手工',
                    'etl_date':today.strftime('%Y%m%d'),
                    'src':'excel导入',
                    'typ':'POS',
                    'cust_no':merchant_no.strip(),
                    'cust_in_no':pos_no.strip(),
                    'note':merchant_addr,
                    'sub_typ':typ
                }
                #print temp
                pos_value=g.db_session.query(D_POS).filter(D_POS.merchant_no==merchant_no.strip(),D_POS.pos_no==pos_no.strip()).all()

                if pos_value:
                     raise Exception(u"POS已存在,不能添加")
                else:     
                     g.db_session.add(D_POS(**temp))
                     g.db_session.add(CustHook(**temp2))
            except Exception,e:    
                g.db_session.rollback()
                print Exception,':',e
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        return u'导入成功'
