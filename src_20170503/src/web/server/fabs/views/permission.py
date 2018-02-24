# -*- coding: utf-8 -*-
"""
    yinsho.api.users
    #####################

    yinsho users view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import PermissionService
from . import route


bp = Blueprint('permission', __name__, url_prefix='/permission')

permissionService = PermissionService()

@route(bp, '/init_user_pwd',methods=['POST'])
def init_user_pwd():
    return permissionService.init_user_pwd(**request.json)

@route(bp, '/menus')
def menu_dump():
    return permissionService.menu_dump()

@route(bp, '/get_permission_list',methods=['POST'])
def get_permission_list():
    return permissionService.get_permission_list(**request.json)

@route(bp, '/save_permission_list',methods=['POST'])
def save_permission_list():
    return permissionService.save_permission_list(**request.json)

@route(bp, '/user_menus')
def user_menu_dump():
    user_name = g.web_session.user.user_name
    return permissionService.user_menu_dump(user_name)

@route(bp, '/user_permission_menus')
def user_permission_menus_dump():
    user_name = g.web_session.user.user_name
    return permissionService.user_permission_menu_dump(user_name)

@route(bp, '/group_menus_select',methods=['POST'])
def group_menus_select():
    return permissionService.group_menu_select(**request.json)

@route(bp, '/user_permission_group_select',methods=['POST'])
def user_permission_group_select():
    return permissionService.user_permission_group_select(**request.json)

@route(bp, '/user_permission_group_save',methods=['POST'])
def user_permission_group_save():
    return permissionService.user_permission_group_save(**request.json)

@route(bp, '/group_menus_save',methods=['POST'])
def group_menus_add():
    return permissionService.group_menus_save(**request.json)

@route(bp, '/users',methods=['POST'])
def users():
    return permissionService.users(**request.json)

@route(bp, '/groups',methods=['POST'])
def groups():
    return permissionService.groups(**request.json)


@route(bp, '/groups_permission',methods=['POST'])
def groups_permission():
    return permissionService.groups_permission(**request.json)

@route(bp, '/user_groups',methods=['POST'])
def user_groups():
    return permissionService.user_groups(request.json.get('user_id'))

@route(bp, '/user_groups_save',methods=['POST'])
def user_groups_save():
    return permissionService.user_groups_save(**request.json)

@route(bp, '/user_branches')
def user_branches():
    user_id = g.web_session.user.role_id
    return permissionService.user_branches(user_id)

@route(bp, '/para_menu_save',methods=['POST'])
def para_menu_save():
    return permissionService.para_menu_save(**request.json)
@route(bp, '/menu_update',methods=['POST'])
def menu_update():
    return permissionService.menu_update(**request.json)
@route(bp, '/menu_save',methods=['POST'])
def menu_save():
    return permissionService.menu_save(**request.json)
@route(bp, '/user_update',methods=['POST'])
def user_update():
    return permissionService.user_update(**request.json)
@route(bp, '/user_save',methods=['POST'])
def user_save():
    return permissionService.user_save(**request.json)


@route(bp, '/groupdata_save',methods=['POST'])
def groupdata_save():
    return permissionService.groupdata_save(**request.json)

@route(bp, '/groupdata_edit',methods=['POST'])
def groupdata_edit():
    return permissionService.groupdata_edit(**request.json)

@route(bp, '/groupdata_delete',methods=['POST'])
def groupdata_delete():
    return permissionService.groupdata_delete(**request.json)

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

