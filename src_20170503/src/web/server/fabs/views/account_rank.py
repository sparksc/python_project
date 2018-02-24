#-*-coding:utf-8-*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services.account_rank import Account_rankService
from . import route


bp = Blueprint('account_rank', __name__, url_prefix='/account_rank')

account_rankService = Account_rankService()


@route(bp, '/add_save',methods=['POST'])
def add_save():
    return account_rankService.add_save(**request.json)
@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return account_rankService.edit_save(**request.json)
@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return account_rankService.upload(local_path,file1.filename)
@route(bp,'/delete',methods=['POST'])
def delete():
    return account_rankService.delete(**request.json)
@route(bp,'/calculate',methods=['POST'])
def calculate():
    return account_rankService.calculate(**request.json)
    """
@route(bp,'/credentials',methods=['POST'])
def credentials():
    return account_rankService.credentials(**request.json)
    """
    """
@route(bp,'/managers',methods=['POST'])
def managers():
    return data_inputService.managers(**request.json)
    """
