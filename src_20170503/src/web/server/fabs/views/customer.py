# -*- coding: utf-8 -*-
"""
    yinsho.api.customers
    #####################

    yinsho customers view module
方法:

    *----------*---------------------------------------------*-------------*
    |HTTP 方法 |  URL                                        |   动作      |
    *----------*---------------------------------------------*-------------*
    |GET       | https://[host]/form/api/v1.0/tasks          | 检索任务列表|
    |GET       | https://[host]/form/api/v1.0/tasks/[task_id]| 检索某个任务|
    |POST      | https://[host]/form/api/v1.0/tasks          | 创建新任务  |
    |PUT       | https://[host]/form/api/v1.0/tasks/[task_id]| 更新任务    |
    |DELETE    | https://[host]/form/api/v1.0/tasks/[task_id]| 删除任务    |
    *----------*---------------------------------------------*-------------*

"""

from flask import Blueprint, request, json, abort, current_app, jsonify

from ..services import CustomerService
from ..base import helpers
from . import route

customerService = CustomerService()
bp = Blueprint('customers', __name__, url_prefix='/customers')

@route(bp, '/roleparty', methods=['POST'])
def queryroleparty():
    u'''组织机构判断查询'''
    return customerService.queryroleparty(**request.json)

@route(bp, '/', methods=['POST'])
def create():
    return customerService.create_customer(**request.json)

@route(bp, '/', methods=['GET'])
def query_customers():
    return customerService.query_customers(**request.args)

@route(bp, '/<customer_id>', methods=['GET'])
def query_customer(customer_id):
    return customerService.query_customer(customer_id)

@route(bp, '/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    return customerService.update_customer(customer_id, **request.json)

@route(bp, '/<customer_id>', methods=['DELETE'])
def delete(customer_id):
    return customerService.delete_customer(customer_id)

@route(bp, '/<customer_id>/academic_record', methods=['POST'])
def create_academic_record(customer_id):
    return customerService.create_academic_record(customer_id, **reqeust.json)

@route(bp, '/<customer_id>/academic_record', methods=['GET'])
def query_academic_records(customer_id):
    return customerService.query_academic_record(customer_id)

@route(bp, '/<customer_id>/academic_record/<record_id>', methods=['GET'])
def query_academic_record(customer_id, record_id):
    return customerService.query_academic_record(customer_id, record_id)

@route(bp, '/<customer_id>/academic_record/<record_id>', methods=['DELETE'])
def delete_academic_record(customer_id, record_id):
    return customerService.delete_academic_record(customer_id, record_id)

@route(bp, '/person', methods=['POST'])
def person_create():
    return customerService.create_person_customer(**request.json)


@route(bp, '/company', methods=['POST'])
def company_create():
    return customerService.create_company_customer(**request.json)

@route(bp, '/company', methods=['GET'])
def query_company_customers():
    return customerService.query_company_customers(**request.args)

@route(bp, '/company/<customer_id>', methods=['GET'])
def query_company_customer(customer_id):
    return customerService.query_company_customer(customer_id)


@route(bp, '/company/<customer_id>', methods=['PUT'])
def update_company_customer(customer_id):
    return customerService.update_company_customer(customer_id, **request.json)

@route(bp,'/persons/',methods=['GET'])
def query_persons():
    return customerService.query_persons(**request.args)

@route(bp,'/companys/',methods=['GET'])
def query_companys():
    return customerService.query_companys(**request.args)

@route(bp,'/assos/<cust_id>',methods=['GET'])
def query_asso(cust_id):
    return customerService.query_asso(cust_id,**request.args)

@route(bp, '/socialInsu/<customer_id>', methods=['PUT'])
def update_socialInsu(customer_id):
    return customerService.update_socialInsu(customer_id, **request.json)

@route(bp, '/principal/<customer_id>', methods=['PUT'])
def update_principal(customer_id):
    return customerService.update_principal(customer_id, **request.json)

@route(bp, '/contCom/<customer_id>', methods=['PUT'])
def update_contCom(customer_id):
    return customerService.update_contCom(customer_id, **request.json)

@route(bp, '/invesMang/<customer_id>', methods=['PUT'])
def update_invesMang(customer_id):
    return customerService.update_invesMang(customer_id, **request.json)

@route(bp, '/capitStr/<customer_id>', methods=['PUT'])
def update_capitStr(customer_id):
    return customerService.update_capitStr(customer_id, **request.json)

@route(bp, '/clientCurr/<customer_id>', methods=['PUT'])
def update_clientCurr(customer_id):
    return customerService.update_clientCurr(customer_id, **request.json)

@route(bp, '/level/person/<customer_id>', methods=['GET'])
def level_person(customer_id):
    return customerService.level_person(customer_id)

@route(bp, '/query_spou/<customer_id>', methods=['GET'])
def query_spou(customer_id):
    return customerService.query_spou(customer_id)

@route(bp, '/query_relatives/<customer_id>', methods=['GET'])
def query_relatives(customer_id):
    return customerService.query_relatives(customer_id)

@route(bp, '/update_relatives/', methods=['PUT'])
def update_relatives():
    return customerService.update_relatives( **request.json)
    






