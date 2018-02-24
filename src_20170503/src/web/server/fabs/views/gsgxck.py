# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import GsgxckService
from . import route


bp = Blueprint('gsgxck', __name__, url_prefix='/gsgxck')

gsgxckService = GsgxckService()

@route(bp, '/add_save',methods=['POST'])
def add_save():
    return gsgxckService.add_save(**request.json)

@route(bp, '/save',methods=['POST'])
def save():
    return gsgxckService.save(**request.json)

@route(bp, '/update',methods=['POST'])
def update():
    return gsgxckService.update(**request.json)

@route(bp, '/account_move',methods=['POST'])
def account_move():
    return gsgxckService.account_move(**request.json)

@route(bp, '/batch_account_move',methods=['POST'])
def batch_account_move():
    return gsgxckService.batch_account_move(**request.json)

@route(bp, '/batch_account_move_all',methods=['POST'])
def batch_account_move_all():
    return gsgxckService.batch_account_move_all(**request.json)

@route(bp, '/batch_account_move_before',methods=['POST'])
def batch_account_move_before():
    return gsgxckService.batch_account_move_before(**request.json)

@route(bp, '/batch_account_move_delete',methods=['POST'])
def batch_account_move_delete():
    return gsgxckService.batch_account_move_delete(**request.json)

@route(bp, '/get_top',methods=['POST'])
def get_top():
    return gsgxckService.get_top(**request.json)

@route(bp, '/get_top_cust',methods=['POST'])
def get_top_cust():
    return gsgxckService.get_top_cust(**request.json)

@route(bp, '/batch_account_move_check',methods=['POST'])
def batch_account_move_check():
    return gsgxckService.batch_account_move_check(**request.json)

@route(bp, '/batch_account_move_sum',methods=['POST'])
def batch_account_move_sum():
    return gsgxckService.batch_account_move_sum(**request.json)

@route(bp, '/batch_account_move_sum_with_hook',methods=['POST'])
def batch_account_move_sum_with_hook():
    return gsgxckService.batch_account_move_sum_with_hook(**request.json)

@route(bp, '/batch_account_move_sum_with_hook_all',methods=['POST'])
def batch_account_move_sum_with_hook_all():
    return gsgxckService.batch_account_move_sum_with_hook_all(**request.json)

@route(bp, '/staff_all_hook_batch_move',methods=['POST'])
def staff_all_hook_batch_move():
    return gsgxckService.staff_all_hook_batch_move(**request.json)

@route(bp, '/staff_all_hook_batch_move_cancel',methods=['POST'])
def staff_all_hook_batch_move_cancel():
    return gsgxckService.staff_all_hook_batch_move_cancel(**request.json)
 
@route(bp, '/batch_cust_move',methods=['POST'])
def batch_cust_move():
    return gsgxckService.batch_cust_move(**request.json)

@route(bp, '/batch_cust_move_all',methods=['POST'])
def batch_cust_move_all():
    return gsgxckService.batch_cust_move_all(**request.json)

@route(bp, '/batch_account_move_before_all',methods=['POST'])
def batch_account_move_before_all():
    return gsgxckService.batch_account_move_before_all(**request.json)

@route(bp, '/batch_account_move_all_delete',methods=['POST'])
def batch_account_move_all_delete():
    return gsgxckService.batch_account_move_all_delete(**request.json)

@route(bp, '/batch_cust_move_before',methods=['POST'])
def batch_cust_move_before():
    return gsgxckService.batch_cust_move_before(**request.json)

@route(bp, '/batch_cust_move_before_all',methods=['POST'])
def batch_cust_move_before_all():
    return gsgxckService.batch_cust_move_before_all(**request.json)

@route(bp, '/batch_cust_move_delete',methods=['POST'])
def batch_cust_move_delete():
    return gsgxckService.batch_cust_move_delete(**request.json)
@route(bp, '/batch_cust_move_before_all_delete',methods=['POST'])
def batch_cust_move_before_all_delete():
    return gsgxckService.batch_cust_move_before_all_delete(**request.json)

@route(bp, '/batch_cust_move_check',methods=['POST'])
def batch_cust_move_check():
    return gsgxckService.batch_cust_move_check(**request.json)

@route(bp, '/batch_cust_move_sum',methods=['POST'])
def batch_cust_move_sum():
    return gsgxckService.batch_cust_move_sum(**request.json)
 
