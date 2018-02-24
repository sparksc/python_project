# -*- coding:utf-8 -*-
#!/bin/python  

from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random,sys 
from datetime import datetime,timedelta

from etl.base.conf import *
import etl.base.util as util
from etl.star.dim import *
from etl.star.transformdict import *
from etl.base.singleton import singleton
     
from etl.base.logger import info

from etl.star.starbase import StarManage, StarBase


from etl.star.model.ccrdacct2 import CcrdAcct2


def starun(etldate):

    db = DBConnect()
    try:
        db.cursor.execute("delete from F_CREDIT_BAD where date_id= ?",(etldate))
        db.conn.commit()
    finally:
        db.closeDB()
    lastdate = int(util.daycalc(etldate,-1))

    sm = StarManage(2,[])
    #sm.start_dim_process()
    sm.start_fact_process()
    #sm.setDimQueue()
    sm.start()

    ds1 = CcrdAcct2()
    StarBase().files2fact2(ds1, sm)
    sm.finish()


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
            starun(etldate)
            etldate=int(daycalc(etldate,1))
