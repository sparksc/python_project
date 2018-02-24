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
     
condecimal = getcontext()
"""
折人民币
"""
def cny(stardate,etldate):
    try:
        oneday=datetime.now()
        db = util.DBConnect()
        print "cny:开始"
        while stardate<=etldate:
            sql0="""
            DELETE FROM REPORT_SALE_RMB_EXG WHERE DATE_ID=?
            """
            db.cursor.execute(sql0,int(stardate))
            db.conn.commit()
            sql="""
            INSERT INTO REPORT_SALE_RMB_EXG
            select a.DATE_ID,nvl(b.open_branch_code,a.THIRD_BRANCH_CODE),nvl(b.BRANCH_NAME,a.THIRD_BRANCH_NAME),a.SALE_CODE,a.SALE_NAME ,a.cust_name,a.CUST_NO,money
            from
            (select F.DATE_ID,R.THIRD_BRANCH_CODE,THIRD_BRANCH_NAME,R.SALE_CODE,R.SALE_NAME ,da.cust_name,da.CUST_NO,ROUND(SUM(F.BALANCE*R.PERCENT*0.01*P.RMB_EXG_RATE*0.0000000001),0) money
             FROM F_BALANCE F
             join d_cust_info da on f.cst_no=da.cust_no
             INNER JOIN  D_ACCOUNT_PRICE P ON P.ID=F.ACCOUNT_PRICE_ID
             INNER JOIN D_SALE_MANAGE_RELA R ON R.MANAGE_ID = F.MANAGE_ID
             INNER JOIN d_account d on f.ACCOUNT_ID=d.id
             WHERE F.ACCOUNT_PRICE_ID  = P.ID AND P.CCY  IN ( 'AUD','EUR','GBP','HKD','JPY','SGD','USD' )
             AND F.DATE_ID=? AND F.BALANCE !=0 and left(da.CUST_NO,2)='82' and f.ACCT_TYPE='1' and  d.CLOSE_DATE_ID>=F.DATE_ID
             GROUP BY F.DATE_ID,R.THIRD_BRANCH_CODE,SALE_CODE ,da.CUST_NAME,da.cust_no,R.THIRD_BRANCH_NAME,R.SALE_NAME) a
            left join
            (

             select d.CST_NO,d.ccy,d.open_branch_code,b.BRANCH_NAME
             from D_ACCOUNT d
             join BRANCH b on d.OPEN_BRANCH_CODE=b.BRANCH_CODE
             where ccy='CNY' and left(CST_NO,2)='82'
             and CST_NO in 
             (select CST_NO
              from
              (select d.CST_NO,d.open_branch_code
               from D_ACCOUNT d
               where ccy='CNY' and left(CST_NO,2)='82'
               group by d.CST_NO,d.open_branch_code)
              group by CST_NO having count(*)=1)
             group by d.CST_NO,d.ccy,d.open_branch_code,b.BRANCH_NAME 
            ) b
            on a.CUST_NO=b.CST_NO 
            """
            db.cursor.execute(sql,int(stardate))
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
        cny(stardate,etldate)
        print "cny",stardate,etldate,"完成",datetime.now()-d1
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
