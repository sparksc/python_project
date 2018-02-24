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

from etl.star.epay import EPay
from etl.star.atm import ATM
#from etl.star.pos import POS
from etl.star.terminal import Terminal
from etl.star.loancontract import loanCon
#from etl.star.ccrdmpur import CCRDMPUR
from etl.star.ccrdacct import CCRDACCT
from etl.star.zfbkj import ZFBKJ
from datetime import datetime 
#def run_etl_main(startdate,enddate,q1,q2,q3,qbalance,model=None):
def run_etl_main(startdate,enddate,q1,q2,model=None):
    print "load dims "
    info("start_run_etl_main:%s,model=%s"%(str(startdate),model))
    d1=datetime.now()
    etldate = int(startdate)
    Config().etldate = etldate
    #load_dims(q1,q2,q3) 

    #TBD CCRD MPUR跑,跑完打开 plwu
    load_dims(q2)  
    print "load dims ,times=",datetime.now()-d1
    print "run_etl_man step1..."        
    print etldate

    if model == 'E':
        util.delete_contract(etldate,int(enddate),'丰收e支付')
        util.delete_contract(etldate,int(enddate),'新丰收e支付')
    elif model == 'L':
        util.delete_contract(etldate,int(enddate),'贷款合同')
    elif model == 'T':
        util.delete_contract(etldate,int(enddate),'自助终端')
    elif model == 'A':
        util.delete_contract(etldate,int(enddate),'ATM')
    elif model == 'P':
        util.delete_contract(etldate,int(enddate),'POS')
    elif model == 'Z':
        util.delete_contract(etldate,int(enddate),'支付宝快捷支付')
    elif model == 'C':
        util.delete_creditbad2(etldate,int(enddate))
    elif model == 'CM':
        util.delete_creditmpur(etldate,int(enddate))
        util.delete_creditbad2(etldate,int(enddate)) #TBD
    else:
        util.delete_contract(etldate,int(enddate),'丰收e支付')
        util.delete_contract(etldate,int(enddate),'新丰收e支付')
        util.delete_contract(etldate,int(enddate),'贷款合同')
        util.delete_contract(etldate,int(enddate),'支付宝快捷支付')
        #util.delete_creditmpur(etldate,int(enddate))
        #util.delete_creditbad2(etldate,int(enddate)) #TBD

    while int(etldate) <= int(enddate):
        print "run_etl_main step2...",etldate    
        info("run_etl_main step2:%d,model=%s"%( int(etldate),model) )
        d1=datetime.now()
        Config().etldate = etldate
        Config().stretldate=util.tostrdate(etldate)
        if model == 'E':
            info("run EPAY")    
            EPay().loadtofact(q1,q1)
        elif model == 'L':
            info("run LOANCONTRACT")
            loanCon().loadtofact(q1,q1)
        elif model == 'CM':
            info("run CCRDMPUR")    
        elif model == 'T':
            info("run TERMINAL")    
            Terminal().loadtofact(q1,q1)
        elif model == 'A':
            info("run ATM")    
            ATM().loadtofact(q1,q1)
        elif model == 'P':
            info("run POS")    
            POS().loadtofact(q1,q1)
        elif model == 'Z':
            info("run ZFBKJ")    
            ZFBKJ().loadtofact(q1,q1)
        else:
            info("run EPAY")    
            EPay().loadtofact(q1,q1)
            info("run CCRDACCT")    
            info("run ZFBKJ")    
            ZFBKJ().loadtofact(q1,q1)
            loanCon().loadtofact(q1,q1) #贷款合同
        etldate=int(daycalc(etldate,1))
        util.fix_seq_id('D_CUST_CONTRACT','D_CUST_CONTRACT_SEQ')
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

if __name__=='__main__':
    #print "..."
    arglen=len(sys.argv)
    if arglen ==3:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        etldate=startdate
        while int(etldate) <= int(enddate):
            print etldate
        #dims_start()
            run_etl(etldate,etldate)
            etldate=daycalc(etldate,1)
        #dims_finish()
    elif arglen ==4:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        model=sys.argv[3]
        #dims_start()
        etldate=startdate
        while int(etldate) <= int(enddate):
            print etldate
            run_etl(etldate,etldate,model)
            etldate=daycalc(etldate,1)
            #run_etl(startdate,enddate,model)
        #dims_finish()
    else :
        print "please input python etl_account.py yyyyMMdd yyyyMMdd [model]"
