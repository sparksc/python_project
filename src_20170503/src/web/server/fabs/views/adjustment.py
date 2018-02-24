# -*- coding: utf-8 -*-
"""
    yinsho.api.repossession
    #####################

    yinsho users view module

"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import AdjustmentService
from ..base import helpers
from . import route

adjustmentService = AdjustmentService()

bp = Blueprint('adjustment', __name__, url_prefix='/adjustment')

@route(bp, '/save', methods=['POST'])
def save():
    return adjustmentService.save(**request.json)

@route(bp, '/update/', methods=['POST'])
def update():
    return adjustmentService.update(**request.json)

@route(bp, '/submit', methods=['PUT'])
def submit():
    return adjustmentService.submit(**request.json)

@route(bp, '/submit', methods=['POST'])
def save_submit():
    return adjustmentService.save_submit(**request.json)

@route(bp, '/query/', methods=['GET'])
def query():
    return adjustmentService.query(**request.args)

@route(bp, '/query/<application_id>', methods=['GET'])
def querybyid(application_id):
    return adjustmentService.query_by_id(application_id)

