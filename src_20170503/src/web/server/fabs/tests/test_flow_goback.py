# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
import unittest
from sqlalchemy import and_

import logging
from ..model.user import *
from ..model.credit import *
from ..model.task import *
from ..model.transaction import *
from ..model.application import *
from ..workflow import task
from ..workflow.data import *
from ..workflow.parameter import *
from sys import modules

log = logging.getLogger()

class TestFlowBack(unittest.TestCase):
    count=0
    def setUp(self):
        self.session=simple_session()

    def test_basic_process(self):
        application_id = 1
        #back_activity_name = u'投资申请'
        back_activity_name = u'支行审贷小组抵贷资产审议'

        # self.flow_back(application_id, back_activity_name)

        user = self.session.query(User).filter(User.role_id==117).first()
        self.flow_continue(application_id, user)
        user = self.session.query(User).filter(User.role_id==118).first()
        self.flow_continue(application_id, user)

    def flow_continue(self,application_id, user):
        transaction  = self.session.query(ApplicationTransaction).filter(ApplicationTransaction.application_id==application_id).first()
        self.process_task(transaction, user)

    def flow_back(self, application_id, activity_name):
        application_transaction = ApplicationTransaction.__table__

        tran_act = self.session.query(Application,TransactionActivity.transaction_activity_id,TransactionActivity.transaction_id,TransactionActivity) \
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

        del_trans_all = self.session.query(TransactionActivity).filter(and_(TransactionActivity.transaction_id==transaction_id,TransactionActivity.transaction_activity_id>transaction_activity_id)).all()

        for tran in del_trans_all:
            self.session.delete(tran)

        log.debug('reset transction_activity [%s] finished status ' % (transaction_id,transaction_id))
        transaction_activity.finished = None

        self.session.flush()
        self.session.commit()


    def process_task(self,transation,user):
        groups = []
        for group in user.user_groups:
            groups.append(group.group.group_name)

        task_list = task.get_task(transation)
        for t in task_list:
            role = get_parameter(t.activity,u"角色")
            if role and role in groups:
                t.user = user
                t.active()
                t.finish()

    def tearDown(self):
        logging.debug("start teardown")

