# -*- coding:utf-8 -*-
#!/bin/python  

from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random,sys 
from datetime import datetime,timedelta
from decimal import *
import DB2  
from pprint import pprint

from etl.base.conf import *
import etl.base.util as util
from etl.star.dim import *
from etl.star.transformdict import *
from etl.base.singleton import singleton
     
from etl.star.dim import  DimAccount2,DimAccountGid
from etl.star.model.jorj import Jorj 
from etl.base.logger import info

from etl.star.model.odsfile import CCRDACCT, CCRDCARD
from etl.star.starbase import StarManage, StarBase
from etl.star.model.mbbpaccinf import MBPBACCINF
from etl.star.model.pa_quoteprice import PA_QUOTEPRICE

condecimal = getcontext()

def starrun(etldate):
    db = DBConnect()
    try:
        db.cursor.execute("delete from MB_PB_ACCINF where date_id = ?",(etldate))
        db.conn.commit()

        db.cursor.execute("delete from ODS_EBILLS_PA_QUOTEPRICE where date_id = ?",(etldate))
        db.conn.commit()
    finally:
        db.closeDB()

    sm = StarManage(1,[])
    sm.start_dim_process()
    sm.start_fact_process()
    sm.setDimQueue()
    sm.start()
    StarBase().files2fact2(MBPBACCINF(), sm)
    StarBase().files2fact2(PA_QUOTEPRICE(), sm)
    sm.finish()

    db = DBConnect()
    try:
        usql ="""
            merge into MB_PB_ACCINF f
            using (select  distinct account_no,cst_id,cst_no from d_account  aa where aa.account_class in ('定期分户','活期分户') ) a 
                on f.date_id = ? and a.account_no =f.MAIF_ACCNO 
            when matched then update set f.cst_no=a.cst_no,f.cst_id=a.cst_id
        """
        db.cursor.execute(usql,(etldate))
        db.conn.commit()
    finally:
        db.closeDB()


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
