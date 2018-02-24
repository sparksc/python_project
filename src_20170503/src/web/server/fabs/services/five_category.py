# -*- coding: utf-8 -*-
"""
    yinsho.services.FiveService
    #####################
    yinsho LoanService module
"""
import hashlib, copy
from flask import json, g
from sqlalchemy import and_
from ..model.credit import *
from ..model.transaction import *
from ..model.application import *
from ..model.creditLevel import *
from ..workflow import task
from ..workflow.parameter import *
from ..database.sqlal import simple_session

import decimal
from decimal import Decimal
import datetime
import random

class FiveCategoryService():

    def save(self,**kwargs):
        u''' 五级分类数据暂存 '''
        lend_transaction=kwargs.get('lend_transaction')
        credit_level=kwargs.get('credit_level') 
        application=g.db_session.query(Application).join(ApplicationTransaction,ApplicationTransaction.application_id==Application.id).filter(ApplicationTransaction.transaction_id==lend_transaction.get('application_transaction_id')).first()
        app =Application(status=u'暂存',customer=application.customer,product_code='961')
        at = ApplicationTransaction(application=app,transaction_name=u"%s五级分类申请"%(application.customer.party.name)) 
        g.db_session.add(at)
        g.db_session.commit()
        credit_level.update({
                             'lend_transaction_id':lend_transaction.get('transaction_id'),
                              'application_transaction_id':at.transaction_id, 
                            })
        cate = CreditLevel(**credit_level)
        g.db_session.add(cate)
        return {'credit_level':cate}

    def update(self,Udata):
        u''' 五级分类信息更新 '''
        kwargs = Udata.get('kwargs')
        app_id = Udata.get('application_id')
        issue_date = kwargs.get('issue_date')[0:10] if kwargs.get('issue_date')!=None else None
        due_date = kwargs.get('due_date')[0:10] if kwargs.get('due_date')!=None else None
        extend_date = kwargs.get('extend_date')[0:10] if kwargs.get('extend_date')!=None else None
        kwargs.update({'issue_date':issue_date,'due_date':due_date,'extend_date':extend_date})
        Cate = g.db_session.query(FC_App).filter(FC_App.app_id==app_id)
        Cate.update(kwargs)
        g.db_session.commit()
        return {'success':True}

    def submit(self, **kwargs):
        u''' 五级分类申请提交 '''
        credit_level=kwargs.get('credit_level')
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"五级分类业务流程").first()
        cl=g.db_session.query(CreditLevel).filter(CreditLevel.id == credit_level.get('id')).first()
        at=cl.application_transaction
        start(at, start_activity) 
        g.db_session.query(Application).filter(Application.id == at.application_id).update({'status':u'调查'}) 
        return {'success':True}

    def save_submit(self,**kwargs):
        u''' 五级分类申请保存后提交 '''
        credit_level = self.save(**kwargs) 
        g.db_session.commit()
        credit_level=credit_level.get('credit_level')
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"五级分类业务流程").first()
        cl=g.db_session.query(CreditLevel).filter(CreditLevel.id == credit_level.id).first()
        at=cl.application_transaction
        start(at, start_activity)
        g.db_session.query(Application).filter(Application.id == at.application_id).update({'status':u'调查'})
        return {'credit_level':credit_level}

    def query(self, **kwargs):
        u''' 查询五级分类列表 '''
        q = g.db_session.query(CreditLevel).all()
        rst_list=[{'credit_level':r,'lend_transaction':r.lend_transaction,'party':r.lend_transaction.application_transaction.application.customer.party,'application':r.application_transaction.application,'product':r.lend_transaction.application_transaction.application.product } for r in q] 
        return rst_list

    def query_by_id(self,application_id):
        u'''根据application_id查询五级分类内容 '''
        r = g.db_session.query(CreditLevel).join(ApplicationTransaction,ApplicationTransaction.transaction_id==CreditLevel.application_transaction_id).filter(ApplicationTransaction.application_id==application_id).first()
        rst_data={'credit_level':r,'lend_transaction':r.lend_transaction,'party':r.lend_transaction.application_transaction.application.customer.party,'application':r.application_transaction.application,'product':r.lend_transaction.application_transaction.application.product} 
        return rst_data    
