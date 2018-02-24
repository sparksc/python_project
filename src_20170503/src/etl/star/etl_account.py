# -*- coding:utf-8 -*-
#!/bin/python  

from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random,sys 
from datetime import datetime,timedelta
from decimal import *
import DB2  

from etl.base.conf import *
import etl.base.util as util
from etl.star.dim import *
from etl.star.transformdict import *
from etl.base.singleton import singleton

from etl.star.custview import CustView
from etl.star.fbillaccount import FBillAccount
from etl.star.financialsale import FinancialSale
from etl.star.ftransation import FTransAtion
from etl.star.BLFMCNAFINSERT import Blfmcnaf
from etl.star.pos_insert import PosInsert
from etl.star.atm_insert import AtmInsert
from etl.star.model.translog import *
from etl.star.CORE_BLFMMTRNINSERT import Blfmmtrn
from etl.star.ebills_qry_settlement_corpInsert import qry_settlement_corp
from etl.star.corp_bhfmcmrdInsert import corp_bhfmcmrd
from etl.star.core_bhfmcmrm_direct import core_bhfmcmrm_direct
from etl.star.update.update_last_trade_date import update_ltd
from etl.star.update.update_fbalance_org_id import update_orgid
from datetime import datetime 

def run_etl_main(startdate,enddate,q1,q2,model=None):
    info("start_run_etl_main:%s,model=%s"%(str(startdate),model))
    d1=datetime.now()
    etldate = int(startdate)
    Config().etldate = etldate
    #load_dims(q1,q2,q3) 
    load_dims(q2) 
    if model == 'C':
        util.delete_fcustview(etldate,int(enddate))
    elif model == 'F':
        util.delete_financialsale(etldate,int(enddate))
    elif model == 'T':
        util.delete_fcacctjrnl(etldate,int(enddate))
    elif model =='POS':
        util.delete_pos_insert(etldate,int(enddate))
    elif model =='CORP':#国际业务按客户
        util.delete_ebills_qry_settlement_corp(etldate,int(enddate))
    elif model =='CASH_INFO':#现金调拨信息信息
        util.delete_core_bhfmcmrd(etldate,int(enddate))
    elif model =='CASH_DIR':#现金调拨方向
        util.delete_CORE_BHFMCMRM_DIRECT(etldate,int(enddate))
    elif model =='ATM':
        util.delete_atm_insert(etldate,int(enddate))
    elif model == 'FTBHB':
        util.delete_financialsale(etldate,int(enddate))
        util.delete_fcacctjrnl(etldate,int(enddate))
        util.delete_fbillacount(etldate,int(enddate))
        util.delete_blfm(etldate,int(enddate))
        util.delete_blfmmtrn(etldate,int(enddate))
    elif model == 'BILL':
        util.delete_fbillacount(etldate,int(enddate))
    elif model=='HXHK':  #核销清单
        util.delete_blfm(etldate,int(enddate))
    elif model=='BLFMM':#逾期还款清单
        util.delete_blfmmtrn(etldate,int(enddate))
    else:
        pass

    while int(etldate) <= int(enddate):
        print "run_etl_main step2...",etldate    
        d1=datetime.now()
        Config().etldate = etldate
        Config().stretldate=util.tostrdate(etldate)
        if model == 'C':
            info("run CUSTVIEW")    
            CustView().loaddbtofact(q1,q1)
        elif model == 'F':
            info("run financialsale")
            FinancialSale().loadtofact(q2,q2)    
        elif model == 'T':
            info("run FTransAtion")
            FTransAtion().loadtofact(q2,q2)    
        elif model == 'CORP':#国际业务按客户
            qry_settlement_corp().loadtofact(q2,q2)
        elif model =='CASH_INFO':#现金调拨信息信息
            corp_bhfmcmrd().loadtofact(q2,q2)
        elif model =='CASH_DIR':#现金调拨方向
            core_bhfmcmrm_direct().loadtofact(q2,q2)
        elif model =='POS':#新增POS助农
            PosInsert().loadtofact(q2,q2)
        elif model =='ATM':#新增ATM助农
            AtmInsert().loadtofact(q2,q2)
        elif model == 'FTBHB':
            info("run financialsale")
            FinancialSale().loadtofact(q2,q2)    
            info("run FTransAtion")
            FTransAtion().loadtofact(q2,q2)    
            info("run Fbill")
            FBillAccount().loadtofact(q2,q2)    
            info("run Blfmcnaf")
            Blfmcnaf().loadtofact(q2,q2)
            info("run Blfmmtrn")
            Blfmmtrn().loadtofact(q2,q2)
        elif model == 'BILL':
            info("run Fbill")
            FBillAccount().loadtofact(q2,q2)    
        elif model=='HXHK':#核销清单       F_CORE_BLFMCNAF  
            Blfmcnaf().loadtofact(q2,q2)
        elif model=='BLFMM':##逾期还款清单  F_CORE_BLFMMTRN
            Blfmmtrn().loadtofact(q2,q2)
        else:
            pass
        etldate=int(daycalc(etldate,1))
        util.fix_seq_id('D_ACCOUNT','D_ACCOUNT_SEQ_NEW')
    info("finish_run_etl_main:%s,model=%s"%(str(startdate),model))
 
def run_etl(startdate,endate,model=None):
    manager = multiprocessing.Manager()
    q1=manager.Queue()
    q2=manager.Queue()
    pw1 = Process(target=queue2db, args=( q1, ))
    pw2 = Process(target=queue2db, args=(  q2, ))
    
    pw1.start()
    pw2.start()

    info("q1_proces_id=%s"%(str(pw1.pid)))
    info("q2_proces_id=%s"%(str(pw2.pid)))
    run_etl_main(  startdate,endate ,q1,q2,model)
    q1.put(None)
    q2.put(None)
    pw1.join()
    pw2.join()

def runstar(etldate,enddate,model=None):
    if model is None:
        dims_start()
        while int(etldate) <= int(enddate):
            print etldate
            run_etl(etldate,etldate)
            etldate=daycalc(etldate,1)
        dims_finish()
    else:
        dims_start()
        while int(etldate) <= int(enddate):
            print etldate
            run_etl(etldate,etldate,model)
            etldate=daycalc(etldate,1)
        dims_finish()
        

if __name__=='__main__':
    #print "..."
    arglen=len(sys.argv)
    if arglen ==3:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        etldate=startdate
        runstar(etldate,enddate)
        #dims_start()
        #while etldate<=enddate:
        #    print etldate
        #    run_etl(etldate,etldate)
        #    etldate=daycalc(etldate,1)
        #dims_finish()
    elif arglen ==4:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        model=sys.argv[3]
        etldate=startdate
        runstar(etldate,enddate,model)
        #dims_start()
        #while etldate<=enddate:
        #    print etldate
        #    run_etl(etldate,etldate,model)
        #    etldate=daycalc(etldate,1)
        #dims_finish()
    else :
        print "please input python etl_account.py yyyyMMdd yyyyMMdd [model]"
