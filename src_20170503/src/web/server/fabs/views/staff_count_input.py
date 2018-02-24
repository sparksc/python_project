# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import staff_sal_countService
from . import route


bp = Blueprint('staff_count_input', __name__, url_prefix='/staff_count_input')

Staff_sal_countService=staff_sal_countService()

@route(bp, '/add_count',methods=['POST'])
def add_count():
    return Staff_sal_countService.add_count(**request.json)

@route(bp, '/edit_save',methods=['POST'])
def edit_save():
    return Staff_sal_countService.edit_save(**request.json)
