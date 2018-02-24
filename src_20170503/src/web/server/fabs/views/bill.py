# -*- coding: utf-8 -*-
"""
    yinsho.api.bill
    #####################

    yinsho bill 

"""

from flask import Blueprint, request, json, abort, current_app, jsonify,session as web_session, g
from werkzeug import secure_filename
from ..services import BillService
from ..base import helpers
from . import route
import os

billService = BillService()

bp = Blueprint('bill', __name__, url_prefix='/bill')

@route(bp, '/query/<application_id>', methods=['POST'])
def bill_query(application_id):
    return billService.bill_query(application_id,**request.json)

@route(bp, '/update/<bill_id>', methods=['PUT'])
def bill_update(bill_id):
    return billService.bill_update(bill_id,**request.json)

@route(bp, '/create/<application_id>', methods=['POST'])
def bill_create(application_id):
    return billService.bill_create(application_id,**request.json)

@route(bp, '/query_info/<application_id>', methods=['GET'])
def bill_query_info(application_id):
    return billService.bill_query_info(application_id)

@route(bp, '/delete/<bill_id>', methods=['PUT'])
def bill_delete(bill_id):
    return billService.bill_delete(bill_id)

@route(bp, '/check/<application_id>', methods=['POST'])
def bill_check(application_id):
    return billService.bill_check(application_id,**request.json)

@route(bp, '/check_query/<application_id>', methods=['GET'])
def bill_check_query(application_id):
    return billService.bill_check_query(application_id)

'''
    票据清单数据导入上传
'''
@route(bp,'/listBill/upload/',methods=["POST"])
def listBill_upload():
    files = request.files.getlist('file')
    file = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = os.path.join(upload_path,secure_filename(file.filename))
    file.save(local_path)
    application_id = request.form.get('application_id')
    return billService.listBill_import_data(local_path, application_id)

'''
    票据录入数据导入上传
'''
@route(bp,'/Bill/upload/',methods=["POST"])
def Bill_upload():
    files = request.files.getlist('file')
    file = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = os.path.join(upload_path,secure_filename(file.filename))
    file.save(local_path)
    application_id = request.form.get('application_id')
    return billService.Bill_import_data(local_path, application_id)

@route(bp, '/query_dis_name/<account_no>', methods=['GET'])
def query_dis_name(account_no):
    return billService.query_dis_name(account_no)
