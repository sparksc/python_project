# -*- coding: utf-8 -*-
"""
    yinsho.services.StandingBookService
    #####################
    yinsho LoanService module
"""
import hashlib, copy
from flask import json, g
from sqlalchemy import and_
from ..model.credit import *
from ..model.transaction import *
from ..model.contract import *
from ..model.application import *
from ..model.creditLevel import *
from ..workflow import task
from ..workflow.parameter import *
from ..database.sqlal import simple_session
from ..base.xlsutil import write_cell
import decimal
from decimal import Decimal
import xlwt
import xlrd
from xlutils.copy import copy
import datetime
import random

class StandingBookService():

    def save(self,**kwargs):
        u''' 诉讼台账提起诉讼 '''
        debt=kwargs.get('debt')
        litigation_book=kwargs.get('litigation_book')
        litigation_book.update({'debt_id':debt.get('id'),'from_date':datetime.datetime.strptime(litigation_book.get('from_date'),'%Y-%m-%d')}) 
        book=LitigationBook(**litigation_book)
        g.db_session.add(book)
        g.db_session.commit()
        log=LitigationBookLog(litigation_book_id=book.id,date=litigation_book.get('from_date'),name=litigation_book.get('status'))
        g.db_session.add(log)
        return {'litigation_book':book}

    def save_repossession(self,**kwargs):
        u''' 以物抵债台账保存 '''
        repossession=kwargs.get('repossession')
        repossession=kwargs.get('repossession')
        id = repossession.get('id')
        repossession.pop('id')
        repossession.pop('application_transaction')
        repossession.pop('lend_transaction')
        repossession.pop('repossession_book')
        g.db_session.query(Repossession).filter(Repossession.id==id).update(repossession)
        book = RepossessionBook(repossession_id=id)
        g.db_session.add(book)
        return {'book':book}

    def update_repossession(self,**kwargs):
        u''' 更新以物抵债台账内容 '''
        repossession=kwargs.get('repossession')
        repossession=kwargs.get('repossession')
        id = repossession.get('id')
        repossession.pop('id')
        repossession.pop('application_transaction')
        repossession.pop('lend_transaction')
        repossession.pop('repossession_book')
        g.db_session.query(Repossession).filter(Repossession.id==id).update(repossession)
        return {'success':True}
   

    def update(self,**kwargs):
        u''' 诉讼台账更新 '''
        litigation_book=kwargs.get('litigation_book')
        litigation_book_log=kwargs.get('litigation_book_log')
        litigation_book_log.update({'litigation_book_id':litigation_book.get('id'),'date':datetime.datetime.strptime(litigation_book_log.get('date'),'%Y-%m-%d')})
        log=LitigationBookLog(**litigation_book_log)
        g.db_session.add(log)
        g.db_session.query(LitigationBook).filter(LitigationBook.id==litigation_book.get('id')).update({'status':litigation_book_log.get('name')})
        return {'success':True}

    def query(self,litigation_book_id):
        u''' 查询五级分类列表 '''
        book=g.db_session.query(LitigationBook).filter(LitigationBook.id==litigation_book_id).first()
        return {'litigation_book':book}

    def query_debt(self):
        u''' 查询借据列表 '''
        q = g.db_session.query(Debt,TransactionContractRelation).join(TransactionContractRelation,TransactionContractRelation.contract_id==Debt.contract_id).all()
        rst_list=[{'debt':r.Debt,'contract':r.Debt.contract,'lend_transaction_info':r.TransactionContractRelation.lend_transaction,'aplication_info':r.TransactionContractRelation.lend_transaction.application_transaction.application,'party':r.TransactionContractRelation.lend_transaction.application_transaction.application.customer.party,'product':r.TransactionContractRelation.lend_transaction.application_transaction.application.product} for r in q]
        return rst_list

    def query_list(self):
        u''' 查询诉讼台账列表 '''
        q = g.db_session.query(LitigationBook,Debt,TransactionContractRelation).join(Debt,Debt.id==LitigationBook.debt_id).join(TransactionContractRelation,TransactionContractRelation.contract_id==Debt.contract_id).order_by(LitigationBook.id).all()
        rst_list=[{'litigation_book':r.LitigationBook,'debt':r.Debt,'contract':r.Debt.contract,'lend_transaction_info':r.TransactionContractRelation.lend_transaction,'application_info':r.TransactionContractRelation.lend_transaction.application_transaction.application,'party':r.TransactionContractRelation.lend_transaction.application_transaction.application.customer.party,'product':r.TransactionContractRelation.lend_transaction.application_transaction.application.product} for r in q]
        return rst_list

    def query_repossession(self):
        u''' 查询以物抵债台账列表 '''
        q = g.db_session.query(RepossessionBook).order_by(RepossessionBook.id).all()
        rst_list=[{'book':r,'repossession':r.repossession,'lend_transaction':r.repossession.lend_transaction,'application':r.repossession.application_transaction.application,'party':r.repossession.application_transaction.application.customer.party,'product':r.repossession.lend_transaction.application_transaction.application.product} for r in q]
        return rst_list

    def export_book(self,**kwargs):
        u''' 导出诉讼台账列表 '''
        book=xlwt.Workbook(encoding='utf-8')
        sheet=book.add_sheet('sheet1',cell_overwrite_ok=True)
        algn1 = xlwt.Alignment()
        algn1.wrap = 1
        style = xlwt.XFStyle()
        style.alignment = algn1
        data=kwargs.get('data')
        i = 0
        sheet.write(0,0,'序号')
        sheet.write(0,1,'放贷支行')
        sheet.write(0,2,'借款人名称')
        sheet.write(0,3,'贷款金额')
        sheet.write(0,4,'贷款余额')
        sheet.write(0,5,'欠息合计')
        sheet.write(0,6,'起诉时本息合计')
        sheet.write(0,7,'是否已停息')
        sheet.write(0,8,'抵押物情况')
        sheet.write(0,9,'抵押物价值')
        sheet.write(0,10,'提起诉讼时间')
        sheet.write(0,11,'工作进度')
        sheet.write(0,12,'判决日期')
        sheet.write(0,13,'备注')
        for index in data:
            i = i+1
            sheet.write(i,0,index.get('litigation_book').get('id'))
            sheet.write(i,1,index.get('application_info').get('handle_branch'))
            sheet.write(i,2,index.get('party').get('name'))
            sheet.write(i,3,index.get('debt').get('amount'))
            sheet.write(i,4,'')
            sheet.write(i,5,'')
            sheet.write(i,6,'')
            sheet.write(i,7,'是')
            sheet.write(i,8,'')
            sheet.write(i,9,'')
            sheet.write(i,10,index.get('litigation_book').get('from_date'))
            log = g.db_session.query(LitigationBookLog).filter(LitigationBookLog.litigation_book_id==index.get('litigation_book').get('id')).order_by(LitigationBookLog.date).all()
            status=''
            for l in log:
                status += l.date.strftime('%Y%m%d')+' '+l.name+'\n'
            sheet.write(i,11,status,style)
            sheet.write(i,12,index.get('litigation_book').get('end_date'),style)
            sheet.write(i,13,'')
            
        report_filename = '../web/fabs/static/standing_book/standing_book_export.xls'
        book.save(report_filename) 
        return {'file':'static/standing_book/standing_book_export.xls'}



    def export_repossession_book(self,**kwargs):
        u''' 导出诉讼台账列表 '''
        data=kwargs.get('data')
        book=xlwt.Workbook(encoding='utf-8')
        sheet=book.add_sheet('sheet1',cell_overwrite_ok=True)
        algn1 = xlwt.Alignment()
        algn1.wrap = 1
        algn1.horz=xlwt.Alignment().HORZ_CENTER
        style = xlwt.XFStyle()
        style.alignment = algn1
        font1=xlwt.Font() 
        font1.height=0x140 
        style.font=font1
        sheet.write_merge(0,0,0,23,'以物抵债明细表',style)
        i = 1
        sheet.write(1,0,'序号')
        sheet.write(1,1,'抵入行名称')
        sheet.write(1,2,'借款人名称')
        sheet.write(1,3,'本金')
        sheet.write(1,4,'表内利息')
        sheet.write(1,5,'表外利息')
        sheet.write(1,6,'本息合计')
        sheet.write(1,7,'入账金额')
        sheet.write(1,8,'其中:利息')
        sheet.write(1,9,'其中税费')
        sheet.write(1,10,'截至当前本金余额')
        sheet.write(1,11,'已收租金')
        sheet.write(1,12,'原抵入本金')
        sheet.write(1,13,'资产名称')
        sheet.write(1,14,'数量')
        sheet.write(1,15,'贷款时的评估价')
        sheet.write(1,16,'抵入时的评估价')
        sheet.write(1,17,'抵入方式')
        sheet.write(1,18,'位置')
        sheet.write(1,19,'备注')
        sheet.write(1,20,'交财务租金')
        sheet.write(1,21,'表外租金')
        sheet.write(1,22,'是否我行出租')
        sheet.write(1,23,'年租金')
        for index in data:
            i = i+1 
            sheet.write(i,0,index.get('book').get('id'))
            sheet.write(i,1,index.get('application').get('handle_branch'))
            sheet.write(i,2,index.get('party').get('name'))
            sheet.write(i,3,index.get('lend_transaction').get('amount'))
            sheet.write(i,7,index.get('repossession').get('in_amount'))
            sheet.write(i,8,index.get('repossession').get('in_accrual'))
            sheet.write(i,9,index.get('repossession').get('in_tax'))
            sheet.write(i,10,index.get('repossession').get('in_balance'))
            sheet.write(i,11,index.get('repossession').get('received_rent'))
            sheet.write(i,12,index.get('repossession').get('principal'))
            sheet.write(i,13,index.get('repossession').get('gty_name'))
            sheet.write(i,14,index.get('repossession').get('gty_area'))
            sheet.write(i,15,index.get('repossession').get('gty_amount_credit'))
            sheet.write(i,16,index.get('repossession').get('gty_amount_rep'))
            sheet.write(i,17,index.get('repossession').get('arrived_in_type'))
            sheet.write(i,18,index.get('repossession').get('gty_address'))
            sheet.write(i,19,index.get('repossession').get('remark'))
           
        report_filename = '../web/fabs/static/standing_book/standing_book_export.xls'
        book.save(report_filename) 
        return {'file':'static/standing_book/standing_book_export.xls'}






