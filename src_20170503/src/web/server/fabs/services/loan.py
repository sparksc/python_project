# -*- coding: utf-8 -*-
"""
    yinsho.services.LoanService
    #####################
    yinsho LoanService module
"""
import hashlib, copy
import  xlwt
from flask import json, g, current_app
from sqlalchemy import and_
from sqlalchemy import desc
from ..model.credit import *
from ..model.transaction import *
from ..model.application import *
from ..model.contract import *
from ..model.guarantee import *
from ..workflow import task
from ..workflow.parameter import *
from ..database.sqlal import simple_session
from ..base import core_inf

import decimal
from decimal import Decimal
import datetime
import random
from .service import BaseService

class LoanService(BaseService):

    def save(self, **kwargs):
        u'''放款保存 '''
        customer = kwargs.get('customer')
        transaction_info = kwargs.get('transaction_info')
        application_info = kwargs.get('application_info')
        lend_transaction = kwargs.get('lend_transaction')
        if lend_transaction ==None:
            lend_transaction ={}
        product_code = application_info.get('product_code')
        

        discount_deadline = lend_transaction.get('discount_deadline');
        if discount_deadline:
            discount_deadline = datetime.datetime.strptime(discount_deadline,'%Y-%m-%d')
        discount_firstend = lend_transaction.get('discount_firstend');
        if discount_firstend:
            discount_firstend = datetime.datetime.strptime(discount_firstend,'%Y-%m-%d')
        lend_transaction.update({
                                'application_transaction_id':transaction_info.get('transaction_id'),
                                'lend_type':'lend_transaction',
                                'amount':transaction_info.get('amount'),
                                'product_code':product_code,
                                'repayment_method':application_info.get('repayment_method'),
                                'repayment_times':application_info.get('repayment_times'),
                                'transaction_name':customer.get('name')+'的放款申请',
                                })
        lend_transaction=LendTransaction(**lend_transaction)
        g.db_session.add(lend_transaction)
        g.db_session.commit()
        return {'msg':'保存成功'}

    def save_acceptanceBill(self, **kwargs):
        u'''承兑汇票签发保存 '''
        customer = kwargs.get('customer')
        transaction_info = kwargs.get('transaction_info')
        application_info = kwargs.get('application_info')
        lend_transaction = kwargs.get('lend_transaction')
        if lend_transaction ==None:
            lend_transaction ={}
        product_code = application_info.get('product_code')
        discount_deadline = lend_transaction.get('discount_deadline');
        if discount_deadline:
            discount_deadline = datetime.datetime.strptime(discount_deadline,'%Y-%m-%d')
        discount_firstend = lend_transaction.get('discount_firstend');
        if discount_firstend:
            discount_firstend = datetime.datetime.strptime(discount_firstend,'%Y-%m-%d')
        lend_transaction.update({
                                'application_transaction_id':transaction_info.get('transaction_id'),
                                'amount':transaction_info.get('amount'),
                                'lend_type':'acceptance_bill_loan',
                                'product_code':product_code,
                                'repayment_method':application_info.get('repayment_method'),
                                'repayment_times':application_info.get('repayment_times'),
                                'transaction_name':customer.get('name')+'的放款申请',
                                'bill_kind':application_info.get('bill_kind'),
                                'repayment_method':application_info.get('repayment_method'), 
                                'bill_type':application_info.get('bill_type'),
                                'main_gua_type':application_info.get('main_gua_type'),
                                'purpose_type':application_info.get('purpose_type'),
                                'repayment_from':application_info.get('repayment_from'),
                                })
        lend_transaction=AcceptanceBillLoan(**lend_transaction)
        g.db_session.add(lend_transaction)
        return {'msg':'保存成功'}


    def submit(self, **kwargs):
        u'''放款申请'''
        application_info = kwargs.get('application_info')
        rst = g.db_session.query(ApplicationTransaction, Application) \
            .join(Application, Application.id == ApplicationTransaction.application_id)\
            .filter(Application.id == application_info.get('id')).first()
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

        g.db_session.flush()
        task_list = task.get_task(at)
        next_step = []
        for t in task_list:
              if t.finished==None:
                  role=get_parameter(t.activity,u"角色")
                  rst=g.db_session.query(UserGroup).join(Group,UserGroup.group_id==Group.id).filter(Group.group_name==role).all() 
                  users =[{'user_name': r.user.user_name,'name':r.user.name} for r in rst ] 
                  next_step.append({'activity':t.activity,'role':role,'users':users})
        return {'next_step':next_step} 


        return {'msg':'申请成功'}

    def loan(self,**kwargs):
        u'''  放款  '''
        #print kwargs
        customer = kwargs.get('customer')
        transaction_info = kwargs.get('transaction_info')
        application_info = kwargs.get('application_info')
        lend_transaction = kwargs.get('lend_transaction')
        product_name = kwargs.get('product_name')
        product_code = application_info.get('product_code')
        user = g.web_session.user
        application_id = application_info.get('id')
        transaction_id = lend_transaction.get('transaction_id')
        #放款接口
        contract_transaction = g.db_session.query(TransactionContractRelation).filter(TransactionContractRelation.transaction_id == transaction_id).first()
        if contract_transaction:
            contract = g.db_session.query(Contract).filter(Contract.contract_id == contract_transaction.contract_id).first()
        
        #贴现
        if product_code == '023':
            return self.loan_discount(**kwargs)       #签发
        elif product_code == '007':
            core_rt = core_inf.trans130101(customer,transaction_info,application_info,lend_transaction,user,{'product_name':product_name})
        #一般贷款
        else:
            core_rt1 = core_inf.trans120000(customer,transaction_info,application_info,lend_transaction,user,{'product_name':product_name})
            print core_rt1
            if core_rt1:
                core_rt2 = core_inf.lend_trans(customer,transaction_info,application_info,lend_transaction,user,{'product_name':product_name})
        return core_rt2


    def update_acceptanceBill(self, **kwargs):
        u'''承兑汇票签发更新 '''
        customer = kwargs.get('customer')
        product_code = kwargs.get('application_info').get('product_code')

        transaction_info = kwargs.get('transaction_info')
        application_info = kwargs.get('application_info')
        lend_transaction = kwargs.get('lend_transaction')
        #lend_transaction.pop('bill_rate_sum');
        application_id = application_info.get('id')
        product_name = kwargs.get('product_name')
        transaction_id=lend_transaction.get('transaction_id')
        lend_transaction.pop('transaction_id')
        if lend_transaction.get('transaction_activity'):
           lend_transaction.pop('transaction_activity')
        if lend_transaction.get('transaction'):
           lend_transaction.pop('transaction')
        lend_transaction.pop('transaction_name')
        lend_transaction.pop('transaction_type')
        lend_transaction.pop('party_id')
        lend_transaction.pop('transaction_timestamp')
        lend_transaction.pop('transaction_date_id')
        lend_transaction.pop('currency_code')
	lend_transaction.pop('debt_interest')
        lend_transaction.pop('sub_return_data')
        a = g.db_session.query(LendTransaction).filter(LendTransaction.transaction_id == transaction_id).first()
        for k in lend_transaction.keys():
             a.__setattr__(k,lend_transaction.get(k)) 
        '''
        user = g.web_session.user
        core_rt = core_inf.lend_trans(customer,transaction_info,application_info,lend_transaction,user,{'product_name':product_name})
        '''
        g.db_session.commit()
        return {'msg':'更新成功'}




    def update(self, **kwargs):
        u'''放款更新 '''
        print '------------------------------------------'
        customer = kwargs.get('customer')
        product_code = kwargs.get('application_info').get('product_code')
        if product_code == '023':
            return self.update_discount(**kwargs)

        transaction_info = kwargs.get('transaction_info')
        application_info = kwargs.get('application_info')
        lend_transaction = kwargs.get('lend_transaction')
        #lend_transaction.pop('bill_rate_sum');
        application_id = application_info.get('id')
        product_name = kwargs.get('product_name')
        if lend_transaction.get('transaction_id'):
           transaction_id=lend_transaction.get('transaction_id')
           lend_transaction.pop('transaction_id')
        if lend_transaction.get('transaction_activity'):
           lend_transaction.pop('transaction_activity')
        if lend_transaction.get('transaction'):
           lend_transaction.pop('transaction')
        if lend_transaction.get('transaction_name'):
           lend_transaction.pop('transaction_name')
        
        if lend_transaction.get('transaction_type') != None:
           lend_transaction.pop('transaction_type')
        if lend_transaction.get('party_id'):
           lend_transaction.pop('party_id')
        if lend_transaction.get('transaction_timestamp'):
           lend_transaction.pop('transaction_timestamp')
        if lend_transaction.get('transaction_date_id'):
           lend_transaction.pop('transaction_date_id')
        if lend_transaction.get('currency_code'):
           lend_transaction.pop('currency_code')
         
        lend_transaction.pop('party_id')
        lend_transaction.pop('transaction_timestamp')
        lend_transaction.pop('transaction_type')
        lend_transaction.pop('transaction_date_id')
        lend_transaction.pop('currency_code')
         
        g.db_session.query(LendTransaction).filter(LendTransaction.transaction_id == transaction_id).update(lend_transaction)
        '''
        user = g.web_session.user
        core_rt = core_inf.lend_trans(customer,transaction_info,application_info,lend_transaction,user,{'product_name':product_name})
        '''
        g.db_session.commit()
        return {'msg':'更新成功'}



    #-------------------  贴现放款界面操作  ------------------------
    def update_discount(self,**kwargs):
        u''' 贴现放款更新 '''
        customer = kwargs.get('customer')
        party_id = customer.get('id')
        transaction_info = kwargs.get('transaction_info')
        application_info = kwargs.get('application_info')
        lend_transaction = kwargs.get('lend_transaction')
        #lend_transaction.pop('bill_rate_sum');
        loan_type_code = application_info.get('product_code')
        bill_num = lend_transaction.get('bill_num')
        application_id = application_info.get('id')
        check = kwargs.get('check')
        if check == 'yes':
            quote_report =  kwargs.get('quote_report')
            sur_rep = None
            if quote_report == u'否' or quote_report in[None,'null']:
                sur_rep = g.db_session.query(SurveyReport).filter(SurveyReport.party_id==party_id).filter(SurveyReport.product_code == loan_type_code).order_by(desc(SurveyReport.end_date)).first()
                if sur_rep == None:
                    return {"msg":"必须生成调查报告"}
            amount = lend_transaction.get('amount')
            if application_id == None or bill_num in [0,None,'null']:
                return {"msg":"请输入票据数量"}
            app = g.db_session.query(Application).filter(Application.id == application_id).first()
            #if len(app.bill_check) == 0:
            #    return {"msg":"没有验票"}

            #判断是否有票据
            if len(app.bill) == 0:
                return {"msg":"没有票据"}
            
            if(len(app.bill) != int(bill_num)):
                return {"msg":"票据数量不对"}
            total = 0
            total_amount = 0
            discount_deadline = lend_transaction.get('discount_deadline')
            discount_firstend = lend_transaction.get('discount_firstend')
            for bill in app.bill:
                total = Decimal(total) + Decimal(bill.discount_interest)
                total_amount = Decimal(total_amount) + Decimal(bill.bill_amount)
                if discount_firstend:
                    if discount_firstend > str(bill.bill_due_date):
                        return {"msg":"最早到期日验证失败"}
                    if discount_deadline < str(bill.bill_due_date):
                        return {"msg":"最晚到期日验证失败"}
                else:
                    return {'msg':"请输入票据到期时间"}
                lend_transaction.update({'bill_rate_sum':str(total)})
            print amount
            print total_amount 
            if(Decimal(amount) != Decimal(total_amount)):
                return {"msg":"票据金额总和和申请金额不一致"}
                
        product_name = kwargs.get('product_name')
        transaction_id=lend_transaction.get('transaction_id')
        lend_transaction.pop('transaction_id')
        '''
        if lend_transaction.get('transaction_activity'):
           lend_transaction.pop('transaction_activity')
        if lend_transaction.get('transaction'):
           lend_transaction.pop('transaction')
        if lend_transaction.get('transaction_name'):
           lend_transaction.pop('transaction_name')
        '''
        lend_transaction.pop('transaction_type')
        lend_transaction.pop('party_id')
        lend_transaction.pop('transaction_timestamp')
        lend_transaction.pop('transaction_date_id')
        lend_transaction.pop('currency_code')
        lend_transaction.pop('transaction_name')
        if(lend_transaction.get('journal_no')):
            lend_transaction.pop('journal_no')
        g.db_session.query(Application).filter(Application.id == application_id).update(application_info)
        g.db_session.query(LendTransaction).filter(LendTransaction.transaction_id == transaction_id).update(lend_transaction)
        '''
        user = g.web_session.user
        core_rt = core_inf.lend_trans(customer,transaction_info,application_info,lend_transaction,user,{'product_name':product_name})
        '''
        g.db_session.commit()
        return {'msg':'更新成功'}

    def loan_discount(self,**kwargs):
        u"""   贴现放款   """
        customer = kwargs.get('customer')
        transaction_info = kwargs.get('transaction_info')
        application_info = kwargs.get('application_info') 
        lend_transaction = kwargs.get('lend_transaction') 
        product_name = kwargs.get('product_name')
        product_code = application_info.get('product_code') 
        user = g.web_session.user
        application_id = application_info.get('id')
        transaction_id = lend_transaction.get('transaction_id')
        app = g.db_session.query(Application).filter(Application.id == application_id).first()
        if len(app.bill_check) < 2 :
            return {"msg":"验票人数不足2人"}

        #放款接口
        contract_transaction = g.db_session.query(TransactionContractRelation).filter(TransactionContractRelation.transaction_id == transaction_id).first()
        if contract_transaction: 
            contract = g.db_session.query(Contract).filter(Contract.contract_id == contract_transaction.contract_id).first()
            contract_no = contract.contract_no
        else:
            contract_no = ''
        #贴现
        rst = g.db_session.query(Bill_message).filter(Bill_message.application_id == application_id).all()
        rt = []
        for r in rst:
            it = r.__dict__
            #去除转字典生成的项
            if it.get('_sa_instance_state'):
                it.pop('_sa_instance_state')
            core_rt = core_inf.trans130211(customer,transaction_info,application_info,lend_transaction,user,{'product_name':product_name, 'bill_kill':it.get('bill_kill'), 'bill_type':it.get('bill_type'), 'bill_no':it.get('bill_no'), 'bill_amount':it.get('bill_amount'), 'bill_from_date':it.get('bill_from_date'), 'bill_due_date':it.get('bill_due_date'), 'bill_person':it.get('bill_person'), 'bill_start_branch':it.get('bill_start_branch'), 'bill_pay_branch_no':it.get('bill_pay_branch_no'), 'payee':it.get('payee'), 'discount_rate':it.get('discount_rate'), 'contract_no':contract_no})
            rt.append(core_rt)
        return {'msg':'放款成功','result':rt}

    def query(self, transaction_id):
        q = g.db_session.query(LendTransaction,TransactionContractRelation).outerjoin(TransactionContractRelation,TransactionContractRelation.transaction_id==LendTransaction.transaction_id).filter(LendTransaction.application_transaction_id == transaction_id).first()
        #print 'execute',q.execute_rate
        lend_tran=None
        lend_rel=None
        if q :
            lend_tran =  q.LendTransaction.__dict__
            lend_rel = q.TransactionContractRelation
            if lend_tran.get('_sa_instance_state'):
                lend_tran.pop('_sa_instance_state')
            bill_rate_sum = lend_tran.get('bill_rate_sum')
        rst_list={'lend_transaction':lend_tran}
        if  lend_rel :
             rst_list.update({'contract':lend_rel.lend_contract})
        return rst_list


    def query_acceptanceBill(self, transaction_id):
        q = g.db_session.query(AcceptanceBillLoan,TransactionContractRelation).outerjoin(TransactionContractRelation,TransactionContractRelation.transaction_id==AcceptanceBillLoan.transaction_id).filter(AcceptanceBillLoan.application_transaction_id == transaction_id).first()
        rst_list={}
        if q :
            lend_tran =  q.AcceptanceBillLoan.__dict__
            if lend_tran.get('_sa_instance_state'):
                lend_tran.pop('_sa_instance_state')
            rst_list={'lend_transaction':lend_tran} 
            lend_rel = q.TransactionContractRelation
            if lend_rel:
                contract=lend_rel.lend_contract
                rst_list.update({'contract':contract})
        return rst_list



    def query_lend(self, application_id):
        q = g.db_session.query(LendTransaction).join(ApplicationTransaction,ApplicationTransaction.transaction_id==LendTransaction.application_transaction_id).filter(ApplicationTransaction.application_id==application_id).first()
        lend_tran=None
        if q :
            lend_tran =  q.__dict__
            if lend_tran.get('_sa_instance_state'):
                lend_tran.pop('_sa_instance_state')
        rst_list={'lend_transaction':lend_tran}
        return rst_list

    def loan_print(self, **kwargs):
        """
            放款通知书打印
        """
        generate_date = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        upload_path = current_app.config.get('UPLOAD_PATH')

        style = xlwt.easyxf('align: wrap on')
        wb = xlwt.Workbook()
        ws = wb.add_sheet(u"生成时间：%s" % generate_date, cell_overwrite_ok=True)

        ws.write(0, 3, unicode('放款通知书'))

        row_size = len(kwargs)
        for idx, key in enumerate(kwargs):
            clm1 = 0
            clm2 = 2
            if idx>row_size/2 and row_size > 6:
                idx = idx - (row_size/2 + 1 )
                clm1 += 4
                clm2 += 4
            ws.write(idx+2, clm1, key)
            if (kwargs.get(key)).find('?') == -1:
                ws.write(idx+2, clm2, kwargs.get(key), style)
            if len(kwargs.get(key))>10:
                ws.row(idx+2).height_mismatch = True
                ws.row(idx+2).height = 2 * 256


        homedir = os.getcwd()
        upload_path = homedir + '/../web/fabs/static'


        file_name = '/loan_%s.xls' % (generate_date)
        file_path = upload_path + file_name
        wb.save(file_path)

        os.system('unoconv -f pdf -o %s %s' % (upload_path, file_path))
        return "%s" % ('/fabs/static/loan_%s.pdf' % generate_date)

    def query_list(self, transaction_id=None):
        u'''查询贷款列表'''
        q = g.db_session.query(LendTransaction)
        if transaction_id:
             q = q.filter(LendTransaction.transaction_id == transaction_id[0])
        rst=q.all()
        lend_tran=None
        rst_list=[]
        if rst :
            for r in rst:
                lend_tran =  r.__dict__
                party=r.application_transaction.application.customer.party
                if lend_tran.get('_sa_instance_state'):
                     lend_tran.pop('_sa_instance_state')
                bill_rate_sum = lend_tran.get('bill_rate_sum')
                rst_data={'lend_transaction':lend_tran,
                          'party':party,
                          'product':r.application_transaction.application.product
                          }
                rst_list.append(rst_data)
        return rst_list

        
