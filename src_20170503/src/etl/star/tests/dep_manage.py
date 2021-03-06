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
from etl.base.logger import info

     
condecimal = getcontext()
tfile = "/tmp/balance_manage_id.del"
loadfile = "/tmp/load_balance_manage_id.sql"
load_sh = "/tmp/load_balance_manage_id.sh"
logfile = "/tmp/load_balance_manage_id.log"

def get_dep_acct_manage(db,sql,etldate):
    testfile = "/tmp/dep_%s.del"%(str(etldate))
    if  os.path.exists(testfile):os.remove(testfile)
    test_file = file(testfile,'a')
    test_csv = csv.writer(test_file)

    info("get_dep_acct_manage:sql[%s],etldate[%s]"%(sql,str(etldate)))
    db.cursor.execute(sql,etldate)
    row = db.cursor.fetchone()
    while row:
        test_csv.writerow(list(row))
        m_id,flag = DimManage().find_dep_acct_key(row[4],row[0])
        #if not flag:
        #    m_id,flag = DimManage().find_dep_cust_key(row[4],row[1])
        data = (row[2],row[3],m_id)
        test_csv.writerow(data)
        yield (data,True)
        row = db.cursor.fetchone()
    test_file.close()
    yield (False,False)

def get_fin_acct_manage(db,sql,etldate):
    info("get_fin_acct_manage:sql[%s],etldate[%s]"%(sql,str(etldate)))
    db.cursor.execute(sql,etldate)
    row = db.cursor.fetchone()
    while row:
        m_id,flag = DimManage().find_fin_acct_key(row[4],row[0])
        data = (row[2],row[3],m_id)
        yield (data,True)
        row = db.cursor.fetchone()
    yield (False,False)

def get_loan_acct_manage(db,sql,etldate):
    info("get_loan_acct_manage:sql[%s],etldate[%s]"%(sql,str(etldate)))
    testfile = "/tmp/loan_%s.del"%(str(etldate))
    if  os.path.exists(testfile):os.remove(testfile)
    test_file = file(testfile,'a')
    test_csv = csv.writer(test_file)

    db.cursor.execute(sql,etldate)
    row = db.cursor.fetchone()
    while row:
        #m_id,flag = DimManage().find_loan_acct_key(row[4],row[1])
        #if not flag:
        test_csv.writerow(list(row))
        m_id,flag = DimManage().find_loan_cust_key(row[4],row[1])
        data = (row[2],row[3],m_id)
        test_csv.writerow(data)
        yield (data,True)
        row = db.cursor.fetchone()
    test_file.close()
    yield (False,False)

def get_credit_account_manage(db,sql,etldate):
    info("get_credit_account_manage:sql[%s],etldate[%s]"%(sql,str(etldate)))
    db.cursor.execute(sql,etldate)
    row = db.cursor.fetchone()
    while row:
        m_id,flag = DimManage().find_credit_account_key(row[4],row[0])
        data = (row[2],row[3],m_id)
        yield (data,True)
        row = db.cursor.fetchone()
    yield (False,False)

def get_acpt_acct_manage(db,sql,etldate):
    info("get_acpt_acct_manage:sql[%s],etldate[%s]"%(sql,str(etldate)))
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
    info("writer_manage_id:sql[%s],etldate[%s]"%(s_sql,str(etldate)))
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


        cksql = """select  a.account_no,f.cst_no,f.account_id,f.date_id,o.ORG0_CODE
        from f_balance f
        inner join D_ACCOUNT a on f.account_id = a.id
        inner join d_org o   on f.ORG_ID =  o.id 
        where f.date_id = ? and f.ACCT_TYPE = '1'
            and a.account_no in ('101008751860348','101003638700968','101007402577158','101006707009336','101008400828032','101002095007553','101006718691301')
        """ 
        writer_manage_id(db,get_dep_acct_manage,cksql,etldate)
        print "finish writer_manage_id"

        load_files()
        db.conn.commit()
    finally :
        db.closeDB()

def starrun(etldate):

    DimManage().refresh_cash()

    d1=datetime.now()
    Config().etldate = etldate 
    manager = multiprocessing.Manager()
    q1=manager.Queue()
    pw1 = Process(target=util.queue2db, args=( q1, ))
    pw1.start()
    info("update_balance_manage_load q1_proces_id=%s"%(str(pw1.pid)))
    DimManage().setQueue(q1)
    run(Config().etldate)
    q1.put(None)
    pw1.join()        
    db = util.DBConnect()
    if Config().etldate%100<=8:
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

def call_sale_rela_proc(etldate):
    try :
        db = util.DBConnect()
        OUT_SQLCODE = 1
        OUT_MSG=''
        msg = db.cursor.callproc("P_D_SALE_MANAGE_RELA",[str(Config().etldate),OUT_SQLCODE,OUT_MSG])
        if msg[1]!= 0:
            print "error msg:%s"%msg[2]
            raise Exception("??????Manage??????")
        db.conn.commit()
    finally :
        db.closeDB()
if __name__=='__main__':
    arglen=len(sys.argv)
    print sys.argv 
    if arglen ==3:
        stardate=int(sys.argv[1])
        etldate=int(sys.argv[2])
        print stardate,etldate
        begin=thisdatetime.date(int(str(stardate)[0:4]),int(str(stardate)[4:6]),int(str(stardate)[6:8]))
        end = thisdatetime.date(int(str(etldate)[0:4]),int(str(etldate)[4:6]),int(str(etldate)[6:8]))
        print begin,end
        day = stardate 
        print day
        for i in range((end-begin).days+1):
            Config().etldate = day 
            starrun(Config().etldate)
            print "manage_id:",day,"ok"
            day = util.daycalc(day,1)
            print i,day
        call_sale_rela_proc(20170131)
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
