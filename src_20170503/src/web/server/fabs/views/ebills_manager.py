#-*-coding:utf-8-*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services.ebills_manager import Ebills_ManagerService
from . import route


bp = Blueprint('ebills_manager', __name__, url_prefix='/ebills_manager')

ebills_managerService = Ebills_ManagerService()


@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return ebills_managerService.edit_save(**request.json)

@route(bp,'/manager_upload',methods=['POST'])
def manager_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    current_app.logger.debug( "------"+local_path)
    return ebills_managerService.manager_upload(local_path,file1.filename)


@route(bp,'/ebills_hook_upload',methods=['POST'])
def ebills_hook_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    current_app.logger.debug( "------"+local_path)
    return ebills_managerService.ebills_hook_upload(local_path,file1.filename)

@route(bp,'/ebills_hook_cunkuan_upload',methods=['POST'])
def ebills_hook_cunkuan_upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    current_app.logger.debug( "------"+local_path)
    return ebills_managerService.ebills_hook_cunkuan_upload(local_path,file1.filename)


@route(bp, '/internation_count',methods=['POST'])
def internation_count():
    return ebills_managerService.internation_count(**request.json)


@route(bp, '/hook_edit_save',methods=['POST'])
def hook_edit_save():
    return ebills_managerService.hook_edit_save(**request.json)

@route(bp, '/total_sum_save',methods=['POST'])
def total_sum_save():
    return ebills_managerService.total_sum_save(**request.json)

@route(bp, '/total_cust_info',methods=['POST'])
def total_cust_info():
    return ebills_managerService.total_cust_info(**request.json)

@route(bp, '/org_stand_update',methods=['POST'])
def org_stand_update():
    return ebills_managerService.org_stand_update(**request.json)

@route(bp, '/org_stand_delete',methods=['POST'])
def org_stand_delete():
    return ebills_managerService.org_stand_delete(**request.json)


@route(bp, '/org_cunkuan_update',methods=['POST'])
def org_cunkuan_update():
    return ebills_managerService.org_cunkuan_update(**request.json)

@route(bp, '/org_cunkuan_delete',methods=['POST'])
def org_cunkuan_delete():
    return ebills_managerService.org_cunkuan_delete(**request.json)




