# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import ManagerAddScoService
from . import route
import os, errno


bp = Blueprint('manaddsco', __name__, url_prefix='/manaddsco')

managerAddScoService = ManagerAddScoService()

@route(bp, '/add_save',methods=['POST'])
def add_save():
    return managerAddScoService.add_save(**request.json)

@route(bp, '/save',methods=['POST'])
def save():
    return managerAddScoService.save(**request.json)

@route(bp, '/delete',methods=['POST'])
def delete():
    return managerAddScoService.delete(**request.json)

@route(bp, '/update',methods=['POST'])
def update():
    return managerAddScoService.update(**request.json)

@route(bp, '/account_move',methods=['POST'])
def move():
    return managerAddScoService.account_move(**request.json)

@route(bp, '/batch_move',methods=['POST'])
def batch_move():
    return managerAddScoService.batch_move(**request.json)

@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    print file1.filename
    #upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = '/home/pyuser/wljx/src/web/server/fabs/upload/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return managerAddScoService.upload(local_path)


