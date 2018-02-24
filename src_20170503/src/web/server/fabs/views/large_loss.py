# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import Large_lossService
from . import route


bp = Blueprint('large_loss', __name__, url_prefix='/large_loss')

large_lossService = Large_lossService()
@route(bp, '/save',methods=['POST'])
def save():
    return large_lossService.save(*request.json)

