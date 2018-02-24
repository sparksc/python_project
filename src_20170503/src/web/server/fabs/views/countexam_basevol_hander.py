# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import countExamBasevol 
from . import route
import os, errno


bp = Blueprint('countexam_basevol_hander', __name__, url_prefix='/countexam_basevol_hander')

CountExamBasevol= countExamBasevol()
'''
柜员考核业务量人数
'''
@route(bp, '/count_exam_base_vol_save',methods=['POST'])
def count_exam_base_vol_save():
    return CountExamBasevol.count_exam_base_vol_save(**request.json)

@route(bp, '/count_exam_base_vol_delete',methods=['POST'])
def count_exam_base_vol_delete():
    return CountExamBasevol.count_exam_base_vol_delete(**request.json)

@route(bp, '/count_exam_base_vol_update',methods=['POST'])
def count_exam_base_vol_update():
    return CountExamBasevol.count_exam_base_vol_update(**request.json)

@route(bp, '/count_exam_base_vol_upload',methods=['POST'])
def count_exam_base_vol_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return CountExamBasevol.count_exam_base_vol_upload(local_path,file1.filename)


"""
OCR系统差错率机构排名情况
"""
@route(bp, '/ocr_org_rate_error_save',methods=['POST'])
def ocr_org_rate_error_save():
    return CountExamBasevol.ocr_org_rate_error_save(**request.json)

@route(bp, '/ocr_org_rate_error_delete',methods=['POST'])
def ocr_org_rate_error_delete():
    return CountExamBasevol.ocr_org_rate_error_delete(**request.json)

@route(bp, '/ocr_org_rate_error_update',methods=['POST'])
def ocr_org_rate_error_update():
    return CountExamBasevol.ocr_org_rate_error_update(**request.json)

@route(bp, '/ocr_org_rate_error_upload',methods=['POST'])
def ocr_org_rate_error_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return CountExamBasevol.ocr_org_rate_error_upload(local_path,file1.filename)


"""
OCR系统差错率柜员排名情况
"""
@route(bp, '/ocr_sale_rate_error_save',methods=['POST'])
def ocr_sale_rate_error_save():
    return CountExamBasevol.ocr_sale_rate_error_save(**request.json)

@route(bp, '/ocr_sale_rate_error_delete',methods=['POST'])
def ocr_sale_rate_error_delete():
    return CountExamBasevol.ocr_sale_rate_error_delete(**request.json)

@route(bp, '/ocr_sale_rate_error_update',methods=['POST'])
def ocr_sale_rate_error_update():
    return CountExamBasevol.ocr_sale_rate_error_update(**request.json)

@route(bp, '/ocr_sale_rate_error_upload',methods=['POST'])
def ocr_sale_rate_error_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return CountExamBasevol.ocr_sale_rate_error_upload(local_path,file1.filename)

"""
ocr系统一类差错率机构排名情况
"""
@route(bp, '/ocr_first_error_save',methods=['POST'])
def ocr_first_error_save():
    return CountExamBasevol.ocr_first_error_save(**request.json)

@route(bp, '/ocr_first_error_delete',methods=['POST'])
def ocr_first_error_delete():
    return CountExamBasevol.ocr_first_error_delete(**request.json)

@route(bp, '/ocr_first_error_update',methods=['POST'])
def ocr_first_error_update():
    return CountExamBasevol.ocr_first_error_update(**request.json)

@route(bp, '/ocr_first_error_upload',methods=['POST'])
def ocr_first_error_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return CountExamBasevol.ocr_first_error_upload(local_path,file1.filename)


"""
柜员上交清算中心现金清分整点差错情况
"""
@route(bp, '/cash_error_rate_save',methods=['POST'])
def cash_error_rate_save():
    return CountExamBasevol.cash_error_rate_save(**request.json)

@route(bp, '/cash_error_rate_delete',methods=['POST'])
def cash_error_rate_delete():
    return CountExamBasevol.cash_error_rate_delete(**request.json)

@route(bp, '/cash_error_rate_update',methods=['POST'])
def cash_error_rate_update():
    return CountExamBasevol.cash_error_rate_update(**request.json)

@route(bp, '/cash_error_rate_upload',methods=['POST'])
def cash_error_rate_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return CountExamBasevol.cash_error_rate_upload(local_path,file1.filename)

"""
柜员履职发现（阻止）重大差错或风险事故情况表
"""
@route(bp, '/counter_reason_save',methods=['POST'])
def counter_reason_save():
    return CountExamBasevol.counter_reason_save(**request.json)

@route(bp, '/counter_reason_delete',methods=['POST'])
def counter_reason_delete():
    return CountExamBasevol.counter_reason_delete(**request.json)

@route(bp, '/counter_reason_update',methods=['POST'])
def counter_reason_update():
    return CountExamBasevol.counter_reason_update(**request.json)

@route(bp, '/counter_reason_upload',methods=['POST'])
def counter_reason_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return CountExamBasevol.counter_reason_upload(local_path,file1.filename)
