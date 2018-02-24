# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
from sqlalchemy.orm import aliased
import unittest
import json
import time
import logging
from ..model.guarantee import *
from sys import modules
import datetime
import random
logging.basicConfig(level=logging.DEBUG)

class TestCustomerInfo(unittest.TestCase):
    def setUp(self):
        logging.debug("执行setup")
        self.session=simple_session()
        #Base.metadata.drop_all(self.session.bind)
        Base.metadata.create_all(self.session.bind)
       
    def testAddGuarantee(self):
        dy = MrgeBuilding(gty_type=u"一般担保",
                          gty_method=u"抵押",
                          bldg_type=u"房产类型:住房",
                          bldg_district=u"房屋所在区域:乌海XXX")
        self.session.add(dy)

    def tearDown(self):
        #self.session.rollback()
        #Base.metadata.drop_all(self.session.bind)
        self.session.commit()

