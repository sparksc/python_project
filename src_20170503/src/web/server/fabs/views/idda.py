# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import IddaService
from ..base import helpers
from . import route

iddaService = IddaService()
print(1111)
bp = Blueprint('idda', __name__, url_prefix='/idda')

@route(bp, '/idda_save',methods=['POST'])
def idda_save():
    print('ok')
    return iddaService.idda_save(**request.json)

@route(bp, '/type_update',methods=['POST'])
def type_update():
    return iddaService.type_update(**request.json)


@route(bp, '/type_delete',methods=['POST'])
def type_delete():
    return iddaService.type_delete(**request.json)

