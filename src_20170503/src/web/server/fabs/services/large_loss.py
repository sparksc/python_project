# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all

from ..base import utils
from ..model import T_JGC_JXKH_CS_LIUSHI


class Large_lossService():
    """ Target Service  """

    def save(self,*kwargs):
	para_id = kwargs[2]
	sjlx ={u'对私存款':1,u'对公存款':2,u'对私贷款':3,u'对公贷款':4}
	g.db_session.query(T_JGC_JXKH_CS_LIUSHI).filter(T_JGC_JXKH_CS_LIUSHI.para_id == para_id).update({'jyje':kwargs[1]})
	return u"保存成功"
