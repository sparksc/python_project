# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import TParaService
from . import route

tParaService = TParaService()

bp = Blueprint('tpara', __name__, url_prefix='/tpara')

@route(bp, '/type_save',methods=['POST'])
def type_save():
    return tParaService.type_save(**request.json)

@route(bp, '/type_update',methods=['POST'])
def type_update():
    return tParaService.type_update(**request.json)

@route(bp, '/header_save',methods=['POST'])
def header_save():
    return tParaService.header_save(**request.json)

@route(bp, '/header_update',methods=['POST'])
def header_update():
    return tParaService.header_update(**request.json)

@route(bp, '/para_save',methods=['POST'])
def para_save():
    return tParaService.para_save(**request.json)

@route(bp, '/row_update',methods=['POST'])
def row_update():
    return tParaService.row_update(**request.json)

@route(bp, '/detail_update',methods=['POST'])
def detail_update():
    return tParaService.detail_update(**request.json)
