#-*-coding:utf-8-*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services.branch_funong_card import Branch_funong_cardService
from . import route


bp = Blueprint('branch_funong_card', __name__, url_prefix='/branch_funong_card')

branch_funong_cardService = Branch_funong_cardService()

    
@route(bp, '/count_save',methods=['POST'])
def count_save():
    return branch_funong_cardService.count_save(**request.json)

@route(bp,'/count_upload',methods=['POST'])
def count_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename
    file1.save(local_path)
    return branch_funong_cardService.count_upload(local_path,file1.filename)

@route(bp,'/conunt_del',methods=['POST'])
def conunt_del():
    return branch_funong_cardService.conunt_del(**request.json)


@route(bp,'/count_edit_save',methods=['POST'])
def count_edit_save():
    return branch_funong_cardService.count_edit_save(**request.json)
