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
from etl.star.manage import DimManage
     
condecimal = getcontext()
tfile = "/tmp/balance_manage_id.del"
loadfile = "/tmp/export_hook.sql"
load_sh = "/tmp/export_hook.sh"
logfile = "/tmp/export_hook.log"

def backup_files(step=""):
    if  os.path.exists(loadfile):os.remove(loadfile)
    newfile = open(loadfile,'w')
    newfile.write("connect to %s user %s using %s;"%(DSN,USER,PASSWD))
    targetfile = "/home/develop/src/etl/star/update/backup/ACCOUNT_HOOK_%s_%s_ALL.del%s"%(Config().etldate,time.strftime("%Y%m%d%H%M%S",time.localtime()),step)
    export_sql = """\n export to %s of del modified by decplusblank datesiso select * from ydw.account_hook;"""%targetfile
    newfile.write(export_sql)
    targetfile = "/home/develop/src/etl/star/update/backup/CUST_HOOK_%s_%s_ALL.del%s"%(Config().etldate,time.strftime("%Y%m%d%H%M%S",time.localtime()),step)
    export_sql = """\n export to %s of del modified by decplusblank datesiso select * from ydw.cust_hook;"""%targetfile
    newfile.write(export_sql)
    newfile.write("\n terminate;")
    newfile.close()

    if  os.path.exists(load_sh):os.remove(load_sh)
    runbat = open(load_sh,'w')
    runbat.write("\n db2 -tvf %s"%loadfile)
    runbat.write("\n exit")
    runbat.close()

    os.system("sh "+ load_sh)


"""
对于每天新生成的自动认定，自动同步batch_id
按照要求只同步全部移交的情况
"""
def syn_hook_batch_id(etldate):
    db = util.DBConnect()
    try :
        sql ="""
           SELECT C.ID, FROM_TELLER_NO
           FROM YDW.CUST_HOOK_BATCH C
           WHERE DEAL_STATUS != '已移交' AND DEAL_STATUS != '不同意' and hook_typ = '全部移交' order by ID DESC 
           """
        db.cursor.execute(sql)
        row=db.cursor.fetchone()
        movelist = {}
        while row:
            movelist[str(row[1])] = row[0]
            row = db.cursor.fetchone()

        for i in movelist:
            print i, movelist[i]

            au_sql="""
            update ACCOUNT_HOOK set BATCH_ID = ? where MANAGER_NO= ? and ETL_DATE = ? and (BATCH_ID is null or BATCH_ID = 0 or BATCH_ID = -1)
            """

            cu_sql="""
            update CUST_HOOK set BATCH_ID = ? where MANAGER_NO= ? and ETL_DATE = ? and (BATCH_ID is null or BATCH_ID = 0 or BATCH_ID = -1)
            """
            db.cursor.execute(au_sql,movelist[i],i,etldate)
            db.cursor.execute(cu_sql,movelist[i],i,etldate)
            db.conn.commit()
    finally :
        db.closeDB()

def add_hook_his(db, etldate, movelist):
    date_sql = """
                select L_MONTHEND_ID from d_date where id = ?
               """
    db.cursor.execute(date_sql,etldate)
    end_date = db.cursor.fetchone()
    print end_date,end_date[0]

    for i in movelist:
        au_sql="""
            insert into account_hook_his_query (MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, ACCOUNT_NO, NOTE, ID, SUB_TYP, CARD_NO, FOLLOW_CUST, BALANCE, BATCH_ID, CUST_IN_NO, EXIST_AVG_BALANCE, ADD_AVG_BALANCE) 
            select MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, ?, STATUS, ETL_DATE, SRC, TYP, ACCOUNT_NO, NOTE, ID, SUB_TYP, CARD_NO, FOLLOW_CUST, BALANCE, BATCH_ID, CUST_IN_NO, EXIST_AVG_BALANCE, ADD_AVG_BALANCE from account_hook where batch_id = ?
        """
        cu_sql="""
            insert into CUST_HOOK_HIS_QUERY  (MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, CUST_NO, TYP, NOTE, ID, CUST_IN_NO, SUB_TYP, BALANCE, BATCH_ID, EXIST_AVG_BALANCE, ADD_AVG_BALANCE, HIDE)  
            select MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, ?, STATUS, ETL_DATE, SRC, CUST_NO, TYP, NOTE, ID, CUST_IN_NO, SUB_TYP, BALANCE, BATCH_ID, EXIST_AVG_BALANCE, ADD_AVG_BALANCE, HIDE from cust_hook where BATCH_ID = ?
        """
        db.cursor.execute(au_sql,end_date[0], i[0])
        db.cursor.execute(cu_sql,end_date[0], i[0])

