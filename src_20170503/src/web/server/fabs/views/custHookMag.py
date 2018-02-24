# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g
from ..services import custHookMagService
from . import route


bp = Blueprint('custHookMag', __name__, url_prefix='/custHookMag')

custHookMagService = custHookMagService()

@route(bp, '/cust_move',methods=['POST'])
def cust_move():
    return custHookMagService.cust_move(**request.json)

@route(bp, '/distribute',methods=['POST'])
def distribute():
    return custHookMagService.distribute(**request.json)

@route(bp, '/batch_cust_move',methods=['POST'])
def batch_account_move():
    return custHookMagService.batch_cust_move(**request.json)

@route(bp, '/batch_cust_move_before',methods=['POST'])
def batch_account_move_before():
    return custHookMagService.batch_cust_move_before(**request.json)

@route(bp, '/batch_cust_move_delete',methods=['POST'])
def batch_account_move_delete():
    return custHookMagService.batch_cust_move_delete(**request.json)

@route(bp, '/single_move',methods=['POST'])
def single_move():
    return custHookMagService.single_move(**request.json)

@route(bp, '/single_move_cust',methods=['POST'])
def single_move_cust():
    return custHookMagService.single_move_cust(**request.json)

@route(bp, '/single_approve',methods=['POST'])
def single_approve():
    return custHookMagService.single_approve(**request.json)

@route(bp, '/get_top',methods=['POST'])
def get_top():
    return custHookMagService.get_top(**request.json)
