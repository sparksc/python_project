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
     
from etl.star.model.curtrans import CurTrans
from etl.star.model.fixtrans import FixTrans
from etl.star.model.loantrans import LoanTrans
from etl.star.model.transdetails import Transdetails
from etl.star.model.CORE_BLFMMTRN import BLFMMTRN 
#from etl.star.model.farm_mon_atm import atm_auth_histroy
from etl.star.model.transdetails import Transdetails
from etl.base.logger import info


condecimal = getcontext()

@singleton
class Blfmmtrn():
    """
        交易明细事实
    """
    def __init__(self):
        pass
        
    def files2fact(self,ds,q1):
        d0 = datetime.now()
        insertsql = ds.fact_sql()
        idx = 0 
        d1=datetime.now()
        print "start ,times=",datetime.now()-d1
        rs =[]
        qwork = q1
        count = 1
        for row,newflag in ds.to_fact_row() :     
            if row is None : break
            r = ds.get_one_fact(row) 
            #print r
            idx = idx + 1
            if idx > 10000 :
                print "to_fact_row ,times=",datetime.now()-d1
                info("insert into custvies account 10000:"+str(datetime.now() - d0))
                d0 = datetime.now()
                idx = 0        

            if q1 is None :
                if r is not None:
                    print "####CUST###",r,insertsql
                    pass
            else:
                if r != None:
                    qwork.put( ( insertsql ,r) )
                else:
                    pass
    def loadtofact(self,q1,q2):
        info("db2fact ,custview")
        #self.files2fact(CurTrans(),q1)#活期交易明细
        #self.files2fact(FixTrans(),q1)#定期交易明细
        #self.files2fact(LoanTrans(),q2)#贷款交易明细
     #  self.files2fact(Transdetails(),q2)#交易明细
        #self.files2fact(Posp_auth_histroy(),q2)
        self.files2fact(BLFMMTRN(),q2) 
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
            Blfmmtrn().loadtofact(None,None)
            etldate=int(daycalc(etldate,1))
