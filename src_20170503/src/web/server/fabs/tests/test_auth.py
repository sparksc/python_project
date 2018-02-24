# -*- coding:utf-8 -*-
import logging
from nose.tools import eq_, raises, assert_true
logging.basicConfig(level=logging.DEBUG)
from ..model.user import *
import datetime
import uuid
session=simple_session()
def create_user():
    Base.metadata.drop_all(session.bind)
    Base.metadata.create_all(session.bind)


## 模拟用户授权
def add_user():
    user = User(role_id ='1',user_name = 'tom' )
    logging.debug("insert user")
    password = Password(factor_id= 2,algorithm = 'md5',credential = 'qwe123',factor_type = 'password',user_id = 1) 
    logging.debug("insert password")
    auth = AuthenticationType( code = 'password',name ='口令认证',description = '用于用户的登录口令认证')
    logging.debug("init auchc_tpye")
    session.add_all([user,password,auth ])
    session.commit()
    logging.debug("init success")


#＃ 模拟用户认证
def auth_user():
    ##TODO  暂时没有加上用户角色role
    user_id = 1 
    user_password = 'qwe1' 
    user = session.query(User).filter(User.role_id == 1).one()
    if user is None : raise u"用户不存在"
    password = session.query(Password).filter(Password.user_id == user.role_id).one() 
    if password is None : raise "无认证方式"
    auth_type = session.query(AuthenticationType).filter(AuthenticationType.code == password.factor_type) .one()
    assert_true(isinstance(auth_type, AuthenticationType)) 
    ## 添加认证纪录
    
    if password.credential == user_password:
         ## 认证成功，添加认证纪录
         auth = Authentication(user_id =1,authentication_type_code = auth_type.code,passed = True,fail_reason = 'null',time = datetime.datetime.now()) 
         ## 添加用户会话 登录成功
         usersession = UserSession(from_time = datetime.datetime.now(),active = True,user_id = 1,authentication_id = auth.authentication_id)    
         session.add_all([auth,usersession]) 
         session.commit()
    else:
         ## 认证失败，添加认证纪录
         auth = Authentication(user_id =1,authentication_type_code = auth_type.code,passed = False ,fail_reason = '用户登录密码错误',time = datetime.datetime.now())
         session.add(auth)
         session.commit()
    logging.debug("user auth is over")


def test_auth():
  #  create_user()
  #  add_user()
    auth_user()
