#-*-coding:utf-8-*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services.ebank_replace import Ebank_replaceService
from . import route


bp = Blueprint('ebank_replace', __name__, url_prefix='/ebank_replace')

ebank_replaceService = Ebank_replaceService()


@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return ebank_replaceService.edit_save(**request.json)
@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return ebank_replaceService.upload(local_path,file1.filename)
@route(bp,'/delete',methods=['POST'])
def delete():
    return ebank_replaceService.delete(**request.json)
@route(bp,'/credentials',methods=['POST'])
def credentials():
    return ebank_replaceServiceService.credentials(**request.json)


