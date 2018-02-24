# -*- coding: utf-8 -*-
"""
    yinsho.services.BasicSalaryService
    #####################

    yinsho BasicSalaryService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func,or_
from sqlalchemy.orm import joinedload_all

from ..base import utils
# from ..model import Permission, Menu, User, UserGroup, Group, GroupMenu, Branch, UserBranch
from ..model import Branch, T_JGC_JXKH_CS_JBXC


class BasicSalaryService():

    def posname_load(self):
		results = g.db_session.query(T_JGC_JXKH_CS_JBXC).filter(T_JGC_JXKH_CS_JBXC.sjlx == '2').order_by(T_JGC_JXKH_CS_JBXC.para_id).all()
		items = []
		for r in results:
			items.append({'item_id':r.para_id,'dxmc':r.dxmc,'money':r.je1})
		return items

    def posname_edit_save(self,**kwargs):
		id = kwargs.get('item_id')
		dxmc = kwargs.get('dxmc')
		je1 = kwargs.get('money')
		g.db_session.query(T_JGC_JXKH_CS_JBXC).filter(T_JGC_JXKH_CS_JBXC.para_id==id).update({T_JGC_JXKH_CS_JBXC.dxmc:dxmc,T_JGC_JXKH_CS_JBXC.je1:je1})
		return u'修改成功'


    def poslev_load(self):
		results = g.db_session.query(T_JGC_JXKH_CS_JBXC).filter(T_JGC_JXKH_CS_JBXC.sjlx == '8').order_by(T_JGC_JXKH_CS_JBXC.para_id).all()
		items = []
		for r in results:
			items.append({'item_id':r.para_id,'dxmc':r.dxmc,'money':r.je1})
		return items

    def poslev_edit_save(self,**kwargs):
		id = kwargs.get('item_id')
		dxmc = kwargs.get('dxmc')
		je1 = kwargs.get('money')
		g.db_session.query(T_JGC_JXKH_CS_JBXC).filter(T_JGC_JXKH_CS_JBXC.para_id==id).update({T_JGC_JXKH_CS_JBXC.dxmc:dxmc,T_JGC_JXKH_CS_JBXC.je1:je1})
		return u'修改成功'

    def salary_load(self):
		results = g.db_session.query(T_JGC_JXKH_CS_JBXC).filter(or_(T_JGC_JXKH_CS_JBXC.sjlx == '6',T_JGC_JXKH_CS_JBXC.sjlx == '5')).order_by(T_JGC_JXKH_CS_JBXC.para_id).all()
		items = []
		for r in results:
			items.append({'item_id':r.para_id,'dxmc':r.dxmc,'money':r.je1})
		return items

    def salary_edit_save(self,**kwargs):
		id = kwargs.get('item_id')
		dxmc = kwargs.get('dxmc')
		je1 = kwargs.get('money')
		g.db_session.query(T_JGC_JXKH_CS_JBXC).filter(T_JGC_JXKH_CS_JBXC.para_id==id).update({T_JGC_JXKH_CS_JBXC.dxmc:dxmc,T_JGC_JXKH_CS_JBXC.je1:je1})
		return u'修改成功'

    def edu_load(self):
		results = g.db_session.query(T_JGC_JXKH_CS_JBXC).filter(T_JGC_JXKH_CS_JBXC.sjlx == '1').all()
		items = []
		for r in results:
			items.append({'item_id':r.para_id,'dxmc':r.dxmc,'money':r.je1})
		return items

    def edu_edit_save(self,**kwargs):
		id = kwargs.get('item_id')
		dxmc = kwargs.get('dxmc')
		je1 = kwargs.get('money')
		g.db_session.query(T_JGC_JXKH_CS_JBXC).filter(T_JGC_JXKH_CS_JBXC.para_id==id).update({T_JGC_JXKH_CS_JBXC.dxmc:dxmc,T_JGC_JXKH_CS_JBXC.je1:je1})
		return u'修改成功'

    def delete(self,**kwargs):
		item_id = kwargs.get('item_id')
		g.db_session.query(T_JGC_JXKH_LR_QM).filter(T_JGC_JXKH_LR_QM.id==item_id).delete()
		return u'删除成功'

