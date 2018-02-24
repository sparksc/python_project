# -*- coding:utf-8 -*-
import unittest
from nose.tools import eq_, assert_true, raises
from ..server import service
from ..server.svc import services

def test_basic():
    @service
    def func(request):
        return request
    eq_(func("ok"),"ok")
    eq_(len(services),1)
    assert_true("func" in services)
    eq_(services['func'], func)



