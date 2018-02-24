# -*- coding: utf-8 -*-
"""
    yinsho.api.basicsalary
    #####################

    yinsho basic salary view module
"""

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import BasicSalaryService
from . import route


bp = Blueprint('basicsalary', __name__, url_prefix='/basicsalary')

basicSalaryService = BasicSalaryService()


@route(bp, '/posname_load',methods=['POST'])
def posname_load():
    return basicSalaryService.posname_load()

@route(bp, '/posname_edit_save',methods=['POST'])
def posname_edit_save():
    return basicSalaryService.posname_edit_save(**request.json)

@route(bp, '/poslev_load',methods=['POST'])
def poslev_load():
    return basicSalaryService.poslev_load()

@route(bp, '/poslev_edit_save',methods=['POST'])
def poslev_edit_save():
    return basicSalaryService.poslev_edit_save(**request.json)

@route(bp, '/salary_load',methods=['POST'])
def salary_load():
    return basicSalaryService.salary_load()

@route(bp, '/salary_edit_save',methods=['POST'])
def salary_edit_save():
    return basicSalaryService.salary_edit_save(**request.json)

@route(bp, '/edu_load',methods=['POST'])
def edu_load():
    return basicSalaryService.edu_load()

@route(bp, '/edu_edit_save',methods=['POST'])
def edu_edit_save():
    return basicSalaryService.edu_edit_save(**request.json)
