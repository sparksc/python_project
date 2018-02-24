# -*- coding: utf-8 -*-
"""
    yinsho.api.hand_input
    #####################

    yinsho hand_input view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import HandInputService
from . import route


bp = Blueprint('handinput', __name__, url_prefix='/handinput')

handInputService = HandInputService()


@route(bp, '/load',methods=['POST'])
def load():
    return handInputService.load()

@route(bp, '/branches',methods=['POST'])
def branches():
    return handInputService.branches()

@route(bp, '/add_save',methods=['POST'])
def add_save():
    return handInputService.add_save(**request.json)
	
@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return handInputService.edit_save(**request.json)	

@route(bp, '/delete',methods=['POST'])
def delete():
    return handInputService.delete(**request.json)	



@route(bp, '/loan_load',methods=['POST'])
def loan_load():
    return handInputService.loan_load()

@route(bp, '/loan_add_save',methods=['POST'])
def loan_add_save():
    return handInputService.loan_add_save(**request.json)
	
@route(bp, '/loan_edit_save',methods=['POST'])
def loan_edit_save():
    return handInputService.loan_edit_save(**request.json)	

