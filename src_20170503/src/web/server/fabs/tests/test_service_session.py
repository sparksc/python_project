# -*- coding:utf-8 -*- from nose.tools import eq_, raises, assert_true
from nose.tools import assert_true
import unittest
import datetime
from functools import wraps

import logging
from ..model.user import *
from sys import modules


logging.basicConfig(level=logging.DEBUG)


class TestSession(unittest.TestCase):


    def setUp(self):
        self.session=simple_session()
        self.engine = self.session.bind
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        logging.debug("set up test")

    def delete_user(self):
        logging.debug("delete user")
        persistentUser = self.session.query(User).filter(User.role_id==1).delete()
        self.session.commit()

    def add_user(self):
        logging.debug("add user")

        user = User(role_id=1,user_name='Jensen')
        factor = Password(user=user,algorithm='MD5',credential='123')
        self.session.add(factor)
        self.session.commit()

        persistentUser = self.session.query(User).get(1)
        assert_true(persistentUser.user_name==user.user_name)

    def add_user2(self):
        logging.debug("add user")

        user = User(role_id=2,user_name='Jensen2')
        factor = Password(user=user,algorithm='MD5',credential='123')
        self.session.add(factor)
        self.session.commit()

        persistentUser = self.session.query(User).get(2)
        assert_true(persistentUser.user_name==user.user_name)

    def filter_user(self):
        logging.debug("filter user")
        user = self.session.query(User).filter(User.user_name=='Jensen')



    def login(self):
        role_id = 1
        user_name = 'Jensen'
        credential = '423'

        auth_type = AuthenticationType(code='010001',name='LOGIN',description='LOGIN')

        time = datetime.datetime.now()
        fail_reason = None
        user = self.session.query(User).filter(User.user_name==user_name).first()
        try:
            if user==None:raise Exception('uername does not exist')
            #Password.algorithm=='MD5',
            password = self.session.query(Password).filter( Password.credential==credential).first()
            if password==None:raise Exception('password authentication failed')

        except Exception as e:
            fail_reason = e[0]

        if user:
            auth = Authentication(user=user,authentication_type=auth_type, passed=True \
                    , fail_reason=fail_reason, time=time )

            from_time = datetime.datetime.today()
            thru_time = from_time + datetime.timedelta(minutes=3)

            user_session = UserSession(from_time=from_time, thru_time= thru_time \
                    , active=True,  user = user, authentication = auth)

            self.session.add_all([auth, auth_type, user_session])
            #from sqlalchemy import inspect
            #insp_user_session = inspect(user_session)
            #if insp_user_session.persistent:
            #if p_auth.persistent:
            #    logging.debug('Session Is Persistens')


            self.session.commit()

        return user

    def test_session(self):
        self.delete_user()
        self.add_user()
        self.add_user2()
        self.filter_user()
        logging.debug('test_session start')

        self.login()

        '''
        auth_type = self.session.query(AuthenticationType).filter(AuthenticationType.code=='010001')
        assert_true(auth_type is not None)
        '''

        logging.debug('test_session end')

    def tearDown(self):
        #self.session.rollback()
        #self.session.close()
        #Base.metadata.drop_all(self.engine)
        logging.debug("tear down test")


