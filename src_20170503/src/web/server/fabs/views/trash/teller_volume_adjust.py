# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import CounterFineAmountService
from . import route
import os, errno


bp = Blueprint('teller_volume_adjust', __name__, url_prefix='/teller_volume_adjust')

counterFineAmountService = CounterFineAmountService()
'''
柜员扣罚金额手工维护
'''
@route(bp, '/volume_save',methods=['POST'])
def volume_save():
    return counterFineAmountService.volume_save(**request.json)

@route(bp, '/volume_delete',methods=['POST'])
def volume_delete():
    return counterFineAmountService.volume_delete(**request.json)

@route(bp, '/volume_update',methods=['POST'])
def volume_update():
    return counterFineAmountService.volume_update(**request.json)

@route(bp, '/volume_upload',methods=['POST'])
def volume_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return counterFineAmountService.volume_upload(local_path,file1.filename)

'''
网点自助设备
'''
@route(bp, '/dot_save',methods=['POST'])
def dot_save():
    return counterFineAmountService.dot_save(**request.json)

@route(bp, '/dot_delete',methods=['POST'])
def dot_delete():
    return counterFineAmountService.dot_delete(**request.json)

@route(bp, '/dot_update',methods=['POST'])
def dot_update():
    return counterFineAmountService.dot_update(**request.json)

@route(bp, '/dot_upload',methods=['POST'])
def dot_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return counterFineAmountService.dot_upload(local_path,file1.filename)

'''
柜员业务量代收代付手工维护
'''
@route(bp, '/pay_save',methods=['POST'])
def pay_save():
    return counterFineAmountService.pay_save(**request.json)

@route(bp, '/pay_delete',methods=['POST'])
def pay_delete():
    return counterFineAmountService.pay_delete(**request.json)

@route(bp, '/pay_update',methods=['POST'])
def pay_update():
    return counterFineAmountService.pay_update(**request.json)

@route(bp, '/pay_upload',methods=['POST'])
def pay_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return counterFineAmountService.pay_upload(local_path,file1.filename)

'''
柜员业务量计酬手工维护
'''
@route(bp, '/business_save',methods=['POST'])
def business_save():
    return counterFineAmountService.business_save(**request.json)

@route(bp, '/business_delete',methods=['POST'])
def business_delete():
    return counterFineAmountService.business_delete(**request.json)

@route(bp, '/business_update',methods=['POST'])
def business_update():
    return counterFineAmountService.business_update(**request.json)

@route(bp, '/business_upload',methods=['POST'])
def business_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return counterFineAmountService.business_upload(local_path,file1.filename)

'''柜员参与考核人数的手工维护'''
@route(bp, '/exam_save',methods=['POST'])
def exam_save():
    return counterFineAmountService.exam_save(**request.json)

@route(bp, '/exam_delete',methods=['POST'])
def exam_delete():
    return counterFineAmountService.exam_delete(**request.json)

@route(bp, '/exam_update',methods=['POST'])
def exam_update():
    return counterFineAmountService.exam_update(**request.json)

@route(bp, '/exam_upload',methods=['POST'])
def exam_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return counterFineAmountService.exam_upload(local_path,file1.filename)


'''柜员担任其他工作天数的手工维护'''
@route(bp, '/other_save',methods=['POST'])
def other_save():
    return counterFineAmountService.other_save(**request.json)

@route(bp, '/other_delete',methods=['POST'])
def other_delete():
    return counterFineAmountService.other_delete(**request.json)

@route(bp, '/other_update',methods=['POST'])
def other_update():
    return counterFineAmountService.other_update(**request.json)

@route(bp, '/other_upload',methods=['POST'])
def other_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return counterFineAmountService.other_upload(local_path,file1.filename)

''' 柜员计酬调整值手工维护'''
@route(bp, '/adjust_save',methods=['POST'])
def adjust_save():
    return counterFineAmountService.adjust_save(**request.json)

@route(bp, '/adjust_delete',methods=['POST'])
def adjust_delete():
    return counterFineAmountService.adjust_delete(**request.json)

@route(bp, '/adjust_update',methods=['POST'])
def adjust_update():
    return counterFineAmountService.adjust_update(**request.json)

@route(bp, '/adjust_upload',methods=['POST'])
def adjust_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return counterFineAmountService.adjust_upload(local_path,file1.filename)


'''员工请假天数'''
@route(bp, '/lieve_save',methods=['POST'])
def lieve_save():
    return counterFineAmountService.lieve_save(**request.json)

@route(bp, '/lieve_delete',methods=['POST'])
def lieve_delete():
    return counterFineAmountService.lieve_delete(**request.json)

@route(bp, '/lieve_update',methods=['POST'])
def lieve_update():
    return counterFineAmountService.lieve_update(**request.json)

@route(bp, '/lieve_upload',methods=['POST'])
def lieve_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return counterFineAmountService.lieve_upload(local_path,file1.filename)







