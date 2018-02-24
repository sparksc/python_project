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
     
#from etl.star.model.loan_pt import Loan_pt 
#from etl.star.model.loan_aj import Loan_aj
#from etl.star.model.loan_tx import Loan_tx
from etl.star.model.loan_liabilty import Loan_Liabilty
from etl.base.logger import info


condecimal = getcontext()

@singleton
class LoanHook():
    def __init__(self):
        self.table_desc = util.get_table_desc("ACCOUNT_HOOK")
        
    def files2fact(self,ds):
        try:
            db = util.DBConnect()
            custsql = ds.cust_sql()
            rs =[]
            idx=0
            for row,flag in ds.to_fact_row() :     
                if flag == False: continue
                if row is None : break
                r = ds.transfor_one_fact(row,self.table_desc) 
                if not r: continue
                idx = idx + 1
                rs.append(r)
                if idx > 10000 :
                    print "to_fact_row ,times=",datetime.now()-d1
                    info("insert into loan_hook  100:"+str(datetime.now() - d0))
                    idx = 0        
                    #print rs
                    db.cursor.executemany(custsql,rs)
                    db.conn.commit()
                    rs = []
            if len(rs)>0:
                #print rs
                db.cursor.executemany(custsql,rs)
                db.conn.commit()
                rs = []
        finally :
            db.closeDB()
           
    def makeloan2dep(self,etldate):
        try:
            db = util.DBConnect()
            mersql = """
                merge into ACCOUNT_HOOK a 
                using(
                    select d.account_no,c.MANAGER_NO teller_no,d.THIRD_BRANCH_CODE BRANCH_CODE,min(d.open_date_id,?) open_date_id 
                    from CUST_HOOK c 
                    inner join m_dep_account d on d.cst_no = c.cust_in_no and d.account_class in ('定期分户','活期风户')  
                    where d.account_no not in  (select a.account_no from account_hook a)
                ) t on a.account_no =  t.account_no
                when not matched then 
                    INSERT (ACCOUNT_NO,MANAGER_NO,ORG_NO,PERCENTAGE,HOOK_TYPE,START_DATE,END_DATE,STATUS,ETL_DATE,SRC,TYP,MAKEUP) 
                    VALUES(t.ACCOUNT_NO,t.teller_no,t.BRANCH_CODE,100,'存贷挂钩',t.open_date_id,30001231,'正常',?,'后端认定','存款','否')"""
            print etldate,etldate
            db.cursor.execute(mersql,[etldate,etldate])
            db.conn.commit()
        finally :
            db.closeDB()

 
    def loadtofact(self,q1,q2):
        info("LOAN HOOK")
        self.files2fact(Loan_Liabilty())#贷款责任登记簿
        #self.makeloan2dep(Config().etldate)
 
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
