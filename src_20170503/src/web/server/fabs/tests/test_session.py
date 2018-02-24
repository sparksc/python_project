# -*- coding:utf-8 -*- from nose.tools import eq_, raises, assert_true
from nose.tools import assert_true
import unittest
import datetime
import json

import logging
from ..model.user import *
from sys import modules
from ..base import helpers
from ..views import app



log = logging.getLogger()

class WebClient(unittest.TestCase):

    @staticmethod
    def post(url, data={}):
        client = app.test_client()
        rv = client.post(url, data=json.dumps(dict(data)), content_type = 'application/json')



class TestSession(unittest.TestCase):

    def test_web_session(self):
        data = WebClient.post('/users/login', data={'username': 'khjl','password':'qwe123'})




