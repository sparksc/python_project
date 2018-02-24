# -*- coding: utf-8 -*-
"""
    yinsho.services.PermissionService
    #####################

    yinsho UsersService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func,text
from sqlalchemy.orm import joinedload_all,joinedload

from ..base import utils
from ..model import Menu, User, UserGroup, BranchGroup, Group, GroupMenu, Branch, UserBranch, PerCon, Target ,Pe_contract_detail,GroupType

  

class poConService():
    """ Performance Service  """

    # TODO: Move to the net db_session object

    def add(self, **kwargs):
        newda= kwargs.get('add_date')
        if(newda['x1'] is None):
            return u'信息请填写完整'
        if(newda['x2'] is None):
            return u'信息请填写完整'
        data={}
        data['group_name']=newda['x1']
        data['group_type_code']=newda['x3']
        g.db_session.add(Group(**data))
        return u"保存成功"
    def department_add(self, **kwargs):
        newda= kwargs.get('add_date')
        if(newda['x1'] is None):
            return u'信息请填写完整'
        if(newda['x2'] is None):
            return u'信息请填写完整'
       #gb=Group(group_name=newda['x1'],group_type_code=4)    
        data={}
        data['group_id']=newda['x1']['id']
        data['branch_id']=newda['x2']
        g.db_session.add(BranchGroup(**data))
        return u"保存成功"

    def type_add(self,**kwargs):
        type_name = kwargs.get('type_name')
        type_code = kwargs.get('type_code')
        if(type_name is None):
            raise Exception(u'信息请填写完整')
        if(type_code is None):
            raise Exception(u'信息请填写完整')
        data={}
        data['type_name']=type_name
        data['type_code']=type_code
        g.db_session.add(GroupType(**data))
        return 'ok'
    def groups(self):
        return g.db_session.query(GroupType).order_by(GroupType.type_code).all()

    def group_delete(self,**kwargs):
        
        qm=g.db_session.query(UserGroup).filter(UserGroup.group_id==kwargs.get('delete_id')).first()
        if(qm):
            return '该岗位存在岗位关系，无法删除，请检查！'
        g.db_session.query(Group).filter(Group.id==kwargs.get('delete_id')).delete()
        return u"删除成功"

    def department_delete(self,**kwargs):
        g.db_session.query(BranchGroup).filter(BranchGroup.id==kwargs.get('delete_id')).delete()
        return u"删除成功"

    def department_edit_save(self, **kwargs):
        newdata =  kwargs.get('up_date')
        print newdata
        oid =newdata['x4']
        ngid=newdata['x2']
        g.db_session.query(UserGroup).filter(UserGroup.group_id==oid).update({'group_id':ngid})
        #qq={}
        #qq['group_name']=newdata['x2']
        #qq['group_type_code']=4
        #g.db_session.query(Group).filter(Group.id==gid).update(qq)
        bgid=newdata['x1']
        bg={}
        bg['branch_id']=newdata['x3']
        bg['group_id']=ngid
        g.db_session.query(BranchGroup).filter(BranchGroup.id==bgid).update(bg)
        return u"保存成功"

    def group_edit_save(self, **kwargs):
        newdata =  kwargs.get('up_date')
        id =newdata['x1']
        qq={}
        qq['id']=newdata['x1']
        qq['group_name']=newdata['x2']
        g.db_session.query(Group).filter(Group.id==id).update(qq)
        return u"保存成功"
         
    def check_groups(self,**kwargs):
        search_name=kwargs.get('name')
        print(search_name)
        print(g.db_session.query(Group).filter(Branch.role_id==int(search_name)).all())
        return g.db_session.query(Group).filter(Branch.role_id==int(search_name)).all()

    def ords(self,**kwargs):
        pid=kwargs.get('pid')
        print(pid)
        result = g.db_session.query(Branch).order_by(Branch.role_id).all()
        n=0
        for r in result :
            if r.role_id == pid :
                break
            else :
                n=n+1
                continue
        return n

