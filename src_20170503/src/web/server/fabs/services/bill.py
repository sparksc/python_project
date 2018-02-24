# -*- coding: utf-8 -*-
"""
    yinsho.services.BillServic
    #####################

    yinsho BillServic module
"""
from ..model.party import *
from .service import BaseService
import hashlib, copy
from flask import json, g
from sqlalchemy import and_
from ..model.credit import *
from ..model.transaction import *
from ..model.application import *
from ..model.task import Task
from ..workflow import task
from ..workflow.parameter import *
from ..database.sqlal import simple_session
from ..base import core_inf 

import decimal
from decimal import Decimal
import datetime
import random
import datetime
import xlrd

class BillService(BaseService):
    def bill_query(self,application_id ,**kwargs):
        bill_no = kwargs.get('bill_no')
        product_type = kwargs.get('product_type')
        print product_type
        if bill_no == -1:
            party = None
        else:
            party = g.db_session.query(Bill_message).filter(Bill_message.bill_no == bill_no).filter(Bill_message.product_type == product_type).first()
        count = g.db_session.query(Bill_message).filter(Bill_message.application_id == application_id).filter(Bill_message.product_type == product_type).count()
        bill_type = g.db_session.query(Bill_message).filter(Bill_message.application_id == application_id).first()
        count = count + 1;
        print party
        if party != None:
            msg = 'err'
        else:
            msg = 'success'
        return {'msg':msg, 'count':count, 'bill_type':bill_type}

    def bill_update(self,bill_id,**kwargs):
        bill=kwargs
        if bill.get('bill_from_date'):
            bill_from_date = datetime.datetime.strptime(bill.get('bill_from_date'), u"%Y-%m-%d")
            bill.pop('bill_from_date')
            bill.update({'bill_from_date':bill_from_date})
        if bill.get('bill_due_date'):
            bill_due_date = datetime.datetime.strptime(bill.get('bill_due_date'), u"%Y-%m-%d")
            bill.pop('bill_due_date')
            bill.update({'bill_due_date':bill_due_date})
        if bill.get('discount_date'):
            discount_date = datetime.datetime.strptime(bill.get('discount_date'), u"%Y-%m-%d")
            bill.pop('discount_date')
            bill.update({'discount_date':discount_date})
        if bill.get('discount_due_date'):
            discount_due_date = datetime.datetime.strptime(bill.get('discount_due_date'), u"%Y-%m-%d")
            bill.pop('discount_due_date')
            bill.update({'discount_due_date':discount_due_date})
        if bill.get('deal_date'):
            deal_date = datetime.datetime.strptime(bill.get('deal_date'), u"%Y-%m-%d")
            bill.pop('deal_date')
            bill.update({'deal_date':deal_date})
        bill.pop('id')
        bill.pop('application_id')
        #bill.pop('application')
        g.db_session.query(Bill_message).filter(Bill_message.id == bill_id).update(bill)
        g.db_session.commit()

    def bill_create(self,application_id,**kwargs):
        bill=kwargs
        if bill.get('bill_from_date'):
            bill_from_date = datetime.datetime.strptime(bill.get('bill_from_date'), u"%Y-%m-%d")
            bill.pop('bill_from_date')
            bill.update({'bill_from_date':bill_from_date})
        if bill.get('bill_due_date'):
            bill_due_date = datetime.datetime.strptime(bill.get('bill_due_date'), u"%Y-%m-%d")
            bill.pop('bill_due_date')
            bill.update({'bill_due_date':bill_due_date})
        if bill.get('discount_date'):
            discount_date = datetime.datetime.strptime(bill.get('discount_date'), u"%Y-%m-%d")
            bill.pop('discount_date')
            bill.update({'discount_date':discount_date})
        if bill.get('discount_due_date'):
            discount_due_date = datetime.datetime.strptime(bill.get('discount_due_date'), u"%Y-%m-%d")
            bill.pop('discount_due_date')
            bill.update({'discount_due_date':discount_due_date})
        if bill.get('deal_date'):
            deal_date = datetime.datetime.strptime(bill.get('deal_date'), u"%Y-%m-%d")
            bill.pop('deal_date')
            bill.update({'deal_date':deal_date})
        bill.update({'application_id':application_id})
        ddd = Bill_message(**bill)
        g.db_session.add(ddd)
        g.db_session.commit()

    def bill_query_info(self,application_id):
        u''' 查询票据信息 '''
        rst = g.db_session.query(Bill_message).filter(Bill_message.application_id == application_id).all()
        bill_info_list=[]
        for r in rst:
            it = r.__dict__
            #去除转字典生成的项
            if it.get('_sa_instance_state'):
                it.pop('_sa_instance_state')
            bill_info_list.append(it)
        return bill_info_list

    def bill_delete(self, bill_id):
        u''' 删除票据信息 '''
        g.db_session.query(Bill_message).filter(Bill_message.id == bill_id).delete()
        g.db_session.commit()
        return {'msg':u'删除成功'}

    def bill_check(self, application_id,**kwargs):
        u''' 票据检查 '''
        print kwargs
        user_name = kwargs.get('user_name')
        app = g.db_session.query(Application).filter(Application.id == application_id).first();
        if app.bill_check:
            if len(app.bill_check) ==2:
                return {"msg":"已经有2个人验票了"}
            bill_check = app.bill_check[0]
            if user_name == bill_check.user_name:
                return {"msg":"你已验票,不能重复验票"}
            billcheck = BillCheck(user_name=user_name,application=app);
            g.db_session.add(billcheck)
        else :
            billcheck = BillCheck(user_name=user_name,application=app);
            g.db_session.add(billcheck)
        g.db_session.commit()
        return {'msg':u'验票成功'}

    def bill_check_query(self,application_id):
        u''' 验票人数量检查   '''
        app = g.db_session.query(Application).filter(Application.id == application_id).first();
        if app.bill_check:
            if len(app.bill_check) == 2:
                return {'msg':'success'}
            else:
                return {'msg':'验票人数不够'}
        else:
            return {'msg':'未验票'}

    def listBill_import_data(self, filepath, application_id):
        """
            清单批量录入
        """
    
        data = xlrd.open_workbook(filepath)
        sheet = data.sheet_by_index(0)
        #行
        nrows = sheet.nrows
        bill_type_sign = ""
        key = 1
        bill_list = []
        for r in range(1,nrows):
            bill_amount = sheet.cell(r,0).value
            bill_kill = sheet.cell(r,1).value
            bill_person = sheet.cell(r,2).value
            bill_from_date = sheet.cell(r,3).value
            bill_due_date = sheet.cell(r,4).value
            bill_person_acc = sheet.cell(r,5).value
            bill_no = sheet.cell(r,6).value
            bill_start_branch = sheet.cell(r,7).value
            proposer_start_branch = sheet.cell(r,8).value
            bill_pay_branch_no = sheet.cell(r,9).value
            payee = sheet.cell(r,10).value
            accptor_addr = sheet.cell(r,11).value
            proposer_acc = sheet.cell(r,12).value
            bill_type = sheet.cell(r,13).value
            print r
            if(accptor_addr=='' or bill_amount=='' or bill_person=='' or bill_from_date=='' or bill_due_date=='' or bill_person_acc=='' or bill_start_branch=='' or proposer_start_branch=='' or payee=='' or proposer_acc=='' or bill_type==''):
                return 'err'
            #票据日期判断  票据号长度
            if bill_type == '电票':
                if len(bill_no) != 30:
                    return 'err'
                if self.year(bill_from_date, bill_due_date):
                    print 'succ'
                else :
                    return 'err'
            else:
                if len(bill_no) != 0:
                    return 'err'
                if self.month(bill_from_date, bill_due_date):
                    print 'succ'
                else :
                    return 'err'
            #票据种类判断
            if key == 1:
                bill_type_sign = bill_type
                key = 0
            else :
                if(bill_type_sign != bill_type):
                    return 'err'
 
            bill_list.append({'bill_amount':bill_amount, 'bill_kill':bill_kill, 'bill_person':bill_person, 'bill_from_date':bill_from_date, 'bill_due_date':bill_due_date, 'bill_person_acc':bill_person_acc, 'bill_no':bill_no, 'bill_start_branch':bill_start_branch, 'proposer_start_branch':proposer_start_branch, 'bill_pay_branch_no':bill_pay_branch_no, 'payee':payee, 'accptor_addr':accptor_addr, 'proposer_acc':proposer_acc, 'bill_type':bill_type})
        for b in bill_list:
            print b
            b.update({'application_id':application_id})
            ddd = Bill_message(**b)
            g.db_session.add(ddd)
        g.db_session.commit()
        return 'succ'

    def Bill_import_data(self, filepath, application_id):
        """
            批量票据录入
        """
        data = xlrd.open_workbook(filepath)
        sheet = data.sheet_by_index(0)
        #行 
        nrows = sheet.nrows
        bill_type_sign = ""
        key = 1
        bill_list = []
        for r in range(1,nrows):
            bill_no = sheet.cell(r,0).value
            bill_amount = sheet.cell(r,1).value
            bill_kill = sheet.cell(r,2).value
            check_bill_type = sheet.cell(r,3).value
            bill_from_date = sheet.cell(r,4).value
            bill_due_date = sheet.cell(r,5).value
            bill_person = sheet.cell(r,6).value            
            bill_start_branch = sheet.cell(r,7).value           
            bill_pay_branch_no = sheet.cell(r,8).value          
            bill_person_acc = sheet.cell(r,9).value           
            payee = sheet.cell(r,10).value         
            proposer_start_branch = sheet.cell(r,11).value           
            proposer_acc = sheet.cell(r,12).value          
            discount_date = sheet.cell(r,13).value
            discount_due_date = sheet.cell(r,14).value
            discount_rate = sheet.cell(r,15).value
            use_date = sheet.cell(r,16).value
            more_bill_no = sheet.cell(r,17).value
            is_more_bill = sheet.cell(r,18).value
            is_deal_bg = sheet.cell(r,19).value
            is_bill_check = sheet.cell(r,20).value
            accptor_no = sheet.cell(r,21).value
            accptor_rank = sheet.cell(r,22).value
            accptor_addr = sheet.cell(r,24).value 
            bill_type = sheet.cell(r,25).value
            phone = sheet.cell(r,26).value
            is_ror = sheet.cell(r,27).value
            accptor_agreement_no = sheet.cell(r,28).value
            deal_no = sheet.cell(r,29).value  
            deal_amount = sheet.cell(r,30).value
            deal_date = sheet.cell(r,31).value
            pay_branch = sheet.cell(r,31).value
            discount_type = sheet.cell(r,33).value 
            
            if(accptor_addr=='' or bill_amount=='' or bill_person=='' or bill_from_date=='' or bill_due_date=='' or bill_person_acc=='' or bill_no=='' or bill_start_branch=='' or proposer_start_branch=='' or payee=='' or proposer_acc=='' or bill_type=='' or bill_pay_branch_no=='' or discount_date=='' or discount_rate=='' or accptor_rank=='' or use_date=='' or discount_type==''):
                return 'err'
            #票据日期判断  票据号长度
            if bill_type == '电票':
                if len(bill_no) != 30:
                    return 'err'
                if self.year(bill_from_date, bill_due_date):
                    print 'succ'
                else :
                    return 'err'
            else:
                if len(bill_no) != 16:
                    return 'err'
                if self.month(bill_from_date, bill_due_date):
                    print 'succ'
                else :
                    return 'err'
            #票据种类判断
            if key == 1:
                bill_type_sign = bill_type
                key = 0
            else :
                if(bill_type_sign != bill_type):
                    return 'err'
            d1 = bill_from_date.split('-')
            d2 = bill_due_date.split('-')
            d3 = datetime.datetime(int(d1[0]),int(d1[1]),int(d1[2]))
            d4 = datetime.datetime(int(d2[0]),int(d2[1]),int(d2[2]))
            discount_interest = Decimal(Decimal(int(bill_amount) * (d4-d3).days * int(discount_rate))/Decimal(30*1000)).quantize(Decimal('0.00'))
            print discount_interest
            bill_list.append({'bill_no':bill_no, 'bill_amount':bill_amount, 'bill_kill':bill_kill, 'check_bill_type':check_bill_type,  'bill_from_date':bill_from_date, 'bill_due_date':bill_due_date, 'bill_person':bill_person, 'bill_start_branch':bill_start_branch, 'bill_pay_branch_no':bill_pay_branch_no, 'bill_person_acc':bill_person_acc, 'payee':payee, 'proposer_start_branch':proposer_start_branch, 'proposer_acc':proposer_acc, 'discount_date':discount_date, 'discount_due_date':discount_due_date, 'discount_rate':discount_rate, 'use_date':use_date, 'more_bill_no':more_bill_no, 'is_more_bill':is_more_bill, 'is_deal_bg':is_deal_bg, 'is_bill_check':is_bill_check, 'accptor_no':accptor_no, 'accptor_rank':accptor_rank, 'accptor_addr':accptor_addr, 'bill_type':bill_type, 'phone':phone, 'is_ror':is_ror, 'accptor_agreement_no':accptor_agreement_no, 'deal_no':deal_no, 'deal_amount':deal_amount, 'deal_date':deal_date, 'pay_branch':pay_branch, 'discount_type':discount_type, 'discount_interest':discount_interest})
        for b in bill_list:
            b.update({'application_id':application_id})
            ddd = Bill_message(**b)
            g.db_session.add(ddd)
        g.db_session.commit()
        return 'succ'

    def year(self,date1,date2):
        year1 = str(date1)[0:4]
        year2 = str(date2)[0:4]
        year = int(year2) - int(year1)
        if year < 0 or year > 1:
            return 0
        month1 = str(date1)[5:7]
        month2 = str(date2)[5:7]
        month = int(month1) - int(month2)
        if month < 0:
            return 0
        elif month == 0:
            day1 = str(date1)[-2:]
            day2 = str(date2)[-2:]
            day = int(day1) - int(day2)
            if day < 0:
                return 0
        elif year == 0 and month == 0:
            if day >= 0:
                return 0
        return 1

    def month(self,date1,date2):
        year1 = str(date1)[0:4]
        year2 = str(date2)[0:4]
        year = int(year2) - int(year1)
        month1 = str(date1)[5:7]
        month2 = str(date2)[5:7]
        print month2
        print month1
        month21 = int(month2) - int(month1)
        month12 = int(month1) - int(month2)
        day1 = str(date1)[-2:]
        day2 = str(date2)[-2:]
        day = int(day1) - int(day2)
        if year < 0 or year > 1:
            return 0
        if year == 0:
            if month21 > 6:    
                return 0
            elif month21 == 6:
                if day < 0:
                #if day > 0:
                    return 0
            elif month21 == 0:
                if day >= 0:
                #if day <= 0:
                    return 0
        if year == 1:
            if month12 < 6:
                return 0
            elif month12 == 6:
                if day < 0:
                    return 0
        return 1

    #核心接口单独写服务
    def query_dis_name(self, account_no):
        core_rt = core_inf.trans120201(account_no)
        return core_rt
