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
     
"""
每次报表之前先将所有员工信息初始化在不同的报表中，后续报表全部做更新
1、注意程序，不能删除信息
2、如果已经存在则会导致重复
"""
def report_init(stardate,etldate):
    try:
        db = util.DBConnect()
        while stardate<=etldate:
            """
            信用卡初始化
            """
            sql_cr="""
            DELETE FROM YDW.REPORT_MANAGER_CREDITCARD WHERE DATE_ID=?
            """
            db.cursor.execute(sql_cr,int(stardate))
            db.conn.commit()
            sql0="""
            INSERT INTO YDW.REPORT_MANAGER_CREDITCARD(DATE_ID, ORG_CODE, ORG_NAME, SALE_CODE, SALE_NAME)
            SELECT %s,B.BRANCH_CODE, B.BRANCH_NAME, F.USER_NAME, F.NAME FROM BRANCH B
            JOIN USER_BRANCH U ON U.BRANCH_ID=B.ROLE_ID
            JOIN F_USER F ON U.USER_ID=F.ROLE_ID
            WHERE LEFT(B.BRANCH_CODE,1)!='M' 
            UNION
            SELECT %s, B.BRANCH_CODE, B.BRANCH_NAME, B.BRANCH_CODE, B.BRANCH_NAME FROM BRANCH B WHERE LEFT(B.BRANCH_CODE,1)!='M'
            """%(stardate, stardate)
            db.cursor.execute(sql0,int(stardate))

            """
            信用卡不良初始化
            """
            sql_cb="""
            DELETE FROM YDW.REPORT_CREDIT_BAD WHERE DATE_ID=?
            """
            db.cursor.execute(sql_cr,int(stardate))
            db.conn.commit()
            sql0="""
            INSERT INTO YDW.REPORT_CREDIT_BAD(DATE_ID, ORG_CODE, ORG_NAME, SALE_CODE, SALE_NAME)
            SELECT %s,B.BRANCH_CODE, B.BRANCH_NAME, F.USER_NAME, F.NAME FROM BRANCH B
            JOIN USER_BRANCH U ON U.BRANCH_ID=B.ROLE_ID
            JOIN F_USER F ON U.USER_ID=F.ROLE_ID
            WHERE LEFT(B.BRANCH_CODE,1)!='M' 
            UNION
            SELECT %s, B.BRANCH_CODE, B.BRANCH_NAME, B.BRANCH_CODE, B.BRANCH_NAME FROM BRANCH B WHERE LEFT(B.BRANCH_CODE,1)!='M'
            """%(stardate, stardate)
            db.cursor.execute(sql0,int(stardate))

            """
            其他业务初始化
            """
            sql_ot="""
            DELETE FROM YDW.report_manager_other WHERE DATE_ID=?
            """
            db.cursor.execute(sql_ot,int(stardate))
            db.conn.commit()
            sql1="""
            INSERT INTO YDW.report_manager_other(DATE_ID, ORG_CODE, ORG_NAME, SALE_CODE, SALE_NAME)
            SELECT %s,B.BRANCH_CODE, B.BRANCH_NAME, F.USER_NAME, F.NAME FROM BRANCH B
            JOIN USER_BRANCH U ON U.BRANCH_ID=B.ROLE_ID
            JOIN F_USER F ON U.USER_ID=F.ROLE_ID
            WHERE LEFT(B.BRANCH_CODE,1)!='M' 
            UNION
            SELECT %s, B.BRANCH_CODE, B.BRANCH_NAME, B.BRANCH_CODE, B.BRANCH_NAME FROM BRANCH B WHERE LEFT(B.BRANCH_CODE,1)!='M'
            """%(stardate, stardate)
            db.cursor.execute(sql1,int(stardate))

            """
            贷款初始化
            """
            sql_lo="""
            DELETE FROM YDW.REPORT_MANAGER_LOAN WHERE DATE_ID=?
            """
            db.cursor.execute(sql_lo,int(stardate))
            db.conn.commit()
            sql2="""
            INSERT INTO YDW.REPORT_MANAGER_LOAN(DATE_ID, ORG_CODE, ORG_NAME, SALE_CODE, SALE_NAME)
            SELECT %s,B.BRANCH_CODE, B.BRANCH_NAME, F.USER_NAME, F.NAME FROM BRANCH B
            JOIN USER_BRANCH U ON U.BRANCH_ID=B.ROLE_ID
            JOIN F_USER F ON U.USER_ID=F.ROLE_ID
            WHERE LEFT(B.BRANCH_CODE,1)!='M' 
            UNION
            SELECT %s, B.BRANCH_CODE, B.BRANCH_NAME, B.BRANCH_CODE, B.BRANCH_NAME FROM BRANCH B WHERE LEFT(B.BRANCH_CODE,1)!='M'
            """%(stardate, stardate)
            db.cursor.execute(sql2,int(stardate))

            """
            存款初始化
            """
            sql_de="""
            DELETE FROM YDW.REPORT_MANAGER_DEP WHERE DATE_ID=?
            """
            db.cursor.execute(sql_de,int(stardate))


            sql_de="""
            DELETE FROM YDW.REPORT_MANAGER_DEP_MONTH WHERE DATE_ID=?
            """
            db.cursor.execute(sql_de,int(stardate))

            db.conn.commit()

            sql3="""
            INSERT INTO YDW.REPORT_MANAGER_DEP(DATE_ID, ORG_CODE, SALE_CODE)
            SELECT %s,B.BRANCH_CODE, F.USER_NAME  FROM BRANCH B
            JOIN USER_BRANCH U ON U.BRANCH_ID=B.ROLE_ID
            JOIN F_USER F ON U.USER_ID=F.ROLE_ID
            WHERE LEFT(B.BRANCH_CODE,1)!='M' 
            UNION
            SELECT %s, B.BRANCH_CODE,  B.BRANCH_CODE FROM BRANCH B WHERE LEFT(B.BRANCH_CODE,1)!='M'
            UNION
            SELECT %s,  A.ORG_NO,A.MANAGER_NO FROM ACCOUNT_HOOK A
            JOIN D_ORG O ON O.ORG0_CODE=A.ORG_NO
            JOIN F_USER M ON M.USER_NAME=A.MANAGER_NO
            WHERE LEFT(A.ORG_NO,1)!='M'
            UNION
            SELECT %s,D.THIRD_BRANCH_CODE,D.SALE_CODE 
            FROM D_SALE_MANAGE_RELA D 
            JOIN V_STAFF_INFO V ON D.SALE_CODE=V.USER_NAME 
            JOIN D_ORG DG ON DG.ORG0_CODE=V.ORG AND DG.ORG1_CODE=D.SECOND_BRANCH_CODE
            WHERE LEFT(D.THIRD_BRANCH_CODE,1)!='M' AND D.THIRD_BRANCH_CODE!='无' AND D.DIM_DATE=%s
            """%(stardate, stardate,stardate,stardate,str(stardate)[0:4])
            db.cursor.execute(sql3,int(stardate))

            sql3="""
            INSERT INTO YDW.REPORT_MANAGER_DEP_MONTH(DATE_ID, ORG_CODE, SALE_CODE)
            SELECT %s,B.BRANCH_CODE, F.USER_NAME  FROM BRANCH B
            JOIN USER_BRANCH U ON U.BRANCH_ID=B.ROLE_ID
            JOIN F_USER F ON U.USER_ID=F.ROLE_ID
            WHERE LEFT(B.BRANCH_CODE,1)!='M' 
            UNION
            SELECT %s, B.BRANCH_CODE,  B.BRANCH_CODE FROM BRANCH B WHERE LEFT(B.BRANCH_CODE,1)!='M'
            UNION
            SELECT %s,  A.ORG_NO,A.MANAGER_NO FROM ACCOUNT_HOOK A
            JOIN D_ORG O ON O.ORG0_CODE=A.ORG_NO
            JOIN F_USER M ON M.USER_NAME=A.MANAGER_NO
            WHERE LEFT(A.ORG_NO,1)!='M'
            UNION
            SELECT %s,D.THIRD_BRANCH_CODE,D.SALE_CODE 
            FROM D_SALE_MANAGE_RELA D 
            JOIN V_STAFF_INFO V ON D.SALE_CODE=V.USER_NAME 
            JOIN D_ORG DG ON DG.ORG0_CODE=V.ORG AND DG.ORG1_CODE=D.SECOND_BRANCH_CODE
            WHERE LEFT(D.THIRD_BRANCH_CODE,1)!='M' AND D.THIRD_BRANCH_CODE!='无' AND D.DIM_DATE=%s
            """%(stardate, stardate,stardate,stardate,str(stardate)[0:4])
            db.cursor.execute(sql3,int(stardate))

            db.conn.commit()
            stardate=int(util.daycalc(stardate,1))
    finally :
        db.closeDB()

if __name__=='__main__':
    arglen=len(sys.argv)
    print sys.argv 
    d1=datetime.now()
    if arglen ==3:
        stardate=int(sys.argv[1])
        etldate=int(sys.argv[2])
        print stardate,etldate
        report_init(stardate,etldate)
        print "finish",datetime.now()-d1
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
