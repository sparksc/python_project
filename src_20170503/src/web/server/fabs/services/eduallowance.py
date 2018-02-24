# -*- coding: utf-8 -*-
"""
    yinsho.services.EduAllowanceService
    #####################

    yinsho EduAllowanceService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload_all

from ..base import utils
# from ..model import Permission, Menu, User, UserGroup, Group, GroupMenu, Branch, UserBranch
from ..model import Branch, T_JGC_JXKH_CS_JBXC


class EduAllowanceService():
    def edu_load(self):
		results = g.db_session.query(T_JGC_JXKH_CS_JBXC).filter(T_JGC_JXKH_CS_JBXC.sjlx == '1').order_by(T_JGC_JXKH_CS_JBXC.para_id).all()
		items = []
		for r in results:
			items.append({'item_id':r.para_id,'dxmc':r.dxmc,'money':r.je1})
		return items
#	return results
    def edu_edit_save(self,**kwargs):
		id = kwargs.get('item_id')
		dxmc = kwargs.get('dxmc')
		je1 = kwargs.get('money')
		print id,dxmc,je1
		g.db_session.query(T_JGC_JXKH_CS_JBXC).filter(T_JGC_JXKH_CS_JBXC.para_id==id).update({T_JGC_JXKH_CS_JBXC.dxmc:dxmc,T_JGC_JXKH_CS_JBXC.je1:je1})
		return u'修改成功'

