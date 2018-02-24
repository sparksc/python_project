# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import DepstockmtfinputService
from . import route
import os, errno


bp = Blueprint('depstockmtfinput', __name__, url_prefix='/depstockmtfinput')

depstockmtfinputService = DepstockmtfinputService()

@route(bp, '/save',methods=['POST'])
def save():
    return depstockmtfinputService.save(**request.json)

@route(bp, '/delete',methods=['POST'])
def delete():
    return depstockmtfinputService.delete(**request.json)

@route(bp, '/update',methods=['POST'])
def update():
    return depstockmtfinputService.update(**request.json)




