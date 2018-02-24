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
    更新贷款年积数
"""
def update_yearpdt(startdate,enddate):
    try :
        d1=datetime.now()
        db = util.DBConnect()
        etldate=startdate
        while int(etldate)<=int(enddate):
            if str(etldate)[4:]=='0101':
                m_sql ="""
                update F_BALANCE set YEAR_PDT = BALANCE where DATE_ID= ? and ACCT_TYPE in (1,4)
                """
                print 'YEAR_BEG_ID',etldate
                db.cursor.execute(m_sql,int(etldate))
            else:
                m_sql ="""
                MERGE INTO F_BALANCE F1
                USING F_BALANCE F2 ON F1.ACCOUNT_ID=F2.ACCOUNT_ID AND F1.DATE_ID= ? AND F2.DATE_ID = ? AND F1.ACCT_TYPE in (1,4) AND F2.ACCT_TYPE in (1,4)
                WHEN MATCHED THEN UPDATE SET F1.YEAR_PDT=F2.YEAR_PDT+F1.BALANCE
                """
                #m1_sql ="""
                #MERGE INTO F_BALANCE F1
                #USING F_BALANCE F2 ON F1.ACCOUNT_ID=F2.ACCOUNT_ID AND F1.DATE_ID= ? AND F2.DATE_ID = ? AND F1.ACCT_TYPE in (1,4) AND F2.ACCT_TYPE in (1,4)
                #WHEN MATCHED THEN UPDATE SET F1.ORG_ID=F2.ORG_ID
                #"""
                #tmp_sql ="""
                #update F_BALANCE set ORG_ID=(select id from D_ORG where ORG0_CODE='966163') where ACCOUNT_ID in (
                #select ACCOUNT_ID from F_BALANCE f
                #join D_LOAN_ACCOUNT a on f.ACCOUNT_ID=a.ID
                #join D_ORG o on f.ORG_ID=o.ID and o.ORG0_CODE='966166'
                #where f.DATE_ID= ? and a.OPEN_BRANCH_CODE='966166' and f.ACCT_TYPE=4 
                #) and DATE_ID= ? and ACCT_TYPE=4"""
                db.cursor.execute(m_sql,int(etldate),int(util.daycalc(etldate,-1)))
                #db.cursor.execute(tmp_sql,int(etldate),int(etldate))
            print etldate,datetime.now()-d1
            etldate=int(util.daycalc(etldate,1))
            db.conn.commit()
    finally :
        db.closeDB()

if __name__=='__main__':
    update_yearpdt(20170201,20170204)
