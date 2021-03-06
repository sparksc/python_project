# -*- coding:utf-8 -*-
#!/bin/python  
import os,sys
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random  
from datetime import timedelta,datetime
import datetime as thisdatetime
from decimal import *
import DB2  
import csv

import etl.base.util as util
from etl.base.conf import Config,DSN,USER,PASSWD
from etl.star.manage import DimManage
     
condecimal = getcontext()
tfile = "/tmp/balance_manage_id.del"
loadfile = "/tmp/load_balance_manage_id.sql"
load_sh = "/tmp/load_balance_manage_id.sh"
logfile = "/tmp/load_balance_manage_id.log"
def get_dep_acct_manage(db,sql,etldate):
    db.cursor.execute(sql,etldate)
    row = db.cursor.fetchone()
    while row:
        m_id,flag = DimManage().find_dep_acct_key(row[4],row[0])
        #if not flag:
        #    m_id,flag = DimManage().find_dep_cust_key(row[4],row[1])
        data = (row[2],row[3],m_id)
        yield (data,True)
        row = db.cursor.fetchone()
    yield (False,False)

def get_fin_acct_manage(db,sql,etldate):
    db.cursor.execute(sql,etldate)
    row = db.cursor.fetchone()
    while row:
        m_id,flag = DimManage().find_fin_acct_key(row[4],row[0])
        data = (row[2],row[3],m_id)
        yield (data,True)
        row = db.cursor.fetchone()
    yield (False,False)

def get_loan_acct_manage(db,sql,etldate):
    db.cursor.execute(sql,etldate)
    row = db.cursor.fetchone()
    while row:
        #m_id,flag = DimManage().find_loan_acct_key(row[4],row[1])
        #if not flag:
        m_id,flag = DimManage().find_loan_cust_key(row[4],row[1])
        data = (row[2],row[3],m_id)
        yield (data,True)
        row = db.cursor.fetchone()
    yield (False,False)

def get_credit_account_manage(db,sql,etldate):
    db.cursor.execute(sql,etldate)
    row = db.cursor.fetchone()
    while row:
        m_id,flag = DimManage().find_credit_account_key(row[4],row[0])
        data = (row[2],row[3],m_id)
        yield (data,True)
        row = db.cursor.fetchone()
    yield (False,False)

def get_acpt_acct_manage(db,sql,etldate):
    db.cursor.execute(sql,etldate)
    row = db.cursor.fetchone()
    while row:
        m_id,flag = DimManage().find_acpt_cust_key(row[4],row[1])
        data = (row[2],row[3],m_id)
        yield (data,True)
        row = db.cursor.fetchone()
    yield (False,False)

def writer_manage_id(db,func,s_sql,etldate):
    d1=datetime.now()
    d_file = file(tfile,'a')
    d_file_csv = csv.writer(d_file)
    count = 0
    for (data,flag) in func(db,s_sql,etldate):
        count = count + 1
        if not flag : break
        d_file_csv.writerow(data)
    d_file.close()
    print "data time =",datetime.now()-d1,count

def load_files():
    if  os.path.exists(loadfile):os.remove(loadfile)
    newfile = open(loadfile,'w')
    newfile.write("connect to %s user %s using %s;"%(DSN,USER,PASSWD))
    load_str = "\n load client from %s of del messages %s insert into YDW.BALANCE_MANAGE_ID(ACCT_ID, DATE_ID,MANAGE_ID); "%(tfile,logfile)
    newfile.write(load_str)
    newfile.write("\n terminate;")
    newfile.close()

    if  os.path.exists(load_sh):os.remove(load_sh)
    runbat = open(load_sh,'w')
    runbat.write("\n db2 -tvf %s"%loadfile)
    runbat.write("\n exit")
    runbat.close()

    os.system("sh "+ load_sh)



