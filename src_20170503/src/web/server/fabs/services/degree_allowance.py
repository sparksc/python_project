# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func,or_
from sqlalchemy.orm import joinedload_all

from ..base import utils
from ..model import T_jgc_jxkh_cs_jbxc,Menu


class T_jgc_jxkh_cs_jbxcService():
    """ Target Service  """

    def t_jgc_jxkh_cs_jbxcs(self,**kwargs):
        search_degree=kwargs.get('degree')
	search_allowance=kwargs.get('allowance')
	i:f search_degree and not search_allowance:
	    return g.db_session.query(T_jgc_jxkh_cs_jbxc).filter(T_jgc_jxkh_cs_jbxc.dxmc.like('%'+search_name+'%')).all()
	elif search_code and not search_name:
	    return g.db_session.query(T_jgc_jxkh_cs_jbxc).filter(T_jgc_jxkh_cs_jbxc.gldxbh==search_code).all()
	elif search_name and search_code:
	    return g.db_session.query(T_jgc_jxkh_cs_jbxc).filter(or_(T_jgc_jxkh_cs_jbxc.gldxbh==search_code,T_jgc_jxkh_cs_jbxc.dxmc==search_name)).all()
	elif not search_code and not search_name:
            return g.db_session.query(T_jgc_jxkh_cs_jbxc).all()
 def t_jgc_jxkh_cs_jbxc_save(self, **kwargs):
        dxmc = kwargs.get('add_degree')
	je1 = kwargs.get('add_allowance')
        re = g.db_session.query(T_jgc_jxkh_cs_jbxc).filter(or_(T_jgc_jxkh_cs_jbxc.dxmc==dxmc))
        for r in re :
            if r :
        #for group_id in group_ids:
                return u"交易代码或交易名称已存在！请重新输入！"
        g.db_session.add(T_jgc_jxkh_cs_jbxc(dxmc=dxmc,je1=je1))
        return u"保存成功"
 def t_jgc_jxkh_cs_jbxc_edit_save(self, **kwargs):
        para_id = kwargs.get('edit_para_id')
        mc = kwargs.get('edit_degree')
        je1 = kwargs.get('edit_allowance')
        g.db_session.query(T_jgc_jxkh_cs_jbxc).filter(T_jgc_jxkh_cs_jbxc.para_id == para_id).update(
            {T_jgc_jxkh_cs_jbxc.dxmc:dxmc,T_jgc_jxkh_cs_jbxc.je1:je1})
        return u"保存成功"
:wq

