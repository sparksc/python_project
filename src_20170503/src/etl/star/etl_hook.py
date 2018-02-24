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
import etl.star.update.update_hook_balance as uhb
import etl.star.update.update_fbalance_org_id as ufoi

from etl.star.custview import CustView
from etl.star.fbillaccount import FBillAccount
from etl.star.financialsale import FinancialSale
from etl.star.ftransation import FTransAtion
from etl.star.loanhook import LoanHook
from etl.star.deposithook import DepositHook
from etl.star.ebankhook import EbankHook
from etl.star.financeshook import FinancesHook
from etl.star.stockhook import StockHook
from etl.star.insurancehook import InsuranceHook
from etl.star.creditcardhook import CreditcardHook
from datetime import datetime 
#def run_etl_main(startdate,enddate,q1,q2,q3,qbalance,model=None):
def run_etl_main(startdate,enddate,q1,q2,model=None):
    info("start_run_etl_main:%s-%s,model=%s"%(str(startdate),str(enddate),model))
    d1=datetime.now()
    etldate = int(startdate)
    Config().etldate = etldate
        
    while int(etldate) <= int(enddate):
        d1=datetime.now()
        Config().etldate = etldate
        Config().stretldate=util.tostrdate(etldate)
        info("start_run_etl_main while :%s,model=%s"%(str(etldate),model))
        if model == 'L':
            info("run loan_hook")    
            LoanHook().loadtofact(q1,q2)
        elif model =='D':
            info("run deposit_hook")    
            DepositHook().loadtofact(q1,q2)
        elif model =='E':
            info("run ebank_hook")    
            EbankHook().loadtofact(q1,q2)
        elif model =='F':
            info("run finances_hook")    
            FinancesHook().loadtofact(q1,q2)
        elif model =='S':
            info("run stock_hook")    
            StockHook().loadtofact(q1,q2)
        elif model =='I':
            info("run insurance_hook")    
            InsuranceHook().loadtofact(q1,q2)
        elif model =='C':
            info("run creditcard_hook")    
            CreditcardHook().loadtofact(q1,q2)
        else:    
            info("run loan_hook")    
            LoanHook().loadtofact(q1,q2)
            info("run deposit_hook")    
            DepositHook().loadtofact(q1,q2)
            info("run ebank_hook")    
            EbankHook().loadtofact(q1,q2)
            info("run finances_hook")    
            FinancesHook().loadtofact(q1,q2)
            info("run stock_hook")    
            StockHook().loadtofact(q1,q2)
            info("run insurance_hook")    
            InsuranceHook().loadtofact(q1,q2)
            info("run creditcard_hook")    
            CreditcardHook().loadtofact(q1,q2)
        
        etldate=int(daycalc(etldate,1))
    info("finish_run_etl_main:%s,model=%s"%(str(startdate),model))
 
def run_etl(startdate,enddate,model=None):
    info("run_etl:%s-%s,model[%s]"%(str(startdate),str(enddate),model))
    manager = multiprocessing.Manager()
    q1=manager.Queue()
    q2=manager.Queue()
    pw1 = Process(target=queue2db, args=( q1, ))
    pw2 = Process(target=queue2db, args=(  q2, ))
    
    pw1.start()
    pw2.start()
    info("q1_proces_id=%s"%(str(pw1.pid)))
    info("q2_proces_id=%s"%(str(pw2.pid)))
    run_etl_main(  startdate,enddate ,q1,q2,model)
    q1.put(None)
    q2.put(None)
    pw1.join()
    pw2.join()

def starun(startdate,enddate,model):
    info("starun:%s-%s,model[%s]"%(str(startdate),str(enddate),model))
    if model == None: 
        etldate=startdate
        while int(etldate) <= int(enddate):
            ufoi.update_orgid(int(etldate),int(etldate))
            run_etl(etldate,etldate)
            etldate=daycalc(etldate,1)
        uhb.del_dup()
        uhb.insert_miss(int(enddate),'存款')                 #补齐正常数据
        uhb.insert_miss(int(enddate),'理财')                 #补齐正常数据
        uhb.insert_miss_percentage(int(enddate),'存款')      #补齐正常分润数据
        uhb.insert_miss_percentage(int(enddate),'理财')      #补齐正常分润数据
        uhb.update_balance(int(enddate))
        util.fix_seq_id('D_MANAGE','D_MANAGE_SEQ')
    else:
        etldate=startdate
        while int(etldate) <= int(enddate):
            run_etl(etldate,etldate,model)
            etldate=daycalc(etldate,1)
        util.fix_seq_id('D_MANAGE','D_MANAGE_SEQ')



if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen ==3:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        starun(startdate,enddate,None)
    elif arglen ==4:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        model=sys.argv[3]
        starun(startdate,enddate,model)
    else:
        print "please input python etl_account.py yyyyMMdd yyyyMMdd [model]"
