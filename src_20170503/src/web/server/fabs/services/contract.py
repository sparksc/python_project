# -*- coding: utf-8 -*-
"""
    yinsho.services.ContractService
    #####################

    yinsho CreditServic module
"""
from ..model.application import *
from .service import BaseService
import hashlib, copy
from flask import json, g
from sqlalchemy import and_
from ..model.transaction import *
from ..model.credit import *
from ..model.contract import *
from ..model.guarantee import *
import time
import datetime
import random,os

class ContractService(BaseService):
 
    def querycontract(self,application_id):
        info=g.db_session.query(GuaranteeContractRelation).join(GuaranteeInfo,GuaranteeContractRelation.gty_info_id == GuaranteeInfo.id).filter(GuaranteeInfo.application_id == application_id).all()
        return info

    def update(self,**kwargs):
        return {'success':True}

    def query(self,contract_no=None,gty_method=None):
        u''' 查询合同列表 '''
        rst= g.db_session.query(GuaranteeContractRelation).join(GuaranteeInfo,GuaranteeInfo.id==GuaranteeContractRelation.gty_info_id).join(Contract,Contract.contract_id==GuaranteeContractRelation.contract_id)
        #rst=g.db_session.query(GuaranteeContractRelation).limit(20).all()
        if contract_no:
            rst=rst.filter(Contract.contract_no==contract_no[0])
        if gty_method:
            rst=rst.filter(GuaranteeInfo.gty_method==gty_method[0])
        contract_list=[{'contract':r.contract,'guarantee_info':r.guarantee_info} for r in rst.all()]
        return contract_list
 
    def query_lend(self,contract_no=None,gty_method=None,product_code=None):
        u''' 查询合同列表 '''
        rst=g.db_session.query(TransactionContractRelation).limit(10).all()
        contract_list=[{'contract':r.lend_contract,'lend_transaction':r.lend_transaction,'party':r.lend_transaction.application_transaction.application.customer.party,'product':r.lend_transaction.application_transaction.application.product,'application_info':r.lend_transaction.application_transaction.application} for r in rst]
        return contract_list
 

    def get(self, contract_id):
        u''' 查询合同详情 '''
        r=g.db_session.query(GuaranteeContractRelation).filter(GuaranteeContractRelation.contract_id == contract_id).first()
        contract_list={'contract':r.contract,'guarantee_info':r.guarantee_info} 
        return contract_list
 
    def submit(self,**kwargs):
        u'''生成合同'''
        application_info = kwargs.get('application_info')
        lend_transaction = kwargs.get('lend_transaction')
        user=g.web_session.user
        branch = g.db_session.query(UserBranch).filter(UserBranch.user_id == user.role_id).first()
        year = time.strftime('%Y',time.localtime(time.time()))
        count=g.db_session.query(Contract).filter(Contract.handle_branch==branch.branch.branch_code).filter(Contract.contract_sign_date.between(datetime.date(int(year), 1, 1),datetime.date(int(year)+1, 1, 1))).count()
        count = count+1
        if count<10:
            count = '0%d'%(count) 
        lend_contract=LendContract(contract_no=u'%s年(乌银)借字%s-%s号'%(year,branch.branch.branch_code,count),contract_type='lend_contract',handle_branch=branch.branch.branch_code,handle_teller=user.user_name,contract_sign_date=datetime.datetime.now())
        lendContract=TransactionContractRelation(lend_contract=lend_contract,transaction_id=lend_transaction.get('transaction_id'))
        g.db_session.add(lendContract)
        g.db_session.commit()
        return {'contract':lend_contract}

    def save(self,**kwargs):
        u'''生成抵质押合同'''
        contract_info=kwargs.get('contract')
        gty_info=kwargs.get('guarantee_info')
        user=g.web_session.user
        branch = g.db_session.query(UserBranch).filter(UserBranch.user_id == user.role_id).first()
        year = time.strftime('%Y',time.localtime(time.time()))
        count=g.db_session.query(Contract).filter(Contract.handle_branch==branch.branch.branch_code).filter(Contract.contract_sign_date.between(datetime.date(int(year), 1, 1),datetime.date(int(year)+1, 1, 1))).count()
        count = count+1
        if count<10:
            count = '0%d'%(count) 
        contract_info.update({'handle_branch':branch.branch.branch_code,
                                   'handle_teller':user.user_name,
                                   'contract_sign_date':datetime.datetime.now()}) 
        con=None
        if gty_info.get('gty_method') == u'质押':
             contract_info.update({'contract_no':u'%s年(乌银)质字%s-%s号'%(year,branch.branch.branch_code,count) })
             con = PledgeContract(**contract_info)
        elif gty_info.get('gty_method') == u'抵押':
             contract_info.update({'contract_no':u'%s年(乌银)抵字%s-%s号'%(year,branch.branch.branch_code,count) })
             con = MortgageContract(**contract_info)
        else :
             contract_info.update({'contract_no':u'%s年(乌银)保字%s-%s号'%(year,branch.branch.branch_code,count) })
             con = WarrandiceContract(**contract_info)
        g.db_session.add(GuaranteeContractRelation(contract = con,gty_info_id=gty_info.get('id')))
        g.db_session.commit() 
        return {'contract':con}

    def list_update(self,**kwargs):
        contract_list = kwargs.get('contracts')
        for contract in contract_list:
            cont = g.db_session.query(Contract).filter(Contract.contract_id ==contract.get('contract_id')).update({'amount':contract.get('amount'),'contract_effect_date':contract.get('begin_date'),'contract_due_date':contract.get('end_date')})
            cont = g.db_session.query(Contract).filter(Contract.contract_id ==contract.get('contract_id')).first()
            if cont.debt == []:
                debt = Debt(amount=contract.get('amount'),
                    begin_date=contract.get('begin_date'),
                    end_date=contract.get('end_date'),
                    is_credit_card = contract.get('is_credit_card'),
                    debt_rate=contract.get('debt_rate'),
                    contract=cont)
                g.db_session.add(debt)
            else:
                g.db_session.query(Debt).filter(Debt.id == cont.debt[0].id).update({'amount':contract.get('amount'),'begin_date':contract.get('begin_date'),'end_date':contract.get('end_date'),'is_credit_card':contract.get('is_credit_card'),'debt_rate':contract.get('debt_rate')})

    def list_query(self,transaction_id):
        tran_cons = g.db_session.query(TransactionContractRelation).filter(TransactionContractRelation.transaction_id == transaction_id).all()
        cont_list = []
        for tran_con in  tran_cons:
            contract_info={}
            con = tran_con.lend_contract
            contract_info.update({'contract_id':con.contract_id,'contract_no':con.contract_no})
            print contract_info
            debt = g.db_session.query(Debt).filter(Debt.contract_id == con.contract_id).first()
            if debt:
               debt = debt
            else:
               continue;#return {'contracts':[]}
            contract_info.update({'debt_id':debt.id,'begin_date':debt.begin_date,'end_date':debt.end_date,'amount':debt.amount,'is_credit_card':debt.is_credit_card,'debt_rate':debt.debt_rate})
            cont_list.append(contract_info)
        print cont_list
        return {'contracts':cont_list}


    def query_payment(self,debt_id):
        payment = g.db_session.query(Payment).filter(Payment.debt_id == debt_id).first()
        return payment
    
    def update_payment(self,**kwargs):
        debt_id =  kwargs.get('debt_id')
        #kwargs.pop('debt_id')
        if 'application_id' in kwargs.keys():
            kwargs.pop('application_id')
        if 'debt' in kwargs.keys():
            kwargs.pop('debt')
        if 'id' in kwargs.keys():
            kwargs.pop('id')
        payment = g.db_session.query(Payment).filter(Payment.debt_id == debt_id).first()
        print kwargs
        if payment:
           g.db_session.query(Payment).filter(Payment.debt_id == debt_id).update(kwargs)   
        else:
           payment = Payment(**kwargs) 
           g.db_session.add(payment)

        return {'msg':u"更新成功"}
