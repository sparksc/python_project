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
from ..model import Branch,Menu,User,UserBranch,Gsgx_dk


class GsgxdkService():
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
        g.db_session.add(Gsgx_dk(drrq=drrq,jgbh=jgbh,dxbh=dxbh,dxxh=dxxh,gldxbh=gldxbh,fjdxbh=fjdxbh,glje1=glje1,glrq1=glrq1,glrq2=glrq2,dxmc=dxmc,ck_type=ck_type,newflag=newflag))
        return u"保存成功"

    def save(self,**kwargs):
        self.ckyy = ['drrq','jgbh','dxbh','dxxh','gldxbh','fjdxbh','glje1','glrq1','glrq2','dxmc','dk_type','newflag']
        newdata =  kwargs.get('newdata')
        data ={}
        for k,v in newdata.items():
            if k in self.ckyy : data[k] = v
        g.db_session.add(Gsgx_dk(**data))
        return u"ok" 

    def update(self,**kwargs):
        self.ckyy = ['drrq','jgbh','dxbh','dxxh','gldxbh','fjdxbh','glje1','glrq1','glrq2','dxmc','dk_type','newflag','para_id']
        newdata =  kwargs.get('newdata')
        pid = newdata.get('para_id')
        newdata.pop('para_id');
        data ={}
        #for k,v in newdata.items():
        #    if k in self.ckyy : data[k] = v
        g.db_session.query(Gsgx_dk).filter(Gsgx_dk.para_id == pid).update(newdata)
        return u"ok"  
    
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
        g.db_session.add(Gsgx_dk(drrq=drrq,jgbh=jgbh,dxbh=dxbh,dxxh=dxxh,gldxbh=gldxbh,fjdxbh=fjdxbh,glje1=glje1,glrq1=glrq1,glrq2=glrq2,dxmc=dxmc,ck_type=ck_type,newflag=newflag))
        
        g.db_session.query(Gsgx_dk).filter(Gsgx_dk.para_id == pid).update({Gsgx_dk.glrq2:glrq1})
        return u"操作成功"

    def batch_move(self, **kwargs):
        newdata = kwargs.get('newdata')
        updatelist = kwargs.get('update_key')

        for pid  in updatelist:
            q = g.db_session.query(Gsgx_dk).filter(Gsgx_dk.para_id == pid).update({Gsgx_dk.glrq2:newdata['glrq1']})
        for pid in updatelist:
            data = g.db_session.query(Gsgx_dk).filter(Gsgx_dk.para_id == pid).first();
            datadict = newdata
            datadict['dxbh'] = data.dxbh
            datadict['dxxh'] = data.dxxh
            datadict['fjdxbh'] = data.fjdxbh
            datadict['dxmc'] = data.dxmc
            g.db_session.add(Gsgx_dk(**datadict))

        return u'移交成功'

            








