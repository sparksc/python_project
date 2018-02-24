# -*- coding: utf-8 -*-
"""
    yinsho.api.users
    #####################

    yinsho users view module

"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import LoanService
from ..services import UsersService
from ..base import helpers
from . import route

loanService = LoanService()
usersService = UsersService()

bp = Blueprint('loan', __name__, url_prefix='/loan')

@route(bp, '/save', methods=['POST'])
def save():
    return loanService.save(**request.json)

@route(bp, '/acceptanceBill/save', methods=['POST'])
def save_acceptanceBill():
    return loanService.save_acceptanceBill(**request.json)

@route(bp, '/submit', methods=['POST'])
def submit():
    return loanService.submit(**request.json)

@route(bp, '/loan/', methods=['POST'])
def loan():
    return loanService.loan(**request.json)

@route(bp, '/query/<transaction_id>', methods=['GET'])
def query(transaction_id):
    return loanService.query(transaction_id)

@route(bp, '/acceptanceBill/query/<transaction_id>', methods=['GET'])
def query_acceptanceBill(transaction_id):
    return loanService.query_acceptanceBill(transaction_id)

@route(bp, '/lend_transaction', methods=['GET'])
def query_list():
    return loanService.query_list(**request.args)

@route(bp, '/lend_transaction/<application_id>', methods=['GET'])
def query_lend(application_id):
    return loanService.query_lend(application_id)

@route(bp, '/update', methods=['POST'])
def update():
    return loanService.update(**request.json)

@route(bp, '/acceptanceBill/update', methods=['POST'])
def update_acceptanceBill():
    return loanService.update_acceptanceBill(**request.json)

@route(bp, '/loan_print', methods=['POST'])
def loan_print():
    return loanService.loan_print(**request.json)

