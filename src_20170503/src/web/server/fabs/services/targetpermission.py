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
from ..model import Target,Menu


class TargetService():
    """ Target Service  """

    def targets(self,**kwargs):
        search_name=kwargs.get('name')
	if search_name:
	    return g.db_session.query(Target).filter(Target.name.like('%'+search_name+'%')).all()
        return g.db_session.query(Target).all()

    def target_save(self, **kwargs):
        pei_freq = kwargs.get('add_freq')
        TYPE = kwargs.get('add_type')
	name = kwargs.get('add_name')
	object_type = kwargs.get('add_objtype')
	desc = kwargs.get('add_desc')
        data_src = kwargs.get('add_src')
        
        g.db_session.add(Target(pei_freq=pei_freq,TYPE=TYPE,name=name,object_type=object_type,desc=desc,data_src=data_src))
        return u"保存成功"

    def target_delete(self,**kwargs):
        g.db_session.query(Target).filter(Target.pei_id==kwargs.get('delete_id')).delete()
        return u"删除成功"

    def target_edit_save(self, **kwargs):
        pei_id = kwargs.get('edit_id')
        pei_freq = kwargs.get('edit_freq')
        TYPE = kwargs.get('edit_type')
        name = kwargs.get('edit_name')
        object_type = kwargs.get('edit_objtype')
        desc = kwargs.get('edit_desc')
        data_src = kwargs.get('edit_src')

        g.db_session.query(Target).filter(Target.pei_id==pei_id).delete()
        g.db_session.add(Target(pei_id=pei_id,pei_freq=pei_freq,TYPE=TYPE,name=name,\
object_type=object_type,desc=desc,data_src=data_src))
        return u"保存成功"

