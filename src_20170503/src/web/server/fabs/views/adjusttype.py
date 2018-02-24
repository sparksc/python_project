# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import AdjusttypeS
from . import route

adjusttypeService = AdjusttypeS()

bp = Blueprint('adjusttype', __name__, url_prefix='/adjusttype')

@route(bp, '/type_save',methods=['POST'])
def type_save():
    return adjusttypeService.type_save(**request.json)

@route(bp, '/type_update',methods=['POST'])
def type_update():
    return adjusttypeService.type_update(**request.json)


@route(bp, '/type_delete',methods=['POST'])
def type_delete():
    return adjusttypeService.type_delete(**request.json)


@route(bp, '/detail_update',methods=['POST'])
def detail_update():
    return adjusttypeService.detail_update(**request.json)
