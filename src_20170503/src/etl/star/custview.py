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
     
from etl.star.model.fcustview import F_CustView
from etl.base.logger import info


condecimal = getcontext()

@singleton
class CustView():
    def __init__(self):
        self.table_desc = util.get_table_desc("D_CUST")
        
    def db2fact(self,ds,q1,q2):
        d0 = datetime.now()
        insertsql = ds.fact_sql()
        idx = 0 
        d1=datetime.now()
        print "start ,times=",datetime.now()-d1
        rs =[]
        que = [q1,q2]
        qwork = q1
        count = 1
        for row in ds.to_fact_row() :     
            if row is None : break
            r = ds.get_one_fact(row,self.table_desc) 
            idx = idx + 1
            if idx > 10000 :
                print "to_fact_row ,times=",datetime.now()-d1
                info("insert into custvies account 10000:"+str(datetime.now() - d0))
                d0 = datetime.now()
                idx = 0        

            if q1 is None :
                print "####CUST###",r,insertsql
                #pass
            else:
                if r != False:
                    rs.append(r)
                    if len(rs)>10000:
                        for ir in rs:
                            qwork.put( ( insertsql ,ir) )
                        rs = []
                        qwork = que[count%2]
                        load_dims(qwork)#维度表进程切换    
                        count = count+1
                    else:
                        pass
        if len(rs)>0:
            for ir in rs:
                q1.put((insertsql,ir)) 
    def loaddbtofact(self,q1,q2):
        info("db2fact ,custview")
        self.db2fact(F_CustView(),q1,q2)#客户资产负债表
 
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
            CustView().loaddbtofact(None)
            etldate=int(daycalc(etldate,1))
