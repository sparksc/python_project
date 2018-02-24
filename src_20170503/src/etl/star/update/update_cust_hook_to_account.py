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
     
def insert_account_hook_by_cust(etldate,typ):
    try :
        db = util.DBConnect()
        #查找客户账户挂钩
        #状态全部到account——hook，当批准的时候，会同步修改acccout_hook,cust_hook
        print "find cust_hook"
        c_sql ="""
        SELECT 
            CUST_NO, MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, %s, END_DATE, STATUS, ETL_DATE, SRC, TYP,SUB_TYP, NOTE, CUST_IN_NO, BATCH_ID
        FROM 
            YDW.CUST_HOOK 
        WHERE 
            TYP = ? 
            ---and CUST_IN_NO='81068464720'
            ---and status in ( '已审批', '正常', '待审批', '预提交审批' ,'录入已审批' ) 
        """%( str(etldate) )

        db.cursor.execute(c_sql,typ)
        chook = {}
        tmp = db.cursor.fetchone()
        while tmp:
            key = tmp[2] +"-" + tmp[-2]  #机构号+客户内码
            datas = chook.get(key)
            if datas is None:
                datas = []
            datas.append( list(tmp) )
            chook[key] = datas
            tmp = db.cursor.fetchone()
        print "find account_hook"
        #查找当前有效挂钩关系
        #结束日期是否要考虑？TODO
        a_sql="""
         select 
            ORG_NO||'-'||ACCOUNT_NO,MANAGER_NO,PERCENTAGE,id,FOLLOW_CUST
         from 
            account_hook a 
         where 
            a.TYP =  ? 
            ---and a.account_no='101002101464759'
        """
        db.cursor.execute(a_sql,typ)
        ahook = {}
        tmp=db.cursor.fetchone()
        while tmp:
            datas = ahook.get( tmp[0] )
            if datas is None:
                datas = []
            datas.append( list(tmp) )
            ahook[ tmp[0] ] = datas
            tmp = db.cursor.fetchone()

        i_sql="""
            INSERT INTO YDW.ACCOUNT_HOOK(
                    MANAGER_NO, ORG_NO, PERCENTAGE, HOOK_TYPE, START_DATE, END_DATE, STATUS, ETL_DATE, SRC, TYP, SUB_TYP, NOTE, CUST_IN_NO, BATCH_ID, ACCOUNT_NO, CARD_NO, FOLLOW_CUST) 
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """

        u_sql = """
            update ACCOUNT_HOOK ah
            set ah.PERCENTAGE=?
            where id = ?
        """

        print "find balance"
        #查找到当天所有满足条件的账户
        #1.年积数>0,存款或者理财
        f_sql = """
        select 
            a.ACCOUNT_NO,f.CST_NO,o.ORG0_CODE 
        from F_BALANCE f
        join D_ACCOUNT a on f.ACCOUNT_ID=a.ID
        join D_ORG o on f.ORG_ID=o.ID
        where 
            f.ACCT_TYPE = ?  and f.DATE_ID= ?
        """
        if typ=='存款':
            f_sql = f_sql + " and f.year_pdt >0 "
            db.cursor.execute(f_sql, '1', etldate)
        elif typ=='理财':
            db.cursor.execute(f_sql, '8', etldate)
        else:
            return 
        tmp = db.cursor.fetchone()
        ilist = [] 
        ulist = []
        while tmp:
            #检查挂钩关系是否存在（包括比例是否100%）
            #print tmp
            account_no = tmp[0]
            key = tmp[2]+"-"+tmp[0]
            ckey = tmp[2]+"-"+tmp[1]
            cust = chook.get( ckey )
            #没有客户挂钩，跳过
            tmp = db.cursor.fetchone()
            if cust is None: continue

            #有客户挂钩信息，检查当前挂钩比例
            hook = ahook.get(key)
            if hook is None:
                #插入挂钩比例
                lp = 100
                for ck in cust:
                    if ck[3] > lp : continue
                    lp = lp - ck[3]
                    #插入挂钩比例
                    row = ck[1:] + [account_no,account_no,'客户号优先']
                    ilist.append( row )
                    if lp == 0: break
            else:
                #统计已挂钩比例
                p = 0
                for k in hook: 
                    p = p + k[2]
                #大于100？ TODO
                if p >= 100: continue
                #剩余可挂钩比例
                lp = 100 - p
                #print lp
                #从客户挂钩比例获取 
                for ck in cust:
                    #print ck[3],lp
                    #已有挂钩比例，则修改原有挂钩比例，
                    fak = None
                    #查找是否有相同客户经理的挂钩
                    for ak in hook:
                        if ak[1] == ck[1]:
                            fak = ak
                            break
                    #找到有该账号已有相同挂钩比例
                    if  fak is not None:
                        #是否账号优先？
                        if fak[4] == "账号优先": continue
                        #调整可用比例
                        fp = ck[3]      
                        lp = lp - (ck[3] - fak[2])
                        if lp < 0 : continue
                        ulist.append( (fp,fak[3]) )
                    else:
                        if ck[3] > lp : continue
                        row = ck[1:] + [account_no,account_no,'客户号优先']
                        lp = lp - ck[3]
                        ilist.append( row )
                    if lp == 0: break
        db.cursor.executemany(i_sql, ilist)
        db.cursor.executemany(u_sql, ulist)
        db.conn.commit()
    finally :
        db.closeDB()


if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen ==2:
        etldate=int(sys.argv[1])
        insert_account_hook_by_cust(etldate,'存款')
    else:
        print "please input python %s yyyyMMdd"%sys.argv[0]
