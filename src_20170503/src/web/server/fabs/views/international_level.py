#-*-coding:utf-8-*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""
from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services.international_level import Org_levelService
from . import route


bp = Blueprint('international_level', __name__, url_prefix='/international_level')

international_levelService = Org_levelService()

@route(bp,'/conunt_del',methods=['POST'])
def conunt_del():
    return international_levelService.conunt_del(**request.json)

@route(bp,'/calculate',methods=['POST'])
def calculate():
    return international_levelService.calculate(**request.json)

@route(bp,'/change_save',methods=['POST'])
def change_save():
    return international_levelService.change_save(**request.json)

@route(bp,'/affirm',methods=['POST'])
def affirm():
    return international_levelService.affirm(**request.json)
