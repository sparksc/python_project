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
from ..model import Paraset,Menu


class ParasetService():
    """ Target Service  """

    def parasets(self,**kwargs):
        return g.db_session.query(Paraset).all()

    def edit_save(self, **kwargs):
        rqsc = kwargs.get('edit_rqsc')

	g.db_session.query(Paraset).filter(Paraset.yyyxrq == 1).update(
            {Paraset.rqsc:rqsc})

        return u"保存成功"

