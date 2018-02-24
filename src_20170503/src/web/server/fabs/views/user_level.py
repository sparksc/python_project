#-*-coding:utf-8-*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services.user_level import User_levelService
from . import route


bp = Blueprint('user_level', __name__, url_prefix='/user_level')

user_levelService = User_levelService()


@route(bp, '/add_save',methods=['POST'])
def add_save():
    return user_levelService.add_save(**request.json)
@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return user_levelService.edit_save(**request.json)
@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return user_levelService.upload(local_path,file1.filename)
@route(bp,'/delete',methods=['POST'])
def delete():
    return user_levelService.delete(**request.json)
@route(bp,'/credentials',methods=['POST'])
def credentials():
    return user_levelService.credentials(**request.json)


