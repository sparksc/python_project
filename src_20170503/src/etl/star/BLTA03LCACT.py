# -*- coding:utf-8 -*-
#!/bin/python

"""
逾期还款清单
"""

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
from etl.star.BLTA03LCINSERT import FTransAtion
#from etl.star.gas import GAS
#from etl.star.gas_branch import GAS_BRANCH
#from etl.star.gas_do6 import GAS_DO6
#from etl.star.gas_kj import GAS_KJ
from etl.star.model.translog import *
#from etl.star.update.update_manage_org_bal import update_org_manage_bal
from etl.star.update.update_last_trade_date import update_ltd
from etl.star.update.update_fbalance_org_id import update_orgid
from datetime import datetime 
#def run_etl_main(startdate,enddate,q1,q2,q3,qbalance,model=None):
def run_etl_main(startdate,enddate,q1,q2,model=None):
    print "load dims "
    info("start_run_etl_main:%s,model=%s"%(str(startdate),model))
    d1=datetime.now()
    etldate = int(startdate)
    Config().etldate = etldate
    #load_dims(q1,q2,q3) 
    load_dims(q2) 
    print "load dims ,times=",datetime.now()-d1
    print "run_etl_man step1..."        
    print etldate
    if model == 'C':
        util.delete_fcustview(etldate,int(enddate))
    elif model == 'F':
        util.delete_financialsale(etldate,int(enddate))
    elif model == 'T':
        util.delete_blta(etldate,int(enddate))
    elif model == 'BILL':
        util.delete_fbillacount(etldate,int(enddate))
    elif model =='GAS':
        util.delete_gasaccount(etldate,int(enddate))
    else:
        #util.delete_fcustview(etldate,int(enddate))
        util.delete_financialsale(etldate,int(enddate))
        util.delete_fcacctjrnl(etldate,int(enddate))
        util.delete_fbillacount(etldate,int(enddate))

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
        elif model == 'BILL':
            info("run Fbill")
            FBillAccount().loadtofact(q2,q2)    
        elif model =='GAS':
            info("run gas")
            GAS().loadtofact(q2,q2)
            GAS_BRANCH().loadtofact(q2,q2)
            GAS_DO6().loadtofact(q2,q2)
            GAS_KJ().loadtofact(q2,q2)
        else:
            #info("run CUSTVIEW")    
            #CustView().loaddbtofact(q1,q1)
            info("run financialsale")
            FinancialSale().loadtofact(q2,q2)    
            info("run FTransAtion")
            FTransAtion().loadtofact(q2,q2)    
            info("run Fbill")
            FBillAccount().loadtofact(q2,q2)    
        #update_org_manage_bal(etldate)    
        #update_ltd(etldate,etldate)
        #update_orgid(etldate,etldate)
        etldate=int(daycalc(etldate,1))
        util.fix_seq_id('D_ACCOUNT','D_ACCOUNT_SEQ_NEW')
    q1.put(None)
    q2.put(None)
    #q3.put(None)
    info("finish_run_etl_main:%s,model=%s"%(str(startdate),model))
 
def run_etl(startdate,endate,model=None):
    manager = multiprocessing.Manager()
    q1=manager.Queue()
    q2=manager.Queue()
    #q3=manager.Queue()
    #qbalance=manager.Queue()
    pw1 = Process(target=queue2db, args=( q1, ))
    pw2 = Process(target=queue2db, args=(  q2, ))
    #pw3 = Process(target=queue2db, args=(  q3, ))
    #pw4 = Process(target=queue2db, args=( qbalance, ))
    #pw5 = Process(target=run_etl_main, args=(  startdate,endate ,q1,q2,q3 ,qbalance))
    
    print "start queue2db 1"
    pw1.start()
    print "start queue2db 2"
    pw2.start()
    print "start queue2db 3"    
    #pw3.start()
    print "start queue2db 4"    
    #pw4.start()
    #print "start queue2db 5"    
    #pw5.start()
    #run_etl_main(  startdate,endate ,q1,q2,q3,qbalance,model)
    d1=datetime.now()
    run_etl_main(  startdate,endate ,q1,q2,model)
    #pw5.join()
    print "wait queue"
    #pw4.join()
    #print "balance insert finish"
    pw1.join()
    print "dim insert finish",datetime.now()-d1
    #pw3.join()
    pw2.join()
    print "pw2 insert finish",datetime.now()-d1
    #插入表到d_account,d_cust
if __name__=='__main__':
    #print "..."
    arglen=len(sys.argv)
    if arglen ==3:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        etldate=startdate
        dims_start()
        while etldate<=enddate:
            print etldate
            run_etl(etldate,etldate)
            etldate=daycalc(etldate,1)
        dims_finish()
    elif arglen ==4:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        model=sys.argv[3]
        etldate=startdate
        dims_start()
        while etldate<=enddate:
            print etldate
            run_etl(etldate,etldate,model)
            etldate=daycalc(etldate,1)
        dims_finish()
    else :
        print "please input python etl_account.py yyyyMMdd yyyyMMdd [model]"
