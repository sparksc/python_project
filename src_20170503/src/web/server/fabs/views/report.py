# -*- coding: utf-8 -*-

from flask import Blueprint, request, json, abort, current_app, jsonify
from werkzeug import secure_filename
from ..services import ReportService, readxls
from ..base import helpers
from . import route
import os

reportService = ReportService()
bp = Blueprint('reportItemss', __name__, url_prefix='/reports')
@route(bp, '/items', methods=['GET'])   
def query_reports():
    return reportService.query_reports()

@route(bp, '/<record_id>', methods=['GET'])
def query_reportItems(record_id):
    print record_id
    return reportService.query_reportItems(record_id)
    
@route(bp, '/types', methods=['GET'])   
def query_reporttypes():
    return reportService.query_reporttypes()
    
@route(bp, '/save', methods=['POST'])
def save_report_record():
    reportService.save_report_record(**request.json)
    return True

@route(bp,'/delete',methods=['GET'])
def delete_report_record():
    return reportService.delete_report_record(**request.args)

@route(bp,'/query',methods=['GET'])
def query_report_record():
    return reportService.query_report_record(**request.args)

@route(bp,'/updatereadonly/',methods=['POST'])
def updatereadonly():
    return  reportService.updatereadonly(**request.json)
@route(bp,'/querydata/',methods=['GET'])
def query_report_data():
    return reportService.query_report_data(**request.args)
    
'''
    数据导入上传
'''
@route(bp,'/upload/',methods=["POST"])
def upload():
    files = request.files.getlist('file')
    file = files[0]
    upload_path = current_app.config.get('UPLOAD_PATH')
    local_path = os.path.join(upload_path,secure_filename(file.filename))
    file.save(local_path) 
    record_id = request.form.get('record_id')
    report_id = request.form.get('report_id')
    readxls.import_data(local_path, record_id, report_id)
    
# @route(bp,'/compute/',methods=["POST"])
# def compute():
    # return reportService.compute(**request.json)



