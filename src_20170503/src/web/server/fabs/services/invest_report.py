# -*- coding: utf-8 -*-
"""
    yinsho.services.InvestReportService
    #####################

    yinsho CreditServic module
"""
from ..model.party import *
from ..model.application import *
from .service import BaseService
import hashlib, copy
from flask import json, g
from sqlalchemy import and_
from ..model.report import *
from ..model.transaction import *
from ..model.application import *
from ..model.credit import *
from ..workflow import task
from ..workflow.parameter import *
from ..database.sqlal import simple_session
from ..base import core_inf
from ..base.xlsutil import write_cell
import decimal
from decimal import Decimal
import datetime
import random,os
import xlwt
import xlrd
from xlutils.copy import copy

class InvestReportService(BaseService):

    def save(self,**kwargs):
        u''' 保存调查报告内容 '''
        application_id=kwargs.get('application_id')
	rst = g.db_session.query(ApplicationTransaction).filter(ApplicationTransaction.application_id ==application_id).first()
        trans = rst
        app=trans.application
        cust=app.customer
        homedir = os.getcwd()
        xls_path=homedir+'/fabs/static/investigate_report/'
        rb = xlrd.open_workbook(xls_path+'test.xls',formatting_info=True)
        wb = copy(rb)
        wb.encoding = 'utf-8'
        sh = wb.get_sheet(0)
        write_cell(sh, 0, 0, unicode("%s贷前调查报告 "%(cust.party.name)))
        write_cell(sh, 0, 2, unicode('调查时间：    2016年1月8日'))
        write_cell(sh, 0, 7, unicode('%s,因周转资金短缺，申请贴现100000.00元，业务种类为贴现，借款人在我行开立个人结算账户，在我行发生结算业务，与我行业务往来良好。')%(cust.party.name))
        report_filename = xls_path+'%s.xls'%(application_id)
        wb.save(report_filename) 
        file_path = 'static/investigate_report/%s.pdf '%(application_id) 
        os.system('unoconv -f pdf -o ../web/fabs/%s %s '%(file_path,report_filename))
        end_date=datetime.datetime.now()+datetime.timedelta(days = 365) 
        survey_report=SurveyReport(from_date=datetime.datetime.now(),end_date=end_date,product_code=app.product_code,party_id=app.customer.party_id,report_path=file_path)
        g.db_session.add(survey_report)
        g.db_session.commit()
        g.db_session.query(Application).filter(Application.id==app.id).update({'survey_report_id':survey_report.id})
        g.db_session.commit()
        #if os.path.exists('%s/../web/fabs/%s'%(homedir,file_path)):
        return {'success':True,'src':file_path}
        #else:
         #    return {'success':False,'msg':u'保存文件出错'}

    def submit(self,**kwargs):
        u'''提交调查报告 '''
        application_id=kwargs.get('application_id')
        rst = g.db_session.query(ApplicationTransaction, Application) \
            .join(Application, Application.id == ApplicationTransaction.application_id)\
            .filter(Application.id == application_id).first()
        at = rst.ApplicationTransaction
        a = rst.Application
        if a is None:
            raise Exception('交易不存在!')
        user = g.web_session.user
        groups = []
        for group in user.user_groups:
            groups.append(group.group.group_name)

        task_list = task.get_task(at)
        for t in task_list:
            role = get_parameter(t.activity,u"角色")
            if role and role in groups:
                t.user = user
                t.active()
                t.finish()
                g.db_session.query(Application).filter(Application.id == a.id).update({Application.status:t.activity.activity_name})
        g.db_session.commit()         

        return {'msg':'提交成功'}

    def update(self,**kwargs):
        u'''更新调查报告 '''
        return {'success':True}

    def query(self,transaction_id):
        u''' 查询数据   '''
        return {'success':True}
 
    def get(self, application_id):
        u''' 获取调查报告地址 '''
        app=g.db_session.query(Application).filter(Application.id == application_id).first()
        if app.survey_report:
            file_path=app.survey_report.report_path
            return {'success':True,'src':file_path}
        return {'success':True,'src':''}
         
