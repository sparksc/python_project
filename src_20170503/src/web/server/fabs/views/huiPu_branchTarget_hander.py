# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g,current_app

from ..services import huiPuBranchTarGetHander 
from . import route
import os, errno


bp = Blueprint('huiPu_branchTarget_hander', __name__, url_prefix='/huiPu_branchTarget_hander')

HuiPuBranchTarGetHander= huiPuBranchTarGetHander()
'''
支行目标任务手工
'''
@route(bp, '/branchhander_save',methods=['POST'])
def branchhander_save():
    return HuiPuBranchTarGetHander.branchhander_save(**request.json)

@route(bp, '/branchhander_delete',methods=['POST'])
def branchhander_delete():
    return HuiPuBranchTarGetHander.branchhander_delete(**request.json)

@route(bp, '/branchhander_update',methods=['POST'])
def branchhander_update():
    return HuiPuBranchTarGetHander.branchhander_update(**request.json)

@route(bp, '/branchhander_upload',methods=['POST'])
def branchhander_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return HuiPuBranchTarGetHander.branchhander_upload(local_path,file1.filename)


'''整村授信手工'''

@route(bp, '/credit_save',methods=['POST'])
def credit_save():
    return HuiPuBranchTarGetHander.credit_save(**request.json)

@route(bp, '/credit_delete',methods=['POST'])
def credit_delete():
    return HuiPuBranchTarGetHander.credit_delete(**request.json)

@route(bp, '/credit_update',methods=['POST'])
def credit_update():
    return HuiPuBranchTarGetHander.credit_update(**request.json)

@route(bp, '/credit_upload',methods=['POST'])
def credit_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return HuiPuBranchTarGetHander.credit_upload(local_path,file1.filename)

