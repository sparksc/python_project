# -*- coding: utf-8 -*-
"""
    yinsho.api.repossession
    #####################

    yinsho users view module

"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import ExtensionService
from ..base import helpers
from . import route

extensionService = ExtensionService()

bp = Blueprint('extension', __name__, url_prefix='/extension')

@route(bp, '/save', methods=['POST'])
def save():
    return extensionService.save(**request.json)

@route(bp, '/update/', methods=['POST'])
def update():
    return extensionService.update(**request.json)

@route(bp, '/submit', methods=['PUT'])
def submit():
    return extensionService.submit(**request.json)

@route(bp, '/submit', methods=['POST'])
def save_submit():
    return extensionService.save_submit(**request.json)

@route(bp, '/query/', methods=['GET'])
def query():
    return extensionService.query(**request.args)

@route(bp, '/query/<application_id>', methods=['GET'])
def querybyid(application_id):
    return extensionService.query_by_id(application_id)

