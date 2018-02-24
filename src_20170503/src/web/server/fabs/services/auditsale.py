# -*- coding: utf-8 -*-
"""
    yinsho.services.AuditsaleService
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

class   AuditsaleService():

    def save(self,**kwargs):
        u''' 核销保存 '''
        lend_transaction=kwargs.get('lend_transaction')
        auditsale=kwargs.get('auditsale') 
        application=g.db_session.query(Application).join(ApplicationTransaction,ApplicationTransaction.application_id==Application.id).filter(ApplicationTransaction.transaction_id==lend_transaction.get('application_transaction_id')).first()
        app =Application(status=u'暂存',customer=application.customer,product_code='974')
        at = ApplicationTransaction(application=app,transaction_name=u"%s核销申请"%(application.customer.party.name)) 
        g.db_session.add(at)
        g.db_session.commit()
        auditsale.update({
                             'lend_transaction_id':lend_transaction.get('transaction_id'),
                              'application_transaction_id':at.transaction_id, 
                            })
        cate = Auditsale(**auditsale)
        g.db_session.add(cate)
        g.db_session.commit()
        return {'auditsale':cate,'application':app}


    def update(self,**kwargs):
        u'''跟新核销内容 '''
        auditsale=kwargs.get('auditsale')
        id = auditsale.get('id')
        auditsale.pop('id') 
        auditsale.pop('application_transaction') 
        auditsale.pop('lend_transaction')
        #auditsale.pop('auditsale_book')
        g.db_session.query(Auditsale).filter(Auditsale.id==id).update(auditsale)
        return {'success':True}

    def submit(self, **kwargs):
        u''' 核销申请提交 '''
        auditsale=kwargs.get('auditsale')
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"贷款核销申请流程").first()
        cl=g.db_session.query(Auditsale).filter(Auditsale.id == auditsale.get('id')).first()
        at=cl.application_transaction
        start(at, start_activity) 
        g.db_session.query(Application).filter(Application.id == at.application_id).update({'status':u'申请'}) 
        return {'success':True}


    def save_submit(self,**kwargs):
        u''' 核销申请保存后提交 '''
        r = self.save(**kwargs) 
        auditsale=r.get('auditsale')
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"贷款核销申请流程").first()
        cl=g.db_session.query(Auditsale).filter(Auditsale.id == auditsale.id).first()
        at=cl.application_transaction
        start(at, start_activity)
        app=g.db_session.query(Application).filter(Application.id == at.application_id).update({'status':u'申请'})
        return {'auditsale':auditsale,'application':app}

    def query(self, **kwargs):
        u''' 查询核销列表 '''
        q = g.db_session.query(Auditsale).all()
        rst_list=[{'auditsale':r,'lend_transaction':r.lend_transaction,'party':r.lend_transaction.application_transaction.application.customer.party,'application':r.application_transaction.application,'product':r.lend_transaction.application_transaction.application.product } for r in q] 
        return rst_list

    def query_by_id(self,application_id):
        u'''根据application_id核销内容 '''
        r = g.db_session.query(Auditsale).join(ApplicationTransaction,ApplicationTransaction.transaction_id==Auditsale.application_transaction_id).filter(ApplicationTransaction.application_id==application_id).first()
        rst_data={'auditsale':r,'lend_transaction':r.lend_transaction,'party':r.lend_transaction.application_transaction.application.customer.party,'application':r.application_transaction.application,'product':r.lend_transaction.application_transaction.application.product} 
        return rst_data    

