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
     
from etl.star.model.ebank_pool import EbankPool

from etl.star.model.ebank_epay import Ebank_epay 
from etl.star.model.ebank_cb import Ebank_cb 
from etl.star.model.ebank_mb import Ebank_mb 
from etl.star.model.ebank_pb import Ebank_pb 
from etl.star.model.ebank_etc import Ebank_etc 
from etl.star.model.ebank_zfb import Ebank_zfb 
from etl.star.model.ebank_kjzf import Ebank_kjzf 
from etl.base.logger import info



condecimal = getcontext()

@singleton
class EbankHook():
    def __init__(self):
        self.table_desc = util.get_table_desc("CUST_HOOK")
        
    def files2fact(self,ds,q1,q2):
        d0 = datetime.now()
        accountsql = ds.account_sql()
        custsql = ds.cust_sql()
        idx = 0 
        d1=datetime.now()
        print "start ,times=",datetime.now()-d1
        #ds.berfore_transfor()
        rs = []
        rs1 = []
        que = [q1,q2]
        qwork = q1
        #load_dims(qwork)#进程切换    
        count = 1
        for row,flag in ds.to_fact_row() :     
            if flag == False: continue
            if row is None : break
            temp = ds.transfor_one_fact(row,self.table_desc) 
            r=temp[0]
            r1=temp[1]
            #r1 = ds.transfor_one_fact(row,self.table_desc,False) 
            #print r1
            idx = idx + 1
            if idx > 10000 :
                print "to_fact_row ,times=",datetime.now()-d1
                info("insert into deposit_hook  100:"+str(datetime.now() - d0))
                idx = 0        
            
            if q1 is None :
                if r is not None or r1 is not None:
                    #print "####插入语句测试###",r
                    #print "####插入语句测试###",r1
                    pass
                pass
            else:
                if r is not None:
                    rs.append(r)
                    if len(rs)>10000:
                        for ir in rs:
                            qwork.put( ( accountsql ,ir) )
                        rs = []
                        qwork = que[count%2]
                        #load_dims(qwork)#维度表进程切换    
                        count = count+1
                    else:
                        pass
                if r1 is not None:
                    rs1.append(r1)
                    #print r1
                    if len(rs1)>10000:
                        for ir in rs1:
                            qwork.put( ( custsql ,ir) )
                        rs1 = []
                        qwork = que[count%2]
                        #load_dims(qwork)#维度表进程切换    
                        count = count+1
                    else:
                        pass
        if len(rs)>0:
            for ir in rs:
                q1.put((accountsql,ir)) 
        if len(rs1)>0:
            for ir in rs1:
                q1.put((custsql,ir)) 
    def loadtofact(self,q1,q2):
        info("EBANK HOOK")
        d = util.get_ebankhook_typ()
        pool = EbankPool()
        pool.cust_info = d 

        self.files2fact(Ebank_kjzf(),q1,q2)#
        self.files2fact(Ebank_epay(),q1,q2)#
        self.files2fact(Ebank_zfb(),q1,q2)#
        self.files2fact(Ebank_pb(),q1,q2)#
        self.files2fact(Ebank_mb(),q1,q2)#
        self.files2fact(Ebank_cb(),q1,q2)#
        self.files2fact(Ebank_etc(),q1,q2)#
 
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
            EbankHook().loadtofact(None,None)
            etldate=int(daycalc(etldate,1))
