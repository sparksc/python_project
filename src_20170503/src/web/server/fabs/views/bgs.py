# -*- coding: utf-8 -*-
"""
    yinsho.api.nets
    #####################

    yinsho brand_group_user view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import BgsService
from . import route


bp = Blueprint('bgs', __name__, url_prefix='/bgs')

bgsService = BgsService()


@route(bp, '/f_branches',methods=['POST'])
def f_branches():
    return bgsService.f_branches()

@route(bp, '/load',methods=['POST'])
def load():
    return bgsService.load()
	
@route(bp, '/groups',methods=['POST'])
def groups():
    return bgsService.groups()	

@route(bp, '/find_user',methods=['POST'])
def find_user():
    return bgsService.find_user(**request.json)	

@route(bp, '/find_users',methods=['POST'])
def find_users():
    return bgsService.find_users(**request.json)	

@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return bgsService.edit_save(**request.json)

@route(bp, '/add_save',methods=['POST'])
def add_save():
    return bgsService.add_save(**request.json)



