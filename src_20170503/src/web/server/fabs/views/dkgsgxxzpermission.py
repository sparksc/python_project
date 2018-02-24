# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import DkgsgxxzService
from . import route


bp = Blueprint('dkgsgxxzpermission', __name__, url_prefix='/dkgsgxxzpermission')

dkgsgxxzService = DkgsgxxzService()

@route(bp, '/add_save',methods=['POST'])
def add_save():
    return dkgsgxxzService.add_save(**request.json)

@route(bp, '/do_batch_move',methods=['POST'])
def do_batch_move():
    return dkgsgxxzService.do_batch_move(**request.json)
