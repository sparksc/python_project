# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import BurankService
from . import route
import os, errno


bp = Blueprint('burank', __name__, url_prefix='/burank')

burankService = BurankService()

@route(bp, '/add_save',methods=['POST'])
def add_save():
    return burankService.add_save(**request.json)

@route(bp, '/save',methods=['POST'])
def save():
    return burankService.save(**request.json)

@route(bp, '/delete',methods=['POST'])
def delete():
    return burankService.delete(**request.json)

@route(bp, '/update',methods=['POST'])
def update():
    return burankService.update(**request.json)

@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    print file1.filename
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path + '/' + file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return burankService.upload(local_path,file1)


