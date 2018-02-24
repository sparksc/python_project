# -*- coding: utf-8 -*-
"""
    yinsho.api.nets
    #####################

    yinsho brand_group_user view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import BguService
from . import route


bp = Blueprint('bgu', __name__, url_prefix='/bgu')

bguService = BguService()


@route(bp, '/f_branches',methods=['POST'])
def f_branches():
    return bguService.f_branches()

@route(bp, '/load',methods=['POST'])
def load():
    return bguService.load()
	
@route(bp, '/groups',methods=['POST'])
def groups():
    return bguService.groups()	

@route(bp, '/find_user',methods=['POST'])
def find_user():
    return bguService.find_user(**request.json)	

@route(bp, '/find_users',methods=['POST'])
def find_users():
    return bguService.find_users(**request.json)	

@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return bguService.edit_save(**request.json)

@route(bp, '/add_save',methods=['POST'])
def add_save():
    return bguService.add_save(**request.json)



