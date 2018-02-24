# -*- coding: utf-8 -*-
"""
    yinsho.api.UniteCreditService
    #####################

    yinsho  UniteCreditService module

"""

from flask import Blueprint, request, json, abort, current_app, jsonify,session as web_session, g

from ..services import UniteCreditService
from ..base import helpers
from . import route

UniteCreditService = UniteCreditService()

bp = Blueprint('unite_credit', __name__, url_prefix='/unite_credit')

@route(bp, '/create/', methods=['GET'])
def unite_credit_create():
    return UniteCreditService.unite_credit_create()

@route(bp, '/query/<uni_id>', methods=['GET'])
def unite_credit_query(uni_id):
    return UniteCreditService.unite_credit_query(uni_id)

@route(bp, '/update/', methods=['PUT'])
def unite_credit_update():
    return UniteCreditService.unite_credit_update(**request.json)

@route(bp, '/query/', methods=['POST'])
def unite_credit_queryList():
    return UniteCreditService.unite_credit_queryList(**request.json)

@route(bp, '/inflow/<untb_id>', methods=['GET'])
def inflow(untb_id):
    return UniteCreditService.inflow(untb_id)

@route(bp, '/query_by_app/<application_id>', methods=['GET'])
def query_by_application(application_id):
    return UniteCreditService.query_by_application(application_id)
