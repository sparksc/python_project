# -*- coding: utf-8 -*-
"""
    yinsho.api.eduallowance
    #####################

    yinsho edu allowance view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import EduAllowanceService
from . import route


bp = Blueprint('eduallowance', __name__, url_prefix='/eduallowance')

eduAllowanceService = EduAllowanceService()


@route(bp, '/edu_load',methods=['POST'])
def edu_load():
    return eduAllowanceService.edu_load()

@route(bp, '/edu_edit_save',methods=['POST'])
def edu_edit_save():
    return eduAllowanceService.edu_edit_save(**request.json)



