# -*- coding: utf-8 -*-
"""
    yinsho.services.DiscountService
    #####################

    yinsho DiscountService module
"""
from ..model.party import *
from .service import BaseService
import hashlib, copy
from flask import json, g
from sqlalchemy import and_
from sqlalchemy import desc
from ..model.credit import *
from ..model.transaction import *
from ..model.application import *
from ..model.task import Task
from ..workflow import task
from ..workflow.parameter import *
from ..database.sqlal import simple_session
from ..base import core_inf 

import decimal
from decimal import Decimal
import datetime
import random
import datetime
import xlrd

class DiscountService(BaseService):

    def save(self,**kwargs):
        u'''  创建贴现申请信息  '''
        party_id = kwargs.get('party_id')
        loan_type_code = kwargs.get('loan_type_code')
        main_gua = kwargs.get('main_gua')
        quote_report =  kwargs.get('quote_report')
        sur_rep = None
        print quote_report
        if quote_report == u'是':
            sur_rep = g.db_session.query(SurveyReport).filter(SurveyReport.party_id==party_id).filter(SurveyReport.product_code == loan_type_code).order_by(desc(SurveyReport.end_date)).first()
            if sur_rep == None:
                return {"error":"无调查报告可以引用"}
            print sur_rep.end_date
            if str(sur_rep.end_date) < str(datetime.datetime.now()):
                return {"error":"调查报告过期"}

        cust = g.db_session.query(Customer).join(Party,Party.id == Customer.party_id).filter(Customer.party_id==party_id).first()
        a = Application(
                        customer_id = cust.role_id,
                        survey_report = sur_rep,
                        product_code = loan_type_code,
                        main_gua_type = main_gua,
                        quote_report = quote_report,
                        status=u'暂存')

        trans=ApplicationTransaction(transaction_name=u"%s的贷款申请"%(cust.party.name),application=a,party=cust.party)
        g.db_session.add(trans)
        g.db_session.commit()

        return {'success':True,'id':a.id}

    def submit(self,**kwargs):
        u''' 进入流程 '''
        transaction_info =  kwargs.get('transaction_info')
        application_info =  kwargs.get('application_info')
        product_code = application_info.get('product_code')
        product = g.db_session.query(Product).filter(Product.product_code == product_code).first()
        if application_info.get('survey_report_id'):
            application_info.pop('survey_report_id')
        app_id = application_info.get('id')
        #application_info.pop('id')
        for k in application_info.keys():
            if application_info.get(k) == None:
                application_info.pop(k)
            elif application_info.get(k) == []:
                application_info.pop(k)
        at = g.db_session.query(ApplicationTransaction).filter(ApplicationTransaction.application_id==app_id).first()
        g.db_session.query(Transaction).filter(Transaction.transaction_id==transaction_info.get('transaction_id')).update(\
        {'transaction_timestamp':datetime.datetime.now(),
        'currency_code':transaction_info.get('currency_code') or 'CNY',
        'amount':transaction_info.get('amount')})
        apply_date = application_info.get('apply_date');
        if apply_date:
            application_info.update({'apply_date':datetime.datetime.strptime(apply_date.strip(),'%Y-%m-%d'),'status':u'贴现申请'})
        print application_info
        g.db_session.query(Application).filter(Application.id==app_id).update(application_info)#
        g.db_session.commit()
        # Start Application Activity
        start_activity = g.db_session.query(Activity).join(Workflow, Workflow.start_activity_id == Activity.activity_id).filter(Workflow.workflow_name==u"贴现业务流程").first()
        start(at, start_activity)
        g.db_session.commit()

        user = g.web_session.user
        groups = []
        for group in user.user_groups:
            groups.append(group.group.group_name)

        task_list = task.get_task(at)
        for t in task_list:
            role = get_parameter(t.activity,u"角色")
            if role and role in groups:
                t.user = user
                t.active()
                t.finish()

        g.db_session.commit()

        return {'application_id':app_id}


