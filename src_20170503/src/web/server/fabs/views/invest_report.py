# -*- coding: utf-8 -*- 
"""
    yinsho.api.report
    #####################
                        
    yinsho  report module
    
"""                       
                         
from flask import Blueprint, request, json, abort, current_app, jsonify,session as web_session, g
                           
from ..services import InvestReportService
from ..base import helpers   
from . import route
                                   
investReportService = InvestReportService()

bp = Blueprint('report', __name__, url_prefix='/report')
                          
@route(bp, '/save', methods=['POST'])
def save():                      
    return investReportService.save(**request.json)

@route(bp, '/submit/', methods=['POST'])
def submit():
    return investReportService.submit(**request.json)

@route(bp, '/update/<application_id>', methods=['PUT'])
def update(application_id):
    why = {'application_id':application_id,'kwargs':request.json}
    return investReportService.update(why)

@route(bp, '/query/<transaction_id>', methods=['GET'])
def query(transaction_id):
    return investReportService.query(transaction_id)

@route(bp, '/<application_id>', methods=['GET'])
def get(application_id):
    return investReportService.get(application_id)

