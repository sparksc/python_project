# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import Staff_sal_inputService
from . import route


bp = Blueprint('staff_sal_input', __name__, url_prefix='/staff_sal_input')

staff_sal_inputService = Staff_sal_inputService()


@route(bp, '/add_save',methods=['POST'])
def add_save():
    return staff_sal_inputService.add_save(**request.json)
@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return staff_sal_inputService.edit_save(**request.json)
@route(bp, '/sdelete',methods=['POST'])
def sdelete():
    current_app.logger.debug('lcl')
    return staff_sal_inputService.sdelete(**request.json)
@route(bp, '/add_count',methods=['POST'])
def add_count():
    return staff_sal_inputService.add_count(**request.json)
@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    current_app.logger.debug( "------"+local_path)
    return staff_sal_inputService.upload(local_path,file1.filename)


