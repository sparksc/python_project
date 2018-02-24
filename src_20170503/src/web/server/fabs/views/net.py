# -*- coding: utf-8 -*-
"""
    yinsho.api.nets
    #####################

    yinsho nets view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import NetService
from . import route


bp = Blueprint('net', __name__, url_prefix='/net')

netService = NetService()


@route(bp, '/net_del',methods=['POST'])
def net_del():
    return netService.net_del(**request.json)


@route(bp, '/nets',methods=['POST'])
def nets():
    return netService.nets()
	
@route(bp, '/net_add_save',methods=['POST'])
def net_add_save():
    return netService.net_add_save(**request.json)	

@route(bp, '/net_edit_save',methods=['POST'])
def net_edit_save():
    return netService.net_edit_save(**request.json)




'''
@route(bp, '/', methods=['POST'])
def create():
    """Returns a list of usersService instances."""
    params = helpers.req_parse(request.json.items(),{
        'password': lambda password,_:helpers.encrypt(password)
    })
    return usersService.create_user_roles(**params)

@route(bp, '/<user_id>')
def show(user_id):
    """Returns a user instance."""
    return usersService.get_or_404(user_id)

#@route(bp, '/<user_id>', methods=['PUT','PATCH'])
@route(bp, '/<user_id>', methods=['PUT','PATCH'])
def update(user_id):
    """Updates a users. Returns the updated users instance."""
    return usersService.update_user_roles(usersService.get_or_404(user_id), **request.json)


@route(bp, '/<user_id>', methods=['DELETE'])
def delete(user_id):
    """Deletes a users. Returns a 204 response."""
    usersService.delete(usersService.get_or_404(user_id))
    return None, 204

'''

