# -*- coding: utf-8 -*-
"""
yinsho.api.seims
#####################

yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import ChooseService
from . import route


bp = Blueprint('chooseservice', __name__, url_prefix='/chooseservice')

chooseService = ChooseService()
'存款客户号移交'
@route(bp, '/choose_depcpremove',methods=['POST'])
def choose_depcpremove ():
    current_app.logger.debug(request.json)
    return chooseService.choose_depcpremove(**request.json)

'电子银行移交'
@route(bp, '/choose_ebankpremove',methods=['POST'])
def choose_ebankpremove ():
    current_app.logger.debug(request.json)
    return chooseService.choose_ebankpremove(**request.json)

'贷款移交'
@route(bp, '/choose_loanpremove',methods=['POST'])
def choose_loanpremove ():
    current_app.logger.debug(request.json)
    return chooseService.choose_loanpremove(**request.json)

