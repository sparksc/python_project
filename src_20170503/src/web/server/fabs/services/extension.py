# -*- coding: utf-8 -*-
"""
    yinsho.services.ExtensionService
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

class   ExtensionService():

    def save(self,**kwargs):
        u''' 展期保存 '''
        lend_transaction=kwargs.get('lend_transaction')
        extension=kwargs.get('extension') 
        application=g.db_session.query(Application).join(ApplicationTransaction,ApplicationTransaction.application_id==Application.id).filter(ApplicationTransaction.transaction_id==lend_transaction.get('application_transaction_id')).first()
        app =Application(status=u'暂存',customer=application.customer,product_code='972')
        at = ApplicationTransaction(application=app,transaction_name=u"%s展期申请"%(application.customer.party.name)) 
        g.db_session.add(at)
        g.db_session.commit()
        extension.update({
                             'lend_transaction_id':lend_transaction.get('transaction_id'),
                              'application_transaction_id':at.transaction_id, 
                            })
        cate = Extension(**extension)
        g.db_session.add(cate)
        g.db_session.commit()
        return {'extension':cate,'application':app}


    def update(self,**kwargs):
        u'''跟新展期内容 '''
        extension=kwargs.get('extension')
        id = extension.get('id')
        extension.pop('id') 
        extension.pop('application_transaction') 
        extension.pop('lend_transaction')
        #extension.pop('extension_book')
        g.db_session.query(Extension).filter(Extension.id==id).update(extension)
        return {'success':True}

    def submit(self, **kwargs):
        u''' 展期申请提交 '''
        extension=kwargs.get('extension')
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"贷款展期申请流程").first()
        cl=g.db_session.query(Extension).filter(Extension.id == extension.get('id')).first()
        at=cl.application_transaction
        start(at, start_activity) 
        g.db_session.query(Application).filter(Application.id == at.application_id).update({'status':u'申请'}) 
        return {'success':True}


    def save_submit(self,**kwargs):
        u''' 展期申请保存后提交 '''
        r = self.save(**kwargs) 
        extension=r.get('extension')
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"贷款展期申请流程").first()
        cl=g.db_session.query(Extension).filter(Extension.id == extension.id).first()
        at=cl.application_transaction
        start(at, start_activity)
        app=g.db_session.query(Application).filter(Application.id == at.application_id).update({'status':u'申请'})
        return {'extension':extension,'application':app}

    def query(self, **kwargs):
        u''' 查询展期列表 '''
        q = g.db_session.query(Extension).all()
        rst_list=[{'extension':r,'lend_transaction':r.lend_transaction,'party':r.lend_transaction.application_transaction.application.customer.party,'application':r.application_transaction.application,'product':r.lend_transaction.application_transaction.application.product } for r in q] 
        return rst_list

    def query_by_id(self,application_id):
        u'''根据application_id展期内容 '''
        r = g.db_session.query(Extension).join(ApplicationTransaction,ApplicationTransaction.transaction_id==Extension.application_transaction_id).filter(ApplicationTransaction.application_id==application_id).first()
        rst_data={'extension':r,'lend_transaction':r.lend_transaction,'party':r.lend_transaction.application_transaction.application.customer.party,'application':r.application_transaction.application,'product':r.lend_transaction.application_transaction.application.product} 
        return rst_data    

