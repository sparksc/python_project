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


class DkgsgxxzService():
    """ Target Service  """

    def add_save(self, **kwargs):
        drrq = kwargs.get('add_drrq')
        jgbh = kwargs.get('add_jgbh')
        dxbh = kwargs.get('add_zhbh')
        dxxh = kwargs.get('add_zhxh')
        gldxbh = kwargs.get('add_ygh')
	fjdxbh = kwargs.get('add_khh')
	glje1 = kwargs.get('add_gsbl')
	glrq1 = kwargs.get('add_glqsrq')
	glrq2 = kwargs.get('add_gljsrq')
	dxmc = kwargs.get('add_khmc')
	js = 100
	newflag = 0
        g.db_session.add(Gsgx_dk(drrq=drrq,jgbh=jgbh,dxbh=dxbh,dxxh=dxxh,gldxbh=gldxbh,fjdxbh=fjdxbh,glje1=glje1,glrq1=glrq1,glrq2=glrq2,dxmc=dxmc,js=js,newflag=newflag))
        return u"保存成功"

    def do_batch_move(self,**kwargs):
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
