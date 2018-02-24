# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime
from flask import json, g,current_app
from sqlalchemy import and_, func,or_
from sqlalchemy.orm import joinedload_all

from ..base import utils
from ..model import Branch,Menu,User,UserBranch,Gsgx_ck,UserRelation,BranchGroup,Group,UserGroup,GroupType,CustHook,CustHookBatch,AccountHook
from  decimal import Decimal
from ..services.mbox import *


class BranchmanageService():
    """ Target Service  """

    def branchs(self,**kwargs):
        import time
        search_name=kwargs.get('name')
        parent_branch_no = kwargs.get('parent_branch_no')
        branches = None
        if search_name:
            branches = g.db_session.query(Branch).filter(Branch.branch_name.like('%'+search_name+'%')).all()
        elif parent_branch_no and parent_branch_no != '966000':
            parent_branch = g.db_session.query(Branch).filter(Branch.branch_code == parent_branch_no).first()
            branches = g.db_session.query(Branch).filter(or_(Branch.parent_id == parent_branch.role_id, Branch.branch_code == parent_branch_no)).order_by(Branch.role_id).all()
        else:
            branches = g.db_session.query(Branch).order_by(Branch.role_id).all()
        return [{"branch_code":b.branch_code,"branch_name":b.branch_name,"role_id":b.role_id,"branch_totalname":b.branch_totalname,"branch_level":b.branch_level,"parent_id":b.parent_id} for b in branches]


    def get_branch_list(self,**kwargs):
        branch_code = kwargs.get('branch_code')
        branch = g.db_session.query(Branch).filter(Branch.branch_code==branch_code).first()

        all_branch = g.db_session.query(Branch).all()

        branch_list = []
        if branch.branch_level != u'支行':
            branch_list.append({'parent_branch':branch, 'child_branch':branch})
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
                    childs.append({'parent_branch':child, 'child_branch':subchild})
                branch_list.append({'parent_branch':branch, 'child_branch':childs})
            else:
                if branch.branch_level != u'支行':
                     branch_list.append({'parent_branch':branch, 'child_branch':child})
                else:
                     zhchilds.append({'parent_branch':branch, 'child_branch':child})
        if branch.branch_level == u'支行':
            branch_list.append({'parent_branch':branch, 'child_branch':zhchilds})
        return branch_list

    def branch(self,**kwargs):
        org_code=kwargs.get('org')
        branch = None
        if org_code:
            branch = g.db_session.query(Branch).filter(Branch.branch_code==org_code).all()
        return [{"branch_code":b.branch_code,"branch_name":b.branch_name,"role_id":b.role_id,"branch_totalname":b.branch_totalname,"branch_level":b.branch_level,"parent_id":b.parent_id} for b in branch]

    def branch_save(self, **kwargs):
        branch_code = kwargs.get('add_code')
        branch_name = kwargs.get('add_name')
        branch_totalname = kwargs.get('add_totalname')
        #isloan = kwargs.get('add_isloan')
        parent_id = kwargs.get('add_parentid')
        
        #g.db_session.add(Branch(branch_code=branch_code,branch_name=branch_name,branch_totalname=branch_totalname,is_loan_branch=isloan,parent_id=parent_id))
        g.db_session.add(Branch(branch_code=branch_code,branch_name=branch_name,branch_totalname=branch_totalname,parent_id=parent_id))
        return u"保存成功"

    def branch_delete(self,**kwargs):
        g.db_session.query(Branch).filter(Branch.role_id==kwargs.get('delete_id')).delete()
        return u"删除成功"

    def branch_edit_save(self, **kwargs):
        role_id = kwargs.get('edit_id')
        branch_code = kwargs.get('edit_code')
        branch_name = kwargs.get('edit_name')
        branch_totalname = kwargs.get('edit_totalname')
        #isloan = kwargs.get('edit_isloan')
        parent_id = kwargs.get('edit_parentid')
        g.db_session.query(Branch).filter(Branch.role_id == role_id).update(
            {Branch.branch_code: branch_code,Branch.branch_name:branch_name,Branch.branch_totalname:branch_totalname,Branch.parent_id:parent_id})
        return u"保存成功"

    def check_branchs(self,**kwargs):
        search_name=kwargs.get('name')
        print(search_name)
        print(g.db_session.query(Branch).filter(Branch.role_id==int(search_name)).all())
        return g.db_session.query(Branch).filter(Branch.role_id==int(search_name)).all()

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

    def users(self,**kwargs):
        search_id=kwargs.get('branch_id')
        search_id=str(search_id)
        print kwargs
        current_app.logger.debug(search_id)
        current_app.logger.debug(g.db_session.query(User)\
        .join(UserBranch,UserBranch.user_id==User.role_id)\
        .filter(UserBranch.branch_id==search_id).order_by(User.user_name).statement)

        rest=g.db_session.query(User)\
        .join(UserBranch,UserBranch.user_id==User.role_id)\
        .filter(UserBranch.branch_id==search_id).order_by(User.user_name).all()
        return [{"role_id":k.role_id,"user_name":k.user_name,"name":k.name,"work_status":k.work_status} for k in rest]

    def branchgroup(self,**kwargs):
        search_id=kwargs.get('branch_id')
        rest=g.db_session.query(Group)\
        .join(BranchGroup,BranchGroup.group_id==Group.id)\
        .filter(BranchGroup.branch_id==search_id).all()
        return [{"group_id":k.id,"group_name":k.group_name} for k in rest]
        return rest

    def find_users_by_branches(self,**kwargs):
        search_id=kwargs.get('branch_id')
        is_khjl = kwargs.get('is_khjl')
        print search_id
        slist = search_id.split(',')
        if is_khjl:
            rest=g.db_session.query(User)\
            .join(UserBranch,UserBranch.user_id==User.role_id)\
            .join(UserGroup,UserGroup.user_id == User.role_id)\
            .join(Group,Group.id == UserGroup.group_id)\
            .join(Branch, UserBranch.branch_id == Branch.role_id)\
            .filter(Group.group_type_code == '2000')\
            .filter(Group.group_name <> u'非客户经理')\
            .filter(Branch.branch_code.in_(slist)).order_by(User.user_name).all()
        else:
            rest_sql = g.db_session.query(User)\
            .join(UserBranch,UserBranch.user_id==User.role_id)\
            .join(Branch, UserBranch.branch_id == Branch.role_id)\
            .filter(Branch.branch_code.in_(slist))
            print rest_sql
            rest = rest_sql.order_by(User.user_name).all()


        return [{"role_id":k.role_id,"user_name":k.user_name,"name":k.name,"work_status":k.work_status} for k in rest]

    def add_save(self, **kwargs):
        drrq = kwargs.get('add_khrq')
        jgbh = kwargs.get('add_jgbh')
        dxbh = kwargs.get('add_zhbh')
        dxxh = kwargs.get('add_zhxh')
        gldxbh = kwargs.get('add_ygh')
        fjdxbh = kwargs.get('add_khh')
        glje1 = kwargs.get('add_gsbl')
        glrq1 = kwargs.get('add_glqsrq')
        glrq2 = kwargs.get('add_gljsrq')
        dxmc = kwargs.get('add_khmc')
        ck_type = kwargs.get('add_cklx')
        newflag = 0
        g.db_session.add(Gsgx_ck(drrq=drrq,jgbh=jgbh,dxbh=dxbh,dxxh=dxxh,gldxbh=gldxbh,fjdxbh=fjdxbh,glje1=glje1,glrq1=glrq1,glrq2=glrq2,dxmc=dxmc,ck_type=ck_type,newflag=newflag))
        return u"保存成功"

    #通过 职务判断 权限控制
    def get_user_permission(self,**kwargs):
        user_id = kwargs.get('user_id')
        q = g.db_session.query(UserGroup).join(User,User.role_id==UserGroup.user_id).join(Group,Group.id==UserGroup.group_id).join(GroupType,GroupType.type_code==Group.group_type_code).filter(User.role_id == user_id).filter(Group.group_type_code == '5000').filter(Group.group_name.like("%管理%")).all()
        return len(q)

    def get_staff(self,**kwargs):
        branch_code=kwargs.get('branch_code')

        rest=g.db_session.query(User)\
        .join(UserBranch,UserBranch.user_id==User.role_id)\
        .join(Branch,Branch.role_id==UserBranch.branch_id)\
        .filter(Branch.branch_code==branch_code).order_by(User.user_name).all()
        return [{"role_id":k.role_id,"user_name":k.user_name,"name":k.name,"work_status":k.work_status} for k in rest]
        return rest
    
    def hide(self,**kwargs):
        try:
            cust_id=kwargs.get('cust_id')

            g.db_session.query(CustHook).filter(CustHook.id == cust_id).update({CustHook.hide:0})
            return u'隐藏成功'
        except Exception, e:
            return str(e)

    def do_allot(self,**kwargs):
        try:
            cust_id = kwargs.get('cust_id')
            to_teller_no = kwargs.get('to_teller_no')
            typ = kwargs.get('typ')

            #取接收人的岗位类型
            old_data  = g.db_session.query(CustHook).filter(CustHook.id == cust_id).first()
            
            datadict = {}
            datadict['status'] = u'录入待审批'
            datadict['manager_no'] = to_teller_no
            print datadict
            g.db_session.query(CustHook).filter(CustHook.id == cust_id).update(datadict)
            if old_data.typ in [u'存款',u'理财']:
                g.db_session.query(AccountHook).filter(AccountHook.org_no == old_data.org_no,AccountHook.typ == old_data.typ,AccountHook.status == u'待手工',AccountHook.follow_cust == u'客户号优先', AccountHook.cust_in_no == old_data.cust_in_no).update(datadict)
            if old_data.typ == u'电子银行':
                g.db_session.query(CustHook).filter(CustHook.cust_in_no == old_data.cust_in_no,CustHook.org_no == old_data.org_no, CustHook.typ == old_data.typ, CustHook.status == u'待手工').update(datadict)
            return u'分配成功'
        except Exception, e:
            g.db_session.rollback()
            print Exception,':',e
            return str(e)

    def show(self,**kwargs):
        try:
            cust_id = kwargs.get('cust_id')

            g.db_session.query(CustHook).filter(CustHook.id == cust_id).update({CustHook.hide:1})
            return u'显示成功'
        except Exception, e:
            return str(e)

    def show_org(self,**kwargs):
        try:
            cust_id = kwargs.get('cust_id')

            org_no = g.db_session.query(CustHook.org_no).filter(CustHook.id == cust_id).first()
            org_no = org_no[0]
            return org_no
        except Exception, e:
            return str(e)

    def permission(self,**kwargs):
        try:
            user_name = kwargs.get('user_name')
            print user_name 
       
            is_true = g.db_session.query(User.user_name).join(UserGroup,UserGroup.user_id==User.role_id).filter(User.user_name==user_name).filter(UserGroup.group_id==1016).first()
            print is_true
            if is_true == None:
                if_true = 0
            else:
                if_true = 1
            print if_true
            return if_true
        except Exception, e:
            return str(e)
