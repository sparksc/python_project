# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import ParasetService
from . import route


bp = Blueprint('parasetpermission', __name__, url_prefix='/parasetpermission')

parasetService = ParasetService()


@route(bp, '/parasets',methods=['POST'])
def parasets():
    return parasetService.parasets(**request.json)

@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return parasetService.edit_save(**request.json)


