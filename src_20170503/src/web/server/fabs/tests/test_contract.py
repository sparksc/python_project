# -*- coding:utf-8 -*-
import logging
import unittest
from nose.tools import eq_, raises, assert_true
logging.basicConfig(level=logging.DEBUG)
from ..model.credit import *
from ..model.application import *
import datetime
import uuid
session=simple_session()
def db():
    Base.metadata.create_all(session.bind)

def aa():
    #pass
    codes = ('330','330_1','331','331_1','332','332_1','333','333_1','523','523_1','525','525_1','527','527_1','529','540','540_1','541','541_1','369_1','368_1','370_1','341','342','343','536','117')
    credit_table = g.db_session.query(Application).filter(Application.product_code.in_(codes)).all()
    
class TestContract(unittest.TestCase):
    def test_add_credit(self):
        codes = ('330','330_1','331','331_1','332','332_1','333','333_1','523','523_1','525','525_1','527','527_1','529','540','540_1','541','541_1','369_1','368_1','370_1','341','342','343','536','117')
        cons = session.query(Application).filter(Application.product_code.in_(codes)).all()
        for con in cons:
             credit=CommercialHouseCredit(application_id=con.id)
             session.add(credit)
        session.commit()

if __name__ == '__main__':
     test_db()
