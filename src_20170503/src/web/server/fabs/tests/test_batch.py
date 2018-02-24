# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
from sqlalchemy.orm import aliased
import unittest
import json
import time
import logging

from ..model.common import *
from ..model.batch import *
from ..model.party import *
from ..model.customer import *
from sys import modules
import datetime
import random
u'''  批量导入测试  '''
class TestBatch(unittest.TestCase):
    def setUp(self):
        logging.debug("执行setup")
        self.session=simple_session()
        Base.metadata.create_all(self.session.bind)

    def fhdkfhz(self):
        fhdkfhz_eles = self.session.query(CreateTable).filter(CreateTable.table_name == 'fhdkfhz').order_by(CreateTable.id).all()
        
        kls=[]
        for ele in fhdkfhz_eles:
            kls.append(ele.element)
        fl = open('./20160101/whmis_fhdkfhz.unl','r')
        line = fl.readline()
        vls = line.split(':')
        vls = vls[:-1]
        logging.debug(len(vls))
        logging.debug(len(kls))
        info={}
        for idx,k in enumerate(kls):
            info.update({k:vls[idx]})
        #data = "','".join(vls)
        #data = "'" + data + "'"
        #logging.debug(data)
        logging.debug(info)
        fhdkfhz = FHDKFHZ(**info)
        self.session.add(fhdkfhz)
 
    def testBatchLoad(self):
        self.fhdkfhz()

        
    def tearDown(self):
        #self.session.rollback()
        #Base.metadata.drop_all(self.session.bind)
        self.session.commit() 
