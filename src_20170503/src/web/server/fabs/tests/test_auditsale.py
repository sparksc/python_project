# -*- coding:utf-8 -*-

import unittest
from ..database import simple_session, Base, engine
from ..model.creditLevel import Auditsale

import logging

log = logging.getLogger()

class TestAuditsale(unittest.TestCase):

    def setUp(self):
        self.session=simple_session()

    def test_create_extension(self):
        Auditsale.__table__.create(engine)

    def tearDown(self):
        logging.debug("finish!!!")

