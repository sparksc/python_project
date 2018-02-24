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
#补齐存款和理财的ACCOUNT_HOOK记录(too slow)        
def insert_miss(etldate,typ):
    print 'insert_miss begin', etldate
    try :
        db = util.DBConnect()
        c_sql ="""
        SELECT CUST_NO, MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP,SUB_TYP, NOTE, CUST_IN_NO, BATCH_ID
            FROM YDW.CUST_HOOK WHERE TYP = ? and status in ('已审批', '正常', '待审批', '预提交审批') and etl_date = ? and PERCENTAGE = 100
        """
        db.cursor.execute(c_sql,typ, etldate)
        chdict={}
        tmp=db.cursor.fetchone()
        while tmp:
            chdict[tmp[-2]+tmp[2]+tmp[1]]=list(tmp)  #待手工、录入待审批、录入已审批记录 内码+机构号+客户经理 = list
            tmp=db.cursor.fetchone()
        print len(chdict),typ    


        #基于全部100%的认定关系
        a_hook_sql="""
        select distinct ACCOUNT_NO,MANAGER_NO from account_hook a where a.TYP = ? 
        """
        db.cursor.execute(a_hook_sql,typ)
        ahlist_hook = {}
        tmp_hook = db.cursor.fetchone()
        while tmp_hook:
            ahlist_hook[tmp_hook[0]] = tmp_hook[1]  #帐号挂钩 账号 = 客户经理号码
            tmp_hook = db.cursor.fetchone()
        print len(ahlist_hook),typ  


        f_sql="""
        select distinct a.ACCOUNT_NO,f.CST_NO,o.ORG0_CODE,b.manager_no from F_BALANCE f
        join D_ACCOUNT a on f.ACCOUNT_ID=a.ID
        join D_ORG o on f.ORG_ID=o.ID
        join (SELECT CUST_IN_NO,ORG_NO,MANAGER_NO  FROM YDW.CUST_HOOK WHERE TYP = ?  and status in ('已审批', '正常', '待审批', '预提交审批') and etl_date = ? and PERCENTAGE = 100 ) b on f.CST_NO= b.CUST_IN_NO and o.ORG0_CODE=b.ORG_NO
        where f.ACCT_TYPE = ?  and f.DATE_ID= ?
        """
        if typ=='存款':
            db.cursor.execute(f_sql,typ,etldate,'1',etldate)
        elif typ=='理财':
            db.cursor.execute(f_sql,typ,etldate,'8',etldate)
        else:
            return 
        fdict={}
        tmp=db.cursor.fetchone()
        while tmp:
            fdict[tmp[0]+'!'+tmp[3]]=tmp[1]+tmp[2]+tmp[3]       #账号 ! 客户经理 = 内码 + 机构号 + 客户经理
            tmp=db.cursor.fetchone()
        i_sql="""
        INSERT INTO YDW.ACCOUNT_HOOK_CJLI(MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, SUB_TYP, NOTE, CUST_IN_NO, BATCH_ID, ACCOUNT_NO, CARD_NO, FOLLOW_CUST) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, ?)
        """
        ilist=[]
        for i in fdict:             #i=
            accounts = i.split('!')
            if accounts[0] not in ahlist_hook:     #不存在账号的认定
                if chdict.get(fdict.get(i)):
                    ilist.append(chdict.get(fdict.get(i))[1:]+[i.split('!')[0],i.split('!')[0],'客户号优先'])
        db.cursor.executemany(i_sql,ilist)
        db.conn.commit()
    finally :
        db.closeDB()

