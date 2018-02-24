# -*- coding: utf-8 -*-
"""
    yinsho.services.RepossessionService
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

class RepossessionService():

    def save(self,**kwargs):
        u''' 以物抵债数据暂存 '''
        lend_transaction=kwargs.get('lend_transaction')
        repossession=kwargs.get('repossession') 
        application=g.db_session.query(Application).join(ApplicationTransaction,ApplicationTransaction.application_id==Application.id).filter(ApplicationTransaction.transaction_id==lend_transaction.get('application_transaction_id')).first()
        app =Application(status=u'暂存',customer=application.customer,product_code='971')
        at = ApplicationTransaction(application=app,transaction_name=u"%s以物抵债申请"%(application.customer.party.name)) 
        g.db_session.add(at)
        g.db_session.commit()
        repossession.update({
                             'lend_transaction_id':lend_transaction.get('transaction_id'),
                              'application_transaction_id':at.transaction_id, 
                            })
        cate = Repossession(**repossession)
        g.db_session.add(cate)
        g.db_session.commit()
        return {'repossession':cate,'application':app}


    def update(self,**kwargs):
        u'''跟新以物抵债内容 '''
        repossession=kwargs.get('repossession')
        id = repossession.get('id')
        repossession.pop('id') 
        repossession.pop('application_transaction') 
        repossession.pop('lend_transaction')
        repossession.pop('repossession_book')
        g.db_session.query(Repossession).filter(Repossession.id==id).update(repossession)
        return {'success':True}

    def submit(self, **kwargs):
        u''' 以物抵债申请提交 '''
        repossession=kwargs.get('repossession')
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"抵贷资产流程").first()
        cl=g.db_session.query(Repossession).filter(Repossession.id == repossession.get('id')).first()
        at=cl.application_transaction
        start(at, start_activity) 
        g.db_session.query(Application).filter(Application.id == at.application_id).update({'status':u'申请'}) 
        return {'success':True}


    def save_submit(self,**kwargs):
        u''' 以物抵债申请保存后提交 '''
        r = self.save(**kwargs) 
        repossession=r.get('repossession')
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"抵贷资产流程").first()
        cl=g.db_session.query(Repossession).filter(Repossession.id == repossession.id).first()
        at=cl.application_transaction
        start(at, start_activity)
        app=g.db_session.query(Application).filter(Application.id == at.application_id).update({'status':u'申请'})
        return {'repossession':repossession,'application':app}

    def query(self, **kwargs):
        u''' 查询以物抵债列表 '''
        q = g.db_session.query(Repossession).all()
        rst_list=[{'repossession':r,'lend_transaction':r.lend_transaction,'party':r.lend_transaction.application_transaction.application.customer.party,'application':r.application_transaction.application,'product':r.lend_transaction.application_transaction.application.product } for r in q] 
        return rst_list

    def query_by_id(self,application_id):
        u'''根据application_id以物抵债内容 '''
        r = g.db_session.query(Repossession).join(ApplicationTransaction,ApplicationTransaction.transaction_id==Repossession.application_transaction_id).filter(ApplicationTransaction.application_id==application_id).first()
        rst_data={'repossession':r,'lend_transaction':r.lend_transaction,'party':r.lend_transaction.application_transaction.application.customer.party,'application':r.application_transaction.application,'product':r.lend_transaction.application_transaction.application.product} 
        return rst_data    
    def savereport(self,**kwargs):
        u'''以物抵债报告内容全'''
        print kwargs
        report=RepossessionReport(**kwargs)
        g.db_session.add(report)  
        return True
