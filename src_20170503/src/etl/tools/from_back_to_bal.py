# -*- coding:utf-8 -*- 
from sqlalchemy.orm import aliased
import time,os,random,sys
import DB2
from decimal import Decimal

import etl.base.util as util
import etl.star.model.interestutil as iu
import datetime

def run_import(etldate):
    cust_sql="""
        insert into ydw.F_ACCOUNT_BALANCE select
        id,ACCOUNT_ID,DATE_ID,ACCOUNT_TYPE_ID,BALANCE,START_INTEREST,DUE_DATE,OPEN_DATE,CLOSE_DATE,LAST_BALANCE,ADJ_INTEREST,GROUP_ID,ORG_ID,YEAR_PDT,0 as interest_pdt,CST_NO,ACCOUNT_CLASS,
        PAY_INTEREST,CONTRACT_RATE,EXECUTE_RATE,INTEREST_MONTH,INTEREST_DAY,PLAN_INTEREST
        from ydw.F_ACCOUNT_BALANCE_back  f
        where f.DATE_ID = %s
    """%etldate
    print cust_sql
    '''
    try :
        db = util.DBConnect()
        db.cursor.execute(cust_sql)
        db.conn.commit()
    finally :
        db.closeDB()
    '''

if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen==3:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        print "begin************",startdate
        etldate = startdate
        while etldate <= enddate:
            run_import(etldate)
            etldate = iu.daycalc(etldate,2)
        print "end*************", enddate
    else:
        print "please input python import_hook.py [startdate] [enddate]"
