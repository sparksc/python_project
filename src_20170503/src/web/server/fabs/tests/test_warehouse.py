# -*- coding:utf-8 -*-
from ..model.warehouse import *
from .configure import Configure
from nose.tools import eq_, raises, assert_true
import unittest
import logging
logging.basicConfig(level=logging.DEBUG)

#from ..model.user import *
from ..model.warehouse.account import *
def test_user_model():
    with Configure() as tc:
        DWBase.metadata.drop_all(tc.database.engine)
        DWBase.metadata.create_all(tc.database.engine)
        u"""
        tc.database.session.add(Account(name=u"zj",number=u"01"))
        tc.database.session.add(Account(name=u"hb",number=u"02"))
        tc.database.session.commit()
        l=[]
        for i in tc.database.session.query(Account).order_by(Account.number):
            l.append((i.name, i.number))
            assert_true(isinstance(i, Account))
            logging.debug("%s"%str(i))
        eq_(l, [(u'zj', u'01'), (u'hb', u'02')])
        """

