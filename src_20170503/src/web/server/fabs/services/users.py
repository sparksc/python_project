# -*- coding: utf-8 -*-
"""
    yinsho.services.UsersService
    #####################

    yinsho UsersService module
"""
import hashlib, copy,datetime
from flask import json, g
from sqlalchemy import and_, func

from .service import BaseService
from ..model.user import *
from ..base import helpers
from ..base.utils import to_md5
from ..services.mbox import *
from ..model.date import *


class UsersService():
    """ User Service  """
    __model__ = User

    # TODO: Move to the user db_session object
    def login(self, user_name, credential):
        """  Login Authentication

        Args:
            user_name:  Login user name
            credential: Login user password
        Returns:
            The UserSession object.
        Raises:
            Exception:
                - uername does not exist
                - password authentication failed
        """

        auth_type = g.db_session.query(AuthenticationType).filter(
            AuthenticationType.code == '010001').first()

        user = g.db_session.query(User).join(Factor.user).join(Factor.password) \
            .filter(User.user_name == user_name, Password.credential == str(to_md5(credential))).first()

        if not user:
            raise Exception(u"用户名或密码验证失败!")

        #非正常账户登录提示
        status = g.db_session.query(User).filter(User.user_name == user_name,User.work_status == u'在职').first()

        if not status:
            raise Exception(u"非在职状态员工无法登录!")

        # generate user_session
        g.db_session.query(UserSession).filter(UserSession.user == user).update({'active':False})

        from_time = datetime.datetime.utcnow()
        thru_time = from_time + datetime.timedelta(minutes=15)
        auth = Authentication( user=user, authentication_type=auth_type, passed=False, time=from_time)
        user_session = UserSession(user_session_id=helpers.generate_uuid()
                                   , from_time=from_time, thru_time=thru_time, active=True
                                   , user=user, authentication=auth)
        g.db_session.add_all([auth, auth_type, user_session])

        # The user has the login
        
        '''
        if user_session and user_session.thru_time >= datetime.datetime.utcnow():
            expiration = datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=30)
            user_session.thru_time = expiration
        else:
            from_time = datetime.datetime.utcnow()
            thru_time = from_time + datetime.timedelta(minutes=30)
            time = datetime.datetime.utcnow()
            auth = Authentication(
                user=user, authentication_type=auth_type, passed=False, time=time)

            user_session = UserSession(user_session_id=helpers.generate_uuid(),
                                       from_time=from_time, thru_time=thru_time, active=True, user=user, authentication=auth)

            g.db_session.add_all([auth, auth_type, user_session])
        '''

        branch_list = []
        branch = g.db_session.query(Branch).join(UserBranch,UserBranch.branch_id==Branch.role_id).join(User,User.role_id==UserBranch.user_id).filter(User.user_name==user_name).first()
        branch_list = self.get_branch_list(branch.branch_code)
        user_session.branch_list = branch_list

        mbox = MboxService()
        user_session.message_count = mbox.mbox_query_count(user.role_id)
        """
        if not self.check_batch_status_and_date():
            raise Exception(u'省联社数据还未下发,请稍候使用系统!')
        """

        g.db_session.commit()
        return user_session

    def get(self, id):
        date_now = datetime.datetime.utcnow()
        user = g.db_session.query(UserSession).filter(UserSession.user_session_id == id).first()
        if not user: raise Exception(u"认证失败")
        if not user.active: raise Exception(u"异地登录")
        if not user.thru_time >= date_now :raise Exception('登录超时!')
        # TODO: Add update web session thru_time
        thru_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        user.thru_time = thru_time
        return user

    def auth(self, id):
        """
            根据token获取session状态
        """
        date_now = datetime.datetime.utcnow()
        user_session = g.db_session.query(UserSession).filter( UserSession.user_session_id == id).first()
        if not user_session:raise Exception('请登录后操作!')
        if not user_session.active:raise Exception('异地登录!')
        if not user_session.thru_time >= date_now :raise Exception('登录超时!')
        '''
        if not user:
            raise Exception(u"认证失败")
        # TODO: Add update web session thru_time
        thru_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        user.thru_time = thru_time
        '''
        thru_time = now() + datetime.timedelta(minutes=30)
        user_session.thru_time = thru_time
        return user_session

    def all(self):
        users = g.db_session.query(User).all()
        return users

    '''
    def login(self,username,password):
        user = g.db_session.query(User).filter(User.user_name == username).first()
        if user is None : raise Exception(u"用户不存在")
        passwd= g.db_session.query(Password).filter(and_(Password.user_id == user.role_id , Password.credential == password)).first()
        if passwd is None : raise Exception(u"密码错误")
        return user
    '''

    def auth_type(self, type_code):
        auth_type = g.db_session.query(AuthenticationType).filter(
            AuthenticationType.code == password.factor_type).one()
        if password is None:
            raise "无认证方式"
        return auth_type

    # 添加用户认证纪录
    def add_auth(self, user_id, authentication_type_code, passed, fail_reason, time=datetime.datetime.now()):
        auth = Authentication(
            user_id, authentication_type_code=authentication_type_code, passed=passed, fail_reason=fail_reason, time=time)
        g.db_session.add(auth)
        g.db_session.commit()

    # 添加用户会话纪录
    def add_userSession(self, user_id, authentication_id, from_time=None):
        if from_time is None:
            from_time = datetime.datetime.now()
        usersession = UserSession(
            from_time=from_time, active=True, user_id=user_id, authentication_id=authentication_id)
        g.db_session.add(usersession)
        g.db_session.commit()

    # 修改用户密码 TBD old_password
    def update_user_pwd(self, user_id, new_password):
        pss = g.db_session.query(Password).filter(Password.user_id == user_id).first()
        pss.credential = to_md5(new_password)
        g.db_session.commit()
        return u"修改密码成功"
    def init_user_pwd(self, user_name, password):
        user = g.db_session.query(Password).join(User, User.role_id == Password.user_id).filter(User.user_name == user_name).first()
        if user:
            user.credentital = to_md5(password)
            return u"重置密码成功"
        else:
            return u"无此柜员"
              

    # 更新用户会话
    def update_userSession(self, user_id):
        thru_date = datetime.datetime.now()
        g.db_session.query(UserSession).filter(UserSession.user_id == user_id, UserSession.thru_time == None).update(
            {UserSession.thru_time: thru_date, UserSession.active: False})
        g.db_session.commit()

    def query_group(self, user_name):
        user = g.web_session.user
        groups = []
        for group in user.user_groups:
            groups.append(group.group.group_name)
        return json.dumps({'groups': groups})
    
    def update_ws(self,*kwargs):
        user_id = kwargs[3];
        g.db_session.query(User).filter(User.role_id == user_id).update({'work_status':kwargs[2]})
        return u'修改成功'

    def get_group_type(self):
        rs =[]
        q = g.db_session.query(Group,GroupType).join(GroupType,Group.group_type_code==GroupType.type_code).all()
        data = {}
        for item in q:
            key=item.GroupType.type_name
            value=item.Group.group_name
            if key in data:
                data[key].append(value)
            else:
                data[key] = [] 
                data[key].append(value)
        rs.append(data)
        return rs

    def get_group_department(self):
        q = g.db_session.query(Group,GroupType).join(GroupType,Group.group_type_code==GroupType.type_code).filter(GroupType.type_name == '部门').all()
        return [{"id":b.Group.id,"department_name":b.Group.group_name} for b in q]

    def get_branch_list(self, branch_code):
        branch = g.db_session.query(Branch).filter(Branch.branch_code==branch_code).first()

        all_branch = g.db_session.query(Branch).all()

        branch_list = []
        if branch.branch_level != u'支行':
            branch_list.append({'parent_branch':{'branch_code': branch.branch_code, 'branch_name': branch.branch_name}, 'child_branch':{'branch_code': branch.branch_code, 'branch_name': branch.branch_name}})
        first_branch = g.db_session.query(Branch).filter(Branch.parent_id == branch.role_id).order_by(Branch.branch_code).all()
        zhchilds = []
        for child in first_branch:
            data = child.branch_code
            if child.branch_level == u'支行':
                #sub_branch = g.db_session.query(Branch).filter(Branch.parent_id == child.role_id).all()
                sub_branch = []
                for b in all_branch:
                    if b.parent_id == child.role_id:
                        sub_branch.append(b)
                childs = []
                for subchild in sub_branch:
                    childs.append({'parent_branch':{'branch_code': child.branch_code, 'branch_name': child.branch_name}, 'child_branch':{'branch_code': subchild.branch_code, 'branch_name': subchild.branch_name}})
                branch_list.append({'parent_branch':{'branch_code': branch.branch_code, 'branch_name': branch.branch_name}, 'child_branch':childs})
            else:
                if branch.branch_level != u'支行':
                     branch_list.append({'parent_branch':{'branch_code': branch.branch_code, 'branch_name': branch.branch_name}, 'child_branch': {'branch_code': child.branch_code, 'branch_name': child.branch_name}})
                else:
                     zhchilds.append({'parent_branch':{'branch_code': branch.branch_code, 'branch_name': branch.branch_name}, 'child_branch':{'branch_code': child.branch_code, 'branch_name': child.branch_name}})
        if branch.branch_level == u'支行':
            branch_list.append({'parent_branch':{'branch_code': branch.branch_code, 'branch_name': branch.branch_name}, 'child_branch':zhchilds})
        return branch_list

    def is_init_password(self, user_name):
        """
        初始密码提示修改密码
        """

        t_password = Password.__table__
        q_pac = g.db_session.query(User) \
            .join(Factor, and_(Factor.user_id == User.role_id, Factor.factor_type == 'password')) \
            .join(t_password, t_password.c.factor_id == Factor.factor_id) \
            .filter(and_(User.user_name == user_name, t_password.c.credential == to_md5('qwe123')))

        pac = q_pac.first()
        return pac

    def check_batch_status_and_date(self):
        sys_cal = g.db_session.query(SystemPara).first()
        cd = int(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d'))
        print cd, sys_cal.system_date
        if cd > sys_cal.system_date:
            return False

        return True

