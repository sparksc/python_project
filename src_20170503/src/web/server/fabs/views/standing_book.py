# -*- coding: utf-8 -*-
"""
    yinsho.api.standingBook
    #####################

    yinsho users view module

"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import StandingBookService
from ..base import helpers
from . import route

standingBookService = StandingBookService()

bp = Blueprint('standing_book', __name__, url_prefix='/standing_book')

@route(bp, '/save', methods=['POST'])
def save():
    return standingBookService.save(**request.json)

@route(bp, '/repossession/save', methods=['POST'])
def save_repossession():
    return standingBookService.save_repossession(**request.json)


@route(bp, '/submit', methods=['PUT'])
def submit():
    return standingBookService.submit(**request.json)

@route(bp, '/update', methods=['POST'])
def update():
    return standingBookService.update(**request.json)

@route(bp, '/update_repossession', methods=['POST'])
def update_repossession():
    return standingBookService.update_repossession(**request.json)

@route(bp, '/debt/query/', methods=['GET'])
def query_debt():
    return standingBookService.query_debt()

@route(bp, '/query/<litigation_book_id>', methods=['GET'])
def query(litigation_book_id):
    return standingBookService.query(litigation_book_id)

@route(bp, '/query_list/', methods=['GET'])
def query_list():
    return standingBookService.query_list()

@route(bp, '/query_repossession/', methods=['GET'])
def query_repossession():
    return standingBookService.query_repossession()

@route(bp, '/export/', methods=['POST'])
def export_book():
    return standingBookService.export_book(**request.json)

@route(bp, '/export_repossession/', methods=['POST'])
def export_repossession_book():
    return standingBookService.export_repossession_book(**request.json)
