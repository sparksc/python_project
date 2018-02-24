# -*- coding: utf-8 -*-
"""
    yinsho.api.credit
    #####################

    yinsho  credit module

"""

from flask import Blueprint, request, json, abort, current_app, jsonify,session as web_session, g

#from ..services import DiscountService
#from ..base import helpers
#from . import route
#
#DiscountService = DiscountService()
#
#bp = Blueprint('discount', __name__, url_prefix='/discount')
#
#@route(bp, '/save', methods=['POST'])
#def save_discount():
#    print request.json
#    return DiscountService.save(**request.json)
#
#@route(bp, '/submit', methods=['POST'])
#def submit_discount():
#    return DiscountService.submit(**request.json)

