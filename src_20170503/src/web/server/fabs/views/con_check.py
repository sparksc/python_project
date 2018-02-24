# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import Con_checkService
from . import route


bp = Blueprint('con_check', __name__, url_prefix='/con_check')

con_checkService = Con_checkService()


@route(bp, '/con_checks',methods=['POST'])
def con_checks():
    return con_checkService.con_checks(**request.json)


