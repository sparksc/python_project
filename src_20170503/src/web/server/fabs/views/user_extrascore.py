#-*-coding:utf-8-*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services.user_extrascore import User_extrascoreService
from . import route


bp = Blueprint('user_extrascore', __name__, url_prefix='/user_extrascore')

user_extrascoreService = User_extrascoreService()


@route(bp, '/add_save',methods=['POST'])
def add_save():
    return user_extrascoreService.add_save(**request.json)
@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return user_extrascoreService.edit_save(**request.json)
@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return user_extrascoreService.upload(local_path,file1.filename)
@route(bp,'/delete',methods=['POST'])
def delete():
    return user_extrascoreService.delete(**request.json)

@route(bp,'/calculate',methods=['POST'])
def calculate():
    return user_extrascoreService.calculate(**request.json)

@route(bp,'/credentials',methods=['POST'])
def credentials():
    return user_extrascoreService.credentials(**request.json)
 

