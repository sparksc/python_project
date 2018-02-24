# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import DictDataService
from . import route


bp = Blueprint('dictdata', __name__, url_prefix='/dictdata')

dictDataService = DictDataService()


@route(bp, '/update',methods=['POST'])
def update():
    return dictDataService.update(**request.json)

@route(bp, '/save',methods=['POST'])
def save():
    return dictDataService.save(**request.json)

@route(bp, '/delete',methods=['POST'])
def delete():
    return dictDataService.delete(**request.json)

@route(bp, '/simple_select',methods=['POST'])
def simple_select():
    return dictDataService.simple_select(**request.json)

@route(bp, '/get_dict',methods=['POST'])
def get_dict():
    return dictDataService.get_dict(**request.json)

@route(bp, '/get_dicts',methods=['POST'])
def get_dicts():
    return dictDataService.get_dicts(**request.json)
