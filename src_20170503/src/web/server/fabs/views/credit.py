# -*- coding: utf-8 -*-
"""
    yinsho.api.credit
    #####################

    yinsho  credit module

"""

from flask import Blueprint, request, json, abort, current_app, jsonify,session as web_session, g

from ..services import CreditService
from ..base import helpers
from . import route

creditService = CreditService()

bp = Blueprint('credit', __name__, url_prefix='/credit')

@route(bp, '/querystatus/', methods=['POST'])
def querystatus():
    return creditService.querystatus(**request.json)

@route(bp, '/list/', methods=['GET'])
def query_applications():
    return creditService.query_application_list(**request.args)

@route(bp, '/samequery/list/', methods=['GET'])
def query_sameapplication():
    return creditService.query_sames(**request.args)

@route(bp, '/investquery/list/', methods=['GET'])
def query_investapplication():
    return creditService.query_invest(**request.args)

@route(bp, '/<application_id>', methods=['GET'])
def query_application(application_id):
    return creditService.query_application_detail(application_id)

@route(bp, '/comm_credit/<application_id>', methods=['PUT'])
def comm_credit(application_id):
    return creditService.comm_credit(application_id)

@route(bp, '/save', methods=['POST'])
def save():
    return creditService.save(**request.json)

@route(bp, '/submit/', methods=['POST'])
def submit():
    return creditService.submit(**request.json)

@route(bp, '/update', methods=['PUT'])
def update():
    return creditService.update(**request.json)

@route(bp, '/query/<application_id>', methods=['GET'])
def query(application_id):
    return creditService.query(application_id)

@route(bp, '/task', methods=['GET'])
def query_nodown_deal():
    user = g.web_session.user
    return creditService.query_nodone_deal(user)

@route(bp, '/stask', methods=['GET'])
def query_done_deal():
    # TODO: Update globla
    user = g.web_session.user
    return creditService.query_done_deal(user)

@route(bp, '/task/credit', methods=['POST'])
def query_loan_credit():
    user = g.web_session.user
    return creditService.query_crdit_transaction(user)

@route(bp, '/same_bus_submit/', methods=['POST'])
def same_bus_submit():
    return creditService.same_bus_submit(**request.json)

@route(bp, '/same_bus_con/', methods=['POST'])
def same_bus_com():
    return creditService.same_bus_con(**request.json)

@route(bp, '/same_branch/', methods=['GET'])
def same_branch():
    return creditService.same_branch(**request.args)

@route(bp, '/invest_submit/', methods=['POST'])
def invest_submit():
    return creditService.invest_submit(**request.json)

@route(bp,'/products/<product_type>',methods=['GET'])
def products(product_type):
    return creditService.products(product_type)

@route(bp, '/discount/save', methods=['POST'])
def save_discount():
    print request.json
    return creditService.save_discount(**request.json)

@route(bp, '/discount/submit', methods=['POST'])
def submit_discount():
    return creditService.submit_discount(**request.json)

@route(bp, '/discount/saveInfo', methods=['POST'])
def saveInfo_discount():
    return creditService.saveInfo_discount(**request.json)

@route(bp, '/saveapprove/', methods=['POST'])
def saveapprove():
    return creditService.saveapprove(**request.json)
