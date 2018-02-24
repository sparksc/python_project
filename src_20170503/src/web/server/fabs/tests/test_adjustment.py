# -*- coding:utf-8 -*-

import unittest
from ..database import simple_session, Base, engine
from ..model.creditLevel import Adjustment

import logging

log = logging.getLogger()

class TestAdjustment(unittest.TestCase):

    def setUp(self):
        self.session=simple_session()

    def test_create_extension(self):
        Adjustment.__table__.create(engine)

    def tearDown(self):
        logging.debug("finish!!!")

