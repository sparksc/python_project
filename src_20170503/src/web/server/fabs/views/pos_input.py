# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import Pos_inputService
from . import route


bp = Blueprint('pos_input', __name__, url_prefix='/pos_input')

pos_inputService = Pos_inputService()


@route(bp, '/add_save',methods=['POST'])
def add_save():
    return pos_inputService.add_save(**request.json)
@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return pos_inputService.edit_save(**request.json)
@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return pos_inputService.upload(local_path,file1.filename)


