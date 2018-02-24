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
     
from etl.star.dim import DimBuTransaction, DimEbillsTranType
from etl.star.model.EBILLS_BU_TRANSACTIONINFO import BuTransaction
from etl.base.logger import info

from etl.star.starbase import StarManage, StarBase

condecimal = getcontext()



def snapshot(etldate):
    """
        按月做一个快照
    """
    sql = """
        insert into SNAP_EBILLS_BU_TRANSACTIONINFO(ID,TXNSERIALNO,PROCESSNO,TRADENO,TRADENAME,BELONGORGNO,TRANSACTORGNO,CURRENTBIZNO,SECONDARYBIZNO,PRIMARYBIZNO,LAUNCHMODENO,LAUNCHDATE,FILENO,CURSIGN,INTERETDATE,ISNEEDDECLARE,DECLAREDATE,ISNEEDACCOUNT,ACCOUNTDATE,ISNEEDSWF,SWFDATE,FINISHEDDATE,REVERSEENTRYDATE,CORPNO,IN_CST_NO,CORP_NAME,HANDLEOPERID,CHECKOPERID,MANAGERID,DEBTNO,FAXNOTE,COUNTRYCODE,DATE_ID,TRAN_TYPE_ID,ORG_ID,AMOUNT,USD_AMOUNT)
        select
        ID,TXNSERIALNO,PROCESSNO,TRADENO,TRADENAME,BELONGORGNO,TRANSACTORGNO,CURRENTBIZNO,SECONDARYBIZNO,PRIMARYBIZNO,LAUNCHMODENO,LAUNCHDATE,FILENO,CURSIGN,INTERETDATE,ISNEEDDECLARE,DECLAREDATE,ISNEEDACCOUNT,ACCOUNTDATE,ISNEEDSWF,SWFDATE,FINISHEDDATE,REVERSEENTRYDATE,CORPNO,IN_CST_NO,CORP_NAME,HANDLEOPERID,CHECKOPERID,MANAGERID,DEBTNO,FAXNOTE,COUNTRYCODE,%d,TRAN_TYPE_ID,ORG_ID,amount,usd_amount
        from (
        select  
            d.ID,d.TXNSERIALNO,d.PROCESSNO,d.TRADENO,d.TRADENAME,d.BELONGORGNO,d.TRANSACTORGNO,d.CURRENTBIZNO,d.SECONDARYBIZNO,d.PRIMARYBIZNO,d.LAUNCHMODENO,d.LAUNCHDATE,d.FILENO,d.CURSIGN,d.INTERETDATE,d.ISNEEDDECLARE,d.DECLAREDATE,d.ISNEEDACCOUNT,d.ACCOUNTDATE,d.ISNEEDSWF,d.SWFDATE,d.FINISHEDDATE,d.REVERSEENTRYDATE,d.CORPNO,IN_CST_NO,CORP_NAME,d.HANDLEOPERID,d.CHECKOPERID,d.MANAGERID,d.DEBTNO,d.FAXNOTE,d.COUNTRYCODE,f.DATE_ID,f.TRAN_TYPE_ID,f.ORG_ID,f.amount,f.usd_amount
            , ROW_NUMBER() OVER (PARTITION BY F.TRAN_ID  ORDER BY F.date_id  desc) RN   from d_EBILLS_BU_TRANSACTIONINFO  d 
             inner join f_EBILLS_BU_TRANSACTIONINFO f on d.id=f.TRAN_ID 
             where f.DATE_ID<=%d
             ) ff 
             where ff.rn=1
    """%(etldate,etldate)
    pass
    db = DBConnect()
    try:
        db.cursor.execute("delete from SNAP_EBILLS_BU_TRANSACTIONINFO f where date_id= ?",(etldate))
        db.cursor.execute(sql)
        db.conn.commit()
    finally:
        db.closeDB()


def starrun(etldate):
    db = DBConnect()
    try:
        db.cursor.execute("delete from F_EBILLS_BU_TRANSACTIONINFO f where date_id= ?",(etldate))
        db.conn.commit()
    finally:
        db.closeDB()
    
    manager = multiprocessing.Manager()
    dim1 = DimBuTransaction()
    dim2 = DimEbillsTranType()
    sm = StarManage(1,[dim1, dim2])
    sm.manager = manager
    sm.start_dim_process()
    sm.start_fact_process()
    sm.setDimQueue()
    sm.start()
    StarBase().files2fact2(BuTransaction(), sm)
    sm.finish()
    snapshot(etldate)

 
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
            starrun(etldate)
            etldate=int(daycalc(etldate,1))
