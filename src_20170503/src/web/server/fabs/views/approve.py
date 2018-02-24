# -*- coding: utf-8 -*-
"""
    yinsho.api.approve
    #####################

    yinsho approve view module

方法:
    *----------*---------------------------------------------*-------------*
    |HTTP 方法 |  URL                                        |   动作      |
    *----------*---------------------------------------------*-------------*
    |GET       | https://[host]/form/api/v1.0/tasks          | 检索任务列表|
    |GET       | https://[host]/form/api/v1.0/tasks/[task_id]| 检索某个任务|
    |POST      | https://[host]/form/api/v1.0/tasks          | 创建新任务  |
    |PUT       | https://[host]/form/api/v1.0/tasks/[task_id]| 更新任务    |
    |DELETE    | https://[host]/form/api/v1.0/tasks/[task_id]| 删除任务    |
    *----------*---------------------------------------------*-------------*

"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Blueprint, request, json, abort, current_app, jsonify

from ..services import ApproveService
from ..base import helpers
from . import route

approveService = ApproveService()
appr = Blueprint('approve', __name__, url_prefix='/approvals')

@route(appr, '/approve_flag/<application_id>', methods=['POST'])
def approve_flag(application_id):
    return approveService.approve_flag(application_id,**request.json)

@route(appr, '/<application_id>', methods=['GET'])
def approve_info(application_id):
    return approveService.approve_info(application_id)

@route(appr, '/risk/<application_id>', methods=['GET'])
def query_risk(application_id):
    return approveService.query_risk(application_id)

@route(appr, '/next/<application_id>', methods=['GET'])
def get_next(application_id):
    return approveService.get_next(application_id)


@route(appr, '/risk', methods=['POST'])
def save_risk():
    return approveService.save_risk(**request.json)

@route(appr, '/risk', methods=['PUT'])
def update_risk():
    return approveService.update_risk(**request.json)

@route(appr, '/examine/<application_id>', methods=['GET'])
def query_examine(application_id):
    return approveService.query_examine(application_id)

@route(appr, '/examine', methods=['POST'])
def save_examine():
    return approveService.save_examine(**request.json)

@route(appr, '/examine', methods=['PUT'])
def update_examine():
    return approveService.update_examine(**request.json)


@route(appr, '/<application_id>', methods=['POST'])
def approve(application_id):
    return approveService.approve(application_id, **request.json)

@route(appr, '/bat_approve', methods=['POST'])
def bat_approve():
    return approveService.bat_approve(**request.json)

@route(appr, '/report/<application_id>', methods=['POST'])
def save_report(application_id):
    return approveService.save_report(application_id)

@route(appr, '/report/risk/<risk_id>', methods=['POST'])
def save_risk_report(risk_id):
    return approveService.save_risk_report(risk_id)

@route(appr, '/report/examine/<examine_id>', methods=['POST'])
def save_examine_report(examine_id):
    return approveService.save_examine_report(examine_id)

