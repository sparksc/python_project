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
    删除重复hook记录以及插入待认定的未认定帐号,最后更新存贷款的  余额 和 日均，删除前年销户的account_hook 记录
"""
#删除etl_hook产生的在CUST_HOOK和ACCOUNT_HOOK中的重复数据
def del_dup():
    try :
        db = util.DBConnect()
        c_sql ="""
        SELECT MAX(ID) FROM CUST_HOOK GROUP BY HOOK_TYPE,TYP,SUB_TYP,CUST_IN_NO,ORG_NO,MANAGER_NO HAVING COUNT(1)>1
        """
        db.cursor.execute(c_sql)
        row=db.cursor.fetchall()
        while row:
            dc_sql="""
            DELETE FROM CUST_HOOK WHERE ID = ?   
            """
            db.cursor.executemany(dc_sql,row)    
            db.conn.commit()
            db.cursor.execute(c_sql)
            row=db.cursor.fetchall()
        a_sql ="""
        SELECT MAX(ID) FROM ACCOUNT_HOOK GROUP BY HOOK_TYPE,TYP,ACCOUNT_NO,MANAGER_NO HAVING COUNT(1)>1
        """
        db.cursor.execute(a_sql)
        row=db.cursor.fetchall()
        while row:
            da_sql="""
            DELETE FROM ACCOUNT_HOOK WHERE ID = ?   
            """
            db.cursor.executemany(da_sql,row)    
            db.conn.commit()
            db.cursor.execute(a_sql)
            row=db.cursor.fetchall()
        dc_sql="""
        delete from CUST_HOOK where ID in(
        select a.ID from CUST_HOOK a,(select distinct CUST_IN_NO,ORG_NO,TYP from CUST_HOOK where STATUS in ('待审批','已审批','预提交审批','正常','录入已审批')) b 
        where a.STATUS='待手工' and a.CUST_IN_NO=b.CUST_IN_NO and a.ORG_NO=b.ORG_NO and a.TYP=b.TYP)
        """
        db.cursor.execute(dc_sql)
        da_sql="""
        delete from ACCOUNT_HOOK where ID in (
        select a.ID from ACCOUNT_HOOK a,(select distinct ACCOUNT_NO from ACCOUNT_HOOK where STATUS in ('待审批','已审批','预提交审批','正常','录入已审批')) b 
        where a.STATUS='待手工' and a.ACCOUNT_NO=b.ACCOUNT_NO)
        """
        db.cursor.execute(da_sql)
        u_sql ="""
        merge into CUST_HOOK a
        using D_CUST_INFO b on a.cust_in_no=b.cust_no and a.cust_no='无'
        when matched then update set a.cust_no=b.cust_long_no
        """
        db.cursor.execute(u_sql)
        db.conn.commit()
    finally :
        db.closeDB()

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

        #a_sql="""
        #select distinct ACCOUNT_NO,MANAGER_NO from account_hook a where a.TYP = ?
        #"""
        #db.cursor.execute(a_sql,typ,typ)
        #ahlist={}
        #tmp=db.cursor.fetchone()
        #while tmp:
        #    ahlist[tmp[0]+'!'+tmp[1]]=tmp[0]
        #    tmp=db.cursor.fetchone()
        #print len(ahlist),typ

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
        print len(fdict),typ    
        i_sql="""
        INSERT INTO YDW.ACCOUNT_HOOK(MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, SUB_TYP, NOTE, CUST_IN_NO, BATCH_ID, ACCOUNT_NO, CARD_NO, FOLLOW_CUST) 
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, ?)
        """
        ilist=[]
        for i in fdict:             #i=
            accounts = i.split('!')
            if accounts[0] not in ahlist_hook:     #不存在账号的认定
                if chdict.get(fdict.get(i)):
                    ilist.append(chdict.get(fdict.get(i))[1:]+[i.split('!')[0],i.split('!')[0],'客户号优先'])
                    #print chdict.get(fdict.get(i))
                    print accounts[0], accounts[1]
        print len(ilist),typ
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
        print len(fdict),typ    
        i_sql="""
        INSERT INTO YDW.ACCOUNT_HOOK(MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, SUB_TYP, NOTE, CUST_IN_NO, BATCH_ID, ACCOUNT_NO, CARD_NO, FOLLOW_CUST) 
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

#将存贷款和理财的日均余额更新到CUST_HOOK,和ACCOUNT_HOOK上        
def update_balance(etldate):
    print 'update_balance begin'
    try :
        db = util.DBConnect()
        l_sql ="""
        MERGE INTO CUST_HOOK CH
        USING (
        SELECT F.CST_NO,O.ORG0_CODE,SUM(F.BALANCE) A,SUM(F.YEAR_PDT)/ (SELECT YEAR_DAYS FROM D_DATE WHERE ID=(SELECT L_YEAREND_ID   FROM D_DATE WHERE ID= ?)) AS B FROM F_BALANCE F
        JOIN D_ORG O ON F.ORG_ID=O.ID
        WHERE F.ACCT_TYPE=4 AND F.DATE_ID=(SELECT L_YEAREND_ID FROM D_DATE WHERE ID= ?)
        GROUP BY F.CST_NO,O.ORG0_CODE
        ) X ON CH.TYP='贷款' AND CH.ORG_NO=X.ORG0_CODE AND CH.CUST_IN_NO=X.CST_NO
        WHEN MATCHED THEN UPDATE SET CH.EXIST_AVG_BALANCE=X.B
        """
        db.cursor.execute(l_sql,etldate,etldate)
        db.conn.commit()
        ll_sql ="""
        MERGE INTO CUST_HOOK CH
        USING (
        SELECT F.CST_NO,O.ORG0_CODE,SUM(F.BALANCE) A,SUM(F.YEAR_PDT)/ (SELECT BEG_YEAR_DAYS FROM D_DATE WHERE ID= ?) AS B FROM F_BALANCE F
        JOIN D_ORG O ON F.ORG_ID=O.ID
        WHERE F.ACCT_TYPE=4 AND F.DATE_ID= ?
        GROUP BY F.CST_NO,O.ORG0_CODE
        ) X ON CH.TYP='贷款' AND CH.ORG_NO=X.ORG0_CODE AND CH.CUST_IN_NO=X.CST_NO
        WHEN MATCHED THEN UPDATE SET CH.ADD_AVG_BALANCE=X.B,CH.BALANCE=X.A
        """
        db.cursor.execute(ll_sql,etldate,etldate)
        db.conn.commit()
        d_sql ="""
        MERGE INTO ACCOUNT_HOOK AH
        USING
        (SELECT AH.ID,F.BALANCE,F.YEAR_PDT/ (SELECT YEAR_DAYS FROM D_DATE WHERE ID=(SELECT L_YEAREND_ID FROM D_DATE WHERE ID= ?)) A FROM F_BALANCE F
        JOIN D_ACCOUNT A ON F.ACCOUNT_ID=A.ID 
        JOIN D_ACCOUNT_PRICE P ON F.ACCOUNT_PRICE_ID=P.ID AND P.CCY='CNY'
        JOIN ACCOUNT_HOOK AH ON AH.ACCOUNT_NO=A.ACCOUNT_NO AND AH.TYP='存款'
        WHERE F.DATE_ID=(SELECT L_YEAREND_ID FROM D_DATE WHERE ID= ?) AND F.ACCT_TYPE=1 
        ) X ON AH.ID=X.ID 
        WHEN MATCHED THEN UPDATE SET AH.EXIST_AVG_BALANCE=X.A
        """
        db.cursor.execute(d_sql,etldate,etldate)
        db.conn.commit()
        dd_sql ="""
        MERGE INTO ACCOUNT_HOOK AH
        USING
        (SELECT AH.ID,F.BALANCE,F.YEAR_PDT/ (SELECT BEG_YEAR_DAYS FROM D_DATE WHERE ID= ?) A FROM F_BALANCE F
        JOIN D_ACCOUNT A ON F.ACCOUNT_ID=A.ID 
        JOIN D_ACCOUNT_PRICE P ON F.ACCOUNT_PRICE_ID=P.ID AND P.CCY='CNY'
        JOIN ACCOUNT_HOOK AH ON AH.ACCOUNT_NO=A.ACCOUNT_NO AND AH.TYP='存款'
        WHERE F.DATE_ID= ? AND F.ACCT_TYPE=1 
        ) X ON AH.ID=X.ID 
        WHEN MATCHED THEN UPDATE SET AH.BALANCE=X.BALANCE,AH.ADD_AVG_BALANCE=X.A
        """
        db.cursor.execute(dd_sql,etldate,etldate)
        db.conn.commit()
        f_sql ="""
        MERGE INTO ACCOUNT_HOOK AH
        USING
        (SELECT AH.ID,F.BALANCE,F.YEAR_PDT/ (SELECT YEAR_DAYS FROM D_DATE WHERE ID=(SELECT L_YEAREND_ID FROM D_DATE WHERE ID= ?)) A FROM F_BALANCE F
        JOIN D_ACCOUNT A ON F.ACCOUNT_ID=A.ID --AND A.CLOSE_DATE_ID>F.DATE_ID
        JOIN ACCOUNT_HOOK AH ON AH.ACCOUNT_NO=A.ACCOUNT_NO AND AH.TYP='理财'
        WHERE F.DATE_ID=(SELECT L_YEAREND_ID FROM D_DATE WHERE ID= ?) AND F.ACCT_TYPE=8 
        ) X ON AH.ID=X.ID 
        WHEN MATCHED THEN UPDATE SET AH.EXIST_AVG_BALANCE=X.A
        """
        db.cursor.execute(f_sql,etldate,etldate)
        db.conn.commit()
        ff_sql ="""
        MERGE INTO ACCOUNT_HOOK AH
        USING
        (SELECT AH.ID,F.BALANCE,F.YEAR_PDT/ (SELECT BEG_YEAR_DAYS FROM D_DATE WHERE ID= ?) A FROM F_BALANCE F
        JOIN D_ACCOUNT A ON F.ACCOUNT_ID=A.ID 
        JOIN ACCOUNT_HOOK AH ON AH.ACCOUNT_NO=A.ACCOUNT_NO AND AH.TYP='理财'
        WHERE F.DATE_ID= ? AND F.ACCT_TYPE=8 
        ) X ON AH.ID=X.ID 
        WHEN MATCHED THEN UPDATE SET AH.BALANCE=X.BALANCE,AH.ADD_AVG_BALANCE=X.A
        """
        db.cursor.execute(ff_sql,etldate,etldate)
        db.conn.commit()
        u_sql="""
        MERGE INTO CUST_HOOK CH
        USING (
        SELECT CUST_IN_NO,ORG_NO,SUM(BALANCE) A,SUM(EXIST_AVG_BALANCE) B,SUM(ADD_AVG_BALANCE) C FROM ACCOUNT_HOOK WHERE TYP ='存款' --AND FOLLOW_CUST='客户号优先'
        GROUP BY CUST_IN_NO,ORG_NO
        ) X ON CH.CUST_IN_NO=X.CUST_IN_NO AND CH.ORG_NO=X.ORG_NO AND CH.TYP = '存款'
        WHEN MATCHED THEN UPDATE SET CH.ADD_AVG_BALANCE=X.C,CH.BALANCE=X.A,CH.EXIST_AVG_BALANCE=X.B
        """
        db.cursor.execute(u_sql)
        db.conn.commit()
        uu_sql="""
        MERGE INTO CUST_HOOK CH
        USING (
        SELECT CUST_IN_NO,ORG_NO,SUM(BALANCE) A,SUM(EXIST_AVG_BALANCE) B,SUM(ADD_AVG_BALANCE) C FROM ACCOUNT_HOOK WHERE TYP ='理财' --AND FOLLOW_CUST='客户号优先'
        GROUP BY CUST_IN_NO,ORG_NO
        ) X ON CH.CUST_IN_NO=X.CUST_IN_NO AND CH.ORG_NO=X.ORG_NO AND CH.TYP = '理财'
        WHEN MATCHED THEN UPDATE SET CH.ADD_AVG_BALANCE=X.C,CH.BALANCE=X.A,CH.EXIST_AVG_BALANCE=X.B
        """
        db.cursor.execute(uu_sql)
        db.conn.commit()
    finally :
        db.closeDB()

if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen ==2:
        etldate=int(sys.argv[1])
        del_dup()
        insert_miss(etldate,'存款')
        insert_miss(etldate,'理财')
        insert_miss_percentage(etldate,'存款')      #补齐正常分润数据
        insert_miss_percentage(etldate,'理财')      #补齐正常分润数据
        update_balance(etldate)
    else:
        print "please input python %s yyyyMMdd"%sys.argv[0]
