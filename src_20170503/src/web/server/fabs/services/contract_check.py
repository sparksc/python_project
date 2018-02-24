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
from ..model import PerCon,Menu,Branch


class Contract_checkService():
    """ Target Service  """

    def contract_checks(self,**kwargs):
        search_name=kwargs.get('name')
	if search_name:
	    return g.db_session.query(Target).filter(Target.name.like('%'+search_name+'%')).all()
        return g.db_session.query(PerCon).all()

    def objects(self):
        branches = g.db_session.query(Branch).order_by(Branch.branch_code).all()
        return [{"branch_code":b.branch_code,"branch_name":b.branch_name,"role_id":b.role_id} for b in branches]

