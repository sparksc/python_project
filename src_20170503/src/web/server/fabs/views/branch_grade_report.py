# -*- coding: utf-8 -*-

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services.branch_grade_report import Branch_grade_reportService
from . import route


bp = Blueprint('branch_grade_report', __name__, url_prefix='/branch_grade_report')

branch_grade_reportService = Branch_grade_reportService()

@route(bp, '/update', methods=['POST'])
def update():
    return branch_grade_reportService.update(**request.json)
@route(bp, '/get_grade_param', methods=['POST'])
def get_grade_param():
    return branch_grade_reportService.get_grade_param(**request.json)
@route(bp, '/grade_param', methods=['POST'])
def grade_param():
    return branch_grade_reportService.grade_param(**request.json)
@route(bp, '/get_weight', methods=['POST'])
def get_weight():
    return branch_grade_reportService.get_weight(**request.json)
@route(bp, '/get_score', methods=['POST'])
def get_score():
    return branch_grade_reportService.get_score(**request.json)
@route(bp, '/add_grade', methods=['POST'])
def add_grade():
    return branch_grade_reportService.add_grade(**request.json)
