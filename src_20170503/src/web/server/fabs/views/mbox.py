# -*- coding: utf-8 -*-
from flask import Blueprint, request, json, abort, current_app, jsonify
from ..services import MboxService
from . import route

MboxService = MboxService()
bp = Blueprint('mbox', __name__, url_prefix='/mbox')

'''发送邮件'''
@route(bp, '/send_mbox', methods=['POST'])
def mbox_save():
    MboxService.mbox_send(**request.json)
    return True

'''查询机构'''
@route(bp,'/branch',methods=['GET'])
def branch():
    return MboxService.mbox_branch()

'''查询用户'''
@route(bp,'/user',methods=['GET'])
def user():
    return MboxService.mbox_user(**request.args)

'''查询邮件'''
@route(bp,'/query',methods=['GET'])
def mbox_query():
    return MboxService.mbox_query()

'''邮件已读'''
@route(bp, '/update', methods=['GET'])
def mbox_update():
    return MboxService.mbox_update(**request.args)

'''删除邮件'''
@route(bp, '/del', methods=['GET'])
def find_user_mbox():
    return MboxService.mbox_del(**request.args)
