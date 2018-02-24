# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import CusthkService
from . import route
import os, errno


bp = Blueprint('custhk', __name__, url_prefix='/custhk')

custhkService = CusthkService()

@route(bp, '/add_save',methods=['POST'])
def add_save():
    return custhkService.add_save(**request.json)

@route(bp, '/save',methods=['POST'])
def save():
    return custhkService.save(**request.json)

@route(bp, '/ssave',methods=['POST'])
def ssave():
    return custhkService.ssave(**request.json)

@route(bp, '/hk_acct',methods=['POST'])
def hk_acct():
    return custhkService.hk_acct(**request.json)

@route(bp, '/delete',methods=['POST'])
def delete():
    return custhkService.delete(**request.json)

@route(bp, '/sdelete',methods=['POST'])
def sdelete():
    return custhkService.sdelete(**request.json)

@route(bp, '/ebk_delete',methods=['POST'])
def ebk_delete():
    return custhkService.ebk_delete(**request.json)

@route(bp, '/update',methods=['POST'])
def update():
    return custhkService.update(**request.json)

@route(bp, '/ebk_update',methods=['POST'])
def ebk_update():
    return custhkService.ebk_update(**request.json)

@route(bp, '/supdate',methods=['POST'])
def supdate():
    return custhkService.supdate(**request.json)

@route(bp, '/account_move',methods=['POST'])
def move():
    return custhkService.account_move(**request.json)

@route(bp, '/batch_move',methods=['POST'])
def batch_move():
    return custhkService.batch_move(**request.json)

@route(bp,'/upload_per_cust',methods=['POST'])
def upload_per_cust():
    files = request.files.getlist('files')
    file1 = files[0]
    print file1.filename
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    print local_path
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return custhkService.upload_per_cust(local_path)

@route(bp,'/upload_per_ebank',methods=['POST'])
def upload_per_ebank():
    files = request.files.getlist('files')
    file1 = files[0]
    print file1.filename
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    print local_path
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return custhkService.upload_per_ebank(local_path)

@route(bp, '/approve',methods=['POST'])
def approve():
    return custhkService.approve(**request.json)

@route(bp, '/deny',methods=['POST'])
def deny():
    return custhkService.deny(**request.json)

@route(bp, '/get_staff_name',methods=['POST'])
def get_staff_name():
    return custhkService.get_staff_name(**request.json)

@route(bp, '/get_manlist',methods=['POST'])
def get_manlist():
    return custhkService.get_manlist(**request.json)

@route(bp, '/change_main',methods=['POST'])
def change_main():
    return custhkService.change_main(**request.json)

@route(bp, '/check_manager',methods=['POST'])
def check_manager():
    return custhkService.check_manager(**request.json)

@route(bp, '/ssave_with_cust_hook',methods=['POST'])
def ssave_with_cust_hook():
    return custhkService.ssave_with_cust_hook(**request.json)
