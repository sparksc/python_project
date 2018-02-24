# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import VillageinputService
from . import route
import os, errno


bp = Blueprint('villageinput', __name__, url_prefix='/villageinput')

villageinputService = VillageinputService()

@route(bp, '/save',methods=['POST'])
def save():
    return villageinputService.save(**request.json)

@route(bp, '/delete',methods=['POST'])
def delete():
    return villageinputService.delete(**request.json)

@route(bp, '/update',methods=['POST'])
def update():
    return villageinputService.update(**request.json)

u"""
存款业务计划数参数
"""
@route(bp, '/deposit_save',methods=['POST'])
def deposit_save():
    return villageinputService.deposit_save(**request.json)

@route(bp, '/deposit_delete',methods=['POST'])
def deposit_delete():
    return villageinputService.deposit_delete(**request.json)

@route(bp, '/deposit_update',methods=['POST'])
def deposit_update():
    return villageinputService.deposit_update(**request.json)

@route(bp, '/deposit_upload',methods=['POST'])
def deposit_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    print file1.filename
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename 
    print local_path
    file1.save(local_path)
    return villageinputService.deposit_upload(local_path)

u"""
贷款业务计划参数
"""
@route(bp, '/loan_save',methods=['POST'])
def loan_save():
    return villageinputService.loan_save(**request.json)

@route(bp, '/loan_delete',methods=['POST'])
def loan_delete():
    return villageinputService.loan_delete(**request.json)

@route(bp, '/loan_update',methods=['POST'])
def loan_update():
    return villageinputService.loan_update(**request.json)

@route(bp, '/loan_upload',methods=['POST'])
def loan_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    print file1.filename
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename 
    print local_path
    file1.save(local_path)
    return villageinputService.loan_upload(local_path)

u"""
电子银行业务计划参数
"""
@route(bp, '/ebank_save',methods=['POST'])
def ebank_save():
    return villageinputService.ebank_save(**request.json)

@route(bp, '/ebank_delete',methods=['POST'])
def ebank_delete():
    return villageinputService.ebank_delete(**request.json)

@route(bp, '/ebank_update',methods=['POST'])
def ebank_update():
    return villageinputService.ebank_update(**request.json)

@route(bp, '/ebank_upload',methods=['POST'])
def ebank_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    #print file1.filename
    upload_path = current_app.config.get('UPLOAD_PATH')
    #current_app.logger.debug( "------"+upload_path)
    local_path = upload_path +'/'+file1.filename 
    #print local_path
    file1.save(local_path)
    return villageinputService.ebank_upload(local_path)

u"""
交易码折算率
"""
@route(bp, '/transaction_save',methods=['POST'])
def transaction_save():
    return villageinputService.transaction_save(**request.json)

@route(bp, '/transaction_delete',methods=['POST'])
def transaction_delete():
    return villageinputService.transaction_delete(**request.json)

@route(bp, '/transaction_update',methods=['POST'])
def transaction_update():
    return villageinputService.transaction_update(**request.json)

@route(bp, '/transaction_upload',methods=['POST'])
def transaction_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    print file1.filename
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename 
    print local_path
    file1.save(local_path)
    return villageinputService.transaction_upload(local_path)

u"""
存款绩效试算报表
"""
@route(bp, '/deposit_try',methods=['POST'])
def deposit_try():
    files = request.files.getlist('files')
    file1 = files[0]
    print file1.filename
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename 
    print local_path
    file1.save(local_path)
    return villageinputService.deposit_try(local_path)

u"""
营销入口考核手机银行基础数据导入
"""
@route(bp, '/quarter_term_sale_mbank_base_upload',methods=['POST'])
def quarter_term_sale_mbank_base_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    print file1.filename
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename 
    print local_path
    file1.save(local_path)
    return villageinputService.quarter_term_sale_mbank_base_upload(local_path)

u"""
ETC数据手工导入
"""
@route(bp, '/etc_data_upload',methods=['POST'])
def etc_data_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    print file1.filename
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename 
    print local_path
    file1.save(local_path)
    return villageinputService.etc_data_upload(local_path)

@route(bp, '/etc_org_upload',methods=['POST'])
def etc_org_upload():
    files = request.files.getlist('files')
    org = request.form.get('login_branch_no')
    file1 = files[0]
    print file1.filename
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename 
    print local_path
    file1.save(local_path)
    return villageinputService.etc_org_upload(local_path,org)

@route(bp, '/etc_data_delete',methods=['POST'])
def etc_data_delete():
    return villageinputService.etc_data_delete(**request.json)

@route(bp, '/etc_data_edit',methods=['POST'])
def etc_data_edit():
    return villageinputService.etc_data_edit(**request.json)

u"""
电子银行得分附加分导入
"""
@route(bp, '/ebank_add_save',methods=['POST'])
def ebank_add_save():
    return villageinputService.ebank_add_save(**request.json)

@route(bp, '/ebank_add_delete',methods=['POST'])
def ebank_add_delete():
    return villageinputService.ebank_add_delete(**request.json)

@route(bp, '/ebank_add_update',methods=['POST'])
def ebank_add_update():
    return villageinputService.ebank_add_update(**request.json)

@route(bp, '/ebak_add_upload',methods=['POST'])
def ebak_add_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    print file1.filename
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename 
    print local_path
    file1.save(local_path)
    return villageinputService.ebak_add_upload(local_path)
