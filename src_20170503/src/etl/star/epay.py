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
     
from etl.star.model.fsepay import FsEPay 
from etl.base.logger import info


condecimal = getcontext()

@singleton
class EPay():
    def __init__(self):
        self.table_desc = util.get_table_desc("D_CUST_CONTRACT")
        
    def files2fact(self,ds,q1,q2):
        d0 = datetime.now()
        insertsql = ds.fact_sql()
        idx = 0 
        d1=datetime.now()
        print "start ,times=",datetime.now()-d1
        #print 123
        #ds.berfore_transfor()
        rs =[]
        que = [q1,q2]
        qwork = q1
        load_dims(qwork)#进程切换    
        print "after load_dims,times=",datetime.now()-d1
        count = 1
        for row,flag in ds.to_fact_row() :     
            if flag == False: continue
            if row is None : break
            r = ds.transfor_one_fact(row,self.table_desc) 
            idx = idx + 1
            if idx > 10000 :
                print "to_fact_row ,times=",datetime.now()-d1
                info("insert into f_contract_status 10000:"+str(datetime.now() - d0))
                idx = 0        

            if q1 is None :
                print "####丰收e支付###",r,insertsql
                pass
            else:    
                if r is not None:
                    rs.append(r)
                    if len(rs)>1000:
                        for ir in rs:
                            qwork.put( ( insertsql ,ir) )
                        rs = []
                        qwork = que[count%2]
                        load_dims(qwork)#进程切换    
                        count = count+1
                    else:
                        pass
        rows = ds.contract_fact.values() 
        print "data length :" ,len(rows)
        for r in  rows :
            rs.append(r)
            if len(rs)>1000:
                for ir in rs:
                    qwork.put( ( insertsql ,ir) )
                rs = []
                qwork = que[count%2]
                load_dims(qwork)#进程切换    
                count = count+1
        if len(rs)>0:
            for ir in rs:
               q1.put((insertsql,ir)) 
    def loadtofact(self,q1,q2):
        info("丰收e支付")
        self.files2fact(FsEPay(),q1,q2)#
 
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
            EPay().loadtofact(None,None)
            etldate=int(daycalc(etldate,1))
