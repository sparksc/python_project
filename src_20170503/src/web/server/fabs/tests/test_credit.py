# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
import unittest

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

        ccy=Currency(currency_code=u'CNY',currency_name=u'人民币')
        system_calendar=SystemCalendar(system_calendar_id=20150923)
        product_type=ProductType(code=u'PERSON_BUSI',name=u'个人业务')
        product=Product(product_code=u'PERSON_HOUSE',product_type_code=u'PERSON_BUSI',name=u'个人住房贷款')
        self.session.add_all([ccy, system_calendar, product_type, product])

        resident=Resident(name=u'张三', ric=u'330782199201010101', family_name=u'张', give_name=u'三')
        self.user=User(party=resident, user_name=u'zhangsan')
        self.session.add_all([self.user, resident])

        self.start=StartActivity(activity_name=u"开始")

        self.task=TaskActivity(activity_name=u"审查", task_assign_module='fabs.workflow.default', task_assign_function=u'static_assign')
        self.session.add(self.task)
        set_parameter(self.task, u'用户', u'zhangsan')

        self.flow1=Flow(from_activity=self.start, to_activity=self.task, have_guard=False)
        self.session.add_all([self.start, self.flow1])

        self.task2=TaskActivity(activity_name=u"审批", task_assign_module='fabs.workflow.default', task_assign_function=u'static_assign')
        self.session.add(self.task2)
        set_parameter(self.task2, u'用户', u'zhangsan')

        self.flow2=Flow(from_activity=self.task, to_activity=self.task2, have_guard=False)

        self.end=EndActivity(activity_name=u"结束")
        self.flow3=Flow(from_activity=self.task2, to_activity=self.end, have_guard=False)

        self.session.add_all([self.flow2, self.end, self.flow3])
        self.session.commit()

    def test_basic_process(self):
        logging.debug("transaction tasks")
        #贷款客户
        resident=Resident(name=u'李四', ric=u'330782199201010102', family_name=u'李', give_name=u'四')
        #担保人
        resident1=Resident(name=u'王五', ric=u'330782199201010103', family_name=u'王', give_name=u'五')
        self.session.add(resident,resident1)
        self.session.commit()

        self.lend_transaction=LendTransaction(transaction_name=u'放贷',transaction_date_id=20150923,transaction_timestamp=datetime.datetime.now(),currency_code=u'CNY',amount=1000000,product_code=u'PERSON_HOUSE',standard_rate=46000,rate_float_type=u'浮动比率',rate_float=0,execute_month_rate=3833,term_year=0,term_month=6,term_day=0,thur_date=datetime.date(2016,3,24),repayment_method=u'等额本息还款',grace_period=2,grace_pay_interest=u'免息',main_gua_type=u'抵押',purpose_type=u'购房',save_flag='2')

        self.lend_account=LendAccount(account_number=u'1016722273',account_name=u'李四',currency_code=u'CNY',active=False,standard_rate=46000,rate_float_type=u'浮动比率',rate_float=0,execute_month_rate=3833,thur_date=datetime.date(2016,3,24),repayment_method=u'等额本息还款',grace_period=2,grace_pay_interest=u'免息',main_gua_type=u'抵押',purpose_type=u'购房')
        #TODO：需添加担保信息
        self.session.add_all([self.lend_transaction,self.lend_account])
        self.session.commit()


        t=self.start.bind_transaction(self.lend_transaction)
        for t in task.get_task(self.user):
            logger.debug("for")
            t.finish()


    def test_query():
        res = self.session.execute("select * from lend_transaction lt left join lend_account la on lt.lend_account_id=la.account_id ")
        logging.debug(res)
        #eq_(get_parameter(self.task, u'用户'), u'z3')

    def tearDown(self):
        #self.session.rollback()
        #Base.metadata.drop_all(self.session.bind)
        logging.debug("finish!!!")

