# -*- coding: utf-8 -*-
"""
    yinsho.services.BguService
    #####################

"""
import datetime
from flask import json, g
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all

from ..base import utils
# from ..model import Permission, Menu, User, UserGroup, Group, GroupMenu, Branch, UserBranch
from ..model import Menu, User, UserGroup, Group, GroupMenu, Branch, UserBranch, BranchGroup 


class BgsService():
    """ Bgs Service  """



    def load(self):
        results = g.db_session.query(User,Branch,Group,UserGroup).\
        join(UserBranch,UserBranch.user_id==User.role_id).\
        join(Branch,Branch.role_id==UserBranch.branch_id).\
        join(UserGroup,UserGroup.user_id==User.role_id).\
        order_by(User.role_id).all()
        items = []
        for user,branch,group,ug in results:
            items.append({'user_id':user.role_id,'user_name':user.name,'branch':branch.branch_name,'group':group.group_name,'startdate':ug.startdate,'enddate':ug.enddate})
        return items        


    def f_branches(self):
        return g.db_session.query(Branch).order_by(Branch.role_id).all()

    def groups(self):
        return g.db_session.query(Group).order_by(Group.id).all()

    def find_user(self,**kwargs):
        user_name = kwargs.get('user_id')
        result = g.db_session.query(User).filter(User.user_name==user_name).all()
        if result :
            return 1
        else :
            return 0

    def find_users(self,**kwargs):
        branch_name = kwargs.get('branch_name')
        print branch_name
        return g.db_session.query(User).\
                join(UserBranch,UserBranch.user_id==User.role_id).\
                join(Branch,Branch.role_id==UserBranch.branch_id).\
                filter(Branch.branch_name==branch_name).order_by(User.role_id).all()

    def add_save(self,**kwargs):
        user_name = kwargs.get('user_id')
        startdate = kwargs.get('startdate')
        group_id = kwargs.get('group_id')
        branch_id = kwargs.get('branch_id')
        print kwargs
        result = g.db_session.query(User.role_id).filter(User.user_name==user_name)
        for r in result:
            user_id = r[0]
        result1 = g.db_session.query(UserGroup).filter((UserGroup.user_id==user_id)).all()
        for r1 in result1:
            if r1 and r1.group_id==group_id and r1.enddate=='3000-12-31':
                return 1
        result2 = g.db_session.query(UserBranch).filter((UserBranch.user_id==user_id))
        for r2 in result2:
            if r2 and r2.branch_id!=branch_id:
                for r1 in result1:
                    if r1.enddate=='3000-12-31':
                        return 4 
            if r2:
                g.db_session.query(UserBranch).filter(UserBranch.user_id==user_id).update({UserBranch.branch_id:branch_id})
                g.db_session.add(UserGroup(user_id=user_id,group_id=group_id,startdate=startdate,enddate='3000-12-31'))
                return 3
        g.db_session.add(UserGroup(user_id=user_id,group_id=group_id,startdate=startdate,enddate='3000-12-31'))
        g.db_session.add(UserBranch(user_id=user_id,branch_id=branch_id))
        return 3

    def edit_save(self,**kwargs):
        enddate = kwargs.get('enddate')
        group_id = kwargs.get('group_id')
        g.db_session.query(UserGroup).filter(UserGroup.id==group_id).update({UserGroup.enddate:enddate})
        return u'编辑成功'
