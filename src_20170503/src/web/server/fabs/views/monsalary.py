# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import monsalaryService
from . import route


bp = Blueprint('monsalary', __name__, url_prefix='/monsalary')

monsalaryService = monsalaryService()


@route(bp, '/update',methods=['POST'])
def update():
    return monsalaryService.update(**request.json)
@route(bp, '/save',methods=['POST'])
def save():
    return monsalaryService.save(**request.json)