def merge_account_hook_percentage():
    db = util.DBConnect()
    try :
        sql ="""
            select MANAGER_NO, org_no, account_no, sum(percentage), min(id)
            from account_hook  ah where status = '正常' group by MANAGER_NO, org_no, account_no having count(*) > 1
           """
        db.cursor.execute(sql)
        row=db.cursor.fetchone()
        mergelist={}
        minidlist={}
        while row:
            ckey  = str(row[0] + '!' + row[1] + '!' + row[2])
            mergelist[ckey] = row[3]            #存储比例
            minidlist[ckey] = row[4]            #最小序号
            row = db.cursor.fetchone()

        sql1 = """
            select MANAGER_NO, org_no, account_no, id from account_hook ah where ah.hook_type = '管户' and percentage != 100 and status = '正常' 
            """
        db.cursor.execute(sql1)
        row1 = db.cursor.fetchone()
        mainlist = {}
        while row1:
            ckey  = str(row1[0] + '!' + row1[1] + '!' + row1[2])
            mainlist[ckey] = row1[3]            #存储比例
            row1 = db.cursor.fetchone()

        for i in mergelist:
            ckey = i.split('!')

            if i in mainlist:
                hook_id = mainlist[i]
            else:
                hook_id = minidlist[i]
            percentage = mergelist[i]
            print "key", i, "hook_id:", hook_id, "percentage:", percentage

            update_sql = """
                        update account_hook set percentage = ? where id = ?
                        """
            deal_sql = """
                delete from account_hook ah where status = '正常' and ah.MANAGER_NO = ? and ORG_NO = ? and account_no = ? and id != ?
                """
            db.cursor.execute(update_sql, percentage, hook_id)
            db.cursor.execute(deal_sql, ckey[0], ckey[1], ckey[2], hook_id)
            db.conn.commit()
    finally :
        db.closeDB()

def merge_cust_hook_percentage(typ):
    db = util.DBConnect()
    try :
        sql ="""
            select MANAGER_NO, org_no, cust_in_no, sum(percentage), min(id)
            from cust_hook  ch where status = '正常' and TYP = ?  group by MANAGER_NO, org_no, cust_in_no  having count(*) > 1
           """
        db.cursor.execute(sql, typ)
        row=db.cursor.fetchone()
        mergelist={}
        minidlist={}
        while row:
            ckey  = str(row[0] + '!' + row[1] + '!' + row[2])
            mergelist[ckey] = row[3]            #存储比例
            minidlist[ckey] = row[4]            #最小序号
            row = db.cursor.fetchone()

        sql1 = """
            select MANAGER_NO, org_no, cust_in_no, id from cust_hook ch where ch.hook_type = '管户' and status = '正常' and percentage != 100 and typ = ?
            """
        db.cursor.execute(sql1, typ)
        row1 = db.cursor.fetchone()
        mainlist = {}
        while row1:
            ckey  = str(row1[0] + '!' + row1[1] + '!' + row1[2])
            mainlist[ckey] = row1[3]            #管户ID
            row1 = db.cursor.fetchone()

        for i in mergelist:
            ckey = i.split('!')

            if i in mainlist:
                hook_id = mainlist[i]
            else:
                hook_id = minidlist[i]
            percentage = mergelist[i]
            if int(percentage) > 100:
                raise Exception('percentage > 100')
            print "key", i, "hook_id:", hook_id, "percentage:", percentage

            update_sql = """
                        update cust_hook set percentage = ? where id = ?
                        """
            deal_sql = """
                delete from cust_hook ch where status = '正常' and ch.MANAGER_NO = ? and ch.ORG_NO = ? and ch.cust_in_no= ? and typ = ? and id != ?
                """
            db.cursor.execute(update_sql, percentage, hook_id)
            db.cursor.execute(deal_sql, ckey[0], ckey[1], ckey[2], typ, hook_id)
            db.conn.commit()
    finally :
        db.closeDB()

