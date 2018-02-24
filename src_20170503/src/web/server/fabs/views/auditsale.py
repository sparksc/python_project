# -*- coding: utf-8 -*-
"""
    yinsho.api.repossession
    #####################

    yinsho users view module

"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import AuditsaleService
from ..base import helpers
from . import route

auditsaleService = AuditsaleService()

bp = Blueprint('auditsale', __name__, url_prefix='/auditsale')

@route(bp, '/save', methods=['POST'])
def save():
    return auditsaleService.save(**request.json)

@route(bp, '/update/', methods=['POST'])
def update():
    return auditsaleService.update(**request.json)

@route(bp, '/submit', methods=['PUT'])
def submit():
    return auditsaleService.submit(**request.json)

@route(bp, '/submit', methods=['POST'])
def save_submit():
    return auditsaleService.save_submit(**request.json)

@route(bp, '/query/', methods=['GET'])
def query():
    return auditsaleService.query(**request.args)

@route(bp, '/query/<application_id>', methods=['GET'])
def querybyid(application_id):
    return auditsaleService.query_by_id(application_id)

