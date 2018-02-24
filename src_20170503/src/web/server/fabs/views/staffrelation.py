# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import UserRelationService
from . import route


bp = Blueprint('staffrelation', __name__, url_prefix='/staffrelation')

userRelationService = UserRelationService()


@route(bp, '/update',methods=['POST'])
def update():
    return userRelationService.update(**request.json)

@route(bp, '/tsave',methods=['POST'])
def tsave():
    return userRelationService.tsave(**request.json)

@route(bp, '/tdelt',methods=['POST'])
def tdelt():
    return userRelationService.tdelt(**request.json)

@route(bp, '/save',methods=['POST'])
def save():
    return userRelationService.save(**request.json)

@route(bp, '/delete',methods=['POST'])
def delete():
    return userRelationService.delete(**request.json)

@route(bp, '/simple_select',methods=['POST'])
def simple_select():
    return userRelationService.simple_select(**request.json)

@route(bp, '/newupdate',methods=['POST'])
def newupdate():
    return userRelationService.newupdate(**request.json)

@route(bp, '/update_his',methods=['POST'])
def update_his():
    return userRelationService.update_his(**request.json)
@route(bp, '/edit_his',methods=['POST'])
def edit_his():
    return userRelationService.edit_his(**request.json)
@route(bp, '/delete_his',methods=['POST'])
def delete_his():
    return userRelationService.delete_his(**request.json)

