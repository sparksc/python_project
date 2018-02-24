# -*- coding: utf-8 -*-
"""
    yinsho.services.HandInputService
    #####################

    yinsho HandInputService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all

from ..base import utils
# from ..model import Permission, Menu, User, UserGroup, Group, GroupMenu, Branch, UserBranch
from ..model import Branch, T_JGC_JXKH_LR_QM


class HandInputService():

    def load(self):
        results = g.db_session.query(T_JGC_JXKH_LR_QM,Branch).\
                join(Branch,Branch.branch_code==T_JGC_JXKH_LR_QM.jgbh).\
                filter(T_JGC_JXKH_LR_QM.sjlx == '6').all()
        items= []
        for t,b in results:
                items.append({'item_id':t.id,'date':t.drrq,'branch_code':t.jgbh,'branch_name':b.branch_name,'rate':t.jytdl})
        return items

    def branches(self):
        branches =  g.db_session.query(Branch).order_by(Branch.branch_code).all()
        return [{"branch_code":b.branch_code,"branch_name":b.branch_name,"role_id":b.role_id} for b in branches]

    def add_save(self,**kwargs):
        drrq = kwargs.get('drrq')
        jgbh = kwargs.get('jgbh')
        jytdl = kwargs.get('jytdl')
        g.db_session.add(T_JGC_JXKH_LR_QM(drrq=drrq,jgbh=jgbh,jytdl=jytdl,sjlx='6'))
        return u'添加成功'

    def edit_save(self,**kwargs):
        id = kwargs.get('item_id')
        drrq = kwargs.get('drrq')
        jgbh = kwargs.get('jgbh')
        jytdl = kwargs.get('jytdl')
        g.db_session.query(T_JGC_JXKH_LR_QM).filter(T_JGC_JXKH_LR_QM.id==id).update({T_JGC_JXKH_LR_QM.drrq:drrq,T_JGC_JXKH_LR_QM.jgbh:jgbh,T_JGC_JXKH_LR_QM.jytdl:jytdl})
        return u'编辑成功'

    def delete(self,**kwargs):
        item_id = kwargs.get('item_id')
        g.db_session.query(T_JGC_JXKH_LR_QM).filter(T_JGC_JXKH_LR_QM.id==item_id).delete()
        return u'删除成功'

    def loan_load(self):
        results = g.db_session.query(T_JGC_JXKH_LR_QM,Branch).\
                join(Branch,Branch.branch_code==T_JGC_JXKH_LR_QM.jgbh).\
                filter(T_JGC_JXKH_LR_QM.sjlx == '7').all()
        items= []
        for t,b in results:
                items.append({'item_id':t.id,'date':t.drrq,'branch_code':t.jgbh,'branch_name':b.branch_name,'rate':t.bytdl})
        return items


    def loan_add_save(self,**kwargs):
        drrq = kwargs.get('drrq')
        jgbh = kwargs.get('jgbh')
        bytdl = kwargs.get('bytdl')
        g.db_session.add(T_JGC_JXKH_LR_QM(drrq=drrq,jgbh=jgbh,bytdl=bytdl,sjlx='7'))
        return u'添加成功'

    def loan_edit_save(self,**kwargs):
        id = kwargs.get('item_id')
        drrq = kwargs.get('drrq')
        jgbh = kwargs.get('jgbh')
        bytdl = kwargs.get('bytdl')
        g.db_session.query(T_JGC_JXKH_LR_QM).filter(T_JGC_JXKH_LR_QM.id==id).update({T_JGC_JXKH_LR_QM.drrq:drrq,T_JGC_JXKH_LR_QM.jgbh:jgbh,T_JGC_JXKH_LR_QM.bytdl:bytdl})
        return u'编辑成功'