#补齐存款和理财的ACCOUNT_HOOK记录(too slow)        
def insert_miss_percentage(etldate,typ):
    print 'insert_miss_percentage begin'
    try :
        db = util.DBConnect()
        c_sql ="""
        SELECT CUST_NO, MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP,SUB_TYP, NOTE, CUST_IN_NO, BATCH_ID
            FROM YDW.CUST_HOOK WHERE TYP = ? and status in ('正常') and PERCENTAGE != 100
        """
        db.cursor.execute(c_sql,typ)
        chdict={}
        tmp=db.cursor.fetchone()
        while tmp:
            chdict[tmp[-2]+tmp[2]+tmp[1]]=list(tmp)  #正常分润 内码+机构号+客户经理 = list
            tmp=db.cursor.fetchone()
        print len(chdict),typ    
        a_sql="""
         select distinct ACCOUNT_NO,MANAGER_NO from account_hook a where a.TYP =  ? and a.FOLLOW_CUST='客户号优先'
        """
        db.cursor.execute(a_sql,typ)
        ahlist={}
        tmp=db.cursor.fetchone()
        while tmp:
            ahlist[tmp[0]+'!'+tmp[1]]=tmp[0]    #账号 + 客户经理 = 账号
            tmp=db.cursor.fetchone()
        print len(ahlist),typ

        a_hook_sql="""
        select distinct ACCOUNT_NO,MANAGER_NO from account_hook a where a.TYP = ?  and  a.FOLLOW_CUST='账号优先' 
        """
        db.cursor.execute(a_hook_sql,typ)
        ahlist_hook = {}
        tmp_hook = db.cursor.fetchone()
        while tmp_hook:
            ahlist_hook[tmp_hook[0]] = tmp_hook[1]  #帐号挂钩 账号 = 客户经理号码
            tmp_hook = db.cursor.fetchone()
        print len(ahlist_hook),typ  

        f_sql="""
        select distinct a.ACCOUNT_NO,f.CST_NO,o.ORG0_CODE,b.manager_no from F_BALANCE f
        join D_ACCOUNT a on f.ACCOUNT_ID=a.ID
        join D_ORG o on f.ORG_ID=o.ID
        join (SELECT CUST_IN_NO,ORG_NO,MANAGER_NO  FROM YDW.CUST_HOOK WHERE TYP = ?  and status in ('正常') and PERCENTAGE != 100) b on f.CST_NO= b.CUST_IN_NO and o.ORG0_CODE=b.ORG_NO
        where f.ACCT_TYPE = ?  and f.DATE_ID= ?
        """
        print etldate
        if typ=='存款':
            db.cursor.execute(f_sql,typ,'1',int(etldate))
        elif typ=='理财':
            db.cursor.execute(f_sql,typ,'8',int(etldate))
        else:
            return 
        fdict={}
        tmp=db.cursor.fetchone()
        while tmp:
            fdict[tmp[0]+'!'+tmp[3]]=tmp[1]+tmp[2]+tmp[3]       #账号 ! 客户经理 = 内码 + 机构号 + 客户经理
            tmp=db.cursor.fetchone()
        i_sql="""
        INSERT INTO YDW.ACCOUNT_HOOK_CJLI(MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, SUB_TYP, NOTE, CUST_IN_NO, BATCH_ID, ACCOUNT_NO, CARD_NO, FOLLOW_CUST) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """
        ilist=[]
        for i in fdict:             #最基础的数据
            accounts = i.split('!')
            if accounts[0] not in ahlist_hook:     #不存在账号的账号认定
                if i not in ahlist:     #不存在账号认定的此客户经理信息
                    if chdict.get(fdict.get(i)):    #内码 + 机构 + 客户经理
                        print accounts[0], accounts[1]
                        ilist.append(chdict.get(fdict.get(i))[1:]+[i.split('!')[0],i.split('!')[0],'客户号优先'])
        print len(ilist),typ
        db.cursor.executemany(i_sql,ilist)
        db.conn.commit()
    finally :
        db.closeDB()

if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen ==2:
        etldate=int(sys.argv[1])
        insert_miss(etldate,'存款')
        insert_miss_percentage(etldate,'存款')
    else:
        print "please input python %s yyyyMMdd"%sys.argv[0]
