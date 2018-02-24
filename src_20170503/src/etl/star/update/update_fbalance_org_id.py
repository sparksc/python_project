# -*- coding:utf-8 -*-
#!/bin/python  
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random  
from datetime import datetime,timedelta
from decimal import *
#import DB2  
import csv

import etl.base.util as util
from etl.base.conf import Config
from etl.base.logger import info
     
condecimal = getcontext()
"""
    更新F_BALANCE表上的ORG_ID字段，
"""
def update_orgid(startdate,enddate):
    info("update_orgid:%d-%d"%(startdate,enddate))
    try :
        db = util.DBConnect()
        etldate=startdate
        while int(etldate)<=int(enddate):
            m4_sql="""
            MERGE INTO YDW.F_CONTRACT_STATUS F
            USING (SELECT O.ID DOID ,D.ID COID FROM D_ORG O JOIN D_CUST_CONTRACT D ON O.ORG0_CODE =D.OPEN_BRANCH_NO WHERE D.BUSI_TYPE<>'企业网上银行' and D.BUSI_TYPE<>'ETC') A
            ON A.COID = F.CONTRACT_ID AND F.DATE_ID =?
            WHEN MATCHED THEN UPDATE SET F.ORG_ID=A.DOID
            """
            m6_sql="""
            MERGE INTO YDW.F_CONTRACT_STATUS F
            USING (SELECT O.ID DOID ,C.ID COID FROM D_CUST_CONTRACT C
            JOIN EBANK_ORG D ON D.SUB_TYP in ('企业网上银行', 'ETC') AND C.BUSI_TYPE in ('企业网上银行', 'ETC') AND D.CUST_NET_NO=C.NET_CST_NO AND D.STATUS IN ('正常')
            JOIN D_ORG O ON O.ORG0_CODE=D.ORG_NO) A
            ON A.COID = F.CONTRACT_ID AND F.DATE_ID =?
            WHEN MATCHED THEN UPDATE SET F.ORG_ID=A.DOID
            """
            db.cursor.execute(m4_sql,etldate)
            db.cursor.execute(m6_sql,etldate)
            print etldate
            etldate=int(util.daycalc(etldate,1))
            db.conn.commit()
    finally :
        db.closeDB()

if __name__=='__main__':
    update_orgid(20170218,20170219)
