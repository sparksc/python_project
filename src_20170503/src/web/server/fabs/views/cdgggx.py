# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import CdgggxService
from . import route


bp = Blueprint('cdgggx', __name__, url_prefix='/cdgggx')

cdgggxService = CdgggxService()

@route(bp, '/add_save',methods=['POST'])
def add_save():
    return cdgggxService.add_save(**request.json)

@route(bp, '/save',methods=['POST'])
def save():
    return cdgggxService.save(**request.json)

@route(bp, '/update',methods=['POST'])
def update():
    return cdgggxService.update(**request.json)

@route(bp, '/delete',methods=['POST'])
def delete():
    return cdgggxService.delete(**request.json)

@route(bp, '/move',methods=['POST'])
def move():
    return cdgggxService.move(**request.json)

@route(bp, '/batch_pass',methods=['POST'])
def batch_pass():
    return cdgggxService.batch_pass(**request.json)
    
@route(bp, '/batch_refuse',methods=['POST'])
def batch_refuse():
    return cdgggxService.batch_refuse(**request.json)
