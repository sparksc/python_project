# -*- coding:utf-8 -*-
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
客户经理存款指标报表
"""
def man_dep(stardate,etldate):
    try:
        db = util.DBConnect()
        while stardate<=etldate:
            sql="""
            DELETE FROM REPORT_ORG_DEP WHERE DATE_ID = ?
            """
            sql1="""
            INSERT INTO YDW.REPORT_ORG_DEP(DATE_ID, ORG_CODE, ORG_NAME, PRI_LAST, PRI_THIS) 
            SELECT F.DATE_ID,M.THIRD_BRANCH_CODE,M.THIRD_BRANCH_NAME,
            SUM(F1.BALANCE) AS DSCL,        --对私存量日均存款
            SUM(F.BALANCE)  AS DSXL         --对私现量日均存款
            FROM F_BALANCE F
            LEFT JOIN (SELECT ACCOUNT_ID, BALANCE FROM F_BALANCE F WHERE DATE_ID=(SELECT L_YEAREND_ID FROM D_DATE WHERE ID= ?) ) F1 ON F1.ACCOUNT_ID=F.ACCOUNT_ID
            JOIN D_ACCOUNT A ON F.ACCOUNT_ID=A.ID
            JOIN D_ACCOUNT_TYPE T ON F.ACCOUNT_TYPE_ID=T.ID AND ( LEFT(T.SUBJECT_CODE,4) IN ('2003','2004')
            OR LEFT(T.SUBJECT_CODE,6) IN ('200502') )
            JOIN D_DATE D ON F.DATE_ID=D.ID
            JOIN D_DATE DD ON D.L_YEAREND_ID=DD.ID
            JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID
            WHERE F.DATE_ID =? 
            GROUP BY F.DATE_ID,M.THIRD_BRANCH_CODE,M.THIRD_BRANCH_NAME
            """
            sql2="""
            SELECT 
            SUM(F1.BALANCE) AS DGCL,        --对公存量日均存款
            SUM(F.BALANCE)  AS DGXL,        --对公现量日均存款
            F.DATE_ID,M.THIRD_BRANCH_CODE
            FROM F_BALANCE F
            LEFT JOIN (SELECT ACCOUNT_ID, BALANCE FROM F_BALANCE F WHERE DATE_ID=(SELECT L_YEAREND_ID FROM D_DATE WHERE ID= ?) ) F1 ON F1.ACCOUNT_ID=F.ACCOUNT_ID
            JOIN D_ACCOUNT A ON F.ACCOUNT_ID=A.ID
            JOIN D_ACCOUNT_TYPE T ON F.ACCOUNT_TYPE_ID=T.ID AND ( LEFT(T.SUBJECT_CODE,4) IN ('2001','2002','2006','2011','2014','2012','2013')
            OR LEFT(T.SUBJECT_CODE,6) IN ('200501') OR T.SUBJECT_CODE IN ('20070101','20070201','20070301') )
            JOIN D_DATE D ON F.DATE_ID=D.ID
            JOIN D_DATE DD ON D.L_YEAREND_ID=DD.ID
            JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID
            WHERE F.DATE_ID =? 
            GROUP BY F.DATE_ID,M.THIRD_BRANCH_CODE,M.THIRD_BRANCH_NAME
            """
            sql3="""
            SELECT 
            SUM(F1.BALANCE)  AS DGCL,        --理财存量日均
            SUM(F.BALANCE)  AS DGXL,        --理财现量日均
            F.DATE_ID,M.THIRD_BRANCH_CODE
            FROM F_BALANCE F
            LEFT JOIN (SELECT ACCOUNT_ID, BALANCE FROM F_BALANCE F WHERE DATE_ID=(SELECT L_YEAREND_ID FROM D_DATE WHERE ID= ?) ) F1 ON F1.ACCOUNT_ID=F.ACCOUNT_ID
            JOIN D_ACCOUNT A ON F.ACCOUNT_ID=A.ID
            JOIN D_ACCOUNT_TYPE T ON F.ACCOUNT_TYPE_ID=T.ID AND T.SUBJECT_CODE IN ('20020104','20040108')
            JOIN D_DATE D ON F.DATE_ID=D.ID
            JOIN D_DATE DD ON D.L_YEAREND_ID=DD.ID
            JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID
            WHERE F.DATE_ID =? 
            GROUP BY F.DATE_ID,M.THIRD_BRANCH_CODE,M.THIRD_BRANCH_NAME
            """
            db.cursor.execute(sql,int(stardate))
            db.cursor.execute(sql1,int(stardate),int(stardate))
            db.cursor.execute(sql2,int(stardate),int(stardate))
            row2=db.cursor.fetchall()
            resultrow2=[]
            for i in row2:
                t=list(i[0:])
                resultrow2.append(t)
            #print resultrow2,"pub"
            u_sql2="""
            UPDATE REPORT_ORG_DEP SET PUB_LAST=? ,PUB_THIS=? WHERE DATE_ID=? and  ORG_CODE=?
            """
            db.cursor.executemany(u_sql2,resultrow2)


            db.cursor.execute(sql3,int(stardate),int(stardate))
            row3=db.cursor.fetchall()
            resultrow3=[]
            for i in row3:
                t=list(i[0:])
                resultrow3.append(t)
            print resultrow3
            u_sql3="""
            UPDATE REPORT_ORG_DEP SET FIN_LAST=?, FIN_THIS=? WHERE DATE_ID=? and  ORG_CODE=?
            """
            db.cursor.executemany(u_sql3,resultrow3)

            db.conn.commit()
            print stardate
            stardate=int(util.daycalc(stardate,1))
    finally :
        db.closeDB()

if __name__=='__main__':
    arglen=len(sys.argv)
    print sys.argv 
    if arglen ==3:
        stardate=int(sys.argv[1])
        etldate=int(sys.argv[2])
        print stardate,etldate
        man_dep(stardate,etldate)
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
