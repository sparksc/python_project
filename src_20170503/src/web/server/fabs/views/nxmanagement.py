# -*- coding: utf-8 -*-
"""
    yinsho.api.nxmanagement
    #####################

    nxmanagement api
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g
from ..services import NXBranchService
from ..base import helpers
from . import route
import datetime

bp = Blueprint('nxmanagement', __name__, url_prefix='/nxmanagement')
branchbp = Blueprint('nxbranch', __name__, url_prefix='/nxbranch')


branchService = NXBranchService()

@branchbp.route('/')
def all():
    return jsonify(branches=branchService.all())

@branchbp.route('/<int:id>',methods=['GET'])
def get(id):
    return jsonify(branch=branchService.get(id))

@branchbp.route('/',methods=['POST'])
def add():
    result = branchService.add(**request.json)
    return jsonify(branch=result)

@branchbp.route('/<int:id>',methods=['POST'])
def update_exists(id):
    result = branchService.update_exists(id,**request.json)
    return jsonify(branch=result)

@branchbp.route('/<int:id>',methods=['PUT'])
def update(id):
    result = branchService.update(id,**request.json)
    return jsonify(branch=result[0]),result[1]

@branchbp.route('/<int:id>',methods=['DELETE'])
def delete(id):
    return jsonify(branchService.delete(id))