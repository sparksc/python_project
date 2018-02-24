# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import reportmagService
from . import route

reportmagService = reportmagService()

bp = Blueprint('reportmag', __name__, url_prefix='/reportmag')

@route(bp, '/type_save',methods=['POST'])
def type_save():
    return reportmagService.type_save(**request.json)

@route(bp, '/type_update',methods=['POST'])
def type_update():
    return reportmagService.type_update(**request.json)

@route(bp, '/menu_save',methods=['POST'])
def menu_save():
    return reportmagService.menu_save(**request.json)
