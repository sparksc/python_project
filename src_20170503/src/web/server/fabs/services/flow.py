# -*- coding: utf-8 -*-
"""
    yinsho.services.LoanService
    #####################
    yinsho LoanService module
"""
import hashlib, copy
import  xlwt
from flask import json, g, current_app
from sqlalchemy import and_
from sqlalchemy import desc
from ..model.credit import *
from ..model.transaction import *
from ..model.application import *
from ..model.contract import *
from ..model.guarantee import *
from ..workflow import task
from ..workflow.parameter import *
from ..database.sqlal import simple_session
from ..base import core_inf

import decimal
from decimal import Decimal
import datetime
import random
from .service import BaseService

class FlowService(BaseService):

    def flow_back(self, application_id, activity_name):
        application_transaction = ApplicationTransaction.__table__

        tran_act = g.db_session.query(Application,TransactionActivity.transaction_activity_id,TransactionActivity.transaction_id,TransactionActivity) \
            .outerjoin(application_transaction, application_transaction.c.application_id==Application.id) \
            .outerjoin(TransactionActivity, TransactionActivity.transaction_id==application_transaction.c.application_id) \
            .outerjoin(Transaction, Transaction.transaction_id==application_transaction.c.application_id) \
            .outerjoin(Activity, Activity.activity_id==TransactionActivity.activity_id) \
            .filter(TransactionActivity.transaction_activity_type=="task") \
            .filter(Application.id==application_id) \
            .filter(Activity.activity_name==activity_name) \
            .order_by(TransactionActivity.transaction_activity_id).first()

        transaction_activity_id = tran_act[1]
        transaction_id = tran_act[2]
        transaction_activity = tran_act[3]

        log.debug('transaction [%s] rollback to transction_activity [%s]' % (transaction_id,transaction_id))

        del_trans_all = g.db_session.query(TransactionActivity).filter(and_(TransactionActivity.transaction_id==transaction_id,TransactionActivity.transaction_activity_id>transaction_activity_id)).all()

        for tran in del_trans_all:
            self.session.delete(tran)

        log.debug('reset transction_activity [%s] finished status ' % (transaction_id,transaction_id))
        transaction_activity.finished = None



