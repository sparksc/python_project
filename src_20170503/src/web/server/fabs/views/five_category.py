# -*- coding: utf-8 -*-
"""
    yinsho.api.AfterLoan
    #####################

    yinsho users view module

"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import FiveCategoryService
from ..base import helpers
from . import route

fiveCategoryService = FiveCategoryService()

bp = Blueprint('five_category', __name__, url_prefix='/five_category')

@route(bp, '/save', methods=['POST'])
def save():
    return fiveCategoryService.save(**request.json)

@route(bp, '/submit', methods=['PUT'])
def submit():
    return fiveCategoryService.submit(**request.json)

@route(bp, '/submit', methods=['POST'])
def save_submit():
    return fiveCategoryService.save_submit(**request.json)

@route(bp, '/update/<application_id>', methods=['PUT'])
def update(application_id):
    Udata = {'application_id':application_id,'kwargs':request.json}
    return fiveCategoryService.update(Udata)

@route(bp, '/query/', methods=['GET'])
def query():
    return fiveCategoryService.query(**request.args)

@route(bp, '/query/<application_id>', methods=['GET'])
def querybyid(application_id):
    return fiveCategoryService.query_by_id(application_id)

@route(bp, '/deleteById/', methods=['GET'])
def deletebyid():
    return fiveCategoryService.deletebyid(**request.args)

@route(bp, '/denyById/', methods=['GET'])
def denybyid():
    return fiveCategoryService.denybyid(**request.args)


