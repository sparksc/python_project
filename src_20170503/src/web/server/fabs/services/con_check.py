# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func, text
from sqlalchemy.orm import joinedload_all

from ..base import utils
from ..model import PerCon,Target,Menu,Pe_contract_detail


class Con_checkService():
    """ Target Service  """

    def con_checks(self,**kwargs):
        search_id=kwargs.get('id')
	print(search_id)
	rest=g.db_session.query(Target,Pe_contract_detail)\
        .join(Pe_contract_detail,Pe_contract_detail.pe_pei_id==Target.pei_id)\
	.filter(Pe_contract_detail.contract_id==search_id).all()
        results=[]
	for t,p in rest:
	    results.append({'name':t.name,'data_src':t.data_src,'weight':p.weight,'terget':p.terget,'desc':t.desc,'fact':p.fact,'score':p.score}) 
       # print(rest) 	
        return results
