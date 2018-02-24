# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
from sqlalchemy.orm import aliased
import unittest
import json
import time
import logging
from ..model.user import *
from ..model.asset import *
from ..model.liabilities import *
from ..model.credit import *
from ..model.customer import *
from ..model.transaction import *
from ..model.task import *
from ..model.branch import *
from ..model.approve import *
from ..model.img import *
from ..model.application import *
from ..model.common import *
from ..model.guarantee import *
from ..workflow import task
from ..workflow.parameter import *
from sys import modules
import datetime
import random

log = logging.getLogger()

class TestInterface(unittest.TestCase):
    
    def setUp(self):
        log.debug('Start')
        self.session=simple_session()
        

    def test_interface(self):
        
        
    def tearDown(self):
        log.debug('Bye')
        self.commit()  


