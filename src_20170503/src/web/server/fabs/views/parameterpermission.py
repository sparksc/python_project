# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import ParameterService
from . import route


bp = Blueprint('parameterpermission', __name__, url_prefix='/parameterpermission')

parameterService = ParameterService()


@route(bp, '/parameters',methods=['POST'])
def parameters():
    return parameterService.parameters(**request.json)

@route(bp, '/parameter_save',methods=['POST'])
def parameter_save():
    return parameterService.parameter_save(**request.json)

@route(bp, '/parameter_delete',methods=['POST'])
def parameter_delete():
    return parameterService.parameter_delete(**request.json)

@route(bp, '/parameter_edit_save',methods=['POST'])
def parameter_edit_save():
    return parameterService.parameter_edit_save(**request.json)


