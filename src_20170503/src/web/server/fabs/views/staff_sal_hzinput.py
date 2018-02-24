# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import Staff_sal_hzinputService
from . import route


bp = Blueprint('staff_sal_hzinput', __name__, url_prefix='/staff_sal_hzinput')

staff_sal_hzinputService = Staff_sal_hzinputService()


@route(bp, '/add_save',methods=['POST'])
def add_save():
    return staff_sal_hzinputService.add_save(**request.json)
@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return staff_sal_hzinputService.edit_save(**request.json)
@route(bp, '/sdelete',methods=['POST'])
def sdelete():
    current_app.logger.debug('lcl')
    return staff_sal_hzinputService.sdelete(**request.json)
@route(bp,'/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    current_app.logger.debug( "------"+local_path)
    return staff_sal_hzinputService.upload(local_path,file1.filename)


