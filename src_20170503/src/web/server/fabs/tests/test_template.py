# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
import unittest
import logging
from ..configure import load_json
from ..web.template import *

def test_basic():
    with open('sample.json.cfg') as f:
        cfg=load_json(f)
        tm=TemplateManager()
        tm.build_engines(cfg)
        eq_(len(tm.engines), 1)
        r=tm.render("sample.html",title=u'test')
        eq_(len(r), len(u"<!DOCTYPE html>\n<html>\n    <title>test</title>\n</html>"))
        eq_(r, u"<!DOCTYPE html>\n<html>\n    <title>test</title>\n</html>")
