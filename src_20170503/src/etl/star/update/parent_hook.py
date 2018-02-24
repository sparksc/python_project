# -*- coding:utf-8 -*-
#!/bin/python  
import os,sys
import etl.base.util as util
from multiprocessing import Process,Queue,Pool
import multiprocessing
import os, time, random  
from datetime import datetime,timedelta
from decimal import *
from etl.star.model.odsfile import BFFMDQBE
import DB2  
import csv

import etl.base.util as util
from etl.base.conf import Config
     
#获得当前存款账号挂钩关系, 若账号已有认定关系则不进行自动挂钩
#返回一个字典, ACCOUNT_NO作为key, ACCOUNT_HOOK的一行数据作为value返回
def get_accounthook_pass(atype):
    try:
        db = util.DBConnect()
        sql ="""
        SELECT ACCOUNT_NO, ORG_NO, MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, NOTE,ID, CUST_IN_NO
        FROM YDW.ACCOUNT_HOOK
        where TYP = ?
        """
        db.cursor.execute(sql, atype)
        row = db.cursor.fetchone()
        d = {}
        while row: 
            d[str(row[0])] = list(row)
            row = db.cursor.fetchone()
        return d
    finally:
        db.closeDB()

#汇集户自动归属主程序
#获得每天全量的 [ 汇集户子帐户登记表 CORE_BFFMDQBE ], 遍历子账户.若该子账户为待认定状态或者没有挂钩关系, 则判断主账户的挂钩关系, 子账户挂钩关系与主账户一致.
#PARENT_HOOK主账户挂钩关系表
def parent_hook_start(etldate):

    db = util.DBConnect()

    insert_sql = """
        INSERT INTO YDW.ACCOUNT_HOOK(CUST_IN_NO, ORG_NO, HOOK_TYPE, END_DATE, STATUS, SRC, TYP, SUB_TYP, NOTE, FOLLOW_CUST, BATCH_ID, START_DATE, ETL_DATE, MANAGER_NO, PERCENTAGE, ACCOUNT_NO)
        SELECT DISTINCT CUST_IN_NO, ORG_NO, HOOK_TYPE, END_DATE, STATUS, '汇集户挂钩', '存款', '存款', NOTE, '账户优先', -1,?,?,?,?,?
        FROM PARENT_HOOK WHERE ACCOUNT_NO=?  
        fetch first 1 rows only
        """ 

    update_sql = """
        UPDATE YDW.ACCOUNT_HOOK
        SET STATUS = '正常', FOLLOW_CUST = '账户优先'
        WHERE STATUS = '待手工' AND ACCOUNT_NO = ?
        """ 

    acct_his = get_accounthook_pass('存款')
    dqbe = BFFMDQBE(etldate, "ALL").loadfile2dict3(action_key=13)
    phook = util.get_parent_hook()
    for i in dqbe :    #遍历每天子账户全量
        if i in acct_his :     #判断子账户是否已挂钩
            status = acct_his.get(i)[8]
            if status == '待手工' :
                db.cursor.execute(update_sql,i) #若账户为待手工状态, 更新为正常
                db.conn.commit()
        else:
            parent_acct = dqbe.get(i).get('ZHKHAC19')
            hook= phook.get(parent_acct)
            if hook: 
                for a in hook:
                    manager_no = a[0]
                    percent = int(a[1])
                    db.cursor.execute(insert_sql,etldate,etldate,manager_no,percent,i,parent_acct)
                db.conn.commit()
                
if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen ==2:
        etldate=int(sys.argv[1])
        parent_hook_start(etldate)
    else:
        print "please input python %s yyyyMMdd"%sys.argv[0]
