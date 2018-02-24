# -*- coding: utf-8 -*- 
"""
    yinsho.api.contract
    #####################
                        
    yinsho  report module
    
"""                       
                         
from flask import Blueprint, request, json, abort, current_app, jsonify,session as web_session, g
                           
from ..services import ContractService
from ..base import helpers   
from . import route
                                   
contractService = ContractService()

bp = Blueprint('contact', __name__, url_prefix='/contracts')

@route(bp, '/querycontract/<application_id>', methods=['POST'])
def querycontract(application_id):
    return contractService.querycontract(application_id)
                          
@route(bp, '/save', methods=['POST'])
def save():                      
    return contractService.save(**request.json)

@route(bp, '/submit/', methods=['POST'])
def submit():
    return contractService.submit(**request.json)

@route(bp, '/update/<application_id>', methods=['PUT'])
def update(application_id):
    why = {'application_id':application_id,'kwargs':request.json}
    return contractService.update(why)

@route(bp, '/', methods=['GET'])
def query():
    return contractService.query(**request.args)

@route(bp, '/lend_contract/', methods=['GET'])
def query_lend():
    return contractService.query_lend(**request.args)

@route(bp, '/<contract_id>', methods=['GET'])
def get(contract_id):
    return contractService.get(contract_id)

@route(bp, '/list_update/', methods=['PUT'])
def list_update():
    return contractService.list_update(**request.json)

@route(bp, '/list_query/<transaction_id>', methods=['GET'])
def list_query(transaction_id):
    return contractService.list_query(transaction_id)

@route(bp, '/update_payment/<debt_id>', methods=['PUT'])
def update_payment(debt_id):
    print debt_id
    return contractService.update_payment(**request.json)

@route(bp, '/query_payment/<debt_id>', methods=['GET'])
def query_payment(debt_id):
    return contractService.query_payment(debt_id)
