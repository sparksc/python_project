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
     
from etl.star.dim import  DimCCRDAccount
from etl.base.logger import info

from etl.star.starbase import StarManage, StarBase
from etl.star.model.deposit_hq  import Deposit_hq


condecimal = getcontext()

def starrun(etldate):
    sm = StarManage([])
    StarBase().files2fact(Deposit_hq(), sm)

 


if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen != 3:
        print "please input python %s yyyyyMMdd yyyyMMdd "%(sys.argv[0])
    else:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        etldate=int(startdate)
        while etldate<=int(enddate):    
            print etldate
            Config().etldate =etldate
            Config().stretldate=util.tostrdate(etldate)        
            starrun(etldate)
            etldate=int(daycalc(etldate,1))
