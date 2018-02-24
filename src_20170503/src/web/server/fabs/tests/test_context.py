# -*- coding:utf-8 -*-
#from ..context import context
#from ..context import db
#from ..context import session
from ..database import *
from ..model.date import *
from ..model.user import *
from datetime import date
from nose.tools import eq_, raises, assert_true, ok_
import unittest
import logging
logging.basicConfig(level=logging.DEBUG)

class TestContext(unittest.TestCase):
    def setUp(self):
        self.s=simple_session()
        db.set_session(self.s)
        db.create_all()
        db.add(SystemCalendar(system_code=u'LMS', system_today=True, system_date=date(2015,10,1), system_day=1, system_month=10, system_year=2015))
        man=Resident(name=u'张三', ric=u'330602197404040011', family_name=u'张', give_name=u'三')
        user=User(party=man, user_name=u'z3')
        self.user_session=UserSession(user=user, active=True)
        db.add(self.user_session)
        db.flush()
        context.set_default_system(u'LMS')
    def tearDown(self):
        db.rollback()
        db.drop_all()
    def test_init_session(self):
        session.init_user_session(self.user_session.user_session_id)
        eq_(session.user_session(), self.user_session)
    def test_init_date(self):
        context.init_default_system_date()
        eq_(context.today(), date(2015,10,1))
