# -*- coding:utf-8 -*-
#!/bin/python  
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
    插入已销户的存款账户 balance 为0，
"""
def insert_close(startdate,enddate):
    try :
        d1=datetime.now()
        db = util.DBConnect()
        etldate=startdate
        while int(etldate) <= int(enddate):
            m_sql ="""
            INSERT INTO YDW.F_BALANCE(ACCOUNT_ID, ACCOUNT_TYPE_ID, MANAGE_ID, DATE_ID, ACCOUNT_STATUS_ID, ACCOUNT_PRICE_ID, BALANCE, OUT_BALANCE, CONTRACT_AMT, DR_AMOUNT, CR_AMOUNT, YEAR_PDT, RE_BALANCE, SUM_RE_INTEREST, LUPD_DATE_ID, IN_TO_OUT_AMOUNT, INT_BAL, ACCT_TYPE, CST_NO, INT_AMOUNT, NEXT_INT_DATE_ID, CLAC_INT, LAST_RECV_DATE, LAST_CINT_DATE, RELA_DEP_BAL, ORG_ID, CST_ID, ACCOUNT_TYPE2_ID) 
            SELECT T.ACCOUNT_ID, T.ACCOUNT_TYPE_ID, T.MANAGE_ID, ?, T.ACCOUNT_STATUS_ID, T.ACCOUNT_PRICE_ID, 0, T.OUT_BALANCE, T.CONTRACT_AMT, T.DR_AMOUNT, T.CR_AMOUNT, (case when T.date_id=d.YEAREND_ID then 0 else T.YEAR_PDT end), T.RE_BALANCE, T.SUM_RE_INTEREST, T.LUPD_DATE_ID, T.IN_TO_OUT_AMOUNT, T.INT_BAL, T.ACCT_TYPE, T.CST_NO, T.INT_AMOUNT, T.NEXT_INT_DATE_ID, T.CLAC_INT, T.LAST_RECV_DATE, T.LAST_CINT_DATE, T.RELA_DEP_BAL, T.ORG_ID, T.CST_ID, T.ACCOUNT_TYPE2_ID 
            FROM YDW.F_BALANCE T
            JOIN D_DATE d ON T.DATE_ID=d.ID
            JOIN D_ACCOUNT A ON T.ACCOUNT_ID=A.ID and a.close_date_id<= ? and a.close_date_id>d.L_L_YEAREND_ID
            WHERE T.DATE_ID= ? AND T.ACCT_TYPE=1
            """
            db.cursor.execute(m_sql,int(etldate),int(etldate),int(util.daycalc(etldate,-1)))
            print etldate,datetime.now()-d1
            etldate=int(util.daycalc(etldate,1))
            db.conn.commit()
    finally :
        db.closeDB()

if __name__=='__main__':
    insert_close(20170204,20170204)
