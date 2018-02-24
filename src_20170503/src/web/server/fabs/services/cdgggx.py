# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all

from ..base import utils
from ..model import Branch,Menu,User,UserBranch,Cdgggx


class CdgggxService():
    """ Target Service  """

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
        g.db_session.add(Cdgggx(drrq=drrq,jgbh=jgbh,dxbh=dxbh,dxxh=dxxh,gldxbh=gldxbh,fjdxbh=fjdxbh,glje1=glje1,glrq1=glrq1,glrq2=glrq2,dxmc=dxmc,ck_type=ck_type,newflag=newflag))
        return u"保存成功"

    def save(self,**kwargs):
        self.ckyy = ['drrq','jgbh','dxbh','dxxh','gldxbh','fjdxbh','glje1','glrq1','glrq2','dxmc','gggx','status','check_status','newflag']
        newdata =  kwargs.get('newdata')
        data ={}
        for k,v in newdata.items():
            if k in self.ckyy : data[k] = v
        g.db_session.add(Cdgggx(**data))
        return u"ok" 

    def update(self,**kwargs):
        self.ckyy = ['drrq','jgbh','dxbh','dxxh','gldxbh','fjdxbh','glje1','glrq1','glrq2','dxmc','gggx','status','check_status','newflag','para_id']
        newdata =  kwargs.get('newdata')
        pid = newdata.get('para_id')
        newdata.pop('para_id');
        data ={}
        #for k,v in newdata.items():
        #    if k in self.ckyy : data[k] = v
        g.db_session.query(Cdgggx).filter(Cdgggx.para_id == pid).update(newdata)
        return u"ok" 
    def delete(self,**kwargs):
        newdata = kwargs.get('newdata')
        pid = newdata.get('para_id')
        g.db_session.query(Cdgggx).filter(Cdgggx.para_id == pid).delete()        
    
    def move(self, **kwargs):
        pid = kwargs.get('pid')
        drrq = kwargs.get('move_drrq')
        jgbh = kwargs.get('move_jgbh')
        dxbh = kwargs.get('move_zhbh')
        dxxh = kwargs.get('move_zhxh')
        gldxbh = kwargs.get('move_ygh')
        fjdxbh = kwargs.get('move_khh')
        glje1 = kwargs.get('move_gsbl')
        glrq1 = kwargs.get('move_glqsrq')
        glrq2 = kwargs.get('move_gljsrq')
        dxmc = kwargs.get('move_khmc')
        ck_type = kwargs.get('move_cklx')
        newflag = 0
        g.db_session.add(Cdgggx(drrq=drrq,jgbh=jgbh,dxbh=dxbh,dxxh=dxxh,gldxbh=gldxbh,fjdxbh=fjdxbh,glje1=glje1,glrq1=glrq1,glrq2=glrq2,dxmc=dxmc,ck_type=ck_type,newflag=newflag))
        
        g.db_session.query(Cdgggx).filter(Cdgggx.para_id == pid).update({Cdgggx.glrq2:glrq1})
        return u"操作成功"

    def batch_pass(self, **kwargs):
        newdata = kwargs.get('newdata')
        for pid in newdata:
            q = g.db_session.query(Cdgggx).filter(Cdgggx.para_id == pid).update({'check_status':1,'status':0})
        return u'批量复核成功'

    def batch_refuse(self, **kwargs):
        newdata = kwargs.get('newdata')
        for pid in newdata:
            q = g.db_session.query(Cdgggx).filter(Cdgggx.para_id == pid).update({'check_status':2})
        return u'批量复核成功'

            








