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

from etl.star.dim import DimAccountGid,DimAccount2
from etl.star.group  import DimGroup 

from etl.star.model.dqab import DQAB
from etl.star.model.hqab import HQAB
from etl.star.model.dqabc import DQABC
from etl.star.model.odsmerge import  mergeallfile

FIRSTDATE = 20151220
def put_ds_data(ds1, sm, etldate):
    factsql = ds1.fact_sql()[0]
    d  = ds1.last_type
    cols =  ds1.fact_cols 
    for k in d:
        data = d[k]
        data["DATE_ID"] = etldate

        if str(etldate)[4:8] == '0101':
            data["YEAR_PDT"] = data["BALANCE"] 
        else:
            data["YEAR_PDT"] = data["BALANCE"] + data["YEAR_PDT"]

        data["LAST_BALANCE"] = data["BALANCE"] 
        row = [ data[c] for c in cols]

        #年积数为0,不进入系统
        if data["ACCOUNT_CLASS"] == 'D' or data["ACCOUNT_CLASS"] == 'C':
            if int(str(etldate)[4:8]) >= 102 and data["YEAR_PDT"] == 0:
                continue
        else:
            cd = data["CLOSE_DATE"]
            if int(str(etldate)[4:8]) >= 102 and data["YEAR_PDT"] == 0 and cd != 18991231 and cd < etldate:
                continue
        sm.put_fact_data( (factsql, row) )

def starun(etldate):

    db = DBConnect()
    try:
        print "delete from F_ACCOUNT_BALANCE",etldate
        #db.cursor.execute("delete from F_ACCOUNT_BALANCE f where ACCOUNT_CLASS='D' and date_id= ?",(etldate))
        #db.cursor.execute("delete from F_ACCOUNT_BALANCE f where ACCOUNT_CLASS='H' and date_id= ?",(etldate))
        #db.cursor.execute("delete from F_ACCOUNT_BALANCE f where ACCOUNT_CLASS='C' and date_id= ?",(etldate))
        db.cursor.execute("delete from F_ACCOUNT_BALANCE f where date_id= ?",(etldate))
        db.conn.commit()
        print "finish delete from F_ACCOUNT_BALANCE",etldate
    finally:
        db.closeDB()
    lastdate = int(util.daycalc(etldate,-1))

    #if etldate != FIRSTDATE:
    #    mergeallfile(etldate)

    act2 = DimAccount2()
    act2.start()

    ac = DimAccountGid()

    dim1 = DimAccountTypeExtend()
    dim2 = DimGroup()
    sm = StarManage(10,[dim1,dim2,ac,act2])
    sm.start_dim_process()
    sm.start_fact_process()
    sm.setDimQueue()
    sm.start()

    ds3 = HQAB()
    if etldate >= ds3.firstday:
        StarBase().files2fact2(ds3, sm)
    if etldate >= ds3.firstday:
        put_ds_data(ds3, sm, etldate)
    sm.restart_fact_process()
   
   
    ds1 = DQAB()
    if etldate >= ds1.firstday:
        StarBase().files2fact2(ds1, sm)
    if etldate >= ds1.firstday:
        put_ds_data(ds1, sm, etldate)
    sm.restart_fact_process()

    ds2 = DQABC()
    if etldate >= ds2.firstday:
        StarBase().files2fact2(ds2, sm)
    if etldate >= ds2.firstday:
        put_ds_data(ds2, sm, etldate)
    sm.restart_fact_process()

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
            print '************** ',etldate,'start **************'
            Config().etldate =etldate
            Config().stretldate=util.tostrdate(etldate)        
            starun(etldate)
            print '************** ',etldate,' end  **************'
            etldate=int(daycalc(etldate,1))
