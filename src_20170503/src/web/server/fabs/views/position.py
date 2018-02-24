# -*- coding: utf-8 -*-
"""
    yinsho.api.nets
    #####################

    yinsho performance view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import poConService
from . import route


bp = Blueprint('position', __name__, url_prefix='/position')
poService = poConService()


@route(bp, '/group_delete',methods=['POST'])
def group_delete():
    return poService.group_delete(**request.json)

@route(bp, '/department_delete',methods=['POST'])
def department_delete():
    return poService.department_delete(**request.json)

@route(bp, '/add',methods=['POST'])
def add():
    return poService.add(**request.json)

@route(bp, '/type_add',methods=['POST'])
def type_add():
    return poService.type_add(**request.json)

@route(bp, '/department_add',methods=['POST'])
def department_add():
    return poService.department_add(**request.json)

@route(bp, '/groups',methods=['POST'])
def groups():
    return poService.groups()

@route(bp, '/find',methods=['POST'])
def find():
    return poService.find(**request.json)

@route(bp, '/targets',methods=['POST'])
def targets():
    return poService.targets(**request.json)

@route(bp, '/objects',methods=['POST'])
def objects():
    return poService.objects()

@route(bp, '/save',methods=['POST'])
def save():
    return poService.save()

@route(bp, '/persons',methods=['POST'])
def persons():
    return poService.persons()

@route(bp, '/load',methods=['POST'])
def load():
    return poService.load()
	
@route(bp, '/add_save',methods=['POST'])
def add_save():
    return poService.add_save(**request.json)	

@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return poService.edit_save(**request.json)

@route(bp, '/group_edit_save',methods=['POST'])
def group_edit_save():
    return poService.group_edit_save(**request.json)

@route(bp, '/department_edit_save',methods=['POST'])
def department_edit_save():
    return poService.department_edit_save(**request.json)


