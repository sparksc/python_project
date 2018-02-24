# -*- coding: utf-8 -*-

from flask import Blueprint, request, json, abort, current_app, jsonify, session as web_session, g

from ..services import Man_gradejdgService
from . import route


bp = Blueprint('man_gradejdg', __name__, url_prefix='/man_gradejdg')

man_gradejdgService = Man_gradejdgService()


@route(bp, '/add_save', methods=['POST'])
def add_save():
    return man_gradejdgService.add_save(**request.json)
@route(bp, '/edit_save', methods=['POST'])
def edit_save():
    return man_gradejdgService.edit_save(**request.json)
@route(bp, '/update', methods=['POST'])
def update():
    return man_gradejdgService.update(**request.json)
@route(bp, '/delete', methods=['POST'])
def delete():
    return man_gradejdgService.delete(**request.json)
@route(bp, '/delete_man', methods=['POST'])
def delete_man():
    return man_gradejdgService.delete_man(**request.json)
@route(bp, '/get_grade_param', methods=['POST'])
def get_grade_param():
    return man_gradejdgService.get_grade_param(**request.json)
@route(bp, '/grade_param', methods=['POST'])
def grade_param():
    return man_gradejdgService.grade_param(**request.json)
@route(bp, '/get_weight', methods=['POST'])
def get_weight():
    return man_gradejdgService.get_weight(**request.json)
@route(bp, '/get_score', methods=['POST'])
def get_score():
    return man_gradejdgService.get_score(**request.json)
@route(bp, '/add_grade', methods=['POST'])
def add_grade():
    return man_gradejdgService.add_grade(**request.json)
@route(bp, '/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files')
    file1 = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = upload_path +'/'+file1.filename #os.path.join(upload_path,secure_filename(file.filename))
    file1.save(local_path)
    #gty_id = request.form.get('gty_id')
    return man_gradejdgService.upload(local_path, file1.filename)

