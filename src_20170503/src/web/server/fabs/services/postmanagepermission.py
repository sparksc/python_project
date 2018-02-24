# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime
import time
from flask import json, g
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all

from ..base import utils
from ..model import Group 

class PostmanageService():
    """ Target Service  """

    def posts(self,**kwargs):
        search_post=kwargs.get('search_post')
        postes = None
        postes = g.db_session.query(Group)\
                 .filter(Group.group_name.like('%'+search_post+'%'))\
                 .filter(Group.group_type_code == '5000')\
                 .order_by(Group.id).all()
        return [{"post_name":b.group_name,"post_id":b.id} for b in postes]


    def get_post_list(self,**kwargs):
        post_code = kwargs.get('post_code')
        post = g.db_session.query(Branch).filter(Branch.post_code==post_code).first()
        post_list = []
        post_list.append({'parent_post':post, 'child_post':post})
        first_post = g.db_session.query(Branch).filter(Branch.parent_id == post.role_id).all()
        for child in first_post:
            data = child.post_code
            if child.post_level == u'支行':
                sub_post = g.db_session.query(Branch).filter(Branch.parent_id == child.role_id).all()
                childs = []
                for subchild in sub_post:
                    childs.append({'parent_post':child, 'child_post':subchild})
                post_list.append({'parent_post':post, 'child_post':childs})
            else:
                post_list.append({'parent_post':post, 'child_post':child})
        return post_list

    def post(self,**kwargs):
        org_code=kwargs.get('org')
        post = None
        if org_code:
            post = g.db_session.query(Branch).filter(Branch.post_code==org_code).all()
        return [{"post_code":b.post_code,"post_name":b.post_name,"role_id":b.role_id,"post_totalname":b.post_totalname,"post_level":b.post_level,"parent_id":b.parent_id} for b in post]
        return post

    def post_save(self, **kwargs):
        post_code = kwargs.get('add_code')
        post_name = kwargs.get('add_name')
        post_totalname = kwargs.get('add_totalname')
        isloan = kwargs.get('add_isloan')
        parent_id = kwargs.get('add_parentid')
        
        g.db_session.add(Branch(post_code=post_code,post_name=post_name,post_totalname=post_totalname,is_loan_post=isloan,parent_id=parent_id))
        return u"保存成功"

    def post_delete(self,**kwargs):
        g.db_session.query(Branch).filter(Branch.role_id==kwargs.get('delete_id')).delete()
        return u"删除成功"

    def post_edit_save(self, **kwargs):
        role_id = kwargs.get('edit_id')
        post_code = kwargs.get('edit_code')
        post_name = kwargs.get('edit_name')
        post_totalname = kwargs.get('edit_totalname')
        isloan = kwargs.get('edit_isloan')
        parent_id = kwargs.get('edit_parentid')
        g.db_session.query(Branch).filter(Branch.role_id == role_id).update(
            {Branch.post_code: post_code,Branch.post_name:post_name,Branch.post_totalname:post_totalname,\
Branch.is_loan_post:isloan,Branch.parent_id:parent_id})
        return u"保存成功"

    def check_posts(self,**kwargs):
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
        search_id=kwargs.get('post_id')
        rest=g.db_session.query(User).join(UserBranch,UserBranch.user_id==User.role_id).filter(UserBranch.post_id==search_id).all()
        rs = [{"role_id":k.role_id,"user_name":k.user_name,"name":k.name,"work_status":k.work_status} for k in rest]
        if len(rs)>0:
            return rs
        rest=g.db_session.query(User).join(UserBranch,UserBranch.user_id==User.role_id).join(Branch,UserBranch.post_id==Branch.role_id).filter(Branch.parent_id==search_id).all()
        return [{"role_id":k.role_id,"user_name":k.user_name,"name":k.name,"work_status":k.work_status} for k in rest]

    def find_users_by_postes(self,**kwargs):
        search_id=kwargs.get('post_id')
        is_khjl = kwargs.get('is_khjl')
        print search_id
        slist = search_id.split(',')
        if is_khjl:
            print "todo"
            return "todo"
        else:
            rest_sql = g.db_session.query(User)\
            .join(UserBranch,UserBranch.user_id==User.role_id)\
            .join(Branch, UserBranch.post_id == Branch.role_id)\
            .filter(Branch.post_code.in_(slist))
            print rest_sql
            rest = rest_sql.all()


        return [{"role_id":k.role_id,"user_name":k.user_name,"name":k.name,"work_status":k.work_status} for k in rest]

    #def add_save(self, **kwargs):
    #    drrq = kwargs.get('add_khrq')
    #    jgbh = kwargs.get('add_jgbh')
    #    dxbh = kwargs.get('add_zhbh')
    #    dxxh = kwargs.get('add_zhxh')
    #    gldxbh = kwargs.get('add_ygh')
    #    fjdxbh = kwargs.get('add_khh')
    #    glje1 = kwargs.get('add_gsbl')
    #    glrq1 = kwargs.get('add_glqsrq')
    #    glrq2 = kwargs.get('add_gljsrq')
    #    dxmc = kwargs.get('add_khmc')
    #    ck_type = kwargs.get('add_cklx')
    #    newflag = 0
    #    g.db_session.add(Gsgx_ck(drrq=drrq,jgbh=jgbh,dxbh=dxbh,dxxh=dxxh,gldxbh=gldxbh,fjdxbh=fjdxbh,glje1=glje1,glrq1=glrq1,glrq2=glrq2,dxmc=dxmc,ck_type=ck_type,newflag=newflag))
    #    return u"保存成功"

