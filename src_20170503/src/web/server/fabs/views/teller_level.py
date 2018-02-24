#-*-coding:utf-8-*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services.teller_level import Teller_levelService
from . import route


bp = Blueprint('teller_level', __name__, url_prefix='/teller_level')

teller_levelService = Teller_levelService()


@route(bp, '/add_save',methods=['POST'])
def add_save():
    return teller_levelService.add_save(**request.json)
@route(bp, '/change_save',methods=['POST'])
def change_save():
    return teller_levelService.change_save(**request.json)
@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return teller_levelService.upload(local_path,file1.filename)
@route(bp,'/delete',methods=['POST'])
def delete():
    return teller_levelService.delete(**request.json)
@route(bp,'/calculate',methods=['POST'])
def calculate():
    return teller_levelService.calculate(**request.json)

@route(bp,'/affirm',methods=['POST'])
def affirm():
    return teller_levelService.affirm(**request.json)
