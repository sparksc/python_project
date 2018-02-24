# -*- coding:utf-8 -*-
import os,sys
import DB2  
import csv
import multiprocessing
import os, time, random  
import etl.base.util as util
from decimal import *
from etl.base.conf import Config
from datetime import datetime,timedelta
from multiprocessing import Process,Queue,Pool
from etl.star.model.odsfile import *
     
condecimal = getcontext()
"""
理财业务
"""
def licai_bus(stardate,etldate):
    try:
        oneday=datetime.now()
        db = util.DBConnect()
        print "licai_bus:开始"
        while stardate<=etldate:
            sql0="""
            DELETE FROM  FMS_TRANS_LOG  WHERE DATE_ID=?
            """
            db.cursor.execute(sql0,int(stardate))
            db.conn.commit()
            datas=fms_trans_log(stardate)
            data=[]
            is_repeat="""
            select * from FMS_TRANS_LOG where tran_date=? and APP_SNO=?
            """
            for i in datas:
                db.cursor.execute(is_repeat,[i[1],i[2]])
                qrow=db.cursor.fetchone()
                if qrow is None:
                    data.append(i)

            sql="""
            insert into FMS_TRANS_LOG (DATE_ID,TRAN_DATE,APP_SNO,TEL_TRAN_CODE,ACCEPTMETHOD,TRANS_STATUS,TRAN_BRANCH_CODE,TRAN_TELLER_CODE)
            values(?,?,?,?,?,?,?,?)
            """
            db.cursor.executemany(sql,data)
            db.conn.commit()
            print stardate,"完成",datetime.now()- oneday
            stardate=int(util.daycalc(stardate,1))
    finally :
        db.closeDB()

if __name__=='__main__':
    arglen=len(sys.argv)
    print sys.argv 
    d1=datetime.now()
    if arglen ==3:
        stardate=int(sys.argv[1])
        etldate=int(sys.argv[2])
        print stardate,etldate
        licai_bus(stardate,etldate)
        print "licai_bus",stardate,etldate,"完成",datetime.now()-d1
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
