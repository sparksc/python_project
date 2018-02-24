# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import GsgxdkService
from . import route


bp = Blueprint('gsgxdk', __name__, url_prefix='/gsgxdk')

gsgxdkService = GsgxdkService()

@route(bp, '/add_save',methods=['POST'])
def add_save():
    return gsgxdkService.add_save(**request.json)

@route(bp, '/save',methods=['POST'])
def save():
    return gsgxdkService.save(**request.json)

@route(bp, '/update',methods=['POST'])
def update():
    return gsgxdkService.update(**request.json)

@route(bp, '/move',methods=['POST'])
def move():
    return gsgxdkService.move(**request.json)

@route(bp, '/batch_move',methods=['POST'])
def batch_move():
    return gsgxdkService.batch_move(**request.json)
