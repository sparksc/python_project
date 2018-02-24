# -*- coding:utf-8 -*-

import unittest
from ..model.mbox import *
from ..model.user import User
import datetime

import logging

log = logging.getLogger()

class TestMbox(unittest.TestCase):

    def setUp(self):
        self.session=simple_session()

    def test_send_mbox(self):
        now = datetime.datetime.now()

    def test_read_mbox(self):
        mbox_record = self.session.query(MboxRecord).first()
        log.debug(mbox_record)


    def test_find_user_inbox(self):
        pass

