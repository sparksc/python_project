# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import PostmanageService
from . import route


bp = Blueprint('postmanagepermission', __name__, url_prefix='/postmanagepermission')

postmanageService = PostmanageService()


@route(bp, '/posts',methods=['POST'])
def posts():
    return postmanageService.posts(**request.json)

@route(bp, '/get_post_list',methods=['POST'])
def get_post_list():
    return postmanageService.get_post_list(**request.json)

@route(bp, '/post',methods=['POST'])
def post():
    return postmanageService.post(**request.json)

@route(bp, '/post_save',methods=['POST'])
def post_save():
    return postmanageService.post_save(**request.json)

@route(bp, '/post_delete',methods=['POST'])
def post_delete():
    return postmanageService.post_delete(**request.json)

@route(bp, '/post_edit_save',methods=['POST'])
def post_edit_save():
    return postmanageService.post_edit_save(**request.json)

@route(bp, '/check_posts',methods=['POST'])
def check_posts():
    print(111111111111111111111111111)
    return postmanageService.check_posts(**request.json)

@route(bp, '/ords',methods=['POST'])
def ords():
    return postmanageService.ords(**request.json)

@route(bp, '/users',methods=['POST'])
def users():
    return postmanageService.users(**request.json)

@route(bp, '/find_users_by_postes',methods=['POST'])
def find_users_by_postes():
    return postmanageService.find_users_by_postes(**request.json)

@route(bp, '/add_save',methods=['POST'])
def add_save():
    return postmanageService.add_save(**request.json)
