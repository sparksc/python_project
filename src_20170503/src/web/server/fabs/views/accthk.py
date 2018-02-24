# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import AccthkService
from . import route


bp = Blueprint('accthk', __name__, url_prefix='/accthk')

accthkService = AccthkService()

@route(bp, '/add_save',methods=['POST'])
def add_save():
    return accthkService.add_save(**request.json)

@route(bp, '/save',methods=['POST'])
def save():
    return accthkService.save(**request.json)

@route(bp, '/ssave',methods=['POST'])
def ssave():
    return accthkService.ssave(**request.json)

@route(bp, '/sssave',methods=['POST'])
def sssave():
    return accthkService.sssave(**request.json)

@route(bp, '/parent_save',methods=['POST'])
def parent_save():
    return accthkService.parent_save(**request.json)

@route(bp, '/parent_approve',methods=['POST'])
def parent_approve():
    return accthkService.parent_approve(**request.json)

@route(bp, '/parent_deny',methods=['POST'])
def parent_deny():
    return accthkService.parent_deny(**request.json)

@route(bp, '/delete',methods=['POST'])
def delete():
    return accthkService.delete(**request.json)

@route(bp, '/sdelete',methods=['POST'])
def sdelete():
    return accthkService.sdelete(**request.json)

@route(bp, '/parent_delete',methods=['POST'])
def parent_delete():
    return accthkService.parent_delete(**request.json)

@route(bp, '/update',methods=['POST'])
def update():
    return accthkService.update(**request.json)

@route(bp, '/supdate',methods=['POST'])
def supdate():
    return accthkService.supdate(**request.json)

@route(bp, '/account_move',methods=['POST'])
def move():
    return accthkService.account_move(**request.json)

@route(bp, '/batch_move',methods=['POST'])
def batch_move():
    return accthkService.batch_move(**request.json)

@route(bp, '/switch_pri',methods=['POST'])
def switch_pri():
    return accthkService.switch_pri(**request.json)

@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    print file1.filename
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path + '/' +file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    print local_path
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return accthkService.upload(local_path)

@route(bp, '/approve',methods=['POST'])
def approve():
    return accthkService.approve(**request.json)

@route(bp, '/deny',methods=['POST'])
def deny():
    return accthkService.deny(**request.json)

@route(bp, '/check_manager',methods=['POST'])
def check_manager():
    return accthkService.check_manager(**request.json)

@route(bp, '/check_lr',methods=['POST'])
def check_lr():
    return accthkService.check_lr(**request.json)

