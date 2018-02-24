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
import man_dep_sal as depsal
     
condecimal = getcontext()
"""
客户经理存款指标报表
"""
def man_dep(stardate,etldate):
    try:
        oneday=datetime.now()
        db = util.DBConnect()
        while stardate<=etldate:
            sql="""
            SELECT BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' AND F.ACCT_TYPE=1 THEN NVL(F1.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)/ DD.YEAR_DAYS) AS DSCL,
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' AND F.ACCT_TYPE=1 THEN NVL(F1.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)/ DD.YEAR_DAYS) AS DGCL,
            BIGINT(SUM(NVL(F1.YEAR_PDT,0)*M.PERCENT/ 100)/DD.YEAR_DAYS) AS CL,
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' THEN ( CASE WHEN SUBSTR(DATE_ID,5,2)!='01'THEN (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0))*M.PERCENT/ 100 ELSE NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 END ) ELSE 0 END)/ D.BEG_MONTH_DAYS) AS DSYLJ,--对私月日均
            ----BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81'   THEN (CASE WHEN F.ACCT_TYPE ='8'  THEN (CASE WHEN A.CLOSE_DATE_ID>F.DATE_ID THEN  (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0)+NVL(F2.BALANCE,0))*M.PERCENT/ 100 ELSE 0 END) ELSE (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0)+NVL(F2.BALANCE,0))*M.PERCENT/ 100 END ) ELSE 0 END)/ D.BEG_MONTH_DAYS) AS DSYLJ,--对私月日均
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' THEN ( CASE WHEN SUBSTR(DATE_ID,5,2)!='01'THEN (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0)+NVL(F2.BALANCE,0))*M.PERCENT/ 100 ELSE NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 END ) ELSE 0 END)/ D.BEG_MONTH_DAYS) AS DGYLJ,--对公月日均
            BIGINT(SUM(CASE WHEN SUBSTR(DATE_ID,5,2)!='01' THEN (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0))*M.PERCENT/ 100 ELSE NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 END )/ D.BEG_MONTH_DAYS) AS YLJ,--月日均
            ---- BIGINT(SUM(CASE WHEN F.ACCT_TYPE ='8'  THEN (CASE WHEN A.CLOSE_DATE_ID>F.DATE_ID THEN  (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0)+NVL(F2.BALANCE,0))*M.PERCENT/ 100 ELSE 0 END) ELSE (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0)+NVL(F2.BALANCE,0))*M.PERCENT/ 100 END )/ D.BEG_MONTH_DAYS) AS YLJ,--月日均       
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' AND F.ACCT_TYPE=1 THEN NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)/ D.BEG_YEAR_DAYS) AS DSXL,
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' AND F.ACCT_TYPE=1 THEN NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)/ D.BEG_YEAR_DAYS) AS DGXL,
            BIGINT(SUM(NVL(F.YEAR_PDT,0) *M.PERCENT/ 100)/ D.BEG_YEAR_DAYS) AS XL,
            BIGINT(SUM(CASE WHEN F.ACCT_TYPE=8 THEN NVL(F1.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)/ DD.YEAR_DAYS) AS LCCL,
            BIGINT(SUM(CASE WHEN F.ACCT_TYPE=8 THEN NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)/ D.BEG_YEAR_DAYS) AS LCXL,
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' AND F.ACCT_TYPE=1 THEN NVL(F.BALANCE,0)*M.PERCENT/ 100 ELSE 0 END)), --对私余额
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' AND F.ACCT_TYPE=1 THEN NVL(F.BALANCE,0)*M.PERCENT/ 100 ELSE 0 END)), --对公余额
            BIGINT(SUM(CASE WHEN F.ACCT_TYPE=8 AND A.CLOSE_DATE_ID>F.DATE_ID THEN NVL(F.BALANCE,0)*M.PERCENT/ 100 ELSE 0 END)), --理财余额 
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' AND F.ACCT_TYPE=1 THEN NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)), --对私积数
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' AND F.ACCT_TYPE=1 THEN NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)), --对公积数
            BIGINT(SUM(CASE WHEN F.ACCT_TYPE=8 AND A.CLOSE_DATE_ID>F.DATE_ID THEN NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)), --理财积数 
            BIGINT(SUM(CASE WHEN A.CLOSE_DATE_ID>F.DATE_ID THEN  NVL(F.BALANCE,0)*M.PERCENT/ 100 ELSE 0 END)),  --余额合计
            NVL(M.THIRD_BRANCH_NAME,'无'),NVL(M.SALE_NAME,'无'),F.DATE_ID,M.SALE_CODE,M.THIRD_BRANCH_CODE
            FROM F_BALANCE F
            LEFT JOIN(SELECT DISTINCT ACCOUNT_ID,YEAR_PDT FROM F_BALANCE F  JOIN D_ACCOUNT D ON F.ACCOUNT_ID = D.ID JOIN ACCOUNT_HOOK AH ON D.ACCOUNT_NO = AH.ACCOUNT_NO
            WHERE DATE_ID=(SELECT L_YEAREND_ID FROM D_DATE WHERE ID=?) AND F.ACCT_TYPE IN(1,8) AND AH.START_DATE <=(SELECT L_YEAREND_ID FROM D_DATE WHERE ID=?) ) F1 ON F1.ACCOUNT_ID=F.ACCOUNT_ID
            LEFT JOIN(SELECT ACCOUNT_ID,YEAR_PDT,BALANCE FROM F_BALANCE F WHERE DATE_ID=(SELECT L_MONTHEND_ID FROM D_DATE WHERE ID=?) AND ACCT_TYPE IN(1,8)) F2 ON F2.ACCOUNT_ID=F.ACCOUNT_ID
            -----LEFT JOIN (SELECT ACCOUNT_ID,YEAR_PDT,BALANCE FROM F_BALANCE F WHERE DATE_ID=20161201 AND ACCT_TYPE IN(1,8)) F2 ON F2.ACCOUNT_ID=F.ACCOUNT_ID
            JOIN D_ACCOUNT A ON F.ACCOUNT_ID=A.ID 
            JOIN D_ACCOUNT_TYPE T ON F.ACCOUNT_TYPE_ID=T.ID AND ( F.ACCT_TYPE=8 
            OR LEFT(T.SUBJECT_CODE,4) IN ('2001','2003','2005','2006','2011','2014','2002','2004','2012','2013') 
            OR LEFT(T.SUBJECT_CODE,6) IN ('231401','231409','231421','231499','231403','231402','231422','201712','201713','201714','201702','201703','201704') 
            OR T.SUBJECT_CODE IN ('20070101','20070201','20070301','20170198','20171198'))
            JOIN D_DATE D ON F.DATE_ID=D.ID  
            JOIN D_DATE DD ON D.L_YEAREND_ID=DD.ID
            JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID  
            WHERE F.ACCT_TYPE IN (1,8) AND F.DATE_ID = ?   AND(M.SALE_CODE, M.THIRD_BRANCH_CODE) IN ( select distinct m.SALE_CODE,m.THIRD_BRANCH_CODE from F_BALANCE f join D_ACCOUNT d on d.ID=f.ACCOUNT_ID
            join D_SALE_MANAGE_RELA m on m.MANAGE_ID=f.MANAGE_ID
            where f.DATE_ID=20170131 and d.ID in (select * from tmp_funds_account))---- AND M.SALE_CODE IN ('9660160','X9660160')
            GROUP BY F.DATE_ID,M.THIRD_BRANCH_CODE,M.THIRD_BRANCH_NAME,M.SALE_CODE,M.SALE_NAME,D.BEG_YEAR_DAYS,DD.YEAR_DAYS,D.BEG_MONTH_DAYS
            """
            sql1="""
            UPDATE YDW.REPORT_MANAGER_DEP_TEMP SET  PRI_LAST_AVG=?, PUB_LAST_AVG=?, LAST_AVG=?, PRI_MONTH_AVG=?, PUB_MONTH_AVG=?, MONTH_AVG=?, PRI_THIS_AVG=?, PUB_THIS_AVG=?, THIS_AVG=?, FIN_LAST_AVG=?, FIN_THIS_AVG=?, PRI_BAL=?, PUB_BAL=?, FIN_BAL=?,PRI_PDT=?,PUB_PDT=?,LICAI_PDT=?, BAL=?,ORG_NAME=?,SALE_NAME=? WHERE  DATE_ID=?  AND  SALE_CODE=? AND ORG_CODE=?
            """
            db.cursor.execute(sql,int(stardate),int(stardate),int(stardate),int(stardate))
            #db.cursor.execute(sql,int(stardate),int(stardate),int(stardate))
            row = db.cursor.fetchall()
            resultrow=[]
            for i in row:
                t=list(i[0:])
                resultrow.append(t)
            #print resultrow
            db.cursor.executemany(sql1,resultrow)
            db.conn.commit()
            sql2="""
            MERGE INTO REPORT_MANAGER_DEP_TEMP R 
            USING V_STAFF_INFO V  ON V.USER_NAME=R.SALE_CODE AND R.DATE_ID =? AND R.SALE_NAME IS NULL
            WHEN MATCHED THEN UPDATE SET R.SALE_NAME=V.NAME
            """
            #db.cursor.execute(sql2,int(stardate))
            sql3="""
            MERGE INTO REPORT_MANAGER_DEP_TEMP R 
            USING D_ORG V  ON V.ORG0_CODE=R.ORG_CODE AND R.DATE_ID =? AND R.ORG_NAME IS NULL
            WHEN MATCHED THEN UPDATE SET R.ORG_NAME=V.ORG0_NAME
            """
            #db.cursor.execute(sql3,int(stardate))
            db.conn.commit()
            #"""刷客户经理的佣金报表"""
            #month_end_sql="""
            #select month_end from D_DATE where ID=?
            #"""
            #db.cursor.execute(month_end_sql,stardate)
            #is_month_end=db.cursor.fetchall()
            #if is_month_end[0][0]=='Y': 
            #    depsal.man_dep_sal(etldate)
 
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
        print stardate,etldate
        man_dep(stardate,etldate)
        print stardate,etldate,"完成",datetime.now()-d1
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
