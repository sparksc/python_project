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
     
from etl.star.dim import  DimAccount2,DimAccountGid
from etl.star.model.jorj import Jorj 
from etl.base.logger import info

from etl.star.model.odsfile import CCRDACCT, CCRDCARD
from etl.star.starbase import StarManage, StarBase
from etl.star.model.odsmerge import mergeall_ccrdfile

condecimal = getcontext()

def starrun(etldate):
    if etldate != 20170101: #第一天，手动生成
        mergeall_ccrdfile(etldate)
    db = DBConnect()
    try:
        db.cursor.execute("delete from F_TRANSACTION f where date_id= ?",(etldate))
        db.conn.commit()
    finally:
        db.closeDB()

    acct = CCRDACCT(etldate).loadfile2dict()
    def card_key(row):
        k = row[0].replace(".","").strip()
        return  k
    cards = CCRDCARD(etldate,"ALL").loadfile2dict2([0], card_key)

    manager = multiprocessing.Manager()
    dg = DimAccountGid()
    dim1 = DimAccount2()
    dim1.start()

    dim2 = DimTransAction()
    dim3 = DimTransActionType()
    #遍历acct
    sm = StarManage(2,[dim1,dim2,dim3,dg])
    sm.manager = manager
    sm.start_dim_process()
    sm.start_fact_process()
    sm.setDimQueue()
    sm.start()


    for k in acct:
        row = acct[k]
        k = k.replace(".","").strip()
        card = cards.get( k )
        ac = None
        sn  = 0
        if card is not None:
            for c in card:
                if ac is None: ac = c
                if c["MASTER_NBR"] == c['CARD_NBR'] and int(Decimal( c["ISSUE_NBR"] ) ) >= sn:
                    ac = c
        if ac is not None :
            row["CARD_NO"] = ac["MASTER_NBR"]
        #row["CST_NAME"] = row["CST_NAME"].decode("gbk").encode("utf8").strip()
        #row["ACCOUNT_NAME"] = row["CST_NAME"].decode("gbk").encode("utf8").strip()
        dim1.find_dim_id_by_ccrd(row)

    StarBase().files2fact2(Jorj(), sm)

    sm.finish()
    dim1.finish()

 


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
