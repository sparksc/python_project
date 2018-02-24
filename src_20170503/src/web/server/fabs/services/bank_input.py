# -*- coding: utf-8 -*-
"""
    yinsho.services.BankInputService
    #####################

    yinsho BankInputService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import joinedload_all

from ..base import utils
# from ..model import Permission, Menu, User, UserGroup, Group, GroupMenu, Branch, UserBranch
from ..model import Branch, T_JGC_JXKH_LR_QM, User, UserBranch


class BankInputService():

    def load(self):
        results = g.db_session.query(T_JGC_JXKH_LR_QM,Branch).\
                join(Branch,Branch.branch_code==T_JGC_JXKH_LR_QM.jgbh).\
                filter(T_JGC_JXKH_LR_QM.sjlx == '4').all()
        items= []
        for t,b in results:
                items.append({'item_id':t.id,'date':t.drrq,'branch_id':t.jgbh,'branch_name':b.branch_name,'user_id':t.yggh,'user_name':t.ygxm,'phone_dev':t.sj_fzs,'phone_act':t.sj_hys,'e_dev':t.eyh,'e_act':t.eyhhy})
        return items

    def branches(self):
        branches = g.db_session.query(Branch).order_by(Branch.branch_code).all()
        return [{"branch_code":b.branch_code,"branch_name":b.branch_name,"role_id":b.role_id,"parent_id":b.parent_id} for b in branches]

    def persons(self,**kwargs):
        branch_code = kwargs.get('branch_code')
        users = g.db_session.query(User).\
                join(UserBranch,UserBranch.user_id==User.role_id).\
                join(Branch,Branch.role_id==UserBranch.branch_id).\
                filter(Branch.branch_code==branch_code).order_by(User.user_name).all()
        return [{"role_id":u.role_id,"user_name":u.user_name,"name":u.name} for u in users]


    def add_save(self,**kwargs):
        drrq = kwargs.get('drrq')
        jgbh = kwargs.get('jgbh')
        yggh = kwargs.get('yggh')
        ygxm = kwargs.get('ygxm')
        sj_fzs = kwargs.get('sj_fzs')
        sj_hys = kwargs.get('sj_hys')
        eyh = kwargs.get('eyh')
        eyhhy = kwargs.get('eyhhy')
        if not eyh :
                eyh=0
        if not eyhhy :
                eyhhy=0
        if not sj_fzs :
                sj_fzs=0
        if not sj_hys :
                sj_hys=0
        g.db_session.add(T_JGC_JXKH_LR_QM(drrq=drrq,jgbh=jgbh,yggh=yggh,ygxm=ygxm,sj_fzs=sj_fzs,sj_hys=sj_hys,eyh=eyh,eyhhy=eyhhy,sjlx='4'))
        return u'添加成功'

    def branch_order(self,**kwargs):
        branch_id = kwargs.get('branch_id')
        result = g.db_session.query(Branch).order_by(Branch.branch_code).all()
        n=0
        for r in result :
            if r.branch_code == branch_id :
                break
            else :
                n=n+1
        return n

    def person_order(self,**kwargs):
        user_name = kwargs.get('user_id')
        branch_code = kwargs.get('branch_code')
        result =  g.db_session.query(User).\
                join(UserBranch,UserBranch.user_id==User.role_id).\
                join(Branch,Branch.role_id==UserBranch.branch_id).\
                filter(Branch.branch_code==branch_code).order_by(User.user_name).all()
        n=0
        print user_name
        for r in result :
            print r.user_name
            if r.user_name == user_name :
                break
            else :
                n=n+1
        return n


    def edit_save(self,**kwargs):
        item_id = kwargs.get('item_id')
        drrq = kwargs.get('drrq')
        jgbh = kwargs.get('jgbh')
        yggh = kwargs.get('yggh')
        ygxm = kwargs.get('ygxm')
        sj_fzs = kwargs.get('sj_fzs')
        sj_hys = kwargs.get('sj_hys')
        eyh = kwargs.get('eyh')
        eyhhy = kwargs.get('eyhhy')
        if not eyh :
                eyh == 0
        if not eyhhy :
                eyhhy== 0
        if not sj_fzs :
                sj_fzs== 0
        if not sj_hys :
                sj_hys== 0
        g.db_session.query(T_JGC_JXKH_LR_QM).filter(T_JGC_JXKH_LR_QM.id==item_id).update({T_JGC_JXKH_LR_QM.drrq:drrq,T_JGC_JXKH_LR_QM.jgbh:jgbh,\
                T_JGC_JXKH_LR_QM.yggh:yggh,T_JGC_JXKH_LR_QM.ygxm:ygxm,T_JGC_JXKH_LR_QM.sj_fzs:sj_fzs,T_JGC_JXKH_LR_QM.sj_hys:sj_hys,\
                T_JGC_JXKH_LR_QM.eyh:eyh,T_JGC_JXKH_LR_QM.eyhhy:eyhhy,T_JGC_JXKH_LR_QM.sjlx:'4'})
        return u'修改成功'


    def delete(self,**kwargs):
        item_id = kwargs.get('item_id')
        g.db_session.query(T_JGC_JXKH_LR_QM).filter(T_JGC_JXKH_LR_QM.id==item_id).delete()
        return u'删除成功'







    def e_load(self):
        results = g.db_session.query(T_JGC_JXKH_LR_QM,Branch).\
                join(Branch,Branch.branch_code==T_JGC_JXKH_LR_QM.jgbh).\
                filter(T_JGC_JXKH_LR_QM.sjlx == '2').all()
        items= []
        for t,b in results:
                items.append({'item_id':t.id,'wh_date':t.drrq,'branch_id':t.jgbh,'user_id':t.yggh,'user_name':t.ygxm,'object_id':t.dxbh,'object_name':t.dxmc,'kh_date':t.clrq})
        return items



    def e_add_save(self,**kwargs):
        drrq = kwargs.get('drrq')
        jgbh = kwargs.get('jgbh')
        yggh = kwargs.get('yggh')
        ygxm = kwargs.get('ygxm')
        dxbh  = kwargs.get('dxbh')
        dxmc = kwargs.get('dxmc')
        clrq = kwargs.get('clrq')
        g.db_session.add(T_JGC_JXKH_LR_QM(drrq=drrq,jgbh=jgbh,yggh=yggh,ygxm=ygxm,dxbh=dxbh,dxmc=dxmc,clrq=clrq,sjlx='2'))
        return u'添加成功'

    def e_edit_save(self,**kwargs):
        item_id = kwargs.get('item_id')
        drrq = kwargs.get('drrq')
        jgbh = kwargs.get('jgbh')
        yggh = kwargs.get('yggh')
        ygxm = kwargs.get('ygxm')
        dxbh  = kwargs.get('dxbh')
        dxmc = kwargs.get('dxmc')
        g.db_session.query(T_JGC_JXKH_LR_QM).filter(T_JGC_JXKH_LR_QM.id==item_id).update({T_JGC_JXKH_LR_QM.drrq:drrq,T_JGC_JXKH_LR_QM.jgbh:jgbh,\
                T_JGC_JXKH_LR_QM.yggh:yggh,T_JGC_JXKH_LR_QM.ygxm:ygxm,T_JGC_JXKH_LR_QM.dxbh:dxbh,T_JGC_JXKH_LR_QM.dxmc:dxmc,\
                T_JGC_JXKH_LR_QM.sjlx:'2'})
        return u'修改成功'
