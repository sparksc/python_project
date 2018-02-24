# -*- coding: utf-8 -*-
"""
    yinsho.api.users
    #####################

    yinsho users view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g
import traceback

from ..services import UsersService
from ..base import helpers
from . import route
import datetime





bp = Blueprint('users', __name__, url_prefix='/users')

usersService = UsersService()

@bp.route('/login', methods=['POST'])
def whoami():
    """Returns the user instance of the currently authenticated user."""
    try:
        #if not data:raise Exception(u'请出入正确的用户名和密码')
        username = request.json.get('username')
        password = request.json.get('password')
        user_session = usersService.login(username,password)

        result = { "token": user_session.user_session_id.decode('ascii') }
        data = {'data':\
                    {\
                        'user_name':user_session.user.user_name \
                        , 'name':user_session.user.name \
                        , 'role_id':user_session.user.role_id \
                        , 'current_date':datetime.datetime.now().strftime('%Y-%m-%d') \
                        , 'branch_list': user_session.branch_list \
                        , 'message_count': user_session.message_count \
                    }\
                }
        user = user_session.user
        if user.user_branches:
            data.get('data').update({'branch_code':user.user_branches[0].branch.branch_code,'branch_name':user.user_branches[0].branch.branch_name })
        else:
            data.get('data').update({'branch_code':"-1",'branch_name':u"暂无机构" })
        data.get('data').update({'user_group'+ str(idx) :x.group.group_name for idx,x in enumerate(user_session.user.user_groups)})
        result.update(data)

        # TODO: Encode the session user_session_id to the token
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({ "error": e[0]})

@bp.route('/change_password', methods=['POST'])
def change_password():
    user = g.web_session.user
    usersService.update_user_pwd(user.role_id, request.json.get('password'))
    return u"密码修改成功"


@bp.route('/auth', methods=['POST'])
def auth():
    """Returns the user instance of the currently authenticated user."""
    try:
        user_session = usersService.auth(request.json.get('token'))
        return jsonify({ "data": {'token':user_session}})
    except Exception as e:
        traceback.print_exc()
        return jsonify({ "error": e[0]}),401


@bp.route('/group/<user_name>', methods=['GET'])
def query_group(user_name):
    return usersService.query_group(user_name)

@route(bp, '/update_ws', methods=['POST'])
def update_ws():
    return usersService.update_ws(*request.json)

@route(bp, '/get_group_type', methods=['POST'])
def get_group_type():
    return usersService.get_group_type()

@route(bp, '/get_group_department', methods=['POST'])
def get_group_department():
    return usersService.get_group_department()
