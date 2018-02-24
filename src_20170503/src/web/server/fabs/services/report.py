# -*- coding:utf-8 -*-

from flask import json,g
from ..model.report import *
from ..model.party import *
from ..database import simple_session
from .service import BaseService
import decimal
import string
logging.basicConfig(level=logging.DEBUG)

class ReportService(BaseService):

    def query_reportItems(self,id):
        re_datas = g.db_session.query(ReportItems,ReportData,ReportRecord,Company)  \
            .outerjoin(ReportData,ReportData.item_id==ReportItems.item_id)  \
            .outerjoin(ReportRecord,ReportRecord.id==ReportData.record_id)  \
            .outerjoin(Company,Company.id==ReportRecord.company_id)  \
            .filter(ReportData.report_id==ReportItems.report_id)  \
            .filter(ReportData.record_id==id).order_by(ReportItems.item_id).all()
        data_list = []
        for item in re_datas:
            r_item = item[0] if item[0] else ReportItems()
            r_data = item[1] if item[1] else ReportData()
            r_record = item[2] if item[2] else ReportRecord()
            r_company = item[3] if item[3] else Company()
            if r_data.value1 !=None:
                value1 = "{:,}".format(round(float(decimal.Decimal(r_data.value1)/100),2))
            if r_data.value1 ==None:
                value1 = r_data.value1
            if r_data.value2 !=None:
                value2 = "{:,}".format(round(float(decimal.Decimal(r_data.value2)/100),2))
            if r_data.value2 ==None:
                value2 = r_data.value2
            data_list.append([r_data.record_id, r_item.report_id, r_item.item_name, r_item.item_id, value1, \
                value2 ,r_record.report_period, r_record.year_month ,r_company.company_cn_name ,r_company.org_id,r_item.item_formula ,r_item.item_formula1,r_record.report_date,r_record.opertor_id])
        return data_list

    def query_reporttypes(self):
        reporttypes = g.db_session.query(ReportType).all()
        return reporttypes

    def query_reports(self):
         reportitemss = g.db_session.query(Report).all()
         return reportitemss

    def query_report_record(self,**kwargs):
        u''' 财务报表- 查询 '''
        id = kwargs.get('company_id')[0]
        report_record = g.db_session.query(ReportRecord).filter(ReportRecord.company_id == id).all()
        return report_record

    def save_report_record(self,**kwargs):
        u''' 财务报表- 增加 '''
       # try:
        report_record= ReportRecord(**kwargs)
        g.db_session.add(report_record)
        g.db_session.commit()
       # raise Exception("此条记录已存在")
        report_items = g.db_session.query(ReportItems).order_by(ReportItems.item_id).all()
        for item in report_items:
            report_data1 =  ReportData(record_id=report_record.id, report_id=item.report_id, item_id=item.item_id ,value1=0.0 , value2= 0.0)
            g.db_session.add(report_data1)          

    def delete_report_record(self,**kwargs):
        u''' 财务报表- 删除 '''
        id = kwargs.get('id')[0]
        g.db_session.query(ReportData).filter(ReportData.record_id == id).delete()
        g.db_session.query(ReportRecord).filter(ReportRecord.id == id).delete()
        g.db_session.commit()

    def updatereadonly(self,**kwargs):
        u''' 数据- 修改 '''
        data_list =kwargs.get("report_lists");
        for data in data_list:
            if data[4] != None :
                #data1 = data[4].replace(',','')
                #d_value1=int(decimal.Decimal(data[4].replace(',',''))*100)
                data1 =str(data[4]).replace(',','')
                d_value1=float(decimal.Decimal(data1.replace(',',''))*100)
            if data[4] == None :
                 d_value1=data[4]
            if data[5] != None :
                # data2 = data[5].replace(',','')
                # d_value2=int(decimal.Decimal(data[5].replace(',',''))*100)
                # d_value2=data[5].replace(',','')*100
                data2 =str(data[5]).replace(',','')
                d_value2=float(decimal.Decimal(data2.replace(',',''))*100)
                #data2 =str(data[5]).replace(',','')*100
                #d_value2=data2
            if data[5] == None :
                 d_value2=data[5]
            values = {"value1":d_value1,"value2":d_value2}
            #values = {"value1":data[4],"value2":data[5]}
            g.db_session.query(ReportData).filter(ReportData.record_id==data[0]).filter(ReportData.report_id==data[1]).filter(ReportData.item_id==data[3]).update(values)
            # g.db_session.query(ReportData).filter(ReportData.record_id==data[0]).filter(ReportData.report_id==data[1]).delete()
            # report_data= ReportData(data_list)
            # g.db_session.query(ReportData).add(data_list)
        g.db_session.commit()

    def query_report_data(self,**kwargs):
        u''' 财务报表-查询数据 '''
        report_data= g.db_session.query(ReportData).all()
        return report_data
