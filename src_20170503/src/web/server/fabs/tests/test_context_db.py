# -*- coding:utf-8 -*-
from ..context import db
from ..database import *
from nose.tools import eq_, raises, assert_true, ok_
import unittest
import logging
logging.basicConfig(level=logging.DEBUG)

class Stub(Base):
    __tablename__='stub'
    id=Column(Integer, Sequence('seq_id'), primary_key=True)
    name=Column(String(32), unique=True)

class TestContext(unittest.TestCase):
    def setUp(self):
        self.s=simple_session()
        db.set_session(self.s)
        db.create_all()
    def tearDown(self):
        self.s.rollback()
        db.drop_all()
    def test_db(self):
        ok_(self.s!=None)
        eq_(self.s, db.get_session())
        a=Stub(name=u'A')
        b=Stub(name=u'B')
        db.add(a)
        db.add(b)
        eq_(a, db.query(Stub).filter(Stub.name==u'A').one())
        eq_(b, db.query(Stub).filter(Stub.name==u'B').one())
        db.delete(a)
        q=db.query(Stub).filter(Stub.name==u'A')
        with self.assertRaises(NoResultFound):
            q.one()
        q=db.query(Stub)
        eq_(q.count(), 1)
