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
from ..model import Parameter,Menu


class ParameterService():
    """ Target Service  """

    def parameters(self,**kwargs):
        search_name=kwargs.get('name')
	search_code=kwargs.get('code')
	if search_name and not search_code:
	    return g.db_session.query(Parameter).filter(Parameter.dxmc.like('%'+search_name+'%')).all()
	elif search_code and not search_name:
	    return g.db_session.query(Parameter).filter(Parameter.gldxbh==search_code).all()
	elif search_name and search_code:
	    return g.db_session.query(Parameter).filter(or_(Parameter.gldxbh==search_code,Parameter.dxmc==search_name)).all()
	elif not search_code and not search_name:
            return g.db_session.query(Parameter).all()


    def parameter_save(self, **kwargs):
        gldxbh = kwargs.get('add_code')
	dxmc = kwargs.get('add_name')
	je1 = kwargs.get('add_coef')
        re = g.db_session.query(Parameter).filter(or_(Parameter.gldxbh==gldxbh,Parameter.dxmc==dxmc))
        for r in re :
            if r :
        #for group_id in group_ids:
                return u"交易代码或交易名称已存在！请重新输入！"
        g.db_session.add(Parameter(gldxbh=gldxbh,dxmc=dxmc,je1=je1))
        return u"保存成功"

    def parameter_delete(self,**kwargs):
        g.db_session.query(Parameter).filter(Parameter.id==kwargs.get('delete_id')).delete()
        return u"删除成功"

    def parameter_edit_save(self, **kwargs):
        id = kwargs.get('edit_id')
        gldxbh = kwargs.get('edit_code')
        dxmc = kwargs.get('edit_name')
        je1 = kwargs.get('edit_coef')
        g.db_session.query(Parameter).filter(Parameter.id == id).update(
            {Parameter.gldxbh: gldxbh,Parameter.dxmc:dxmc,Parameter.je1:je1})
        return u"保存成功"

