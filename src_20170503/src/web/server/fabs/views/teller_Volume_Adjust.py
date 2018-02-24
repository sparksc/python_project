# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import teller_Ajust_base 
from . import route
import os, errno


bp = Blueprint('teller_Volume_Adjust', __name__, url_prefix='/teller_Volume_Adjust')

Teller_Ajust_base= teller_Ajust_base()
'''
柜员考核业务量人数
'''
@route(bp, '/teller_V_Adjust_save',methods=['POST'])
def teller_V_Adjust_save():
    return Teller_Ajust_base.teller_V_Adjust_save(**request.json)

@route(bp, '/teller_V_Adjust_delete',methods=['POST'])
def teller_V_Adjust_delete():
    return Teller_Ajust_base.teller_V_Adjust_delete(**request.json)

@route(bp, '/teller_V_Adjust_update',methods=['POST'])
def teller_V_Adjust_update():
    return Teller_Ajust_base.teller_V_Adjust_update(**request.json)

@route(bp, '/teller_V_Adjust_upload',methods=['POST'])
def teller_V_Adjust_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return Teller_Ajust_base.teller_V_Adjust_upload(local_path,file1.filename)

