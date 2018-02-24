# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import Loan_Input
from . import route

Loan_InputService = Loan_Input()

bp = Blueprint('loaninput', __name__, url_prefix='/loaninput')

@route(bp, '/tsave',methods=['POST'])
def tsave():
    return Loan_InputService.tsave(**request.json)

@route(bp, '/loanpersonseach',methods=['POST'])
def loanpersonseach():
    return Loan_InputService.loanpersonseach(**request.json)

@route(bp, '/tedit',methods=['POST'])
def tedit():
    return Loan_InputService.tedit(**request.json)

@route(bp, '/save',methods=['POST'])
def save():
    return Loan_InputService.save(**request.json)


@route(bp, '/tdelt',methods=['POST'])
def tdelt():
    return Loan_InputService.tdelt(**request.json)


@route(bp, '/detail_update',methods=['POST'])
def detail_update():
    return Loan_InputService.detail_update(**request.json)
@route(bp, '/edit',methods=['POST'])
def edit():
    return Loan_InputService.edit(**request.json)

@route(bp, '/delt',methods=['POST'])
def delt():
    return Loan_InputService.delt(**request.json)
