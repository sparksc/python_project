#-*-coding:utf-8-*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services.account_form import Account_formService
from . import route


bp = Blueprint('account_form', __name__, url_prefix='/account_form')

account_formService = Account_formService()


@route(bp, '/add_save',methods=['POST'])
def add_save():
    return account_formService.add_save(**request.json)
@route(bp, '/change_save',methods=['POST'])
def change_save():
    return account_formService.change_save(**request.json)
@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return account_formService.upload(local_path,file1.filename)
@route(bp,'/delete',methods=['POST'])
def delete():
    return account_formService.delete(**request.json)
@route(bp,'/calculate',methods=['POST'])
def calculate():
    return account_formService.calculate(**request.json)
@route(bp,'/affirm',methods=['POST'])
def affirm():
    return account_formService.affirm(**request.json)
