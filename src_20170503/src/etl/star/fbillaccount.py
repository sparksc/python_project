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
     
from etl.star.model.billaccount import BillAccount
from etl.base.logger import info


condecimal = getcontext()

@singleton
class FBillAccount():
    def __init__(self):
        pass
        
    def files2fact(self,ds,q1,q2):
        d0 = datetime.now()
        insertsql = ds.fact_sql()
        idx = 0 
        d1=datetime.now()
        print "start ,times=",datetime.now()-d1
        #ds.berfore_transfor()
        rs =[]
        que = [q1,q2]
        qwork = q1
        count = 1
        for row,flag in ds.to_fact_row() :     
            if flag == False: continue
            if row is None : break
            r = ds.transfor_one_fact(row) 
            idx = idx + 1
            if idx > 10000 :
                print "to_fact_row ,times=",datetime.now()-d1
                info("insert into FBillAccount account 10000:"+str(datetime.now() - d0))
                idx = 0        

            if q1 is None :
                print "####承兑###",r,insertsql
                #pass
        print "idx",idx
        for r in ds.acct_fact.values():
            #print r
            if r != True:
                rs.append([int(Config().etldate)]+r)
            #rs.append([int(Config().etldate)]+r)
            if len(rs)>1000:
                for ir in rs:
                    qwork.put( ( insertsql ,ir) )
                rs = []
        if len(rs)>0:
            print len(rs)
            for ir in rs:
                q1.put((insertsql,ir)) 
            rs = []
    def loadtofact(self,q1,q2):
        info("billaccount")
        self.files2fact(BillAccount(),q1,q2)#承兑余额事实表
 
if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen != 3:
        print "please input python %s yyyyyMMdd yyyyMMdd "%(sys.argv[0])
    else:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        etldate=int(startdate)
        while etldate<=int(enddate):    
            Config().etldate =etldate
            Config().stretldate=util.tostrdate(etldate)        
            FBillAccount().loadtofact(None,None)
            etldate=int(daycalc(etldate,1))
