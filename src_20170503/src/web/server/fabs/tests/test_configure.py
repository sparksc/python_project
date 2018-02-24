# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
import unittest
from ..configure import load_json
from os import environ

def test_basic():
    with open('sample.json.cfg') as f:
        cfg=load_json(f)
        assert_true(isinstance(cfg['database'], dict))
        assert_true(isinstance(cfg.database, dict))
        d=cfg.database['default']
        eq_(d['url'], "mysql+mysqldb://work:work@localhost/work")

        #"dynamic":{
        #   "path":"{{HOME}}/xxx"
        #}
        d=cfg.dynamic
        eq_(d['path'],environ['HOME']+"/xxx")
