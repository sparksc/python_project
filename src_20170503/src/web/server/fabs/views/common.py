# -*- coding: utf-8 -*-
"""
    yinsho.api.common
    #####################

    yinsho common view module

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

from ..services import CommonService
from ..base import helpers
from . import route

commonService = CommonService()
comm = Blueprint('common', __name__, url_prefix='/common')

@route(comm,'/industry/<industry_d>',methods=['GET'])
def query_industry(industry_d):
    return commonService.query_industry(industry_d)

@route(comm,'/industry/cust/<party_id>',methods=['GET'])
def query_industry_cust(party_id):
    return commonService.query_industry_cust(party_id)

@route(comm,'/cust_level/person/create/<cust_id>',methods=['POST'])
def create_person_level(cust_id):
    return commonService.create_person_level(cust_id,**request.json)

@route(comm,'/batch/',methods=['GET'])
def batch():
    return commonService.batch()

def create_person_level(cust_id):
    return commonService.create_person_level(cust_id,**request.json)


