# -*- coding:utf-8 -*-
from ..model import *
from nose.tools import eq_, raises, assert_true, ok_
from datetime import date
import unittest
import logging
logging.basicConfig(level=logging.DEBUG)


def test_query_lend():
    session=simple_session()
    rst = session.execute("""
        select a.* from lend_transaction lt
        inner join transaction_activity ta on ta.transaction_id = lt.transaction_id
        inner join activity a on a.activity_id = ta.activity_id
    """).fetchall()

    logging.debug(rst)

    for r in rst[0]:
        logging.debug(r)
    
        
