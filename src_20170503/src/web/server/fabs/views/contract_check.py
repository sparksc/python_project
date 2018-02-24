# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import Contract_checkService
from . import route


bp = Blueprint('contract_check', __name__, url_prefix='/contract_check')

contract_checkService = Contract_checkService()


@route(bp, '/contract_checks',methods=['POST'])
def contract_checks():
    return contract_checkService.contract_checks(**request.json)


@route(bp, '/objects',methods=['POST'])
def objetcs():
    return contract_checkService.objects()


