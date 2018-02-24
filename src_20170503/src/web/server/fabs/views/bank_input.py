# -*- coding: utf-8 -*-
"""
    yinsho.api.bank_input
    #####################

    yinsho bank_input view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import BankInputService
from . import route


bp = Blueprint('bankinput', __name__, url_prefix='/bankinput')

bankInputService = BankInputService()


@route(bp, '/load',methods=['POST'])
def load():
    return bankInputService.load()

@route(bp, '/e_load',methods=['POST'])
def e_load():
    return bankInputService.e_load()

@route(bp, '/branches',methods=['POST'])
def branches():
    return bankInputService.branches()

@route(bp, '/add_save',methods=['POST'])
def add_save():
    return bankInputService.add_save(**request.json)
	
@route(bp, '/e_add_save',methods=['POST'])
def e_add_save():
    return bankInputService.e_add_save(**request.json)

@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return bankInputService.edit_save(**request.json)	

@route(bp, '/e_edit_save',methods=['POST'])
def e_edit_save():
    return bankInputService.e_edit_save(**request.json)	

@route(bp, '/delete',methods=['POST'])
def delete():
    return bankInputService.delete(**request.json)	

@route(bp, '/branch_order',methods=['POST'])
def branch_order():
    return bankInputService.branch_order(**request.json)

@route(bp, '/person_order',methods=['POST'])
def person_order():
    return bankInputService.person_order(**request.json)





@route(bp, '/persons',methods=['POST'])
def persons():
    return bankInputService.persons(**request.json)	

@route(bp, '/loan_load',methods=['POST'])
def loan_load():
    return handInputService.loan_load()

@route(bp, '/loan_add_save',methods=['POST'])
def loan_add_save():
    return handInputService.loan_add_save(**request.json)
	
@route(bp, '/loan_edit_save',methods=['POST'])
def loan_edit_save():
    return handInputService.loan_edit_save(**request.json)	

