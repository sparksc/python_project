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
如果哪天的insert 补齐销户账户跑啦两次 执行此脚本
"""
def man_dep(stardate,etldate):
    try:
        oneday=datetime.now()
        db = util.DBConnect()
        while stardate<=etldate:
            sql="""
            DELETE FROM F_BALANCE_TEMP
            """
            db.cursor.execute(sql)
            db.conn.commit()
            sql1="""
            INSERT INTO YDW.F_BALANCE_TEMP(ACCOUNT_ID, ACCOUNT_TYPE_ID, MANAGE_ID, DATE_ID, ACCOUNT_STATUS_ID, ACCOUNT_PRICE_ID, BALANCE, OUT_BALANCE, CONTRACT_AMT, DR_AMOUNT, CR_AMOUNT, YEAR_PDT, RE_BALANCE, SUM_RE_INTEREST, LUPD_DATE_ID, IN_TO_OUT_AMOUNT, INT_BAL, ACCT_TYPE, CST_NO, INT_AMOUNT, NEXT_INT_DATE_ID, CLAC_INT, LAST_RECV_DATE, LAST_CINT_DATE, RELA_DEP_BAL, ORG_ID, CST_ID, ACCOUNT_TYPE2_ID)
            SELECT ACCOUNT_ID, ACCOUNT_TYPE_ID, MAX(MANAGE_ID), DATE_ID, ACCOUNT_STATUS_ID, ACCOUNT_PRICE_ID, BALANCE, OUT_BALANCE, CONTRACT_AMT, DR_AMOUNT, CR_AMOUNT, YEAR_PDT, RE_BALANCE, SUM_RE_INTEREST, LUPD_DATE_ID, IN_TO_OUT_AMOUNT, INT_BAL, ACCT_TYPE, CST_NO, INT_AMOUNT, NEXT_INT_DATE_ID, CLAC_INT, LAST_RECV_DATE, LAST_CINT_DATE, RELA_DEP_BAL, MAX(ORG_ID), CST_ID, ACCOUNT_TYPE2_ID FROM F_BALANCE_TMP_TMP FF 
            WHERE FF.ACCOUNT_ID IN  ( SELECT F.ACCOUNT_ID FROM F_BALANCE_TMP_TMP F WHERE F.DATE_ID = ? AND F.ACCT_TYPE = '1' AND F.BALANCE = 0 GROUP BY F.ACCOUNT_ID HAVING COUNT(*) > 1)
            AND  FF.DATE_ID = ? AND FF.ACCT_TYPE = '1' AND FF.BALANCE = 0  GROUP BY ACCOUNT_ID, ACCOUNT_TYPE_ID, DATE_ID, ACCOUNT_STATUS_ID, ACCOUNT_PRICE_ID, BALANCE, OUT_BALANCE, CONTRACT_AMT, DR_AMOUNT, CR_AMOUNT, YEAR_PDT, RE_BALANCE, SUM_RE_INTEREST, LUPD_DATE_ID, IN_TO_OUT_AMOUNT, INT_BAL, ACCT_TYPE, CST_NO, INT_AMOUNT, NEXT_INT_DATE_ID, CLAC_INT, LAST_RECV_DATE, LAST_CINT_DATE, RELA_DEP_BAL,  CST_ID, ACCOUNT_TYPE2_ID
            """
            db.cursor.execute(sql1,int(stardate),int(stardate))
            sql2="""
            DELETE FROM F_BALANCE_TMP_TMP FF 
            WHERE FF.ACCOUNT_ID IN  ( SELECT F.ACCOUNT_ID FROM F_BALANCE_TMP_TMP F WHERE F.DATE_ID = ? AND F.ACCT_TYPE = '1' AND F.BALANCE = 0 GROUP BY F.ACCOUNT_ID HAVING COUNT(*) > 1)
            AND  FF.DATE_ID = ? AND FF.ACCT_TYPE = '1' AND FF.BALANCE = 0
            """
            db.conn.commit()
            db.cursor.execute(sql2,int(stardate),int(stardate))
            sql3="""
            INSERT INTO F_BALANCE_TMP_TMP(ACCOUNT_ID, ACCOUNT_TYPE_ID, MANAGE_ID, DATE_ID, ACCOUNT_STATUS_ID, ACCOUNT_PRICE_ID, BALANCE, OUT_BALANCE, CONTRACT_AMT, DR_AMOUNT, CR_AMOUNT, YEAR_PDT, RE_BALANCE, SUM_RE_INTEREST, LUPD_DATE_ID, IN_TO_OUT_AMOUNT, INT_BAL, ACCT_TYPE, CST_NO, INT_AMOUNT, NEXT_INT_DATE_ID, CLAC_INT, LAST_RECV_DATE, LAST_CINT_DATE, RELA_DEP_BAL, ORG_ID, CST_ID, ACCOUNT_TYPE2_ID)
            SELECT * FROM F_BALANCE_TEMP
            """
            db.cursor.execute(sql3)
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
        man_dep(stardate,etldate)
        print stardate,etldate,"完成",datetime.now()-d1
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
