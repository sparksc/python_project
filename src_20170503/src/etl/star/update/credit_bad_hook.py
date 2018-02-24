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

"""
    1.不考核福农卡, 所有福农卡不在不良计算内(D_CREIDT_CARD表中PRODUCT字段为 0632 的为福农卡)
"""
     
def run(etldate):
    old_critical_dt = 20170101  #信用卡新老划分日期参数
    old_evaluate_dt = 20171231  #老信用卡考核开始日期参数
    months = 6  #移交划界月份数

    try :
        db = util.DBConnect()
        init_sql = """
            DELETE FROM CREDIT_BAD_HOOK WHERE ETL_DATE = ?
        """
        db.cursor.execute(init_sql,etldate)


        print "***** deal with old credit card data *****"

        if etldate > old_evaluate_dt :
            insert_sql = """
            INSERT INTO CREDIT_BAD_HOOK(ORG_NO, MANAGER_NO, CARD_NO, ETL_DATE, FLAG)
                SELECT A.ORG_NO, A.MANAGER_NO, D.CARD_NO, ?, 1
                FROM ACCOUNT_HOOK A
                INNER JOIN D_CREDIT_CARD D ON D.CARD_NO=A.ACCOUNT_NO AND D.PRODUCT != '0632'
                INNER JOIN F_CREDIT_BAD F ON F.CRAD_ID=D.ID
                WHERE F.DATE_ID = ? AND A.TYP = '信用卡' AND A.STATUS in ( '已审批', '正常', '待审批', '预提交审批' ,'录入已审批' ) AND D.OPEN_DATE < ?
            """
            db.cursor.execute(insert_sql, etldate, etldate, old_critical_dt)
            db.conn.commit()
        else : 
            insert_sql = """
            INSERT INTO CREDIT_BAD_HOOK(ORG_NO, MANAGER_NO, CARD_NO, ETL_DATE, FLAG)
                SELECT A.ORG_NO, A.MANAGER_NO, D.CARD_NO, ?, 0
                FROM ACCOUNT_HOOK A
                INNER JOIN D_CREDIT_CARD D ON D.CARD_NO=A.ACCOUNT_NO AND D.PRODUCT != '0632'
                INNER JOIN F_CREDIT_BAD F ON F.CRAD_ID=D.ID
                WHERE F.DATE_ID = ? AND A.TYP = '信用卡' AND A.STATUS in ( '已审批', '正常', '待审批', '预提交审批' ,'录入已审批' ) AND D.OPEN_DATE < ?
            """
            db.cursor.execute(insert_sql, etldate, etldate, old_critical_dt)
            db.conn.commit()
            
        print "***** deal with new credit card data *****"

        print "***** deal with new credit card data moved*****"
        #移交6个月以内的信用卡取原挂钩关系, 即移交记录中的from_teller_no字段
        insert_sql = """
            INSERT INTO CREDIT_BAD_HOOK(ORG_NO, MANAGER_NO, CARD_NO, ETL_DATE, FLAG)
                SELECT A.ORG_NO, T.FROM_TELLER_NO, D.CARD_NO, ?, 1
                FROM ACCOUNT_HOOK A
                INNER JOIN D_CREDIT_CARD D ON D.CARD_NO=A.ACCOUNT_NO AND D.PRODUCT != '0632'
                INNER JOIN F_CREDIT_BAD F ON F.CRAD_ID=D.ID
                INNER JOIN CUST_HOOK_BATCH T ON T.ID=A.BATCH_ID
                WHERE F.DATE_ID = ? AND A.TYP = '信用卡' AND A.STATUS in ( '已审批', '正常', '待审批', '预提交审批' ,'录入已审批' ) AND D.OPEN_DATE >= ?
                AND TIMESTAMPDIFF(64, CHAR(TO_DATE(?,'YYYYMMDD') - TO_DATE(A.ETL_DATE,'YYYYMMDD'))) < ?
            """
        db.cursor.execute(insert_sql, etldate, etldate, old_critical_dt, str(etldate), months)
        db.conn.commit()

        #移交6个月以外的信用卡取现挂钩关系, 即ACCOUNT_HOOK的MANAGER_NO字段(可用CASE WHEN合并)
        insert_sql = """
            INSERT INTO CREDIT_BAD_HOOK(ORG_NO, MANAGER_NO, CARD_NO, ETL_DATE, FLAG)
                SELECT A.ORG_NO, A.MANAGER_NO, D.CARD_NO, ?, 1
                FROM ACCOUNT_HOOK A
                INNER JOIN D_CREDIT_CARD D ON D.CARD_NO=A.ACCOUNT_NO AND D.PRODUCT != '0632'
                INNER JOIN F_CREDIT_BAD F ON F.CRAD_ID=D.ID
                INNER JOIN CUST_HOOK_BATCH T ON T.ID=A.BATCH_ID
                WHERE F.DATE_ID = ? AND A.TYP = '信用卡' AND A.STATUS in ( '已审批', '正常', '待审批', '预提交审批' ,'录入已审批' ) AND D.OPEN_DATE >= ?
                AND TIMESTAMPDIFF(64, CHAR(TO_DATE(?,'YYYYMMDD') - TO_DATE(A.ETL_DATE,'YYYYMMDD'))) >= ?
            """
        db.cursor.execute(insert_sql, etldate, etldate, old_critical_dt, str(etldate), months)
        db.conn.commit()

        print "***** deal with new credit card data no moved*****"
        #若无移交,则挂钩给ACCOUNT_HOOK中的MANAGER_NO
        insert_sql = """
            INSERT INTO CREDIT_BAD_HOOK(ORG_NO, MANAGER_NO, CARD_NO, ETL_DATE, FLAG)
                SELECT A.ORG_NO, A.MANAGER_NO, D.CARD_NO, ?, 1
                FROM ACCOUNT_HOOK A
                INNER JOIN D_CREDIT_CARD D ON D.CARD_NO=A.ACCOUNT_NO AND D.PRODUCT != '0632'
                INNER JOIN F_CREDIT_BAD F ON F.CRAD_ID=D.ID
                LEFT JOIN CUST_HOOK_BATCH T ON T.ID=A.BATCH_ID
                WHERE F.DATE_ID = ? AND T.ID IS Null AND A.TYP = '信用卡' AND A.STATUS in ( '已审批', '正常', '待审批', '预提交审批' ,'录入已审批' ) AND D.OPEN_DATE >= ?
        """
        db.cursor.execute(insert_sql, etldate, etldate, old_critical_dt)
        db.conn.commit()

    finally :
        db.closeDB()


if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen != 3:
        print "please input python %s yyyyyMMdd yyyyMMdd "%(sys.argv[0])
    else:
        startdate=sys.argv[1]
        enddate=sys.argv[2]
        etldate=int(startdate)
        while etldate<=int(enddate):    
            print etldate
            Config().etldate =etldate
            Config().stretldate=util.tostrdate(etldate)        
            run(etldate)
            etldate=int(util.daycalc(etldate,1))
