# -*- coding: utf-8 -*-
"""
    yinsho.api.repossession
    #####################

    yinsho users view module

"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import RepossessionService
from ..base import helpers
from . import route

repossessionService = RepossessionService()

bp = Blueprint('repossession', __name__, url_prefix='/repossession')

@route(bp, '/save', methods=['POST'])
def save():
    return repossessionService.save(**request.json)

@route(bp, '/submit', methods=['PUT'])
def submit():
    return repossessionService.submit(**request.json)

@route(bp, '/submit', methods=['POST'])
def save_submit():
    return repossessionService.save_submit(**request.json)

@route(bp, '/update', methods=['POST'])
def update():
    print '************'
    return repossessionService.update(**request.json)

@route(bp, '/query/', methods=['GET'])
def query():
    return repossessionService.query(**request.args)

@route(bp, '/query/<application_id>', methods=['GET'])
def querybyid(application_id):
    return repossessionService.query_by_id(application_id)

@route(bp, '/savereport', methods=['POST'])
def savereport():
    return repossessionService.savereport(**request.json)
