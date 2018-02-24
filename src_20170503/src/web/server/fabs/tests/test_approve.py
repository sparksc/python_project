# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
import unittest

from sqlalchemy import and_

import logging
from ..model.user import *
from ..model.credit import *
from ..model.task import *
from ..model.transaction import *
from ..workflow import task
from ..workflow.data import *
from ..workflow.parameter import *
from sys import modules
import datetime

logging.basicConfig(level=logging.DEBUG)
class TestWorkflow(unittest.TestCase):
    count=0
    def setUp(self):
        self.session=simple_session()
        Base.metadata.create_all(self.session.bind)
        process_init(self.session)


    def test_basic_process(self):
        logging.debug("############################")
        #{"loan":{"currency_code":"CNY","standard_rate":"2","rate_float":"2","rate_float_type":"浮动比率","execute_month_rate":"2","repayment_method":"等额本息还款","grace_pay_interest":"免息","grace_period":"2","repayment_times":"2","main_gua_type":"信用"},"customer":{"birthday":"2015-10-08","contact":null,"ethnicity":"汉族","family_name":"张","from_party":[],"gender":"男性","give_name":"三","hobbies_and_interests":"钓鱼","id":2,"living_conditions":null,"marital_status":"未婚","monthly_income_of_family":83943949,"name":"张三","politics_status":"中国共产党","ric":"330602197404040011","role":null,"to_party":null,"type_code":"resident"}

        '''
        lend_account=LendAccount(account_number=str(random.randint(100000000000, 999999999999)), account_name=u"贷款账户", active=True, customer_id=cust.role_id , **loan_info)
        lend_tran.update({
            'lend_account':lend_account,
            'transaction_timestamp':datetime.datetime.now(),
            'currency_code':loan_info.get('currency_code'),
            'customer_id':cust.role_id,
        })
        lend_transaction=LendTransaction(**lend_tran)
        '''

        lendTransaction = self.session.query(LendTransaction).get(1)
        logging.debug(lendTransaction.amount)
        logging.debug(lendTransaction.term_month)
        logging.debug(lendTransaction.term_day)
        logging.debug(lendTransaction.purpose)
        logging.debug(lendTransaction.remark)

        logging.debug(lendTransaction.currency_code)
        logging.debug(lendTransaction.customer_id)

        lendAccount = lendTransaction.lend_account

        logging.debug(lendAccount.standard_rate)
        logging.debug(lendAccount.rate_float)
        logging.debug(lendAccount.rate_float_type)
        logging.debug(lendAccount.execute_month_rate)
        logging.debug(lendAccount.repayment_method)
        logging.debug(lendAccount.grace_pay_interest)
        logging.debug(lendAccount.grace_period)
        logging.debug(lendAccount.repayment_times)
        logging.debug(lendAccount.main_gua_type)



        #lendTransaction.update({'opinion':u'通过', 'opinion_remark':u'通过'})

        activity = self.session.query(TransactionActivity).filter( \
                and_(TransactionActivity.transaction_id == lendTransaction.transaction_id   \
                ,TransactionActivity.finished == None )\
                ).first()

        logging.debug(activity.finished)

        logging.debug("############################")


    def tearDown(self):
        #self.session.rollback()
        #Base.metadata.drop_all(self.session.bind)
        logging.debug("finish!!!")

