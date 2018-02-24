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

from etl.star.staff import Staff
from etl.star.customer import Customer
from etl.star.custcore import Custcore
from etl.star.custcredit import Custcredit
from etl.star.cust_info_update import Custupdate
from datetime import datetime 
#def run_etl_main(startdate,enddate,q1,q2,q3,qbalance,model=None):
def run_etl_main(startdate,enddate,q1,q2,model=None):
    info("start_run_etl_main:%s,model=%s"%(str(startdate),model))
    d1=datetime.now()
    etldate = int(startdate)
    Config().etldate = etldate
    while int(etldate) <= int(enddate):
        d1=datetime.now()
        Config().etldate = etldate
        Config().stretldate=util.tostrdate(etldate)
        if model == 'S':
            info("run Staff")    
            Staff().loadtofact(q1,q1)
        elif model == 'O':
            info("run Custcore")    
            Custcore().loadtofact(q1,q1)
        elif model == 'C':
            info("run Customer")    
            Customer().loadtofact(q1,q1)
        elif model == 'R':
            info("run Custcredit")    
            Custcredit().loadtofact(q1,q1)
        elif model == 'U':
            info("run Custcredit")    
            Custupdate().loadtofact(q1,q1)
        elif model == 'OCR':
            info("run Customer")
            Customer().loadtofact(q1,q1)
            hisdict=Customer().hisdict
            info("run Custcore")    
            Custcore().loadtofact(q1,q1,hisdict)
            hisdict=Customer().hisdict
            info("run Custcredit")    
            Custcredit().loadtofact(q1,q1,hisdict)
        else:
            info("run Staff")    
            Staff().loadtofact(q1,q1)
            info("run Customer")    
            Customer().loadtofact(q1,q1)
            info("run Custcore")    
            Custcore().loadtofact(q1,q1)
            info("run Custcredit")    
            Custcredit().loadtofact(q1,q1)
        etldate=int(daycalc(etldate,1))
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
    d1=datetime.now()
    run_etl_main(  startdate,endate ,q1,q2,model)
    q1.put(None)
    q2.put(None)
    pw1.join()
    pw2.join()

def starrun(etldate,enddate,model=None):
   if model is None:
       run_etl(etldate,enddate)
   else:
       run_etl(etldate,enddate,model)

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
            #run_etl(etldate,etldate)
            starrun(etldate,etldate)
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
            #run_etl(etldate,etldate,model)
            starrun(etldate,etldate,model)
            etldate=daycalc(etldate,1)
            #run_etl(startdate,enddate,model)
        #dims_finish()
    else :
        print "please input python etl_account.py yyyyMMdd yyyyMMdd [model]"
