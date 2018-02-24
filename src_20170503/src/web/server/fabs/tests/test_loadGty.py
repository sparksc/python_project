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
from ..model.credit import *
from ..model.application import *
from ..model.common import *
from ..model.contract import *
from ..model.guarantee import *
from ..database.logger import  log
from db2_utils import DB2
log = logging.getLogger()
import ibm_db
#log = logging.getLogger()
#log.basicConfig(level=logging.DEBUG)

conn = ibm_db.connect('HOSTNAME=192.168.10.190;PORT=60000;DATABASE=creditdb;UID=whxd;PWD=pass;','','')

class TestLoadInfo(unittest.TestCase):

    def setUp(self):
        log.debug("执行setup")
        self.session=simple_session()

    def load_gua(self,sql):      
        saving_list=[]
        result = ibm_db.exec_immediate(conn, sql)
        cols = ibm_db.num_fields(result)
        row = ibm_db.fetch_both(result)
        while ( row ):
            saving = {}
            for i in range(0, cols):
               field = ibm_db.field_name(result, i)
               value = row[ibm_db.field_name(result, i)]
               if type(value) in [str,unicode]:
                      value = value.strip()
               saving[field]=value   
            saving_list.append(saving)
            row = ibm_db.fetch_both(result)

        return saving_list

    def load_saving(self):
        log.debug('saving')
        saving_list= self.load_gua('select * from GTY_BASE ,GTY_PAWN_SAVING,GTY_REL where GTY_REL.APP_ID = GTY_BASE.BRW_APP_ID and  GTY_PAWN_SAVING.GTY_ID = GTY_BASE.GTY_ID')
        for saving in saving_list:
            gty = PawnSaving(saving_type=saving.get('SAVING_TYPE'),
                             account_name=saving.get('SAVING_ACC_ID'),
                             saving_amount=saving.get('SAVING_AMOUNT'),
                             pledge_type=u'质押-账户资金',
                             gty_method=saving.get('GTY_METHOD'),
                             gty_ct='人民币',
                             gty_amout=saving.get('GTY_AMOUT'),
                             brw_cus_id=saving.get('BRW_CUS_ID'),
                             brw_cus_name=saving.get('BRW_CUS_NAME'),
                             brw_cus_type=saving.get('BRW_CUS_TYPE'),
                             gty_cus_id=saving.get('GTY_CUS_ID'),
                             gty_cus_name=saving.get('GTY_CUS_NAME'),
                             gty_cus_type=saving.get('GTY_CUS_TYPE'),
                             bfirst_gty=saving.get('BFIRST_GTY'),
                             bboard_appr=saving.get('BBOARD_APPR'),
                             gty_due_date=saving.get('GTY_DUE_DATE'),
                             ins_type=saving.get('INS_TYPE'),
                             ins_id=saving.get('INS_ID'),
                             ins_due_date=saving.get('INS_DUE_DATE'),
                             reg_org_id=saving.get('REG_ORG_ID'),
                             reg_by=saving.get('REG_BY'),
                             reg_date=saving.get('REG_DATE'),
                             updated_time=saving.get('UPDATED_TIME'),
                             gty_status=saving.get('GTY_STATUS'),
                             insp1_id=saving.get('INSP1_ID'),
                             insp2_id=saving.get('INSP2_ID'),
                             gty_total=saving.get('GTY_TOTAL'))
            a=self.session.query(Application).filter(Application.brw_app_id==saving.get('BRW_APP_ID')).first()
            gty_con=Contract(contract_no=saving.get('CON_GTY_ID'))
            if a:
                a_id = a.id
            else:
                a_id =None
            gty_info = GuaranteeInfo(application_id=a_id,
                                     gty_amount=saving.get('GTY_AMOUT'),
                                     gty_customer_name=saving.get('GTY_CUS_NAME'),
                                     gty_method=u'质押'
                                     )        
            gty_rel=GuaranteeContractRelation(contract=gty_con,guarantee_info=gty_info) 
            gty=GuaranteeRelation(guarantee=gty,guarantee_info=gty_info)     
            self.session.add(gty) 
            self.session.add(gty_rel) 
        self.session.commit()

    def load_stub(self):
        log.debug('stub')
        saving_list= self.load_gua('select * from GTY_BASE ,GTY_PAWN_STUB,GTY_REL where GTY_PAWN_STUB.GTY_ID = GTY_BASE.GTY_ID and GTY_REL.APP_ID = GTY_BASE.BRW_APP_ID' )
        for saving in saving_list:
            gty = PawnPerStub(stub_amount=saving.get('STUB_AMOUNT'),
                                          stub_no=saving.get('STUB_NO'),
                                          stub_type=saving.get('STUB_TYPE'),
                                          stub_ct='人民币',
                                          exchange_rate=saving.get('EXCHANGE_RATE'),
                                          beg_date=saving.get('INTEREST_BEG_DATE'),
                                          stub_owner=saving.get('KEEPER'),
                                          stop_payment_date=saving.get('STOP_PAYMENT_DATE'),
                                          stop_payment_status=saving.get('STOP_PAYMENT_STATUS'),
                                          stop_payment_user=saving.get('STOP_PAYMENT_USER'),
                                          stub_account_no=saving.get('STUB_ACCOUNT_NO'),
                                          stub_voucher_type=saving.get('STUB_VOUCHER_TYPE'),
                                          cancel_stop_payment_date=saving.get('CANCEL_STOP_PAYMENT_DATE'),
                                          cancel_stop_payment_user=saving.get('CANCEL_STOP_PAYMENT_USER'),
                                          pledge_type=u'质押-个人定期存单',
                                          gty_method=saving.get('GTY_METHOD'),
                                          gty_ct='人民币',
                                          gty_amout=saving.get('GTY_AMOUT'),
                                          brw_cus_id=saving.get('BRW_CUS_ID'),
                                          brw_cus_name=saving.get('BRW_CUS_NAME'),
                                          brw_cus_type=saving.get('BRW_CUS_TYPE'),
                                          gty_cus_id=saving.get('GTY_CUS_ID'),
                                          gty_cus_name=saving.get('GTY_CUS_NAME'),
                                          gty_cus_type=saving.get('GTY_CUS_TYPE'),
                                          bfirst_gty=saving.get('BFIRST_GTY'),
                                          bboard_appr=saving.get('BBOARD_APPR'),
                                          gty_due_date=saving.get('GTY_DUE_DATE'),
                                          ins_type=saving.get('INS_TYPE'),
                                          ins_id=saving.get('INS_ID'),
                                          ins_due_date=saving.get('INS_DUE_DATE'),
                                          reg_org_id=saving.get('REG_ORG_ID'),
                                          reg_by=saving.get('REG_BY'),
                                          reg_date=saving.get('REG_DATE'),
                                          updated_time=saving.get('UPDATED_TIME'),
                                          gty_status=saving.get('GTY_STATUS'),
                                          insp1_id=saving.get('INSP1_ID'),
                                          insp2_id=saving.get('INSP2_ID'),
                                          gty_total=saving.get('GTY_TOTAL'))
                                          
            a=self.session.query(Application).filter(Application.brw_app_id==saving.get('BRW_APP_ID')).first()
            gty_con=Contract(contract_no=saving.get('CON_GTY_ID'))
            if a:
                a_id = a.id
            else:
                a_id =None
            gty_info = GuaranteeInfo(application_id=a_id,
                                     gty_amount=saving.get('GTY_AMOUT'),
                                     gty_customer_name=saving.get('GTY_CUS_NAME'),
                                     gty_method=u'质押'
                                     )        
            gty_rel=GuaranteeContractRelation(contract=gty_con,guarantee_info=gty_info) 
            gty=GuaranteeRelation(guarantee=gty,guarantee_info=gty_info)     
            self.session.add(gty) 
            self.session.add(gty_rel) 
        self.session.commit()

    def load_rec(self):
        log.debug('rec')
        saving_list= self.load_gua('select * from GTY_BASE ,GTY_PAWN_ACC_REC,GTY_REL where GTY_PAWN_ACC_REC.GTY_ID = GTY_BASE.GTY_ID and GTY_REL.APP_ID = GTY_BASE.BRW_APP_ID' )
        for saving in saving_list:
            gty=PawnAccRec(buyer_name=saving.get('BUYER_NAME'),
                           due_date=saving.get('ACC_REC_DUE_DATE'),
                           acc_rec_amount=saving.get('ACC_REC_AMOUNT'),
                           ct='人民币',
                           pledge_type=u'质押-应收账款',
                           gty_method=saving.get('GTY_METHOD'),
                           gty_ct='人民币',
                           gty_amout=saving.get('GTY_AMOUT'),
                           brw_cus_id=saving.get('BRW_CUS_ID'),
                           brw_cus_name=saving.get('BRW_CUS_NAME'),
                           brw_cus_type=saving.get('BRW_CUS_TYPE'),
                           gty_cus_id=saving.get('GTY_CUS_ID'),
                           gty_cus_name=saving.get('GTY_CUS_NAME'),
                           gty_cus_type=saving.get('GTY_CUS_TYPE'),
                           bfirst_gty=saving.get('BFIRST_GTY'),
                           bboard_appr=saving.get('BBOARD_APPR'),
                           gty_due_date=saving.get('GTY_DUE_DATE'),
                           ins_type=saving.get('INS_TYPE'),
                           ins_id=saving.get('INS_ID'),
                           ins_due_date=saving.get('INS_DUE_DATE'),
                           reg_org_id=saving.get('REG_ORG_ID'),
                           reg_by=saving.get('REG_BY'),
                           reg_date=saving.get('REG_DATE'),
                           updated_time=saving.get('UPDATED_TIME'),
                           gty_status=saving.get('GTY_STATUS'),
                           insp1_id=saving.get('INSP1_ID'),
                           insp2_id=saving.get('INSP2_ID'),
                           gty_total=saving.get('GTY_TOTAL'))

            a=self.session.query(Application).filter(Application.brw_app_id==saving.get('BRW_APP_ID')).first()
            gty_con=Contract(contract_no=saving.get('CON_GTY_ID'))
            if a:
                a_id = a.id
            else:
                a_id =None
            gty_info = GuaranteeInfo(application_id=a_id,
                                     gty_amount=saving.get('GTY_AMOUT'),
                                     gty_customer_name=saving.get('GTY_CUS_NAME'),
                                     gty_method=u'质押'
                                     )        
            gty_rel=GuaranteeContractRelation(contract=gty_con,guarantee_info=gty_info) 
            gty=GuaranteeRelation(guarantee=gty,guarantee_info=gty_info)     
            self.session.add(gty) 
            self.session.add(gty_rel) 

        self.session.commit()

    def load_accp(self):
        log.debug('accp') 
        saving_list= self.load_gua('select * from GTY_BASE ,GTY_PAWN_ACCP,GTY_REL where GTY_PAWN_ACCP.GTY_ID = GTY_BASE.GTY_ID and GTY_REL.APP_ID = GTY_BASE.BRW_APP_ID' )
        for saving in saving_list:
            gty=PawnAccp(bill_no=saving.get('BILL_NO'),
                         accp_bank_name=saving.get('ACCP_BANK_NAME'),
                         accp_bank_class=saving.get('ACCP_BANK_CLASS'),
                         accp_gty_amount=saving.get('BILL_AMOUNT'),
                         issue_date=saving.get('ISSUE_DATE'),
                         due_date=saving.get('DUE_DATE'),
                         breal_trade=saving.get('BREAL_TRADE'),
                         add_tax_invoice_no=saving.get('ADD_TAX_INVOICE_NO'),
                         bill_source=saving.get('BILL_SOURCE'),
                         check_method=saving.get('CHECK_METHOD'),
                         pledge_type='质押-银行承兑汇票',
                         gty_method=saving.get('GTY_METHOD'),
                         gty_amout=saving.get('GTY_AMOUT'),
                         brw_cus_id=saving.get('BRW_CUS_ID'),
                         brw_cus_name=saving.get('BRW_CUS_NAME'),
                         brw_cus_type=saving.get('BRW_CUS_TYPE'),
                         gty_cus_id=saving.get('GTY_CUS_ID'),
                         gty_cus_name=saving.get('GTY_CUS_NAME'),
                         gty_cus_type=saving.get('GTY_CUS_TYPE'),
                         bfirst_gty=saving.get('BFIRST_GTY'),
                         bboard_appr=saving.get('BBOARD_APPR'),
                         gty_due_date=saving.get('GTY_DUE_DATE'),
                         ins_type=saving.get('INS_TYPE'),
                         ins_id=saving.get('INS_ID'),
                         ins_due_date=saving.get('INS_DUE_DATE'),
                         reg_org_id=saving.get('REG_ORG_ID'),
                         reg_by=saving.get('REG_BY'),
                         reg_date=saving.get('REG_DATE'),
                         updated_time=saving.get('UPDATED_TIME'),
                         gty_status=saving.get('GTY_STATUS'),
                         insp1_id=saving.get('INSP1_ID'),
                         insp2_id=saving.get('INSP2_ID'),
                         gty_total=saving.get('GTY_TOTAL'))

            a=self.session.query(Application).filter(Application.brw_app_id==saving.get('BRW_APP_ID')).first()
            gty_con=Contract(contract_no=saving.get('CON_GTY_ID'))
            if a:
                a_id = a.id
            else:
                a_id =None
            gty_info = GuaranteeInfo(application_id=a_id,
                                     gty_amount=saving.get('GTY_AMOUT'),
                                     gty_customer_name=saving.get('GTY_CUS_NAME'),
                                     gty_method=u'质押'
                                     )        
            gty_rel=GuaranteeContractRelation(contract=gty_con,guarantee_info=gty_info) 
            gty=GuaranteeRelation(guarantee=gty,guarantee_info=gty_info)     
            self.session.add(gty) 
            self.session.add(gty_rel) 
        self.session.commit()       

    def load_pawn_other(self):
        log.debug('other')
        saving_list= self.load_gua('select * from GTY_BASE ,GTY_PAWN_OTHER,GTY_REL where GTY_PAWN_OTHER.GTY_ID = GTY_BASE.GTY_ID and GTY_REL.APP_ID = GTY_BASE.BRW_APP_ID' )
        for saving in saving_list:
            gty=PawnOther(pawn_name=saving.get('PAWN_NAME'),
                          pawn_type=saving.get('PAWN_TYPE'),
                          pawn_qty=saving.get('PAWN_QTY'),
                          beg_date=saving.get('BOUGHT_DATE'),
                          due_date=saving.get('DUE_DATE'),
                          pawn_ct='人民币',
                          pawn_amount=saving.get('ORI_PAWN_VALUE'),
                          pledge_type=u'质押-其他',
                          gty_method=saving.get('GTY_METHOD'),
                          gty_ct='人民币',
                          gty_amout=saving.get('GTY_AMOUT'),
                          brw_cus_id=saving.get('BRW_CUS_ID'),
                          brw_cus_name=saving.get('BRW_CUS_NAME'),
                          brw_cus_type=saving.get('BRW_CUS_TYPE'),
                          gty_cus_id=saving.get('GTY_CUS_ID'),
                          gty_cus_name=saving.get('GTY_CUS_NAME'),
                          gty_cus_type=saving.get('GTY_CUS_TYPE'),
                          bfirst_gty=saving.get('BFIRST_GTY'),
                          bboard_appr=saving.get('BBOARD_APPR'),
                          gty_due_date=saving.get('GTY_DUE_DATE'),
                          ins_type=saving.get('INS_TYPE'),
                          ins_id=saving.get('INS_ID'),
                          ins_due_date=saving.get('INS_DUE_DATE'),
                          reg_org_id=saving.get('REG_ORG_ID'),
                          reg_by=saving.get('REG_BY'),
                          reg_date=saving.get('REG_DATE'),
                          updated_time=saving.get('UPDATED_TIME'),
                          gty_status=saving.get('GTY_STATUS'),
                          insp1_id=saving.get('INSP1_ID'),
                          insp2_id=saving.get('INSP2_ID'),
                          gty_total=saving.get('GTY_TOTAL'))

            a=self.session.query(Application).filter(Application.brw_app_id==saving.get('BRW_APP_ID')).first()
            gty_con=Contract(contract_no=saving.get('CON_GTY_ID'))
            if a:
                a_id = a.id
            else:
                a_id =None
            gty_info = GuaranteeInfo(application_id=a_id,
                                     gty_amount=saving.get('GTY_AMOUT'),
                                     gty_customer_name=saving.get('GTY_CUS_NAME'),
                                     gty_method=u'质押'
                                     )        
            gty_rel=GuaranteeContractRelation(contract=gty_con,guarantee_info=gty_info) 
            gty=GuaranteeRelation(guarantee=gty,guarantee_info=gty_info)     
            self.session.add(gty) 
            self.session.add(gty_rel) 

        self.session.commit()

    def load_bldg(self):
        log.debug('bldg')
        saving_list= self.load_gua('select * from GTY_BASE ,GTY_MRGE_BLDG,GTY_REL where GTY_MRGE_BLDG.GTY_ID = GTY_BASE.GTY_ID and GTY_REL.APP_ID = GTY_BASE.BRW_APP_ID' )
        for saving in saving_list:
            gty=MrgeBuilding(bldg_address=saving.get('BLDG_ADDRESS'),
                             bldg_type=saving.get('BLDG_TYPE'),
                             bldg_district=saving.get('BLDG_DISTRICT'),
                             bcommunity=saving.get('BCOMMUNITY'),
                             comm_name=saving.get('COMM_NAME'),
                             bldg_area=saving.get('BLDG_AERA'),
                             bldg_struct=saving.get('BLDG_STRUCT'),
                             belevator=saving.get('BELEVATOR'),
                             land_obtain_method=saving.get('LAND_OBTAIN_METHOD'),
                             rest_use_year=saving.get('REST_USE_YEAR'),
                             bldg_contract_no=saving.get('BLDG_CONTRACT_NO'),
                             bldg_cert_no=saving.get('BLDG_CERT_NO'),
                             land_cert_no=saving.get('LAND_CERT_NO'),
                             bldg_fin_date=saving.get('BLDG_FIN_DATE'),
                             first_bought_date=saving.get('FIRST_BOUGHT_DATE'),
                             org_unit_price=saving.get('ORG_UNIT_PRICE'),
                             bldg_use_status=saving.get('BLDG_USE_STATUS'),
                             pledge_type=u'抵押-房屋所有权',
                             gty_method=saving.get('GTY_METHOD'),
                             gty_ct='人民币',
                             gty_amout=saving.get('GTY_AMOUT'),
                             brw_cus_id=saving.get('BRW_CUS_ID'),
                             brw_cus_name=saving.get('BRW_CUS_NAME'),
                             brw_cus_type=saving.get('BRW_CUS_TYPE'),
                             gty_cus_id=saving.get('GTY_CUS_ID'),
                             gty_cus_name=saving.get('GTY_CUS_NAME'),
                             gty_cus_type=saving.get('GTY_CUS_TYPE'),
                             bfirst_gty=saving.get('BFIRST_GTY'),
                             bboard_appr=saving.get('BBOARD_APPR'),
                             gty_due_date=saving.get('GTY_DUE_DATE'),
                             ins_type=saving.get('INS_TYPE'),
                             ins_id=saving.get('INS_ID'),
                             ins_due_date=saving.get('INS_DUE_DATE'),
                             reg_org_id=saving.get('REG_ORG_ID'),
                             reg_by=saving.get('REG_BY'),
                             reg_date=saving.get('REG_DATE'),
                             updated_time=saving.get('UPDATED_TIME'),
                             gty_status=saving.get('GTY_STATUS'),
                             insp1_id=saving.get('INSP1_ID'),
                             insp2_id=saving.get('INSP2_ID'),
                             gty_total=saving.get('GTY_TOTAL'))

            a=self.session.query(Application).filter(Application.brw_app_id==saving.get('BRW_APP_ID')).first()
            gty_con=Contract(contract_no=saving.get('CON_GTY_ID'))
            if a:
                a_id = a.id
            else:
                a_id =None
            gty_info = GuaranteeInfo(application_id=a_id,
                                     gty_amount=saving.get('GTY_AMOUT'),
                                     gty_customer_name=saving.get('GTY_CUS_NAME'),
                                     gty_method='抵押'
                                     )        
            gty_rel=GuaranteeContractRelation(contract=gty_con,guarantee_info=gty_info) 
            gty=GuaranteeRelation(guarantee=gty,guarantee_info=gty_info)     
            self.session.add(gty) 
            self.session.add(gty_rel) 
        self.session.commit()

    def load_land(self):
        log.debug('land')
        saving_list= self.load_gua('select * from GTY_BASE ,GTY_MRGE_LAND,GTY_REL where GTY_MRGE_LAND.GTY_ID = GTY_BASE.GTY_ID and GTY_REL.APP_ID = GTY_BASE.BRW_APP_ID' )
        for saving in saving_list:
            gty = MrgeLand(land_district=saving.get('LAND_DISTRICT'),
                           land_address=saving.get('LAND_ADDRESS'),
                           land_area=saving.get('LAND_AREA'),
                           land_obtain_method=saving.get('LAND_OBTAIN_METHOD'),
                           land_use_type=saving.get('LAND_USE_TYPE'),
                           land_class=saving.get('LAND_CLASS'),
                           bought_date=saving.get('BOUGHT_DATE'),
                           sale_value=saving.get('SALE_VALUE'),
                           bfin_pay=saving.get('BFIn_PAY'),
                           rest_use_year=saving.get('REST_USE_YEAR'),
                           land_status=saving.get('LAND_STATUS'),
                           bbuilding=saving.get('BBUILDING'),
                           land_use_status=saving.get('LAND_USE_STATUS'),
                           land_cert_no=saving.get('Land_Cert_No'),
                           pledge_type=u'抵押-土地使用权',
                           gty_method=saving.get('GTY_METHOD'),
                           gty_ct='人民币',
                           gty_amout=saving.get('GTY_AMOUT'),
                           brw_cus_id=saving.get('BRW_CUS_ID'),
                           brw_cus_name=saving.get('BRW_CUS_NAME'),
                           brw_cus_type=saving.get('BRW_CUS_TYPE'),
                           gty_cus_id=saving.get('GTY_CUS_ID'),
                           gty_cus_name=saving.get('GTY_CUS_NAME'),
                           gty_cus_type=saving.get('GTY_CUS_TYPE'),
                           bfirst_gty=saving.get('BFIRST_GTY'),
                           bboard_appr=saving.get('BBOARD_APPR'),
                           gty_due_date=saving.get('GTY_DUE_DATE'),
                           ins_type=saving.get('INS_TYPE'),
                           ins_id=saving.get('INS_ID'),
                           ins_due_date=saving.get('INS_DUE_DATE'),
                           reg_org_id=saving.get('REG_ORG_ID'),
                           reg_by=saving.get('REG_BY'),
                           reg_date=saving.get('REG_DATE'),
                           updated_time=saving.get('UPDATED_TIME'),
                           gty_status=saving.get('GTY_STATUS'),
                           insp1_id=saving.get('INSP1_ID'),
                           insp2_id=saving.get('INSP2_ID'),
                           gty_total=saving.get('GTY_TOTAL'))

            a=self.session.query(Application).filter(Application.brw_app_id==saving.get('BRW_APP_ID')).first()
            gty_con=Contract(contract_no=saving.get('CON_GTY_ID'))
            if a:
                a_id = a.id
            else:
                a_id =None
            gty_info = GuaranteeInfo(application_id=a_id,
                                     gty_amount=saving.get('GTY_AMOUT'),
                                     gty_customer_name=saving.get('GTY_CUS_NAME'),
                                     gty_method='抵押'
                                     )        
            gty_rel=GuaranteeContractRelation(contract=gty_con,guarantee_info=gty_info) 
            gty=GuaranteeRelation(guarantee=gty,guarantee_info=gty_info)     
            self.session.add(gty) 
            self.session.add(gty_rel) 
        self.session.commit()

    def vch(self):
        log.debug('vch')
        saving_list= self.load_gua('select * from GTY_BASE ,GTY_MRGE_VCH,GTY_REL where GTY_MRGE_VCH.GTY_ID = GTY_BASE.GTY_ID and GTY_REL.APP_ID = GTY_BASE.BRW_APP_ID' )
        for saving in saving_list:
            gty = MrgeVch(vch_type=saving.get('VCH_TYPE'),
                          vch_brand=saving.get('VCH_BRAND'),
                          vch_model=saving.get('VCH_MODEL'),
                          vch_id=saving.get('VCH_ID'),
                          engine_id=saving.get('ENGINEA_ID'),
                          frame_id=saving.get('FRAME_ID'),
                          milage=saving.get('MILAGE'),
                          vch_status=saving.get('VCH_STATUS'),
                          bought_price=saving.get('BOUGHT_PRICE'),
                          pledge_type=u'抵押-交通工具',
                          gty_method=saving.get('GTY_METHOD'),
                          gty_ct='人民币',
                          gty_amout=saving.get('GTY_AMOUT'),
                          brw_cus_id=saving.get('BRW_CUS_ID'),
                          brw_cus_name=saving.get('BRW_CUS_NAME'),
                          brw_cus_type=saving.get('BRW_CUS_TYPE'),
                          gty_cus_id=saving.get('GTY_CUS_ID'),
                          gty_cus_name=saving.get('GTY_CUS_NAME'),
                          gty_cus_type=saving.get('GTY_CUS_TYPE'),
                          bfirst_gty=saving.get('BFIRST_GTY'),
                          bboard_appr=saving.get('BBOARD_APPR'),
                          gty_due_date=saving.get('GTY_DUE_DATE'),
                          ins_type=saving.get('INS_TYPE'),
                          ins_id=saving.get('INS_ID'),
                          ins_due_date=saving.get('INS_DUE_DATE'),
                          reg_org_id=saving.get('REG_ORG_ID'),
                          reg_by=saving.get('REG_BY'),
                          reg_date=saving.get('REG_DATE'),
                          updated_time=saving.get('UPDATED_TIME'),
                          gty_status=saving.get('GTY_STATUS'),
                          insp1_id=saving.get('INSP1_ID'),
                          insp2_id=saving.get('INSP2_ID'),
                          gty_total=saving.get('GTY_TOTAL'))

            a=self.session.query(Application).filter(Application.brw_app_id==saving.get('BRW_APP_ID')).first()
            gty_con=Contract(contract_no=saving.get('CON_GTY_ID'))
            if a:
                a_id = a.id
            else:
                a_id =None
            gty_info = GuaranteeInfo(application_id=a_id,
                                     gty_amount=saving.get('GTY_AMOUT'),
                                     gty_customer_name=saving.get('GTY_CUS_NAME'),
                                     gty_method='抵押'
                                     )        

            gty_rel=GuaranteeContractRelation(contract=gty_con,guarantee_info=gty_info) 
            gty=GuaranteeRelation(guarantee=gty,guarantee_info=gty_info)     
            self.session.add(gty) 
            self.session.add(gty_rel) 
        self.session.commit()
    def eqp(self):
        log.debug('eqp')
        saving_list= self.load_gua('select * from GTY_BASE ,GTY_MRGE_EQP,GTY_REL where GTY_MRGE_EQP.GTY_ID = GTY_BASE.GTY_ID and GTY_REL.APP_ID = GTY_BASE.BRW_APP_ID' )
        for saving in saving_list:
            gty = MrgeEqp(eqp_brand=saving.get('EQP_BRAND'),
                          eqp_model=saving.get('EQP_MODEL'),
                          eqp_amount=saving.get('EQP_AMOUNT'),
                          invoice_no=saving.get('INVOICE_NO'),
                          bought_date=saving.get('BOUGHT_DATE'),
                          bought_price=saving.get('BOUGHT_PRICE'),
                          eqp_use_status=saving.get('EQP_USE_STATUS'),
                          eqp_location=saving.get('EQP_LOCATION'),
                          pledge_type=u'抵押-设备',
                          gty_method=saving.get('GTY_METHOD'),
                          gty_ct='人民币',
                          gty_amout=saving.get('GTY_AMOUT'),
                          brw_cus_id=saving.get('BRW_CUS_ID'),
                          brw_cus_name=saving.get('BRW_CUS_NAME'),
                          brw_cus_type=saving.get('BRW_CUS_TYPE'),
                          gty_cus_id=saving.get('GTY_CUS_ID'),
                          gty_cus_name=saving.get('GTY_CUS_NAME'),
                          gty_cus_type=saving.get('GTY_CUS_TYPE'),
                          bfirst_gty=saving.get('BFIRST_GTY'),
                          bboard_appr=saving.get('BBOARD_APPR'),
                          gty_due_date=saving.get('GTY_DUE_DATE'),
                          ins_type=saving.get('INS_TYPE'),
                          ins_id=saving.get('INS_ID'),
                          ins_due_date=saving.get('INS_DUE_DATE'),
                          reg_org_id=saving.get('REG_ORG_ID'),
                          reg_by=saving.get('REG_BY'),
                          reg_date=saving.get('REG_DATE'),
                          updated_time=saving.get('UPDATED_TIME'),
                          gty_status=saving.get('GTY_STATUS'),
                          insp1_id=saving.get('INSP1_ID'),
                          insp2_id=saving.get('INSP2_ID'),
                          gty_total=saving.get('GTY_TOTAL'))

            a=self.session.query(Application).filter(Application.brw_app_id==saving.get('BRW_APP_ID')).first()
            gty_con=Contract(contract_no=saving.get('CON_GTY_ID'))
            if a:
                a_id = a.id
            else:
                a_id =None
            gty_info = GuaranteeInfo(application_id=a_id,
                                     gty_amount=saving.get('GTY_AMOUT'),
                                     gty_customer_name=saving.get('GTY_CUS_NAME'),
                                     gty_method='抵押'
                                     )        
            gty_rel=GuaranteeContractRelation(contract=gty_con,guarantee_info=gty_info) 
            gty=GuaranteeRelation(guarantee=gty,guarantee_info=gty_info)     
            self.session.add(gty) 
            self.session.add(gty_rel) 
        self.session.commit()

    def load_mrge_other(self):
        log.debug('other')
        saving_list= self.load_gua('select * from GTY_BASE ,GTY_MRGE_OTHER,GTY_REL where GTY_MRGE_OTHER.GTY_ID = GTY_BASE.GTY_ID and GTY_REL.APP_ID = GTY_BASE.BRW_APP_ID' )
        for saving in saving_list:
            gty=MrgeOther(mrge_name=saving.get('MRGE_BRAND'),
                          mrge_model=saving.get('MRGE_MODEL'),
                          mrge_qty=saving.get('MRGE_AMOUNT'),
                          bought_date=saving.get('BOUGHT_DATE'),
                          bought_price=saving.get('BOUGHT_PRICE'),
                          mrge_location=saving.get('MRGE_LOCATION'),
                          pledge_type=u'抵押-其他',
                          gty_method=saving.get('GTY_METHOD'),
                          gty_ct='人民币',
                          gty_amout=saving.get('GTY_AMOUT'),
                          brw_cus_id=saving.get('BRW_CUS_ID'),
                          brw_cus_name=saving.get('BRW_CUS_NAME'),
                          brw_cus_type=saving.get('BRW_CUS_TYPE'),
                          gty_cus_id=saving.get('GTY_CUS_ID'),
                          gty_cus_name=saving.get('GTY_CUS_NAME'),
                          gty_cus_type=saving.get('GTY_CUS_TYPE'),
                          bfirst_gty=saving.get('BFIRST_GTY'),
                          bboard_appr=saving.get('BBOARD_APPR'),
                          gty_due_date=saving.get('GTY_DUE_DATE'),
                          ins_type=saving.get('INS_TYPE'),
                          ins_id=saving.get('INS_ID'),
                          ins_due_date=saving.get('INS_DUE_DATE'),
                          reg_org_id=saving.get('REG_ORG_ID'),
                          reg_by=saving.get('REG_BY'),
                          reg_date=saving.get('REG_DATE'),
                          updated_time=saving.get('UPDATED_TIME'),
                          gty_status=saving.get('GTY_STATUS'),
                          insp1_id=saving.get('INSP1_ID'),
                          insp2_id=saving.get('INSP2_ID'),
                          gty_total=saving.get('GTY_TOTAL'))

            a=self.session.query(Application).filter(Application.brw_app_id==saving.get('BRW_APP_ID')).first()
            gty_con=Contract(contract_no=saving.get('CON_GTY_ID'))
            if a:
                a_id = a.id
            else:
                a_id =None
            gty_info = GuaranteeInfo(application_id=a_id,
                                     gty_amount=saving.get('GTY_AMOUT'),
                                     gty_customer_name=saving.get('GTY_CUS_NAME'),
                                     gty_method='抵押'
                                     )        
            gty_rel=GuaranteeContractRelation(contract=gty_con,guarantee_info=gty_info) 
            gty=GuaranteeRelation(guarantee=gty,guarantee_info=gty_info)     
            self.session.add(gty) 
            self.session.add(gty_rel) 
        self.session.commit()
    def base(self):
        log.debug('base')
        saving_list= self.load_gua("select * from GTY_BASE ,GTY_REL where GTY_BASE.PLEDGE_TYPE = '' and GTY_REL.APP_ID = GTY_BASE.BRW_APP_ID" )
        for saving in saving_list:
            gty = Guarantee(pledge_type=u'担保',
                                  gty_method=saving.get('GTY_METHOD'),
                                  gty_ct='人民币',
                                  gty_amout=saving.get('GTY_AMOUT'),
                                  brw_cus_id=saving.get('BRW_CUS_ID'),
                                  brw_cus_name=saving.get('BRW_CUS_NAME'),
                                  brw_cus_type=saving.get('BRW_CUS_TYPE'),
                                  gty_cus_id=saving.get('GTY_CUS_ID'),
                                  gty_cus_name=saving.get('GTY_CUS_NAME'),
                                  gty_cus_type=saving.get('GTY_CUS_TYPE'),
                                  bfirst_gty=saving.get('BFIRST_GTY'),
                                  bboard_appr=saving.get('BBOARD_APPR'),
                                  gty_due_date=saving.get('GTY_DUE_DATE'),
                                  ins_type=saving.get('INS_TYPE'),
                                  ins_id=saving.get('INS_ID'),
                                  ins_due_date=saving.get('INS_DUE_DATE'),
                                  reg_org_id=saving.get('REG_ORG_ID'),
                                  reg_by=saving.get('REG_BY'),
                                  reg_date=saving.get('REG_DATE'),
                                  updated_time=saving.get('UPDATED_TIME'),
                                  gty_status=saving.get('GTY_STATUS'),
                                  insp1_id=saving.get('INSP1_ID'),
                                  insp2_id=saving.get('INSP2_ID'),
                                  gty_total=saving.get('GTY_TOTAL'))

            a=self.session.query(Application).filter(Application.brw_app_id==saving.get('BRW_APP_ID')).first()
            gty_con=Contract(contract_no=saving.get('CON_GTY_ID'))
            if a:
                a_id = a.id
            else:
                a_id =None
            gty_info = GuaranteeInfo(application_id=a_id,
                                     gty_amount=saving.get('GTY_AMOUT'),
                                     gty_customer_name=saving.get('GTY_CUS_NAME'),
                                     gty_method='保证'
                                     )        
            gty_rel=GuaranteeContractRelation(contract=gty_con,guarantee_info=gty_info) 
            gty=GuaranteeRelation(guarantee=gty,guarantee_info=gty_info)     
            self.session.add(gty) 
            self.session.add(gty_rel) 
        self.session.commit()

    def load_accp_con(self):
        log.debug('accp')
        saving_list= self.load_gua('select * from  CON_BASE ,CON_ACCP ,APP_BASE where APP_BASE.APP_ID=CON_BASE.APP_ID and  CON_BASE.CON_ID = CON_ACCP.CON_ID ' )
        log.debug(len(saving_list))
        for saving in saving_list:
            con_id=saving.get('CON_ID')
            lend_con = LendContract(contract_no=con_id,
                         amount=saving.get('CON_AMOUNT'),
                         contract_sign_date=saving.get('REG_DATE'), 
                         contract_effect_date=saving.get('LOAN_START_DATE'),
                         contract_due_date=saving.get('LOAN_END_DATE')
                        )
            cust_no = saving.get('CUS_ID')
            cust=self.session.query(Customer).join(Party,Party.id==Customer.party_id).filter(Party.no==cust_no).first()
            if cust:
                a = Application(customer_id=cust.role_id,product_code=saving.get('BIZ_TYPE'),
                              apply_date=saving.get('APP_DATE'),
                              brw_app_id=saving.get('APP_ID'),
                              handle_branch=saving.get('ORG_ID'),
                              handle_person=saving.get('OPT_BY'),
                              register_branch=saving.get('REG_ORG_ID'),
                              register_date=saving.get('REG_DATE'),
                              term_month=saving.get('DUE_MONTH'),
                              overdue_rate=saving.get('PASS_DUE_PENALTY_IR'),
                              shift_rate=saving.get('OTHER_PENALTY_IR'),
                              interest_method=saving.get('CACULATE_METHOD'),
                              repayment_method=saving.get('RETURN_METHOD'),
                              rep_period=saving.get('RETURN_TERMS'),
                              main_gua_type=saving.get('GTY_MAIN_METHOD'),
                              repayment_from=saving.get('RETURN_SOURCE'),
                              status=saving.get('APP_STATUS'),
                              industry_1=saving.get('CLASS_1'),
                              industry_2=saving.get('CLASS_2'),
                              industry_3=saving.get('CLASS_3'),
                              industry_4=saving.get('CLASS_GB'),
                              repayment_times=saving.get('RETURN_PERIOD') if saving.get('RETURN_PERIOD') else 0)
                transaction=ApplicationTransaction(application=a,amount=saving.get('APP_AMOUNT'),
                                             transaction_name=u'%s的贷款申请'%(cust.party.name))
                lend_transaction=AcceptanceBillLoan(application_transaction=transaction,
                                     amount=saving.get('CON_AMOUNT'),
                                     product_code=saving.get('BIZ_TYPE'),
                                     from_date=saving.get('LOAN_START_DATE'),
                                     thur_date=saving.get('LOAN_END_DATE'),
                                     repayment_method=saving.get('RETURN_METHOD'),
                                     rep_period=saving.get('RETURN_TERMS'),
                                     rep_per_fre=saving.get('RETURN_FREQ'),
                                     first_rep_date=saving.get('FIRST_RETURN_DATE'),
                                     repayment_from=saving.get('RETURN_SOURCE'),
                                     compliance_rate=saving.get('BASE_IR'),
                                     product_rate=saving.get('PRODUCT_IR'),
                                     product_float_type=saving.get('FLOAT_IR_TYPE'),
                                     product_rate_float=saving.get('FLOAT_IR_PERCENT'),
                                     execute_rate=saving.get('MONTH_IR'),
                                     overdue_rate_more=saving.get('PASS_DUE_PENALTY_IR'),
                                     overdue_rate=saving.get('PASS_DUE_MONTH_IR'), 
                                     shift_fine_rate=saving.get('OTHER_PENALTY_IR'),
                                     shift_rate=saving.get('OTHER_MONTH_IR'),
                                     debt_interest=saving.get('DEBIT_INTEREST_PERCENT'),
                                     debt_interest_and=saving.get('DEBIT_INTEREST_IR'),
                                     interest_method=saving.get('CACULATE_METHOD'),
                                     interest_period=saving.get('CACULATE_PERIOD'),
                                     int_per_fre =saving.get('CACULATE_FREQ'),
                                     first_int_date=saving.get('FIRST_CACULATE_DATE'),
                                     strate_product=saving.get('STRATEGY_INDUSTRY_TYPE'),
                                     product_update=saving.get('INDUSTRY_TRANSITION_FLAG'),
                                     trade_contract_no=saving.get('TRADE_CONTRACT_NO'),
                                     goods_name=saving.get('GOODS_NAME'),
                                     fee_percent=saving.get('PROC_FEE_PERCENT'),
                                     fee_amount=saving.get('PROC_FEE_AMOUNT'),
                                     pay_method=saving.get('PAY_METHOD'),
                                     pay_bank_name=saving.get('PAY_BANK'),
                                     accp_accounts_bank=saving.get('ISSUE_BANK')
                           )
                lend_rel=TransactionContractRelation(lend_contract=lend_con,lend_transaction=lend_transaction) 
                self.session.add(lend_rel)
        self.session.commit() 

    def load_disc_con(self):
        log.debug('disc')
        saving_list= self.load_gua('select * from  CON_BASE ,CON_DISC_BANK ,APP_BASE where APP_BASE.APP_ID=CON_BASE.APP_ID and CON_BASE.CON_ID = CON_DISC_BANK.CON_ID ' )
        log.debug(len(saving_list))
        for saving in saving_list:
            con_id=saving.get('CON_ID')
            lend_con = LendContract(contract_no=con_id,
                         amount=saving.get('CON_AMOUNT'),
                         contract_sign_date=saving.get('REG_DATE'), 
                         contract_effect_date=saving.get('LOAN_START_DATE'),
                         contract_due_date=saving.get('LOAN_END_DATE')
                        )
            cust_no = saving.get('CUS_ID')
            cust=self.session.query(Customer).join(Party,Party.id==Customer.party_id).filter(Party.no==cust_no).first()
            if cust:
                a = Application(customer_id=cust.role_id,product_code=saving.get('BIZ_TYPE'),
                              apply_date=saving.get('APP_DATE'),
                              handle_branch=saving.get('ORG_ID'),
                              handle_person=saving.get('OPT_BY'),
                              register_branch=saving.get('REG_ORG_ID'),
                              brw_app_id=saving.get('APP_ID'),
                              register_date=saving.get('REG_DATE'),
                              term_month=saving.get('DUE_MONTH'),
                              overdue_rate=saving.get('PASS_DUE_PENALTY_IR'),
                              shift_rate=saving.get('OTHER_PENALTY_IR'),
                              interest_method=saving.get('CACULATE_METHOD'),
                              repayment_method=saving.get('RETURN_METHOD'),
                              rep_period=saving.get('RETURN_TERMS'),
                              main_gua_type=saving.get('GTY_MAIN_METHOD'),
                              repayment_from=saving.get('RETURN_SOURCE'),
                              status=saving.get('APP_STATUS'),
                              industry_1=saving.get('CLASS_1'),
                              industry_2=saving.get('CLASS_2'),
                              industry_3=saving.get('CLASS_3'),
                              industry_4=saving.get('CLASS_GB'),
                              repayment_times=saving.get('RETURN_PERIOD') if saving.get('RETURN_PERIOD') else 0)
                transaction=ApplicationTransaction(application=a,amount=saving.get('APP_AMOUNT'),
                                             transaction_name=u'%s的贷款申请'%(cust.party.name))

                lend_transaction=LendTransaction(application_transaction=transaction,
                                                 amount=saving.get('CON_AMOUNT'),
                                                 discount_firstend=saving.get('BILL_DUE_DATE'),
                                                 bill_num=saving.get('BILL_QTY'),
                                                 product_code=saving.get('BIZ_TYPE'),
                                                 from_date=saving.get('LOAN_START_DATE'),
                                                 thur_date=saving.get('LOAN_END_DATE'),
                                                 repayment_method=saving.get('RETURN_METHOD'),
                                                 rep_period=saving.get('RETURN_TERMS'),
                                                 rep_per_fre=saving.get('RETURN_FREQ'),
                                                 first_rep_date=saving.get('FIRST_RETURN_DATE'),
                                                 repayment_from=saving.get('RETURN_SOURCE'),
                                                 compliance_rate=saving.get('BASE_IR'),
                                                 product_rate=saving.get('PRODUCT_IR'),
                                                 product_float_type=saving.get('FLOAT_IR_TYPE'),
                                                 product_rate_float=saving.get('FLOAT_IR_PERCENT'),
                                                 execute_rate=saving.get('MONTH_IR'),
                                                 overdue_rate_more=saving.get('PASS_DUE_PENALTY_IR'),
                                                 overdue_rate=saving.get('PASS_DUE_MONTH_IR'), 
                                                 shift_fine_rate=saving.get('OTHER_PENALTY_IR'),
                                                 shift_rate=saving.get('OTHER_MONTH_IR'),
                                                 debt_interest=saving.get('DEBIT_INTEREST_PERCENT'),
                                                 debt_interest_and=saving.get('DEBIT_INTEREST_IR'),
                                                 interest_method=saving.get('CACULATE_METHOD'),
                                                 interest_period=saving.get('CACULATE_PERIOD'),
                                                 int_per_fre =saving.get('CACULATE_FREQ'),
                                                 first_int_date=saving.get('FIRST_CACULATE_DATE'),
                                                 strate_product=saving.get('STRATEGY_INDUSTRY_TYPE'),
                                                 product_update=saving.get('INDUSTRY_TRANSITION_FLAG')
                )
                lend_rel=TransactionContractRelation(lend_contract=lend_con,lend_transaction=lend_transaction) 
                self.session.add(lend_rel)
        self.session.commit()


    def load_con(self):
        log.debug('con')
        saving_list= self.load_gua("select * from  CON_BASE ,APP_BASE where APP_BASE.APP_ID =CON_BASE.APP_ID and CON_BASE.BIZ_TYPE not in('007','023') ")
        log.debug(len(saving_list))
        for saving in saving_list:
            con_id=saving.get('CON_ID')
            lend_con = LendContract(contract_no=con_id,
                         amount=saving.get('CON_AMOUNT'),
                         contract_sign_date=saving.get('REG_DATE'), 
                         contract_effect_date=saving.get('LOAN_START_DATE'),
                         contract_due_date=saving.get('LOAN_END_DATE')
                        )
            cust_no = saving.get('CUS_ID')
            cust=self.session.query(Customer).join(Party,Party.id==Customer.party_id).filter(Party.no==cust_no).first()
            if cust:
                a = Application(customer_id=cust.role_id,product_code=saving.get('BIZ_TYPE'),
                              apply_date=saving.get('APP_DATE'),
                              handle_branch=saving.get('ORG_ID'),
                              handle_person=saving.get('OPT_BY'),
                              register_branch=saving.get('REG_ORG_ID'),
                              brw_app_id=saving.get('APP_ID'),
                              register_date=saving.get('REG_DATE'),
                              term_month=saving.get('DUE_MONTH'),
                              overdue_rate=saving.get('PASS_DUE_PENALTY_IR'),
                              shift_rate=saving.get('OTHER_PENALTY_IR'),
                              interest_method=saving.get('CACULATE_METHOD'),
                              repayment_method=saving.get('RETURN_METHOD'),
                              rep_period=saving.get('RETURN_TERMS'),
                              main_gua_type=saving.get('GTY_MAIN_METHOD'),
                              repayment_from=saving.get('RETURN_SOURCE'),
                              status=saving.get('APP_STATUS'),
                              industry_1=saving.get('CLASS_1'),
                              industry_2=saving.get('CLASS_2'),
                              industry_3=saving.get('CLASS_3'),
                              industry_4=saving.get('CLASS_GB'),
                              repayment_times=saving.get('RETURN_PERIOD') if saving.get('RETURN_PERIOD') else 0)
                transaction=ApplicationTransaction(application=a,amount=saving.get('APP_AMOUNT'),
                                             transaction_name=u'%s的贷款申请'%(cust.party.name))

                lend_transaction=LendTransaction(application_transaction=transaction,
                            amount=saving.get('CON_AMOUNT'),
                            product_code=saving.get('BIZ_TYPE'),
                            from_date=saving.get('LOAN_START_DATE'),
                            thur_date=saving.get('LOAN_END_DATE'),
                            repayment_method=saving.get('RETURN_METHOD'),
                            rep_period=saving.get('RETURN_TERMS'),
                            rep_per_fre=saving.get('RETURN_FREQ'),
                            first_rep_date=saving.get('FIRST_RETURN_DATE'),
                            repayment_from=saving.get('RETURN_SOURCE'),
                            compliance_rate=saving.get('BASE_IR'),
                            product_rate=saving.get('PRODUCT_IR'),
                            product_float_type=saving.get('FLOAT_IR_TYPE'),
                            product_rate_float=saving.get('FLOAT_IR_PERCENT'),
                            execute_rate=saving.get('MONTH_IR'),
                            overdue_rate_more=saving.get('PASS_DUE_PENALTY_IR'),
                            overdue_rate=saving.get('PASS_DUE_MONTH_IR'), 
                            shift_fine_rate=saving.get('OTHER_PENALTY_IR'),
                            shift_rate=saving.get('OTHER_MONTH_IR'),
                            debt_interest=saving.get('DEBIT_INTEREST_PERCENT'),
                            debt_interest_and=saving.get('DEBIT_INTEREST_IR'),
                            interest_method=saving.get('CACULATE_METHOD'),
                            interest_period=saving.get('CACULATE_PERIOD'),
                            int_per_fre =saving.get('CACULATE_FREQ'),
                            first_int_date=saving.get('FIRST_CACULATE_DATE'),
                            strate_product=saving.get('STRATEGY_INDUSTRY_TYPE'),
                            product_update=saving.get('INDUSTRY_TRANSITION_FLAG')
                           )
                lend_rel=TransactionContractRelation(lend_contract=lend_con,lend_transaction=lend_transaction) 
                self.session.add(lend_rel)
        self.session.commit()

    def load_payment(self):
        log.debug('payment')
        saving_list= self.load_gua('select * from  CON_BASE ,FUNDFLOW  where CON_BASE.APP_ID =FUNDFLOW.APP_ID ' )
        log.debug(len(saving_list))
        for saving in saving_list:
            con_id=saving.get('CON_ID')
            con=self.session.query(Contract).filter(Contract.contract_no == con_id).first()
            if con:
                debt =Debt(contract_id=con.contract_id,
                               begin_date=saving.get('ISSUE_DATE'),
                               end_date=saving.get('DUE_DATE'),
                               amount=saving.get('LOAN_AMOUNT'),
                               is_credit_card=saving.get('CARD_CREDIT'),
                               extend_date=saving.get('EXTEND_DATE'),
                               extend_time=saving.get('EXTEND_TIME'),
                                ) 
                payment =Payment(debt=debt,
                                     paydetail=saving.get('TRADE_CONTENT'),
                                     repayment_from=saving.get('RETURN_SOURCE'),
                                     payment_method=saving.get('PAYMENT_TYPE'),
                                     amount=saving.get('PAYMENT_AMOUNT'),
                                     settle_type=saving.get('BALANCE_TYPE'),
                                     comm_payer=saving.get('PAYER'),
                                     comm_payee=saving.get('PAYEE'),
                                     payee_account=saving.get('PAYEE_NO'),
                                     vou_type=saving.get('PAY_VOUCHER_TYPE'),
                                     vou_no=saving.get('VOUCHER_NO'),
                                     bank_type=saving.get('PAYEE_BANK_TYPE'), 
                                     bank_no=saving.get('PAYEE_BANK_NO'),
                                     bank_name=saving.get('CREDIT_INPUT_BANK_NAME'),
                                     purpose_type=saving.get('LOAN_USAGE')
                                ) 
                self.session.add(payment) 
        self.session.commit() 


    def test_main(self):
        log.debug('start')
        self.load_accp_con()
        self.load_disc_con()
        self.load_con()
        self.load_payment()
        self.load_stub()
        self.load_rec()
        self.load_accp()
        self.load_pawn_other()
        self.load_bldg()
        self.load_land()
        self.eqp()
        self.vch()
        self.load_mrge_other()
        self.load_saving()
        self.base()

    def tearDown(self):
        self.session.commit() 
        log.debug("Over")
        

