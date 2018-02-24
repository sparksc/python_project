#-*-coding:utf-8-*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services.org_level import Org_levelService
from . import route


bp = Blueprint('org_level', __name__, url_prefix='/org_level')

org_levelService = Org_levelService()


@route(bp, '/add_save',methods=['POST'])
def add_save():
    return org_levelService.add_save(**request.json)

@route(bp, '/change_save',methods=['POST'])
def change_save():
    return org_levelService.change_save(**request.json)
    
@route(bp, '/count_save',methods=['POST'])
def count_save():
    return org_levelService.count_save(**request.json)

@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return org_levelService.upload(local_path,file1.filename)

@route(bp,'/count_upload',methods=['POST'])
def count_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return org_levelService.count_upload(local_path,file1.filename)
    
@route(bp,'/delete',methods=['POST'])
def delete():
    return org_levelService.delete(**request.json)

@route(bp,'/conunt_del',methods=['POST'])
def conunt_del():
    return org_levelService.conunt_del(**request.json)

@route(bp,'/calculate',methods=['POST'])
def calculate():
    return org_levelService.calculate(**request.json)

@route(bp,'/count_edit_save',methods=['POST'])
def count_edit_save():
    return org_levelService.count_edit_save(**request.json)

@route(bp,'/affirm',methods=['POST'])
def affirm():
    return org_levelService.affirm(**request.json)
