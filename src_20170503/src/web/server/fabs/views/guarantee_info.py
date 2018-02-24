# -*- coding: utf-8 -*- 
from flask import Blueprint, request, json, abort, current_app, jsonify
from ..services import  GuaranteeInfoService
from ..base import helpers
from . import route

guaranteeInfoService = GuaranteeInfoService()

bp = Blueprint('guarantee_info', __name__, url_prefix='/guarantee_info')

@route(bp, '/query_party/<customer_name>', methods=['GET'])
def query_party(customer_name):
    return guaranteeInfoService.query_party(customer_name)

@route(bp, '/all_contract_no/<all_contract_no>', methods=['GET'])
def query_allinfo(all_contract_no):
    return guaranteeInfoService.query_allinfo(all_contract_no)

@route(bp, '/save_contract/<contract_id>', methods=['POST'])
def save_contract(contract_id):
    guaranteeInfoService.save_contract(**request.json)
    return True
@route(bp, '/save', methods=['POST'])
def save():
    return guaranteeInfoService.save(**request.json)

@route(bp, '/<guarantee_info_id>', methods=['GET'])
def query(guarantee_info_id):
    return guaranteeInfoService.query(guarantee_info_id)

@route(bp,'/infos/<application_id>',methods=['GET'])
def query_infos(application_id):
    return guaranteeInfoService.query_infos(application_id)

@route(bp, '/<guarantee_info_id>', methods=['PUT'])
def delete(guarantee_info_id):
    return guaranteeInfoService.detele(guarantee_info_id)


@route(bp, '/methods', methods=['GET'])
def query_method():
    return guaranteeInfoService.query_method()

@route(bp, '/InfoSave', methods=['POST'])
def InfoSave():
    guaranteeInfoService.InfoSave(**request.json)
    return True

@route(bp, '/InfoSaves', methods=['POST'])
def InfoSaves():
    guaranteeInfoService.InfoSaves(**request.json)
    return True


