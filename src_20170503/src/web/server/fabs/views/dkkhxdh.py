# -*- coding: utf-8 -*-
"""
    yinsho.api.dkkhxdh
    #####################

    yinsho dkkhxdh view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import DkkhxdhService
from . import route

dkkhxdhService = DkkhxdhService()

bp = Blueprint('dkkhxdh', __name__, url_prefix='/dkkhxdh')

@route(bp, '/khh_save',methods=['POST'])
def khh_save():
    return dkkhxdhService.khh_save(**request.json)

@route(bp, '/khh_update',methods=['POST'])
def khh_update():
    return dkkhxdhService.khh_update(**request.json)


@route(bp, '/khh_delete',methods=['POST'])
def khh_delete():
    return dkkhxdhService.khh_delete(**request.json)


@route(bp, '/detail_update',methods=['POST'])
def detail_update():
    return dkkhxdhService.detail_update(**request.json)
