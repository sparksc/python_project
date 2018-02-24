# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import DepappointService
from . import route


bp = Blueprint('depappoint', __name__, url_prefix='/depappoint')

depappointService = DepappointService()


@route(bp, '/update',methods=['POST'])
def update():
    return depappointService.update(**request.json)

@route(bp, '/save',methods=['POST'])
def save():
    return depappointService.save(**request.json)

@route(bp, '/delete',methods=['POST'])
def delete():
    return depappointService.delete(**request.json)

@route(bp, '/exist',methods=['POST'])
def exist():
    return depappointService.exist(**request.json)