#每月一号跑批最后将审批通过的移交,正式更新到移交接收的人身上,也支持具体转移批次号生效
def run(etldate,batch_id=None):
    db = util.DBConnect()
    movelist = []
    day = etldate % 100
    tag = False
    try :
        if batch_id is None:
            if day > 8:
                sql ="""
                SELECT C.ID, FROM_TELLER_NO, TO_TELLER_NO, HOOK_TYP, TYP, STATUS, DEAL_STATUS
                FROM YDW.CUST_HOOK_BATCH C
                WHERE DEAL_STATUS='同意' 
                """
            #else:
            #    sql ="""
            #    SELECT C.ID, FROM_TELLER_NO, TO_TELLER_NO, HOOK_TYP, TYP, STATUS, DEAL_STATUS
            #    FROM YDW.CUST_HOOK_BATCH C
            #    JOIN F_USER f on c.from_teller_no = f.user_name and f.is_virtual = '是'
            #    WHERE DEAL_STATUS='同意'
            #    """
                tag = True
                db.cursor.execute(sql)
                movelist=db.cursor.fetchall()
        else:    
            sql ="""
            SELECT C.ID, FROM_TELLER_NO, TO_TELLER_NO, HOOK_TYP, TYP, STATUS, DEAL_STATUS
            FROM YDW.CUST_HOOK_BATCH C
            WHERE DEAL_STATUS='同意' and ID = ? 
            """
            db.cursor.execute(sql,batch_id)
            movelist=db.cursor.fetchall()

        if tag:
            add_hook_his(db, etldate, movelist)  #增加拉链历史

        date_sql =  """
                    select MONTHBEG_ID from d_date where id = ?
                    """
        db.cursor.execute(date_sql,etldate)
        end_date = db.cursor.fetchone()

        for i in movelist:
            print i[0]
            au_sql="""
            update ACCOUNT_HOOK set MANAGER_NO = ?,STATUS = '正常',etl_date = ? where BATCH_ID = ?
            """
            cu_sql="""
            update CUST_HOOK    set MANAGER_NO = ?,STATUS = '正常', etl_date = ? where BATCH_ID = ?
            """
            bu_sql="""
            update CUST_HOOK_BATCH  set DEAL_STATUS = '已移交' where ID = ?
            """
            print i[2],end_date[0],i[0]
            db.cursor.execute(au_sql,i[2],end_date[0],i[0])
            db.cursor.execute(cu_sql,i[2],end_date[0],i[0])
            db.cursor.execute(bu_sql,i[0])
            db.conn.commit()
    finally :
        db.closeDB()



#跑批最后将录入已审批状态更新为正常
"""
对于录入生效的，如果是1-8日则生效日期是上个月1日;如果是9-月末则生效日期是当月1日。两个日期均和开户日期进行对比(即目前的开户日期)
"""
def input_pass(etldate):
    db = util.DBConnect()
    day = etldate % 100
    temp_date = etldate
    if day >=1 and day <= 8:    #取上月月初
        temp_date = int(util.daycalc(etldate, -15))

    date_sql =  """ select MONTHBEG_ID from d_date where id = ?  """
    db.cursor.execute(date_sql,temp_date)
    start_date = db.cursor.fetchone()
    print start_date

    try :
        sql ="""
            UPDATE CUST_HOOK SET STATUS='正常', start_date = max(start_date, ?) WHERE STATUS='录入已审批'
        """
        db.cursor.execute(sql, start_date[0])
        sql ="""
            UPDATE ACCOUNT_HOOK SET STATUS='正常' , start_date = max(start_date, ?) WHERE STATUS='录入已审批'
        """
        db.cursor.execute(sql, start_date[0])
        sql ="""
            UPDATE PARENT_HOOK SET STATUS='正常' , start_date = max(start_date, ?) WHERE STATUS='录入已审批'
        """
        db.cursor.execute(sql, start_date[0])
        db.conn.commit()
    finally :
        db.closeDB()

#最后删除account_hook中帐号有帐号优先的,还有客户号优先的错误数据,删除客户号优先的数据
def delete_cust_no_first():
    db = util.DBConnect()
    print "delete cust_no first"
    try:
       sql="""
       DELETE FROM ACCOUNT_HOOK B WHERE B.FOLLOW_CUST='客户号优先' AND (B.ACCOUNT_NO,B.ORG_NO ) IN (SELECT A.ACCOUNT_NO,A.ORG_NO FROM ACCOUNT_HOOK A WHERE A.STATUS='正常' AND A.FOLLOW_CUST='账号优先' )
       """
       sql1="""
       DELETE FROM CUST_HOOK WHERE ID IN (
       SELECT MAX(ID) ID FROM CUST_HOOK WHERE TYP='电子银行' AND STATUS = '正常' GROUP BY CUST_IN_NO, ORG_NO  HAVING COUNT(*) > 1)
       """
       db.cursor.execute(sql)
       db.cursor.execute(sql1)
       db.conn.commit()
    finally:
       db.closeDB()


if __name__=='__main__':
    arglen=len(sys.argv)
    d1=datetime.now()
    print "start"
    Config().etldate = int(sys.argv[1])
    #backup_files()
    if arglen==2:
        #syn_hook_batch_id(Config().etldate)
        #run(Config().etldate)
        input_pass(Config().etldate)
        #merge_cust_hook_percentage('存款')
        #merge_cust_hook_percentage('理财')
        #merge_account_hook_percentage()
        #delete_cust_no_first()
        pass
    elif arglen==3:    
        bid = int(sys.argv[2])
        run(Config().etldate,bid)
        #input_pass(Config().etldate)
        #merge_cust_hook_percentage('存款')
        #merge_cust_hook_percentage('理财')
        #merge_account_hook_percentage()
    print "over time =",datetime.now()-d1
