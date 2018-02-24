# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
import unittest
from ..database import *
from ..configure import load_json
import logging
def test_basic():
    with open('sample.json.cfg') as f:
        cfg=load_json(f)
        dm=DatabaseManager()
        dm.build_engines(cfg)
        eq_(len(dm.engines), 1)

def test_simple():
    s=simple_session()
    eq_('postgresql://work:work@localhost/work', str(s.bind.url))
