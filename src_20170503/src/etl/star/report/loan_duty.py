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
import man_loan_sal_new as loansal
     
condecimal = getcontext()
"""
客户经理贷款指标报表
"""
def man_loan(stardate,etldate):
    try:
        oneday=datetime.now()
        db = util.DBConnect()
        while stardate<=etldate:
            """贷款责任 责任贷款每日余额"""
            sql="""
            SELECT BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' THEN F.BALANCE*M.PERCENT/ 100 ELSE 0 END)) AS DSZRYE,--对私
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' THEN F.BALANCE*M.PERCENT/ 100 ELSE 0 END)) AS DGZRYE,--对公
            F.DATE_ID, M.SALE_CODE 
            FROM F_BALANCE F
            JOIN D_LOAN_ACCOUNT D ON D.ID = F.ACCOUNT_ID
            JOIN D_LOAN_ACCT_RELA M ON M.ACCT_ID = D.CONTRACT_NO AND F.DATE_ID >= M.ISTART_DT AND F.DATE_ID <= M.IEND_DT
            WHERE F.DATE_ID = ? AND F.ACCT_TYPE = '4'
            GROUP BY F.DATE_ID, M.SALE_CODE
            """
            sql1="""
            UPDATE REPORT_MANAGER_LOAN B SET DSZRYE=?,DGZRYE=?,FLAG=1 WHERE DATE_ID=? AND SALE_CODE=? 
            ----UPDATE REPORT_MANAGER_LOAN_TEMP_DUTY B SET DSZRYE=?,DGZRYE=? WHERE DATE_ID=? AND SALE_CODE=? 
            """
            """责任贷款四级不良余额"""
            sql2="""
            SELECT  BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' THEN F.BALANCE*M.PERCENT/ 100 ELSE 0 END)) AS DSZRYE1,--对私
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' THEN F.BALANCE*M.PERCENT/ 100 ELSE 0 END)) AS DGZRYE1, --对公
            F.DATE_ID, M.SALE_CODE 
            FROM F_BALANCE F
            JOIN D_ACCOUNT_STATUS S ON F.ACCOUNT_STATUS_ID = S.ID
            JOIN D_LOAN_ACCOUNT D ON D.ID = F.ACCOUNT_ID
            JOIN D_LOAN_ACCT_RELA M ON M.ACCT_ID = D.CONTRACT_NO AND F.DATE_ID >= M.ISTART_DT AND F.DATE_ID <= M.IEND_DT
            WHERE F.DATE_ID = ? AND F.ACCT_TYPE = '4' AND S.GRADE_FOUR NOT IN ('正常')
            GROUP BY F.DATE_ID, M.SALE_CODE
            """
            sql3="""
            UPDATE REPORT_MANAGER_LOAN B SET DSZRYE1=?,DGZRYE1=?,FLAG=1 WHERE DATE_ID=? AND SALE_CODE=? 
            ----UPDATE REPORT_MANAGER_LOAN_TEMP_DUTY B SET DSZRYE1=?,DGZRYE1=? WHERE DATE_ID=? AND SALE_CODE=? 
            """
            db.cursor.execute(sql,int(stardate))
            row=db.cursor.fetchall()
            resultrow=[]
            for i in row:
                t=list(i[0:])
                resultrow.append(t)
            #print resultrow
            db.cursor.executemany(sql1,resultrow)

            db.cursor.execute(sql2,int(stardate))
            row2=db.cursor.fetchall()
            resultrow2=[]
            for i in row2:
                t=list(i[0:])
                resultrow2.append(t)
            #print resultrow2
            db.cursor.executemany(sql3,resultrow2)
            """责任应收利息"""
            sql4="""
            SELECT BIGINT(SUM(CASE WHEN F.INAKFLAG = '1' THEN F.INABBLNC*M.PERCENT2/ 100 ELSE 0 END)) AS DSYSLX,--表内
            BIGINT(SUM(CASE WHEN F.INAKFLAG = '0' THEN F.INABBLNC*M.PERCENT2/ 100 ELSE 0 END)) AS DGYSLX,--表外
            BIGINT(F.WORKDATE), M.SALE_CODE
            --SUM( F.INABBLNC*M.PERCENT2/ 100 ) AS ZRLX    --合计
            FROM ODS_CORE_BLFMPMIN F
            JOIN D_LOAN_ACCT_RELA M ON M.ACCT_ID = F.INAACONO AND F.WORKDATE >= M.ISTART_DT AND F.WORKDATE <= M.IEND_DT
            WHERE F.WORKDATE = ?  AND F.INAALQFG != '3'
            GROUP BY F.WORKDATE, M.SALE_CODE WITH UR
            """
            sql5="""
            UPDATE REPORT_MANAGER_LOAN  SET DSYSLX=?,DGYSLX=?,FLAG=1 WHERE DATE_ID=? AND SALE_CODE=?
            -----UPDATE REPORT_MANAGER_LOAN_TEMP_DUTY SET DSYSLX=?,DGYSLX=? WHERE DATE_ID=? AND SALE_CODE=?
            """
            db.cursor.execute(sql4,str(stardate))
            row4=db.cursor.fetchall()
            resultrow4=[]
            for i in row4:
                t=list(i[0:])
                resultrow4.append(t)
            #print resultrow4
            db.cursor.executemany(sql5,resultrow4)
            """管户挂钩存款"""
            sql6="""
            SELECT BIGINT(SUM(CASE WHEN LEFT(FF.CST_NO,2)='81' THEN FF.BALANCE ELSE 0 END)) AS DSGGYE,--对私
            BIGINT(SUM(CASE WHEN LEFT(FF.CST_NO,2)='82' THEN FF.BALANCE ELSE 0 END)) AS DGGGYE, --对公
            BIGINT(SUM(CASE WHEN LEFT(FF.CST_NO,2)='81' THEN FF.YEAR_PDT ELSE 0 END)) / DA.BEG_YEAR_DAYS AS DSGGRJ,--对私
            BIGINT(SUM(CASE WHEN LEFT(FF.CST_NO,2)='82' THEN FF.YEAR_PDT ELSE 0 END)) / DA.BEG_YEAR_DAYS AS DGGGRJ, --对公
            FF.DATE_ID, B.SALE_CODE
             FROM F_BALANCE FF
             JOIN (
             SELECT DISTINCT F.DATE_ID AS DATE_ID, M.SALE_CODE AS SALE_CODE, A.CST_NO AS CST_NO, F.ORG_ID AS ORG_ID  FROM D_LOAN_ACCOUNT A
             JOIN F_BALANCE F ON F.ACCOUNT_ID = A.ID --贷款
             JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID  
             WHERE F.ACCT_TYPE=4  and f.YEAR_PDT > 0 AND F.DATE_ID = ? ) B ON FF.CST_NO = B.CST_NO AND B.DATE_ID = FF.DATE_ID AND B.ORG_ID = FF.ORG_ID
             JOIN D_DATE DA ON DA.ID=FF.DATE_ID
             WHERE FF.ACCT_TYPE IN ('1','8') 
             GROUP BY FF.DATE_ID, B.SALE_CODE,DA.BEG_YEAR_DAYS
            """
            sql7="""
            UPDATE REPORT_MANAGER_LOAN  SET DSGGYE=?,DGGGYE=?,DSGGRJ=?,DGGGRJ=?,FLAG=1 WHERE DATE_ID=? AND SALE_CODE=?
            ----UPDATE REPORT_MANAGER_LOAN_TEMP_DUTY SET DSGGYE=?,DGGGYE=? WHERE DATE_ID=? AND SALE_CODE=?
            """
            db.cursor.execute(sql6,int(stardate))
            row6=db.cursor.fetchall()
            resultrow6=[]
            for i in row6:
                t=list(i[0:])
                resultrow6.append(t)
            #print resultrow6
            db.cursor.executemany(sql7,resultrow6)

            db.conn.commit()
            print stardate,"完成",datetime.now()- oneday
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
        man_loan(stardate,etldate)
        print stardate,"完成",datetime.now()-d1
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