def run(etldate):
    try :
        db = util.DBConnect()
        sql ="""truncate table BALANCE_MANAGE_ID IMMEDIATE"""
        db.cursor.execute(sql)
        db.conn.commit()

        if  os.path.exists(tfile):os.remove(tfile) 
        d1=datetime.now()

        cksql = """select  distinct a.account_no,f.cst_no,f.account_id,f.date_id,o.ORG0_CODE
        from f_balance f
        inner join D_ACCOUNT a on f.account_id = a.id
        inner join d_org o   on f.ORG_ID =  o.id 
        inner join deal_account_temp dat on a.account_no = dat.account_no
        where f.date_id = ? and f.ACCT_TYPE = '1'
        """ 
        writer_manage_id(db,get_dep_acct_manage,cksql,etldate)

        finsql = """select distinct  a.account_no,f.cst_no,f.account_id,f.date_id,o.ORG0_CODE
        from f_balance f
        inner join D_ACCOUNT a on f.account_id = a.id
        inner join d_org o   on f.ORG_ID =  o.id 
        inner join deal_account_temp dat on a.account_no = dat.account_no
        where f.date_id = ? and f.ACCT_TYPE = '8'
        """ 
        writer_manage_id(db,get_fin_acct_manage,finsql,etldate)

        dksql = """select distinct  a.account_no,f.cst_no,f.account_id,f.date_id,o.ORG0_CODE
        from f_balance f
        inner join D_LOAN_ACCOUNT a on f.account_id = a.id
        inner join d_org o   on f.ORG_ID =  o.id 
        inner join deal_account_temp dat on a.account_no = dat.account_no
        where f.date_id = ? and f.ACCT_TYPE = '4'
        """ 
        writer_manage_id(db,get_loan_acct_manage,dksql,etldate)
        
        billsql = """select distinct  a.account_no,f.cst_no,f.account_id,f.date_id,o.ORG0_CODE
        from f_balance f
        inner join D_ACCOUNT a on f.account_id = a.id
        inner join d_org o   on f.ORG_ID =  o.id 
        inner join deal_account_temp dat on a.account_no = dat.account_no
        where f.date_id = ? and f.ACCT_TYPE = '7'
        """ 
        writer_manage_id(db,get_acpt_acct_manage,billsql,etldate)

        load_files()
        print "load time =",datetime.now()-d1
        """
            ??????d_manage ????????????????????????????????????etl?????????????????????
        """
        OUT_SQLCODE = 1
        OUT_MSG=''
        msg = db.cursor.callproc("P_D_SALE_MANAGE_RELA",[str(Config().etldate),OUT_SQLCODE,OUT_MSG])
        if msg[1]!= 0:
            print "error msg:%s"%msg[2]

        db.conn.commit()
    finally :
        db.closeDB()

if __name__=='__main__':
    d1=datetime.now()
    Config().etldate = 20170131
    manager = multiprocessing.Manager()
    q1=manager.Queue()
    pw1 = Process(target=util.queue2db, args=( q1, ))
    print "start queue2db 1"
    pw1.start()
    DimManage().setQueue(q1)
    run(Config().etldate)
    q1.put(None)
    pw1.join()        
    db = util.DBConnect()
    if Config().etldate%100<1:
        ldate=int(util.daycalc(Config().etldate,0-Config().etldate%100))
        ldate=int(util.daycalc(ldate,1-ldate%100))
    else:
        ldate=int(util.daycalc(Config().etldate,1-Config().etldate%100))
    mer_sql = """
    merge into YDW.F_BALANCE f                                                                
    using BALANCE_MANAGE_ID b                                                                 
    on f.date_id = ? and f.account_id = b.acct_id 
    when matched then update set f.manage_id=b.manage_id
    """
    begin=thisdatetime.date(int(str(ldate)[0:4]),int(str(ldate)[4:6]),int(str(ldate)[6:8]))
    end = thisdatetime.date(int(str(Config().etldate)[0:4]),int(str(Config().etldate)[4:6]),int(str(Config().etldate)[6:8]))
    for i in range((end-begin).days+1):    
        mer_date = int(util.daycalc(ldate, i))
        db.cursor.execute(mer_sql,mer_date)
        db.conn.commit()
        print mer_date, i,datetime.now()-d1
    mer_sql = """
    merge into YDW.F_BALANCE f 
    using BALANCE_MANAGE_ID b 
    on f.date_id = ?  and f.account_id = b.acct_id 
    when matched then update set f.manage_id=b.manage_id
    """
    db.cursor.execute(mer_sql,Config().etldate)
    db.conn.commit()
    print Config().etldate,datetime.now()-d1
    db.closeDB()
    print "over time =",datetime.now()-d1
