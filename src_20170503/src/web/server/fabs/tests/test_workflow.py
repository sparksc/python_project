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

logging.basicConfig(level=logging.DEBUG)
class TestWorkflow(unittest.TestCase):
    count=0
    def setUp(self):
        self.session=simple_session()
        Base.metadata.create_all(self.session.bind)
        process_init(self.session)

        #man=Resident(name=u'张三', ric=u'330602197404040011', family_name=u'张', give_name=u'三')
        man=Resident(name=u'张三', ric=u'330602197404040011')
        user=User(party=man, user_name=u'z3')
        self.user=user

        start=StartActivity(activity_name=u"开始")
        self.start=start
        self.task=TaskActivity(activity_name=u"审查", task_assign_module='fabs.workflow.default', task_assign_function=u'static_assign')
        self.session.add(self.task)
        set_parameter(self.task, u'用户', u'z3')


        self.flow1=Flow(from_activity=self.start, to_activity=self.task, have_guard=False)
        self.end=EndActivity(activity_name=u"结束")
        self.flow2=Flow(from_activity=self.task, to_activity=self.end, have_guard=False)

        self.session.add_all([self.start, self.task, self.flow1, self.end, self.flow2, man, user])
        self.session.commit()

    def test_basic_process(self):
        self.transaction=Transaction(transaction_name=u'贷款')
        t=self.start.bind_transaction(self.transaction)
        logging.debug("transaction tasks: %s"%str(task.get_task(self.transaction)))
        logging.debug("user tasks: %s"%str(task.get_task(self.user)))
        for t in task.get_task(self.user):
            t.finish()

        eq_(get_parameter(self.task, u'用户'), u'z3')
        #eq_(self.task.user.user_name, u'z3')

    def tearDown(self):
        self.session.rollback()
        Base.metadata.drop_all(self.session.bind)
        logging.debug("start teardown")

