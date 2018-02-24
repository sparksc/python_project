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
from etl.base.conf import Config,DSN,USER,PASSWD
from etl.star.manage_his import DimManage
from etl.star.update.update_d_cust_contract_cst_no import update_cst_no
     
condecimal = getcontext()
tfile = "/tmp/contract_manage_id.del"
loadfile = "/tmp/load_contract_manage_id.sql"
load_sh = "/tmp/load_contract_manage_id.sh"
logfile = "/tmp/load_contract_manage_id.log"

def get_ebank_cust_manage(db,sql,etldate):
    db.cursor.execute(sql,etldate)
    row = db.cursor.fetchone()
    while row:
        if row[4] == '新丰收e支付':
            m_id,flag = DimManage().find_contract_cust_key(row[3],row[0],'丰收e支付')
        else :
            m_id,flag = DimManage().find_contract_cust_key(row[3],row[0],row[4])
        data = (row[1],row[2],m_id)
        yield (data,True)
        row = db.cursor.fetchone()
    yield (False,False)

def get_stock_cust_manage(db,sql,etldate):
    db.cursor.execute(sql,etldate)
    row = db.cursor.fetchone()
    while row:
        m_id,flag = DimManage().find_stock_cust_key(row[3],row[0])
        data = (row[1],row[2],m_id)
        yield (data,True)
        row = db.cursor.fetchone()
    yield (False,False)

def get_loan_cust_manage(db,sql,etldate):
    db.cursor.execute(sql,etldate)
    row = db.cursor.fetchone()
    while row:
        m_id,flag = DimManage().find_loan_cust_key(row[3],row[0])
        data = (row[1],row[2],m_id)
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
    load_str = "\n load client from %s of del messages %s insert into YDW.CONTRACT_MANAGE_ID(CONTRACT_ID, DATE_ID,MANAGE_ID); "%(tfile,logfile)
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
    #update_cst_no()         #ETC更新客户内码
    try :
        db = util.DBConnect()
        sql ="""truncate table CONTRACT_MANAGE_ID IMMEDIATE"""
        db.cursor.execute(sql)
        db.conn.commit()

        if  os.path.exists(tfile):os.remove(tfile) 
        d1=datetime.now()

        ebanksql = """
        select trim(c.CST_NO),f.CONTRACT_ID,f.DATE_ID,o.org0_code,c.BUSI_TYPE from F_CONTRACT_STATUS f
        join D_CUST_CONTRACT c on f.CONTRACT_ID=c.ID
        join D_ORG o on f.org_id=o.id
        where f.DATE_ID = ? and c.BUSI_TYPE in ('支付宝快捷支付') and substr(c.cst_no,1,1)='8'
        """ 
        #writer_manage_id(db,get_ebank_cust_manage,ebanksql,etldate)

        loanconsql = """
        select c.CST_NO,f.CONTRACT_ID,f.DATE_ID,c.OPEN_BRANCH_NO from F_CONTRACT_STATUS f
        join D_CUST_CONTRACT c on f.CONTRACT_ID=c.ID
        where f.DATE_ID = ? and c.BUSI_TYPE='贷款合同'
        """ 
        writer_manage_id(db,get_loan_cust_manage,loanconsql,etldate)

        load_files()
        print "load time =",datetime.now()-d1
        if etldate%100<=8:
            ldate=int(util.daycalc(etldate,0-etldate%100))
            ldate=int(util.daycalc(ldate,1-ldate%100))
        else:
            ldate=int(util.daycalc(etldate,1-etldate%100))
        for i in range(ldate,Config().etldate+1):    
            mer_sql = """
                merge into YDW.F_CONTRACT_STATUS f 
                using CONTRACT_MANAGE_ID b 
                on f.date_id = ? and f.contract_id = b.contract_id  when matched then update set f.manage_id=b.manage_id
            """
            db.cursor.execute(mer_sql,i)
            db.conn.commit()
            print i    
        """
            分割d_manage 测试放在这里，之后是放在etl每日任务的最后
        """
        OUT_SQLCODE = 1
        OUT_MSG=''
        msg = db.cursor.callproc("P_D_SALE_MANAGE_RELA",[str(20150101),OUT_SQLCODE,OUT_MSG])
        if msg[1]!= 0:
            print "error msg:%s"%msg[2]

        db.conn.commit()
    finally :
        db.closeDB()

if __name__=='__main__':
    d1=datetime.now()
    Config().etldate = 20161130
    manager = multiprocessing.Manager()
    q1=manager.Queue()
    pw1 = Process(target=util.queue2db, args=( q1, ))
    print "start queue2db 1"
    pw1.start()
    DimManage().setQueue(q1)
    run(Config().etldate)
    q1.put(None)
    pw1.join()
    print "over time =",datetime.now()-d1
