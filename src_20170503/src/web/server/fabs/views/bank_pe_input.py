# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import BankProfitEarningService
from . import route
import os, errno


bp = Blueprint('bank_pe_input', __name__, url_prefix='/bank_pe_input')

bankProfitEarningService = BankProfitEarningService()

@route(bp, '/add_save',methods=['POST'])
def add_save():
    return bankProfitEarningService.add_save(**request.json)

@route(bp, '/save',methods=['POST'])
def save():
    return bankProfitEarningService.save(**request.json)

@route(bp, '/delete',methods=['POST'])
def delete():
    return bankProfitEarningService.delete(**request.json)

@route(bp, '/update',methods=['POST'])
def update():
    return bankProfitEarningService.update(**request.json)

@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    print file1.filename
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path + '/' + file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return bankProfitEarningService.upload(local_path,file1)


