# -*- coding:utf-8 -*-
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random  
from datetime import datetime,timedelta
from decimal import *
import DB2  
import csv

import etl.base.util as util
from etl.base.conf import Config
import man_dep_sal as depsal
     
condecimal = getcontext()
"""
客户经理旧欠不良
"""
def loan_old(stardate,etldate):
    try:
        oneday=datetime.now()
        db = util.DBConnect()
        while stardate<=etldate:
            yearmonth=str(stardate)[0:6]
            print yearmonth
            """先删除再插入"""
            sql0="""
            DELETE FROM OLD_BAD_LOANS WHERE LCAJDATE=%s
            """%(yearmonth)
            db.cursor.execute(sql0)
            sql="""
            INSERT INTO OLD_BAD_LOANS ( AFAABRNO ,ORG0_NAME,LCAJDATE,DONE_DATE_ID ,RES1,RES2,RES3)
            SELECT LCAABRNO ,ORG0_NAME,LCAJDATE,DUE_DATE_ID ,RES1,RES2,RES3 FROM
            (   (SELECT RNAGBRNO AS LCAABRNO,O.ORG0_NAME,LEFT(RNAUDATE,6) AS  LCAJDATE,D.DUE_DATE_ID, SUM(RNAUAMT ) AS RES1,
            SUM(RNARIAM2 + RNATIAM2+ RNBMIAM2+RNBNIAM2+RNCCIAM2) AS RES2,
            SUM(0) AS RES3
            FROM F_CORE_BLFMMTRN F
            JOIN D_LOAN_ACCOUNT D ON D.ACCOUNT_NO = F.RNAAAC15  AND DAYS(TO_DATE(F.RNAUDATE,'YYYYMMDD'))>DAYS(TO_DATE(D.DUE_DATE_ID,'YYYYMMDD'))
            JOIN D_ORG O ON F.RNAGBRNO=O.ORG0_CODE
            WHERE RNABNOTE IN ('柜面收本金','柜面收本息','柜面收利息 ','自动收本金','自动收本息','自动收利息 ') 
            AND D.DUE_DATE_ID <= 20151231 AND RNAAWBFG='1' AND LEFT(RNAUDATE,6)=%s
            GROUP BY RNAGBRNO,O.ORG0_NAME,LEFT(RNAUDATE,6),D.DUE_DATE_ID)
            UNION ALL
            (SELECT BL.AFAABRNO,O.ORG0_NAME,LEFT(BL.AFBKDATE,6) AS LCAJDATE ,LA.DUE_DATE_ID,SUM(BL.PRINCIPAL) AS RES1,SUM(INTEREST) AS RES2,SUM(0) AS RES3
            FROM F_CORE_BLFMCNAF BL --核销贷款明细
            INNER JOIN D_LOAN_ACCOUNT LA ON BL.AFAAAC15=LA.ACCOUNT_NO AND  DAYS(TO_DATE(BL.AFBKDATE,'YYYYMMDD')) > DAYS(TO_DATE(LA.DUE_DATE_ID,'YYYYMMDD')) 
            INNER JOIN D_ORG O ON BL.AFAABRNO=O.ORG0_CODE
            WHERE LA.DUE_DATE_ID<20160101 AND LEFT(BL.AFBKDATE,6)=%s
            GROUP BY BL.AFAABRNO,O.ORG0_NAME,LEFT(BL.AFBKDATE,6),LA.DUE_DATE_ID)   )
            """%(yearmonth,yearmonth)
            db.cursor.execute(sql)
            #row = db.cursor.fetchall()
            #resultrow=[]
            #for i in row:
            #    t=list(i[0:])
            #    resultrow.append(t)
            ##print resultrow
            #db.cursor.executemany(sql1,resultrow)
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
        loan_old(stardate,etldate)
        print stardate,etldate,"完成",datetime.now()-d1
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
