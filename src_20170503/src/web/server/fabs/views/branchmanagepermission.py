# -*- coding: utf-8 -*-
"""
    yinsho.api.seims
    #####################

    yinsho seims view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import BranchmanageService
from . import route


bp = Blueprint('branchmanagepermission', __name__, url_prefix='/branchmanagepermission')

branchmanageService = BranchmanageService()


@route(bp, '/branchs',methods=['POST'])
def branchs():
    return branchmanageService.branchs(**request.json)

@route(bp, '/get_branch_list',methods=['POST'])
def get_branch_list():
    return branchmanageService.get_branch_list(**request.json)

@route(bp, '/branch',methods=['POST'])
def branch():
    return branchmanageService.branch(**request.json)

@route(bp, '/branch_save',methods=['POST'])
def branch_save():
    return branchmanageService.branch_save(**request.json)

@route(bp, '/branch_delete',methods=['POST'])
def branch_delete():
    return branchmanageService.branch_delete(**request.json)

@route(bp, '/branch_edit_save',methods=['POST'])
def branch_edit_save():
    return branchmanageService.branch_edit_save(**request.json)

@route(bp, '/check_branchs',methods=['POST'])
def check_branchs():
    return branchmanageService.check_branchs(**request.json)

@route(bp, '/ords',methods=['POST'])
def ords():
    return branchmanageService.ords(**request.json)

@route(bp, '/users',methods=['POST'])
def users():
    return branchmanageService.users(**request.json)

@route(bp, '/get_staff',methods=['POST'])
def get_staff():
    return branchmanageService.get_staff(**request.json)

@route(bp, '/find_users_by_branches',methods=['POST'])
def find_users_by_branches():
    return branchmanageService.find_users_by_branches(**request.json)

@route(bp, '/find_users_by_branch',methods=['POST'])
def find_users_by_branch():
    return branchmanageService.find_users_by_branch(**request.json)
    
@route(bp, '/add_save',methods=['POST'])
def add_save():
    return branchmanageService.add_save(**request.json)

@route(bp, '/get_user_permission',methods=['POST'])
def get_user_permission():
    return branchmanageService.get_user_permission(**request.json)

@route(bp, '/branchgroup',methods=['POST'])
def branchgroup():
    return branchmanageService.branchgroup(**request.json)

@route(bp, '/hide', methods=['POST'])
def hide():
    return branchmanageService.hide(**request.json)

@route(bp, '/do_allot', methods=['POST'])
def do_allot():
    return branchmanageService.do_allot(**request.json)

@route(bp, '/show', methods=['POST'])
def show():
    return branchmanageService.show(**request.json)

@route(bp, '/show_org', methods=['POST'])
def show_org():
    return branchmanageService.show_org(**request.json)

@route(bp, '/permission', methods=['POST'])
def permission():
    return branchmanageService.permission(**request.json)

