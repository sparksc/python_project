# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import hallManagerHander 
from . import route
import os, errno


bp = Blueprint('hall_manager_hander', __name__, url_prefix='/hall_manager_hander')

HallManagerHander= hallManagerHander()
'''
客户经理手工维护
'''
@route(bp, '/manager_num_save',methods=['POST'])
def manager_num_save():
    return HallManagerHander.manager_num_save(**request.json)

@route(bp, '/manager_num_delete',methods=['POST'])
def manager_num_delete():
    return HallManagerHander.manager_num_delete(**request.json)

@route(bp, '/manager_num_update',methods=['POST'])
def manager_num_update():
    return HallManagerHander.manager_num_update(**request.json)

@route(bp, '/manager_num_upload',methods=['POST'])
def manager_num_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return HallManagerHander.manager_num_upload(local_path,file1.filename)


'''
客户经理效酬手工
'''
@route(bp, '/manager_sal_hander_save',methods=['POST'])
def manager_sal_hander_save():
    return HallManagerHander.manager_sal_hander_save(**request.json)

@route(bp, '/manager_sal_hander_delete',methods=['POST'])
def manager_sal_hander_delete():
    return HallManagerHander.manager_sal_hander_delete(**request.json)

@route(bp, '/manager_sal_hander_update',methods=['POST'])
def manager_sal_hander_update():
    return HallManagerHander.manager_sal_hander_update(**request.json)

@route(bp, '/manager_sal_hander_upload',methods=['POST'])
def manager_sal_hander_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return HallManagerHander.manager_sal_hander_upload(local_path,file1.filename)


'''
客户经理担任其他工作天数
'''
@route(bp, '/other_save',methods=['POST'])
def other_save():
    return HallManagerHander.other_save(**request.json)

@route(bp, '/other_delete',methods=['POST'])
def other_delete():
    return HallManagerHander.other_delete(**request.json)

@route(bp, '/other_update',methods=['POST'])
def other_update():
    return HallManagerHander.other_update(**request.json)

@route(bp, '/other_upload',methods=['POST'])
def other_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return HallManagerHander.other_upload(local_path,file1.filename)

'''
客户经理请假天数
'''
@route(bp, '/lieve_save',methods=['POST'])
def lieve_save():
    return HallManagerHander.lieve_save(**request.json)

@route(bp, '/lieve_delete',methods=['POST'])
def lieve_delete():
    return HallManagerHander.lieve_delete(**request.json)

@route(bp, '/lieve_update',methods=['POST'])
def lieve_update():
    return HallManagerHander.lieve_update(**request.json)

@route(bp, '/lieve_upload',methods=['POST'])
def lieve_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return HallManagerHander.lieve_upload(local_path,file1.filename)



'''
支行机具天数
'''
@route(bp, '/branch_atm_save',methods=['POST'])
def branch_atm_save():
    return HallManagerHander.branch_atm_save(**request.json)

@route(bp, '/branch_atm_delete',methods=['POST'])
def branch_atm_delete():
    return HallManagerHander.branch_atm_delete(**request.json)

@route(bp, '/branch_atm_update',methods=['POST'])
def branch_atm_update():
    return HallManagerHander.branch_atm_update(**request.json)

@route(bp, '/branch_atm_upload',methods=['POST'])
def branch_atm_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return HallManagerHander.branch_atm_upload(local_path,file1.filename)





