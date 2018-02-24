# -*- coding:utf-8 -*-
#!/bin/python  
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random  
from datetime import datetime,timedelta
from decimal import *
import DB2  

import etl.base.util as util
from etl.base.conf import Config
     
condecimal = getcontext()
"""
"""
def update(db,etldate):
    sql = u"""
    insert into m_manage_org_bal(ym,ACCOUNT_TYPE_ID,MANAGE_ID,ACCT_TYPE,ORG_ID,ACCOUNT_STATUS_ID,balance_sum,OUT_BALANCE_sum,re_balance_sum,INT_BAL_sum,mdays,min_date,max_date,month_days) 
select left(date_id,6) ym, ACCOUNT_TYPE_ID, MANAGE_ID,ACCT_TYPE,ORG_ID, 
    ACCOUNT_STATUS_ID, sum(BALANCE) balance_sum,sum(OUT_BALANCE) 
    OUT_BALANCE_sum, sum(RE_BALANCE) re_balance_sum, 
    sum(INT_BAL) INT_BAL_sum,count(distinct date_id) mdays,min(f.date_id) 
    min_date,max(f.date_id) max_date,d.month_days
from F_BALANCE f
inner join d_date d
on d.id = f.date_id
where f.date_id>=? and f.date_id <= ? and f.acct_type in ('1','4','7','8')
group by ACCOUNT_TYPE_ID, MANAGE_ID,ACCT_TYPE,ORG_ID, ACCOUNT_STATUS_ID,left(date_id,6),d.month_days
    """
    startdate = int('%s%s'%(str(etldate)[:6],'01'))
    db.cursor.execute(sql,(startdate,etldate))
    db.conn.commit()

def delete(db,etldate):
    sql = u"""
        delete m_manage_org_bal where ym =?
    """
    db.cursor.execute(sql,int(str(etldate)[:6]))
    db.conn.commit()
            
from datetime import datetime,timedelta
    
def update_org_manage_bal(etldate):
    d1 = datetime.now()
    try :
        db = util.DBConnect()
        delete(db,etldate)
        update(db,etldate)
        db.conn.commit()
    finally :
        db.closeDB()
    print datetime.now() -d1

if __name__=='__main__':
    etldate = 20140231
    update_org_manage_bal(etldate)
    #update_dxxh_no()
