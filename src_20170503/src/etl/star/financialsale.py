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
     
from etl.star.model.translog import TransLog 
from etl.star.model.fin_prod_enddate import Finprodenddate 
from etl.base.logger import info
from etl.star.model.fin_pro import Finprod 


condecimal = getcontext()

@singleton
class FinancialSale():
    def __init__(self):
        self.table_desc = util.get_table_desc("D_FINACCT")
        
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
        load_dims(qwork)#进程切换    
        count = 1
        for row,flag in ds.to_fact_row() :     
            if flag == False: continue
            if row is None : break
            r = ds.transfor_one_fact(row,self.table_desc) 
            idx = idx + 1
            if idx > 10000 :
                print "to_fact_row ,times=",datetime.now()-d1
                info("insert into F_C_FinancialSale account 10000:"+str(datetime.now() - d0))
                idx = 0        

            if q1 is None :
                print "####理财###",r,insertsql
                #pass
        #print len(ds.acct_fact)        
        for r in ds.acct_fact.values():
            if r != True:rs.append([int(Config().etldate)]+r)
            if len(rs)>10000:
                for ir in rs:
                    qwork.put( ( insertsql ,ir) )
                rs = []
                qwork = que[count%2]
                load_dims(qwork)#进程切换    
                count = count+1
        if len(rs)>0:
            for ir in rs:
                q1.put((insertsql,ir)) 

    def files3fact(self,ds,q1,q2):
        d0 = datetime.now()
        insertsql = ds.fact_sql()
        idx = 0 
        d1=datetime.now()
        print "start ,times=",datetime.now()-d1
        #ds.berfore_transfor()
        rs =[]
        que = [q1,q2]
        qwork = q1
        load_dims(qwork)#进程切换    
        count = 1
        for row,flag in ds.to_fact_row() :     
            if flag == False: continue
            if row is None : break
            r = ds.transfor_one_fact(row,self.table_desc) 
            idx = idx + 1
            if idx > 10000 :
                print "to_fact_row ,times=",datetime.now()-d1
                info("insert into F_C_FinancialSale account 10000:"+str(datetime.now() - d0))
                idx = 0        

            if q1 is None :
                print "####理财###",r,insertsql
                #pass
            else:    
                if r is not None:
                    rs.append(r)
                    if len(rs)>1000:
                        print len(rs),'@'
                        for ir in rs:
                            qwork.put( ( insertsql ,ir) )
                        rs = []
                        qwork = que[count%2]
                        load_dims(qwork)#进程切换    
                        count = count+1
                    else:
                        pass
        print rs,"**********",insertsql,"++++++++++++"
        if len(rs)>0:
            for ir in rs:
                q1.put((insertsql,ir)) 

    def files4fact(self,ds,q1,q2):
       d0 = datetime.now()
       insertsql = ds.fact_sql()
       updatesql = ds.u_sql()
       idx = 0 
       d1=datetime.now()
       print "start ,times=",datetime.now()-d1
       #ds.berfore_transfor()
       rs =[]
       self.hisdict={}
       que = [q1,q2]
       qwork = q1
       #load_dims(qwork)#进程切换    
       count = 1
       for row,flag in ds.to_fact_row() :     
           if flag == False: continue
           if row is None : break
           r,newflag = ds.transfor_one_fact(row,self.table_desc) 
           if newflag:
               runsql=insertsql
           else:
               runsql=updatesql
           idx = idx + 1
           self.hisdict=ds.hisdict
           if idx > 10000 :
               print "to_fact_row ,times=",datetime.now()-d1
               info("insert into fms_prod 10000:"+str(datetime.now() - d0))
               idx = 0        

           if q1 is None and r is not None:
               print "####理财产品信息###",r[0],runsql
               pass
           else:    
               if r is not None:
                   rs.append(r)
                   if len(rs)>0:
                       for ir in rs:
                           qwork.put( ( runsql ,ir) )
                       rs = []
                       qwork = que[count%2]
                       #load_dims(qwork)#进程切换    
                       count = count+1
                   else:
                       pass
       #if len(rs)>0:
       #    for ir in rs:
       #       q1.put((runsql,ir)) 

    def loadtofact(self,q1,q2):
        info("Finprodenddate")
        self.files3fact(Finprodenddate(),q1,q2)#理财产品到期日
        info("Finprodname")
        self.files4fact(Finprod(),q1,q2)#理财产品名称
        info("FMS_TRANS_LOG")
        self.files2fact(TransLog(),q1,q2)#理财余额事实表
 
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
            FinancialSale().loadtofact(None,None)
            etldate=int(daycalc(etldate,1))
