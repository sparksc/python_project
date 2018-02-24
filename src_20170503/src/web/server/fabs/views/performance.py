# -*- coding: utf-8 -*-
"""
    yinsho.api.nets
    #####################

    yinsho performance view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import PerformanceService
from . import route


bp = Blueprint('performance', __name__, url_prefix='/performance')
perService = PerformanceService()


@route(bp, '/del',methods=['POST'])
def delete():
    return perService._del(**request.json)

@route(bp, '/add',methods=['POST'])
def add():
    return perService.add(**request.json)

@route(bp, '/find',methods=['POST'])
def find():
    return perService.find(**request.json)

@route(bp, '/targets',methods=['POST'])
def targets():
    return perService.targets(**request.json)

@route(bp, '/objects',methods=['POST'])
def objects():
    return perService.objects()

@route(bp, '/save',methods=['POST'])
def save():
    return perService.save(**request.json)

@route(bp, '/persons',methods=['POST'])
def persons():
    return perService.persons(**request.json)

@route(bp, '/load',methods=['POST'])
def load():
    return perService.load()
	
@route(bp, '/add_save',methods=['POST'])
def add_save():
    return perService.add_save(**request.json)	

@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return perService.edit_save(**request.json)




