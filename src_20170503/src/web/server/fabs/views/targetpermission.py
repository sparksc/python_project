# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import TargetService
from . import route


bp = Blueprint('targetpermission', __name__, url_prefix='/targetpermission')

targetService = TargetService()


@route(bp, '/targets',methods=['POST'])
def targets():
    return targetService.targets(**request.json)

@route(bp, '/target_save',methods=['POST'])
def target_save():
    return targetService.target_save(**request.json)

@route(bp, '/target_delete',methods=['POST'])
def target_delete():
    return targetService.target_delete(**request.json)

@route(bp, '/target_edit_save',methods=['POST'])
def target_edit_save():
    return targetService.target_edit_save(**request.json)


