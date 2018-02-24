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
     
condecimal = getcontext()
"""
信用卡不良报表
"""
def credit_bad(stardate,etldate):
    try:
        oneday=datetime.now()
        db = util.DBConnect()
        while stardate<=etldate:
            sql0 = """
            UPDATE YDW.REPORT_CREDIT_BAD 
                SET  BAD_BAL=0, ALL_BAL=0, PPL_BAL=0
                    WHERE DATE_ID=?
            """
            db.cursor.execute(sql0,int(stardate))
            db.conn.commit()

            sql1="""
            SELECT SUM(REM_PPL),F.DATE_ID, D.MANAGER_NO  FROM F_CREDIT_MPUR_20161031 F
            INNER JOIN (SELECT DISTINCT A.MANAGER_NO,D.ACCOUNT_NO FROM CREDIT_BAD_HOOK A INNER JOIN D_CREDIT_CARD D ON D.CARD_NO=A.CARD_NO) D ON D.ACCOUNT_NO=F.ACCOUNT_NO
            WHERE F.DATE_ID = ? 
            GROUP BY F.DATE_ID, D.MANAGER_NO
            """
            db.cursor.execute(sql1,int(stardate))
            row1=db.cursor.fetchall()
            resultrow1=[]
            for i in row1:
                t=list(i[0:])
                resultrow1.append(t)
            sql2="""
            UPDATE REPORT_CREDIT_BAD SET PPL_BAL=? WHERE DATE_ID=?  AND SALE_CODE=?
            """
            db.cursor.executemany(sql2,resultrow1)
            """不良 BAD_BAL"""
            sql2="""
            SELECT SUM(CASE WHEN F.MTHS_ODUE > 0 THEN F.STM_BALFRE+F.STM_BALINT+F.STM_BALMP+F.BAL_FREE +F.BAL_INT+F.BAL_MP ELSE 0 END) BAD_BAL,--不良透支金额
            SUM(F.STM_BALFRE+F.STM_BALINT+F.STM_BALMP+F.BAL_FREE +F.BAL_INT+F.BAL_MP) ALL_BAL,  --总额(少分期)                                               
            F.DATE_ID , A.MANAGER_NO                                                                                                                          
            FROM F_CREDIT_BAD F               
            INNER JOIN D_CREDIT_CARD D ON D.ID=F.CRAD_ID
            INNER JOIN (SELECT DISTINCT A.MANAGER_NO,D.ACCOUNT_NO,A.FLAG FROM CREDIT_BAD_HOOK A INNER JOIN D_CREDIT_CARD D ON D.CARD_NO=A.CARD_NO) A ON A.ACCOUNT_NO=D.ACCOUNT_NO
            WHERE F.DATE_ID = ? AND ( -F.BAL_FREE + (CASE WHEN F.BAL_INT_FLAG='-' THEN F.BAL_INT ELSE -F.BAL_INT END) -F.STM_BALFRE  + (CASE WHEN F.STMBALINT_FLAG='-' THEN F.STM_BALINT ELSE -F.STM_BALINT END) -F.BAL_MP - F.STM_BALMP ) < 0 AND F.CLOSE_CODE NOT IN ('W','Q','WQ')
            GROUP BY F.DATE_ID,A.MANAGER_NO       
            """
            db.cursor.execute(sql2,int(stardate))
            row2=db.cursor.fetchall()
            resultrow2=[]
            for i in row2:
                t=list(i[0:])
                resultrow2.append(t)
            sql8="""
            UPDATE REPORT_CREDIT_BAD SET BAD_BAL=?, ALL_BAL=? WHERE DATE_ID=?  AND SALE_CODE=?
            """
            db.cursor.executemany(sql8,resultrow2)
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
        credit_bad(stardate,etldate)
        print stardate,"完成",datetime.now()-d1
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
