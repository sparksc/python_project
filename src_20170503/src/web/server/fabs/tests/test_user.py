# -*- coding:utf-8 -*-
import logging
import unittest
from nose.tools import eq_, raises, assert_true
logging.basicConfig(level=logging.DEBUG)
from ..model.user import *
import datetime
import uuid
session=simple_session()

class TestUser(unittest.TestCase):


    ##  修改用户密码
    def update_user_pwd(self):
        session.query(Password).filter(Password.user_id == 1).update({Password.credential:'qwe1'})
        session.commit()
        logging.debug("update success")
        password = session.query(Password).filter(Password.user_id == 1).first()
        eq_(password.credential,'qwe1')

    ## 更新用户会话
    def update_userSession(self):
        thru_date = datetime.datetime.now()
        session.query(UserSession).filter(UserSession.user_id == 1,UserSession.thru_time == None).update({UserSession.thru_time:thru_date,UserSession.active:False})
        session.commit()
        logging.debug("update success")
        user_session = session.query(UserSession).filter(UserSession.user_id == 1).first()
        eq_(user_session.active,False)

    def test_user(self):
        id = '4061254C9F4111E59D4E98E0D9A8AA23'
        session.query(UserSession).filter(UserSession.user_session_id==id).first()
        logging.debug(session)

        #update_user_pwd()
        #update_userSession()

    def test_group(self):
        pass
