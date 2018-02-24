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
     
from etl.star.model.loan_pt import Loan_pt 
from etl.star.model.loan_aj import Loan_aj
from etl.star.model.loan_tx import Loan_tx
from etl.star.model.loan_liability import Loan_liability
from etl.star.model.loan_contract import Loan_Contract
from etl.base.logger import info


condecimal = getcontext()

@singleton
class LoanHook():
    def __init__(self):
        self.table_desc = util.get_table_desc("ACCOUNT_HOOK")
        
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
            #print r1
            idx = idx + 1
            if idx > 10000 :
                print "to_fact_row ,times=",datetime.now()-d1
                info("insert into loan_hook  100:"+str(datetime.now() - d0))
                idx = 0        
            
            if q1 is None :
                #print "####插入语句测试###",r,accountsql
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
                    if len(rs)>10000:
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
        info("LOAN HOOK")
        #self.files2fact(Loan_liability(),q1,q2)#贷款责任比
        self.files2fact(Loan_Contract(),q1,q2)#贷款合同
        #self.files2fact(Loan_pt(),q1,q2)#普通贷款
        #self.files2fact(Loan_aj(),q1,q2)#按揭贷款
        #self.files2fact(Loan_tx(),q1,q2)#贴现贷款 没有数据
 
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
            LoanHook().loadtofact(None,None)
            etldate=int(daycalc(etldate,1))
