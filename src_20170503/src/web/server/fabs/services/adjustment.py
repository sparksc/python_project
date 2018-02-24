# -*- coding: utf-8 -*-
"""
    yinsho.services.AdjustmentService
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

class   AdjustmentService():

    def save(self,**kwargs):
        u''' 授信金额调整保存 '''
        lend_transaction=kwargs.get('lend_transaction')
        adjustment=kwargs.get('adjustment') 
        application=g.db_session.query(Application).join(ApplicationTransaction,ApplicationTransaction.application_id==Application.id).filter(ApplicationTransaction.transaction_id==lend_transaction.get('application_transaction_id')).first()
        app =Application(status=u'暂存',customer=application.customer,product_code='973')
        at = ApplicationTransaction(application=app,transaction_name=u"%s授信金额调整申请"%(application.customer.party.name)) 
        g.db_session.add(at)
        g.db_session.commit()
        adjustment.update({
                             'lend_transaction_id':lend_transaction.get('transaction_id'),
                              'application_transaction_id':at.transaction_id, 
                            })
        cate = Adjustment(**adjustment)
        g.db_session.add(cate)
        g.db_session.commit()
        return {'adjustment':cate,'application':app}


    def update(self,**kwargs):
        u'''跟新授信金额调整内容 '''
        adjustment=kwargs.get('adjustment')
        id = adjustment.get('id')
        adjustment.pop('id') 
        adjustment.pop('application_transaction') 
        adjustment.pop('lend_transaction')
        #adjustment.pop('adjustment_book')
        g.db_session.query(Adjustment).filter(Adjustment.id==id).update(adjustment)
        return {'success':True}

    def submit(self, **kwargs):
        u''' 授信金额调整申请提交 '''
        adjustment=kwargs.get('adjustment')
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"授信调整流程").first()
        cl=g.db_session.query(Adjustment).filter(Adjustment.id == adjustment.get('id')).first()
        at=cl.application_transaction
        start(at, start_activity) 
        g.db_session.query(Application).filter(Application.id == at.application_id).update({'status':u'申请'}) 
        return {'success':True}


    def save_submit(self,**kwargs):
        u''' 授信金额调整申请保存后提交 '''
        r = self.save(**kwargs) 
        adjustment=r.get('adjustment')
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"授信调整流程").first()
        cl=g.db_session.query(Adjustment).filter(Adjustment.id == adjustment.id).first()
        at=cl.application_transaction
        start(at, start_activity)
        app=g.db_session.query(Application).filter(Application.id == at.application_id).update({'status':u'申请'})
        return {'adjustment':adjustment,'application':app}

    def query(self, **kwargs):
        u''' 查询授信金额调整列表 '''
        q = g.db_session.query(Adjustment).all()
        rst_list=[{'adjustment':r,'lend_transaction':r.lend_transaction,'party':r.lend_transaction.application_transaction.application.customer.party,'application':r.application_transaction.application,'product':r.lend_transaction.application_transaction.application.product } for r in q] 
        return rst_list

    def query_by_id(self,application_id):
        u'''根据application_id授信金额调整内容 '''
        r = g.db_session.query(Adjustment).join(ApplicationTransaction,ApplicationTransaction.transaction_id==Adjustment.application_transaction_id).filter(ApplicationTransaction.application_id==application_id).first()
        rst_data={'adjustment':r,'lend_transaction':r.lend_transaction,'party':r.lend_transaction.application_transaction.application.customer.party,'application':r.application_transaction.application,'product':r.lend_transaction.application_transaction.application.product} 
        return rst_data    

