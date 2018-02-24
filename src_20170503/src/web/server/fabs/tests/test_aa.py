# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
from sqlalchemy.orm import aliased
import unittest
import json
import time
import logging
from sys import modules
import datetime
import random
from ..model.customer import *
from ..model.party import *
from ..model.common import *
from ..model.user import *
from ..model.common import *
from ..model.application import *
from ..model.credit import *
from ..model.contract import *
from ..model.guarantee import *
from ..database.logger import  log
from db2_utils import DB2
log = logging.getLogger()
#log = logging.getLogger()
#log.basicConfig(level=logging.DEBUG)

class TestLoadInfo(unittest.TestCase):

    def setUp(self):
        log.debug("执行setup")
        self.session=simple_session()
 
    def load_con(self):   
        conDb= DB2()
        conDb.db_conn()
        lendDb= DB2()
        lendDb.db_conn()
        i = 0
        conDb.exesql("select * from CON_BASE","CON_BASE")
        while(conDb.row):
            i = i+1
            log.debug(i) 
            biz_type = conDb.get_byName('BIZ_TYPE')
            con_id=conDb.get_byName('CON_ID')
            lend_con = LendContract(contract_no=con_id,
                                    amount=conDb.get_byName('CON_AMOUNT'),
                                    contract_sign_date=conDb.get_byName('REG_DATE'), 
                                    contract_effect_date=conDb.get_byName('LOAN_START_DATE'),
                                    contract_due_date=conDb.get_byName('LOAN_END_DATE')
                                   )
            lend_transaction=None                       
            if biz_type =='023':
                  lendDb.exesql("select * from CON_DISC_BANK where CON_DISC_BANK.CON_ID = '%s'"%(con_id),"CON_DISC_BANK") 
                  while(lendDb.row):
                       lend_transaction=LendTransaction(amount=conDb.get_byName('CON_AMOUNT'),
                                                        discount_firstend=lendDb.get_byName('BILL_DUE_DATE'),
                                                        bill_num=lendDb.get_byName('BILL_QTY'),
                                                        product_code=conDb.get_byName('BIZ_TYPE'),
                                                        from_date=conDb.get_byName('LOAN_START_DATE'),
                                                        thur_date=conDb.get_byName('LOAN_END_DATE'),
                                                        repayment_method=conDb.get_byName('RETURN_METHOD'),
                                                        rep_period=conDb.get_byName('RETURN_TERMS'),
                                                        rep_per_fre=conDb.get_byName('RETURN_FREQ'),
                                                        first_rep_date=conDb.get_byName('FIRST_RETURN_DATE'),
                                                        repayment_from=conDb.get_byName('RETURN_SOURCE'),
                                                        compliance_rate=conDb.get_byName('BASE_IR'),
                                                        product_rate=conDb.get_byName('PRODUCT_IR'),
                                                        product_float_type=conDb.get_byName('FLOAT_IR_TYPE'),
                                                        product_rate_float=conDb.get_byName('FLOAT_IR_PERCENT'),
                                                        execute_rate=conDb.get_byName('MONTH_IR'),
                                                        overdue_rate_more=conDb.get_byName('PASS_DUE_PENALTY_IR'),
                                                        overdue_rate=conDb.get_byName('PASS_DUE_MONTH_IR'), 
                                                        shift_fine_rate=conDb.get_byName('OTHER_PENALTY_IR'),
                                                        shift_rate=conDb.get_byName('OTHER_MONTH_IR'),
                                                        debt_interest=conDb.get_byName('DEBIT_INTEREST_PERCENT'),
                                                        debt_interest_and=conDb.get_byName('DEBIT_INTEREST_IR'),
                                                        interest_method=conDb.get_byName('CACULATE_METHOD'),
                                                        interest_period=conDb.get_byName('CACULATE_PERIOD'),
                                                        int_per_fre =conDb.get_byName('CACULATE_FREQ'),
                                                        first_int_date=conDb.get_byName('FIRST_CACULATE_DATE'),
                                                        strate_product=conDb.get_byName('STRATEGY_INDUSTRY_TYPE'),
                                                        product_update=conDb.get_byName('INDUSTRY_TRANSITION_FLAG')
                       )
                       lendDb.get_next()                      
            if biz_type == '007':
                  lendDb.exesql("select * from CON_ACCP  where CON_ACCP.CON_ID = '%s'"%(con_id),"CON_ACCP") 
                  while(lendDb.row):
                       lend_transaction=AcceptanceBillLoan(amount=conDb.get_byName('CON_AMOUNT'),
                                                        product_code=conDb.get_byName('BIZ_TYPE'),
                                                        from_date=conDb.get_byName('LOAN_START_DATE'),
                                                        thur_date=conDb.get_byName('LOAN_END_DATE'),
                                                        repayment_method=conDb.get_byName('RETURN_METHOD'),
                                                        rep_period=conDb.get_byName('RETURN_TERMS'),
                                                        rep_per_fre=conDb.get_byName('RETURN_FREQ'),
                                                        first_rep_date=conDb.get_byName('FIRST_RETURN_DATE'),
                                                        repayment_from=conDb.get_byName('RETURN_SOURCE'),
                                                        compliance_rate=conDb.get_byName('BASE_IR'),
                                                        product_rate=conDb.get_byName('PRODUCT_IR'),
                                                        product_float_type=conDb.get_byName('FLOAT_IR_TYPE'),
                                                        product_rate_float=conDb.get_byName('FLOAT_IR_PERCENT'),
                                                        execute_rate=conDb.get_byName('MONTH_IR'),
                                                        overdue_rate_more=conDb.get_byName('PASS_DUE_PENALTY_IR'),
                                                        overdue_rate=conDb.get_byName('PASS_DUE_MONTH_IR'), 
                                                        shift_fine_rate=conDb.get_byName('OTHER_PENALTY_IR'),
                                                        shift_rate=conDb.get_byName('OTHER_MONTH_IR'),
                                                        debt_interest=conDb.get_byName('DEBIT_INTEREST_PERCENT'),
                                                        debt_interest_and=conDb.get_byName('DEBIT_INTEREST_IR'),
                                                        interest_method=conDb.get_byName('CACULATE_METHOD'),
                                                        interest_period=conDb.get_byName('CACULATE_PERIOD'),
                                                        int_per_fre =conDb.get_byName('CACULATE_FREQ'),
                                                        first_int_date=conDb.get_byName('FIRST_CACULATE_DATE'),
                                                        strate_product=conDb.get_byName('STRATEGY_INDUSTRY_TYPE'),
                                                        product_update=conDb.get_byName('INDUSTRY_TRANSITION_FLAG'),
                                                        trade_contract_no=lendDb.get_byName('TRADE_CONTRACT_NO'),
                                                        goods_name=lendDb.get_byName('GOODS_NAME'),
                                                        fee_percent=lendDb.get_byName('PROC_FEE_PERCENT'),
                                                        fee_amount=lendDb.get_byName('PROC_FEE_AMOUNT'),
                                                        pay_method=lendDb.get_byName('PAY_METHOD'),
                                                        pay_bank_name=lendDb.get_byName('PAY_BANK'),
                                                        accp_accounts_bank=lendDb.get_byName('ISSUE_BANK')
                       )

                       lendDb.get_next()      
            else:
                lend_transaction=LendTransaction(amount=conDb.get_byName('CON_AMOUNT'),
                                                 product_code=conDb.get_byName('BIZ_TYPE'),
                                                 from_date=conDb.get_byName('LOAN_START_DATE'),
                                                 thur_date=conDb.get_byName('LOAN_END_DATE'),
                                                 repayment_method=conDb.get_byName('RETURN_METHOD'),
                                                 rep_period=conDb.get_byName('RETURN_TERMS'),
                                                 rep_per_fre=conDb.get_byName('RETURN_FREQ'),
                                                 first_rep_date=conDb.get_byName('FIRST_RETURN_DATE'),
                                                 repayment_from=conDb.get_byName('RETURN_SOURCE'),
                                                 compliance_rate=conDb.get_byName('BASE_IR'),
                                                 product_rate=conDb.get_byName('PRODUCT_IR'),
                                                 product_float_type=conDb.get_byName('FLOAT_IR_TYPE'),
                                                 product_rate_float=conDb.get_byName('FLOAT_IR_PERCENT'),
                                                 execute_rate=conDb.get_byName('MONTH_IR'),
                                                 overdue_rate_more=conDb.get_byName('PASS_DUE_PENALTY_IR'),
                                                 overdue_rate=conDb.get_byName('PASS_DUE_MONTH_IR'), 
                                                 shift_fine_rate=conDb.get_byName('OTHER_PENALTY_IR'),
                                                 shift_rate=conDb.get_byName('OTHER_MONTH_IR'),
                                                 debt_interest=conDb.get_byName('DEBIT_INTEREST_PERCENT'),
                                                 debt_interest_and=conDb.get_byName('DEBIT_INTEREST_IR'),
                                                 interest_method=conDb.get_byName('CACULATE_METHOD'),
                                                 interest_period=conDb.get_byName('CACULATE_PERIOD'),
                                                 int_per_fre =conDb.get_byName('CACULATE_FREQ'),
                                                 first_int_date=conDb.get_byName('FIRST_CACULATE_DATE'),
                                                 strate_product=conDb.get_byName('STRATEGY_INDUSTRY_TYPE'),
                                                 product_update=conDb.get_byName('INDUSTRY_TRANSITION_FLAG')
                       )
            lend_rel=TransactionContractRelation(lend_contract=lend_con,lend_transaction=lend_transaction) 
            self.session.add(lend_rel)
            lendDb.exesql("select * from LOAN_BASE  where LOAN_BASE.CON_ID = '%s'"%(con_id),"LOAN_BASE")   
            debt=None
            while(lendDb.row):
                debt =Debt(contract=lend_con,
                           begin_date=lendDb.get_byName('ISSUE_DATE'),
                           end_date=lendDb.get_byName('DUE_DATE'),
                           amount=lendDb.get_byName('LOAN_AMOUNT'),
                           is_credit_card=lendDb.get_byName('CARD_CREDIT'),
                           extend_date=lendDb.get_byName('EXTEND_DATE'),
                           extend_time=lendDb.get_byName('EXTEND_TIME'),
                            ) 
                lendDb.get_next() 
                self.session.add(debt)
            app_id=conDb.get_byName('APP_ID')
            lendDb.exesql("select * from FUNDFLOW  where FUNDFLOW.APP_ID = '%s'"%(app_id),"FUNDFLOW")   
            payment=None
            while(lendDb.row):
                payment =Payment(debt=debt,
                                 paydetail=lendDb.get_byName('TRADE_CONTENT'),
                                 repayment_from=lendDb.get_byName('RETURN_SOURCE'),
                                 payment_method=lendDb.get_byName('PAYMENT_TYPE'),
                                 amount=lendDb.get_byName('PAYMENT_AMOUNT'),
                                 settle_type=lendDb.get_byName('BALANCE_TYPE'),
                                 comm_payer=lendDb.get_byName('PAYER'),
                                 comm_payee=lendDb.get_byName('PAYEE'),
                                 payee_account=lendDb.get_byName('PAYEE_NO'),
                                 vou_type=lendDb.get_byName('PAY_VOUCHER_TYPE'),
                                 vou_no=lendDb.get_byName('VOUCHER_NO'),
                                 bank_type=lendDb.get_byName('PAYEE_BANK_TYPE'), 
                                 bank_no=lendDb.get_byName('PAYEE_BANK_NO'),
                                 bank_name=lendDb.get_byName('CREDIT_INPUT_BANK_NAME'),
                                 purpose_type=lendDb.get_byName('LOAN_USAGE')
                            ) 
                self.session.add(payment)            
                lendDb.get_next() 
            conDb.get_next()

        conDb.close()
        lendDb.close()
        self.session.commit() 
       
    def load_payment(self):   
        conDb= DB2()
        conDb.db_conn()
        lendDb= DB2()
        lendDb.db_conn()
        i = 0

        log.debug("执行 insert loan_base**********")
        conDb.exesql("select * from CON_BASE","CON_BASE")
        while(conDb.row):
            i = i+1
            log.debug(i) 
            con_id=conDb.get_byName('CON_ID')
            lendDb.exesql("select * from LOAN_BASE  where LOAN_BASE.CON_ID = '%s'"%(con_id),"LOAN_BASE")   
            debt=None
            while(lendDb.row):
                con = self.session.query(LendContract).filter(LendContract.contract_no == con_id).first()
                debt =Debt(contract_id=con.contract_id,
                           begin_date=lendDb.get_byName('ISSUE_DATE'),
                           end_date=lendDb.get_byName('DUE_DATE'),
                           amount=lendDb.get_byName('LOAN_AMOUNT'),
                           is_credit_card=lendDb.get_byName('CARD_CREDIT'),
                           extend_date=lendDb.get_byName('EXTEND_DATE'),
                           extend_time=lendDb.get_byName('EXTEND_TIME'),
                            ) 
                lendDb.get_next() 
                self.session.add(debt)
            app_id=conDb.get_byName('APP_ID')
            lendDb.exesql("select * from FUNDFLOW  where FUNDFLOW.APP_ID = '%s'"%(app_id),"FUNDFLOW")   
            payment=None
            while(lendDb.row):
                payment =Payment(debt=debt,
                                 paydetail=lendDb.get_byName('TRADE_CONTENT'),
                                 repayment_from=lendDb.get_byName('RETURN_SOURCE'),
                                 payment_method=lendDb.get_byName('PAYMENT_TYPE'),
                                 amount=lendDb.get_byName('PAYMENT_AMOUNT'),
                                 settle_type=lendDb.get_byName('BALANCE_TYPE'),
                                 comm_payer=lendDb.get_byName('PAYER'),
                                 comm_payee=lendDb.get_byName('PAYEE'),
                                 payee_account=lendDb.get_byName('PAYEE_NO'),
                                 vou_type=lendDb.get_byName('PAY_VOUCHER_TYPE'),
                                 vou_no=lendDb.get_byName('VOUCHER_NO'),
                                 bank_type=lendDb.get_byName('PAYEE_BANK_TYPE'), 
                                 bank_no=lendDb.get_byName('PAYEE_BANK_NO'),
                                 bank_name=lendDb.get_byName('CREDIT_INPUT_BANK_NAME'),
                                 purpose_type=lendDb.get_byName('LOAN_USAGE')
                            ) 
                self.session.add(payment)            
                lendDb.get_next() 
            conDb.get_next()

        conDb.close()
        lendDb.close()

        self.session.commit() 
               
    def load_application(self):   
        lendDb= DB2()
        lendDb.db_conn()
        appDb = DB2()
        appDb.db_conn()

        db2= DB2()
        db2.db_conn()
        gtyDb = DB2()
        gtyDb.db_conn()
        i = 0
        gtyDb.exesql("select * from GTY_BASE ","GTY_BASE")
        while(gtyDb.row):  
            i = i+1
            log.debug(i)
            app_id=gtyDb.get_byName('BRW_APP_ID')
            pledge_type = gtyDb.get_byName('PLEDGE_TYPE')
            gty_id=gtyDb.get_byName('GTY_ID')
            gty=None
            #判断担保物类型 分别查各类表
            if pledge_type =='11':
                log.debug("执行 人民币存款**********")
                db2.exesql("select * from GTY_PAWN_SAVING where GTY_PAWN_SAVING.GTY_ID = '%s' "%(gty_id),"GTY_PAWN_SAVING")
                while(db2.row):
                    gty = PawnSaving(saving_type=db2.get_byName('SAVING_TYPE'),
                                        account_name=db2.get_byName('SAVING_ACC_ID'),
                                        saving_amount=db2.get_byName('SAVING_AMOUNT'))
                    db2.get_next()
            elif pledge_type =='10' :
                log.debug("执行 存单**********")
                db2.exesql("select * from GTY_PAWN_STUB where GTY_PAWN_STUB.GTY_ID = '%s' "%(gty_id),"GTY_PAWN_STUB")
                while(db2.row):
                    if db2.get_byName('STUB_ISSUE_TYPE') == 1:
                        gty = PawnPerStub(stub_amount=db2.get_byName('STUB_AMOUNT'),
                                           stub_no=db2.get_byName('STUB_NO'))
                        #TODO                   
                    else:
                        gty=PawnStub(stub_amount=db2.get_byName('STUB_AMOUNT'),
                                      stub_no=db2.get_byName('STUB_NO')) 
                        #TODO               
                    db2.get_next()
            elif pledge_type == '23':
                log.debug("执行应收账款**********")
                db2.exesql("select * from GTY_PAWN_ACC_REC where GTY_PAWN_ACC_REC.GTY_ID = '%s' "%(gty_id),"GTY_PAWN_ACC_REC")
                while(db2.row):
                    gty=PawnAccRec(buyer_name=db2.get_byName('BUYER_NAME'),
                                 due_date=db2.get_byName('ACC_REC_DUE_DATE'),
                                 acc_rec_amount=db2.get_byName('ACC_REC_AMOUNT') ) 
                    #TODO             
                    db2.get_next()
            elif pledge_type =='25' :     
                log.debug("执行承兑汇票**********")
                db2.exesql("select * from  GTY_PAWN_ACCP where GTY_PAWN_ACCP.GTY_ID = '%s' "%(gty_id),"GTY_PAWN_ACCP")
                while(db2.row):
                    gty=PawnAccp(bill_no=db2.get_byName('BILL_NO'))
                    #TODO
                    db2.get_next()
            elif pledge_type =='27' :
                log.debug("执行其他质押物**********")
                db2.exesql("select * from  GTY_PAWN_OTHER where GTY_PAWN_OTHER.GTY_ID = '%s'"%(gty_id),"GTY_PAWN_OTHER")
                while(db2.row):
                    gty=PawnOther(pawn_name=db2.get_byName('PAWN_NAME'))
                    #TODO
                    db2.get_next()
            elif pledge_type =='01' : 
                log.debug("执行抵押-房产表**********")
                db2.exesql("select * from GTY_MRGE_BLDG where GTY_MRGE_BLDG.GTY_ID = '%s' "%(gty_id),"GTY_MRGE_BLDG")
                while(db2.row):
                    gty=MrgeBuilding(bldg_address=db2.get_byName('BLDG_ADDRESS'))
                    #TODO
                    db2.get_next()
    
            elif pledge_type =='05' : 
                log.debug("执行抵押其他表**********")
                db2.exesql("select * from GTY_MRGE_OTHER where GTY_MRGE_OTHER.GTY_ID = '%s' "%(gty_id),"GTY_MRGE_OTHER")
                while(db2.row):
                    gty=MrgeOther(mrge_name=db2.get_byName('MRGE_BRAND'))
                    #TODO
                    db2.get_next()
                #TODO  pledge_type =='' 为保证担保，，不知数据库有无表，    
                #TODO  GTY_MRGE_LAND,      担保抵押-土地抵押表
                #TODO  GTY_MRGE_VCH,       担保抵押-车辆抵押表
                #TODO  GTY_MRGE_EQP,       担保抵押-设备抵押表
                #TODO  GTY_MRGE_OTHER,     担保抵押-其它抵押表

            lendDb.exesql("select * from APP_RPT where APP_RPT.APP_ID= '%s' "%(app_id),"APP_RPT")
            report =None
            while(lendDb.row):
                report =SurveyReport(from_date=lendDb.get_byName('CHECK_DATE'),
                                     report_content=lendDb.get_byName('CHECK_CONTENT')
                                     )
                lendDb.get_next()
            appDb.exesql("select * from APP_BASE where APP_BASE.APP_ID= '%s' "%(app_id),"APP_BASE")
            a=None
            biz_type = None
            while(appDb.row):
                cust_no=appDb.get_byName('CUS_ID')
                biz_type = appDb.get_byName('BIZ_TYPE') 
                cust=self.session.query(Customer).join(Party,Party.id==Customer.party_id).filter(Party.no==cust_no).first()
                a = Application(customer_id=cust.role_id,
                                product_code=appDb.get_byName('BIZ_TYPE'),
                                survey_report=report)

                # TODO transaction 需完善
                transaction=ApplicationTransaction(application=a,amount=appDb.get_byName('APP_AMOUNT'),
                                                   transaction_name=u'%s的贷款申请'%(cust.party.name))
                self.session.add(transaction)                    
                appDb.get_next()

            if biz_type=='023' or biz_type=='007':
                appDb.exesql("select * from APPC_DISC_BILL_LST where APPC_DISC_BILL_LST.APP_ID= '%s' "%(app_id),"APPC_DISC_BILL_LST")
                while(appDb.row):
                    product_type=None
                    if biz_type=='023':
                        product_type=u'贴现'    
                    elif biz_type=='007':
                        product_type=u'签发'
                    bill =Bill_message(application=a,
                                       bill_kill=appDb.get_by_name('BILL_TYPE'),
                                       product_type=product_type,
                                       bill_type=appDb.get_by_name('BILL_CATEGORY'),
                                       bill_no=appDb.get_by_name('BILL_AMOUNT'),
                                       bill_from_date=appDb.get_by_name('DISC_BILL_DATE'),
                                       bill_due_date=appDb.get_by_name('BILL_DUE_DATE'),
                                       bill_person=appDb.get_by_name('ISSUE_NAME'),
                                       payee=appDb.get_by_name('RECEIVER_NAME'),
                                       bill_start_branch=appDb.get_by_name('ISSUE_BANK_NAME'),
                                       discount_date=appDb.get_by_name('DISC_ISSUE_DATE'),
                                       discount_rate=appDb.get_by_name('DISCOUNT_IR'),
                                       proposer_acc=appDb.get_by_name('RECEIVER_ACC_ID'),
                                       use_date=appDb.get_by_name('INTRANSIT_DAYS'),
                                       discount_interest=appDb.get_by_name('DISCOUNT_ACCRUAL'),
                                       discount_type=appDb.get_by_name('DISCOUNT_TYPE'),
                                       proposer_start_branch=appDb.get_by_name('RECEIVER_BANK'),
                                       bill_person_acc=appDb.get_by_name('ISSUE_ACC_ID'),
                                       more_bill_no=appDb.get_by_name('ADD_TAX_INVOICE_NN'),
                                       accptor_no=appDb.get_by_name('ACCP_ID'),
                                       deal_amount=appDb.get_by_name('TRADE_AMOUNT'),
                                       deal_no=appDb.get_by_name('TRADE_NO'),
                                       deal_date=appDb.get_by_name('TRADE_DATE')
                                      )  
                    appDb.get_next() 
                    self.session.add(bill)
            gty_info = GuaranteeInfo(application=a,gty_amount=gtyDb.get_byName('PLEDGE_CONF_VALUE'))        
            gty=GuaranteeRelation(guarantee=gty,guarantee_info=gty_info)          
            self.session.add(gty) 
            gtyDb.get_next()
         

        db2.close()
        gtyDb.close()
        appDb.close()
        lendDb.close()
        self.session.commit() 

    def test_main(self):
        #self.load_con()
        self.load_application()

    def tearDown(self):
        log.debug("Over")

