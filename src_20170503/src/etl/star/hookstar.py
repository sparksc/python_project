# -*- coding:utf-8 -*-
#!/bin/python  

from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random,sys 
from datetime import datetime,timedelta

from etl.base.conf import *
import etl.base.util as util
from etl.star.dim import *
from etl.star.transformdict import *
from etl.base.singleton import singleton
     
from etl.base.logger import info

from etl.star.starbase import StarManage, StarBase

from etl.star.model.deposit_dq import Deposit_dq 
from etl.star.model.deposit_hq import Deposit_hq 
from etl.star.model.ebank_epay import Ebank_epay 
from etl.star.model.ebank_cb import Ebank_cb 
from etl.star.model.ebank_mb import Ebank_mb 
from etl.star.model.ebank_pb import Ebank_pb 
from etl.star.model.ebank_etc import Ebank_etc 
from etl.star.model.ebank_zfb import Ebank_zfb 
from etl.star.model.ebank_kjzf import Ebank_kjzf 
from etl.star.model.finances import Finances 
from etl.star.model.stock import Stock 
from etl.star.model.insurance import Insurance 
from etl.star.model.creditcard import Creditcard
from etl.star.model.loan_contract import Loan_Contract
from etl.star.model.parent_acct import ParentAccount 

import etl.star.update.update_hook_balance as uhb
import etl.star.update.update_cust_hook_to_account as uchb
import etl.star.update.update_fbalance_org_id as ufoi
import etl.star.update.update_hook as update_hook

from etl.star.update.parent_hook import parent_hook_start
from etl.star.dim import  DimAccountNew,DimAccountGid

def busi_hook(etldate):

    dg = DimAccountGid()
    dim1 = DimAccountNew()
    dim1.start()

    sm = StarManage(1, [dg,dim1])
    sm.start_dim_process()
    sm.start_fact_process()
    sm.setDimQueue()
    sm.start()
    '''
    info("run loan_hook star")
    StarBase().files2fact(Loan_Contract(), sm)
    sm.restart_fact_process()
    info("run loan_hook end")
    info("run deposit_hook")    
    StarBase().files2fact(Deposit_hq(), sm)
    sm.restart_fact_process()
    info("run deposit_dq")    
    StarBase().files2fact(Deposit_dq(), sm)
    sm.restart_fact_process()
    info("run deposit_hook end")    
    info("run ebank_hook star")    
    StarBase().files2fact(Ebank_kjzf(), sm)
    sm.restart_fact_process()
    StarBase().files2fact(Ebank_epay(), sm)
    sm.restart_fact_process()
    StarBase().files2fact(Ebank_zfb(), sm)
    sm.restart_fact_process()
    StarBase().files2fact(Ebank_pb(), sm)
    sm.restart_fact_process()
    StarBase().files2fact(Ebank_mb(), sm)
    sm.restart_fact_process()
    StarBase().files2fact(Ebank_cb(), sm)
    sm.restart_fact_process()
    #StarBase().files2fact(Ebank_etc(), sm)
    #sm.restart_fact_process()
 
    info("run finances_hook")    
    StarBase().files2fact(Finances(), sm)
    sm.restart_fact_process()

    info("run stock_hook") 
    StarBase().files2fact(Stock(), sm)
    sm.restart_fact_process()

    info("run insurance_hook")    
    StarBase().files2fact(Insurance(), sm)
    sm.restart_fact_process()

    info("run creditcard_hook") 
    StarBase().files2fact(Creditcard(), sm)
    sm.restart_fact_process()
    '''

    info("run ParentAccount") 
    StarBase().files2fact(ParentAccount(), sm)
    sm.restart_fact_process()

    sm.finish()


def starun(etldate):
    Config().etldate = int(etldate)
    ufoi.update_orgid(int(etldate),int(etldate))
    info("run busi_hook star") 

    busi_hook(etldate)

    ''' 
    info("run del_dup") 
    uhb.del_dup()
    info("run insert_account_hook_by_cust:存款") 
    uchb.insert_account_hook_by_cust(int(etldate),'存款') #根据客户挂钩补账户挂钩
    info("run insert_account_hook_by_cust:理财") 
    uchb.insert_account_hook_by_cust(int(etldate),'理财') #根据客户挂钩补账户挂钩
    ''' 
    parent_hook_start(etldate)
    util.fix_seq_id('D_MANAGE','D_MANAGE_SEQ')
    util.fix_seq_id('D_MANAGE','D_ACCOUNT_SEQ')

if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen != 3:
        print "please input python %s yyyyyMMdd yyyyMMdd "%(sys.argv[0])
    else:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        etldate=int(startdate)
        while etldate<=int(enddate):    
            print etldate
            Config().etldate = etldate
            Config().stretldate = util.tostrdate(etldate)        
            parent_hook_start(etldate)
            #busi_hook(etldate)
            etldate = int(daycalc(etldate,1))
