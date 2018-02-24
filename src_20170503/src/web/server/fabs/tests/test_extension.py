# -*- coding:utf-8 -*-

import unittest
from ..database import simple_session, current_engine
#from ..model.HZ_STAFF_SAL import REPORT_MANAGER_HZSAL
#from ..model.mbox import PUHUI_BRANCH_TARGET_HANDER
#from ..model.mbox import REPORT_CREDIT_VILLAGNUM 
from ..model.ebank_replace import EBANK_REPLACE_NUM,M_CASH_TRAN_CNT,M_CASH_TRAN_AMOUNT,M_TELLER_TRAN 
from ..model.credit_hook import CreditHook 
from ..model.QRY_SETTLEMENT_MANAGER import EBILLS_QRY_SETTLEMENT_MANAGER 
from ..model.QRY_SETTLEMENT_MANAGER import EBILLS_PA_QUOTEPRICEARV
from ..model.QRY_SETTLEMENT_MANAGER import EBILLS_QRY_SETTLEMENT_CORP
from ..model.QRY_SETTLEMENT_MANAGER import EBILLS_PA_MANAGERCORPINFO
from ..model.QRY_SETTLEMENT_MANAGER import EBILLS_PA_MANAGERINFO
from ..model.QRY_SETTLEMENT_MANAGER import EBILLS_PA_CORP
from ..model.QRY_SETTLEMENT_MANAGER import NEW_EBILLS_BU_TRANSACTIONINFO 
from ..model.QRY_SETTLEMENT_MANAGER import REPORT_SALE_RMB_EXG 
from ..model.QRY_SETTLEMENT_MANAGER import EBILLS_PA_ORG 
from ..model.mbox import TransactionCode
from ..model.permission import *
from ..model.hook import *
from ..model.ebills import EbillsHook
from ..model.ebills import *
from ..model.ebills import EbillsManager 
from ..model.village_input import *
from ..model.STAFF_SAL import *
from ..model.counter_work import *
import logging

log = logging.getLogger()

class TestExtension(unittest.TestCase):

    def setUp(self):
        self.session=simple_session()

    def test_create_mbox(self):
        FMS_TRANS_LOG.__table__.create(current_engine)
        #MID_BUSINESS.__table__.create(current_engine)
        #TELLER_VOLUME_ADJUST.__table__.create(current_engine)
        #CORE_BHFMCMRM_DIRECT.__table__.create(current_engine)
        #CORE_BHFMCMRD.__table__.create(current_engine)
        #OCR_ORG_RATE_ERROR.__table__.create(current_engine)
        #OCR_SALE_RATE_ERROR.__table__.create(current_engine)
        #OCR_FIRST_ERROR.__table__.create(current_engine)
        #CASH_ERROR_RATE.__table__.create(current_engine)
        #COUNTER_REASON.__table__.create(current_engine)
        #COUNTER_EXAM_VOL.__table__.create(current_engine)
        #REPORT_MANAGER_WORKQUALITY_HANDER.__table__.create(current_engine)
        #REPORT_HALL_MANAGER_HANDER.__table__.create(current_engine)
        #REPORT_BRANCH_MANCH_HANDER.__table__.create(current_engine)
        #M_CASH_TRAN_CNT.__table__.create(current_engine)
        #EbillsHook_ORG.__table__.create(current_engine)
        #EbillsHook_CUNKUAN.__table__.create(current_engine)
        #M_CASH_TRAN_AMOUNT.__table__.create(current_engine)
        #M_TELLER_TRAN.__table__.create(current_engine)
        #REPORT_MANAGER_HZSAL.__table__.create(current_engine)
        #REPORT_MANAGER_LOAN.__table__.create(current_engine)
        #AccountForm.__table__.create(current_engine)
        #TellerLevel.__table__.create(current_engine)
        #ManGrade.__table__.create(current_engine)
        #AccountHookHisQuery.__table__.create(current_engine)
        #CustHookHisQuery.__table__.create(current_engine)
        #User_ExtraScore.__table__.create(current_engine)
        #Account_Rank.__table__.create(current_engine)
        #PUHUI_BRANCH_TARGET_HANDER.__table__.create(current_engine)
        #EBILLS_QRY_SETTLEMENT_MANAGER.__table__.create(current_engine)
        #EBILLS_PA_QUOTEPRICEARV.__table__.create(current_engine)
        #EbankOrg.__table__.create(current_engine)
        #QuarterTermSaleMbank.__table__.create(current_engine)
        #EbillsHook.__table__.create(current_engine)
        #EbillsHook_DISINFO.__table__.create(current_engine)
        #REPORT_SALE_RMB_EXG.__table__.create(current_engine)
        #BuyFsj.__table__.create(current_engine)
        #CmRenBao.__table__.create(current_engine)
        #Bank_ProfitEarning_Input.__table__.create(current_engine)
        #OrgPeopleCount.__table__.create(current_engine)
        #Hand_Maintain.__table__.create(current_engine)
        #Burank.__table__.create(current_engine)
        #User_ExtraScore.__table__.create(current_engine)
        #ManGrade.__table__.create(current_engine)
        #ManScore.__table__.create(current_engine)
        #BranchGrade.__table__.create(current_engine)
        #UserLevel.__table__.create(current_engine)
        #TellerLevel.__table__.create(current_engine)
        #Addharvest.__table__.create(current_engine)
        #Insurance.__table__.create(current_engine)
        #Account_Rank.__table__.create(current_engine)
        #AccountForm.__table__.create(current_engine)
        #DelegateHand.__table__.create(current_engine)
        #DelegateForm.__table__.create(current_engine)
        #OrgLevel.__table__.create(current_engine)
        #EbillsManager.__table__.create(current_engine)
        #TransactionCode.__table__.create(current_engine)
        #EBILLS_QRY_SETTLEMENT_CORP.__table__.create(current_engine)
        #EBILLS_PA_MANAGERCORPINFO.__table__.create(current_engine)
        #EBILLS_PA_MANAGERINFO.__table__.create(current_engine)
        #EBILLS_PA_CORP.__table__.create(current_engine)
        #EBILLS_PA_ORG.__table__.create(current_engine)
        #NEW_EBILLS_BU_TRANSACTIONINFO.__table__.create(current_engine)
        #EtcData.__table__.create(current_engine)
        #EBANK_REPLACE_NUM.__table__.create(current_engine)
        #CreditHook.__table__.create(current_engine)
    def tearDown(self):
        logging.debug("finish!!!")

