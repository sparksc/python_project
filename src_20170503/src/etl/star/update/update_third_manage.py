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
    更新F_BALANCE上的ACCOUNT_TYPE2_ID字段(新添),指向ACCOUNT_TYPE2表中 是否第三方管存(未测试，未完成)
"""
def update(db,etldate,filename):
    d1 = datetime.now()
    print str(etldate)+" "+" start",d1

    targetfile = Config().data_path+"/%s/ALL/%s_%s_ALL_%s.del"%(etldate,filename,etldate,Config().branch_code)
    targethandler = file(targetfile, 'r')
    targethandler_csv=csv.reader(targethandler)
    update_data1=[]
    update_data2=[]
    for row in targethandler_csv:
        #u_sql = u"update F_CONTRACT_STATUS set LAST_TRADE_DATE= %s where contract_id=(select ID from D_CUST_CONTRACT where net_cst_no= %s and busi_type='%s') and date_id = %s"%(etldate,row[2],trantype,etldate)
        #db.cursor.execute(u_sql.encode('utf-8'))
        #print row int(row[0][0:8])
        print row
        if row[4][0:2] == '10':
            update_data1.append((1,row[4],etldate))
        elif row[4][0:2] == '62':
            update_data2.append((1,row[4],etldate))
    u1_sql = u"update F_BALANCE set ACCOUNT_TYPE2_ID = ? where ACCOUNT_ID=(select ID from D_ACCOUNT where ACCOUNT_NO = ?) and DATE_ID= ?".encode('utf-8')
    u2_sql = u"update F_BALANCE set ACCOUNT_TYPE2_ID = ? where ACCOUNT_ID=(select ID from D_ACCOUNT where ACCOUNT_NO = (select ACCOUNT_NO from D_DEBIT_CARD where CARD_NO=  ? )) and DATE_ID = ?".encode('utf-8')
    print u1_sql
    print u2_sql

    #db.cursor.executemany(u1_sql,update_data1)
    #db.cursor.executemany(u2_sql,update_data2)
    d2 = datetime.now()
    print str(etldate)+" "+" end",d2-d1
        
def update_ltd(startdate,enddate):
    try :
        db = util.DBConnect()
        etldate=startdate
        while int(etldate)<=int(enddate):
            update(db,etldate,u'TPDM_TS_DLCG_KHXX')
            etldate=int(util.daycalc(etldate,1))
        db.conn.commit()
    finally :
        db.closeDB()

if __name__=='__main__':
    update_ltd(20150101,20150101)
