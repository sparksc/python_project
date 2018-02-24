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
import org_dep as orgdep
from etl.base.logger import info
     
condecimal = getcontext()
"""
客户经理存款指标报表
"""
def sum_last(db, etldate):
    dsql = " delete from  F_BALNCE_LY "
    db.cursor.execute(dsql)
    dsql = " delete from  F_BALNCE_LM "
    db.cursor.execute(dsql)
    db.conn.commit()

    sql = """
    insert into F_BALNCE_LM
        select  f.account_id,f.year_pdt
        from  F_BALANCE f
        inner join d_date d on d.L_MONTHEND_ID = f.date_id
    WHERE
        d.id = ?
        and f.year_pdt !=0
        and f.ACCT_TYPE in ('1','8')
    """
    #如果是1月份，上月末数据不用插入
    if int(str(etldate)[4:6]) != 1 :
        db.cursor.execute(sql, etldate)
    db.conn.commit()

    #理财上年末
    sql = """
        insert into F_BALNCE_LY
        select  
            distinct f11.account_id,f11.year_pdt
        FROM F_BALANCE f11
        JOIN D_ACCOUNT DA11 ON F11.ACCOUNT_ID = DA11.ID 
        JOIN ACCOUNT_HOOK AH11 ON DA11.ACCOUNT_NO = AH11.ACCOUNT_NO
        Inner join d_date d on d.L_YEAREND_ID = f11.date_id
        WHERE d.id = ?
            and F11.year_pdt !=0
           and F11.ACCT_TYPE in ('8')
            AND AH11.START_DATE <= d.L_YEAREND_ID
    """                 
    db.cursor.execute(sql, etldate)
    db.conn.commit()
    print "finish sum_last"

def man_dep(startdate,etldate):
    info("start dep.man_dep %s-%s"%(str(startdate),str(etldate)))

    if int(str(startdate)[0:6]) != int(str(etldate)[0:6]):
        raise Exception("不能跨月执行")

    try:
        oneday=datetime.now()
        db = util.DBConnect()
        sum_last(db, etldate)
        sql0="""
            UPDATE 
                YDW.REPORT_MANAGER_DEP_MONTH
            SET  PRI_LAST_AVG=0, PUB_LAST_AVG=0, LAST_AVG=0, PRI_THIS_AVG=0, 
                PUB_THIS_AVG=0, THIS_AVG=0, FIN_LAST_AVG=0, FIN_THIS_AVG=0, 
                PRI_BAL=0, PUB_BAL=0, FIN_BAL=0, BAL=0, LAST_AVG_SAL=0, 
                ADD_AVG_SAL=0, PRI_MONTH_AVG=0, PUB_MONTH_AVG=0, MONTH_AVG=0, 
                PRI_PDT=0, PUB_PDT=0, LICAI_PDT=0, DEP_SCORE=0, 
                TRY_LAST_AVG_SAL=0, TRY_ADD_AVG_SAL=0
            WHERE 
                DATE_ID >=? and DATE_ID <= ?
        """
        db.cursor.execute(sql0,int(startdate),int(startdate))
        db.conn.commit()

        sql="""
            SELECT 
                0  AS DSCL,
                0 AS DGCL,
                0 AS  CL,
                BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' THEN ( CASE WHEN SUBSTR(F.DATE_ID,5,2)!='01'THEN (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0))*M.PERCENT/ 100 ELSE NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 END ) ELSE 0 END)/ D.BEG_MONTH_DAYS) AS DSYLJ,--对私月日均
                BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' THEN ( CASE WHEN SUBSTR(F.DATE_ID,5,2)!='01'THEN (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0))*M.PERCENT/ 100 ELSE NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 END ) ELSE 0 END)/ D.BEG_MONTH_DAYS) AS DGYLJ,--对公月日均
                BIGINT(SUM(CASE WHEN SUBSTR(F.DATE_ID,5,2)!='01' THEN (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0))*M.PERCENT/ 100 ELSE NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 END )/ D.BEG_MONTH_DAYS) AS YLJ,--月日均
                BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' AND F.ACCT_TYPE=1 THEN NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)/ D.BEG_YEAR_DAYS) AS DSXL,--对私现量
                BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' AND F.ACCT_TYPE=1 THEN NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)/ D.BEG_YEAR_DAYS) AS DGXL,--对公现量
                BIGINT(SUM(NVL(F.YEAR_PDT,0) *M.PERCENT/ 100)/ D.BEG_YEAR_DAYS) AS XL,--现量
                BIGINT(SUM(CASE WHEN F.ACCT_TYPE=8 THEN NVL(F1.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)/ DD.YEAR_DAYS) AS LCCL,--理财存量日均
                BIGINT(SUM(CASE WHEN F.ACCT_TYPE=8 THEN NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)/ D.BEG_YEAR_DAYS) AS LCXL,--理财现量
                BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' AND F.ACCT_TYPE=1 THEN NVL(F.BALANCE,0)*M.PERCENT/ 100 ELSE 0 END)), --对私余额
                BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' AND F.ACCT_TYPE=1 THEN NVL(F.BALANCE,0)*M.PERCENT/ 100 ELSE 0 END)), --对公余额
                BIGINT(SUM(CASE WHEN F.ACCT_TYPE=8 AND A.CLOSE_DATE_ID>F.DATE_ID THEN NVL(F.BALANCE,0)*M.PERCENT/ 100 ELSE 0 END)), --理财余额 
                BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' AND F.ACCT_TYPE=1 THEN NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)), --对私积数
                BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' AND F.ACCT_TYPE=1 THEN NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)), --对公积数
                BIGINT(SUM(CASE WHEN F.ACCT_TYPE=8 AND A.CLOSE_DATE_ID>F.DATE_ID THEN NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 ELSE 0 END)), --理财积数 
                BIGINT(SUM(CASE WHEN A.CLOSE_DATE_ID>F.DATE_ID THEN  NVL(F.BALANCE,0)*M.PERCENT/ 100 ELSE 0 END)),  --余额合计
                NVL(M.THIRD_BRANCH_NAME,'无'),NVL(M.SALE_NAME,'无'),
                F.DATE_ID,M.SALE_CODE,M.THIRD_BRANCH_CODE
            FROM F_BALANCE F
            JOIN D_ACCOUNT A ON F.ACCOUNT_ID=A.ID 
            JOIN D_ACCOUNT_TYPE T ON F.ACCOUNT_TYPE_ID=T.ID 
                AND ( 
                    F.ACCT_TYPE=8 
                    OR LEFT(T.SUBJECT_CODE,4) IN ('2001','2003','2005','2006','2011','2014','2002','2004','2012','2013') 
                    OR LEFT(T.SUBJECT_CODE,6) IN ('231401','231409','231421','231499','231403','231402','231422','201712','201713','201714','201702','201703','201704') 
                    OR T.SUBJECT_CODE IN ('20070101','20070201','20070301','20170198','20171198')
                )
            JOIN D_DATE D ON F.DATE_ID=D.ID  
            JOIN D_DATE DD ON D.L_YEAREND_ID=DD.ID
            JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID  
            --上月末积数
            LEFT JOIN F_BALNCE_LM F2 on F2.ACCOUNT_ID = F.ACCOUNT_ID 
            ---上年理财
            LEFT JOIN F_BALNCE_LY F1 on F1.ACCOUNT_ID = F.ACCOUNT_ID 
            WHERE 
                F.ACCT_TYPE IN (1,8) 
                AND F.DATE_ID >= ? and f.DATE_ID <= ?
                and m.sale_code='9660896'
            GROUP BY F.DATE_ID,M.THIRD_BRANCH_CODE,M.THIRD_BRANCH_NAME,M.SALE_CODE,M.SALE_NAME,D.BEG_YEAR_DAYS,DD.YEAR_DAYS,D.BEG_MONTH_DAYS
        """
        sql1 = """
            UPDATE YDW.REPORT_MANAGER_DEP_MONTH SET  PRI_LAST_AVG=?, PUB_LAST_AVG=?, LAST_AVG=?, PRI_MONTH_AVG=?, PUB_MONTH_AVG=?, MONTH_AVG=?, PRI_THIS_AVG=?, PUB_THIS_AVG=?, THIS_AVG=?, FIN_LAST_AVG=?, FIN_THIS_AVG=?, PRI_BAL=?, PUB_BAL=?, FIN_BAL=?,PRI_PDT=?,PUB_PDT=?,LICAI_PDT=?, BAL=?,ORG_NAME=?,SALE_NAME=? WHERE  DATE_ID=?  AND  SALE_CODE=? AND ORG_CODE=?
       """
        print "execute sum_sql",sql,startdate,etldate
        db.cursor.execute(sql, int(startdate), int(etldate))
        row=db.cursor.fetchone()
        resultrow=[]
        while row:
            resultrow.append( list(row) )
            row = db.cursor.fetchone()
            info("dep.man_dep,sql_update : \n  %s"%(sql1))
        db.cursor.executemany(sql1,resultrow)

        sql2="""
            MERGE INTO REPORT_MANAGER_DEP_MONTH R 
            USING V_STAFF_INFO V  ON V.USER_NAME=R.SALE_CODE AND R.DATE_ID >=?  and r.DATE_ID<= ?
            WHEN MATCHED THEN UPDATE SET R.SALE_NAME=V.NAME
        """
        db.cursor.execute(sql2, int(startdate), int(etldate))

        sql3="""
            MERGE INTO REPORT_MANAGER_DEP_MONTH R 
            USING D_ORG V  ON V.ORG0_CODE=R.ORG_CODE AND R.DATE_ID >=?  and r.DATE_ID<= ?
            WHEN MATCHED THEN UPDATE SET R.ORG_NAME=V.ORG0_NAME
        """
        db.cursor.execute(sql3, int(startdate), int(etldate))
        db.conn.commit()

 
        print startdate,"完成",datetime.now()- oneday
        info("dep.man_dep 完成")

        #更新上年数
        clsql = """
                SELECT 
                     sum(CASE WHEN LEFT(Ff.CST_NO,2)='81' then   ff.year_pdt*ay.percentage /100/d2.year_days else 0 end)  DSCL
                    ,sum(CASE WHEN LEFT(Ff.CST_NO,2)='82' then   ff.year_pdt*ay.percentage /100/d2.year_days else 0 end)  DGCL
                    ,sum(ff.year_pdt/d2.year_days) CL
                    , ay.manager_no
                    , ay.org_no
                FROM f_balance ff
                INNER JOIN D_ORG o ON O.ID = FF.ORG_ID
                inner join d_account a on a.id= ff.account_id
                INNER JOIN ACCOUNT_HOOK ay on ay.account_no  = a.account_no  and ay.org_no = o.org0_code
                INNER JOIN D_DATE D2  ON ff.date_id = D2.ID
                where ff.date_id = ?
                    and ay.start_date<=?
                    and ay.manager_no = '9660896'
                group by  ay.org_no,ay.manager_no
        """
        year = int(str(startdate)[0:4])
        last_year = (year-1)*10000 +1231
        db.cursor.execute(clsql, last_year, last_year)
        row=db.cursor.fetchone()
        lastdata = []
        while row:
            bdate = int(startdate)
            while bdate <= int(etldate):    
                data = list(row)
                data.append( bdate )
                lastdata.append( data )
                bdate = int(util.daycalc(bdate,1))
            row = db.cursor.fetchone()
        sqllast = """
            UPDATE YDW.REPORT_MANAGER_DEP_MONTH SET  PRI_LAST_AVG=?, PUB_LAST_AVG=?, LAST_AVG=?
            WHERE  SALE_CODE=? AND ORG_CODE=? and date_id = ?
        """
        info("dep.man_dep,sql : \n  %s"%(sqllast))
        db.cursor.executemany(sqllast, lastdata)
        db.conn.commit()

        """刷客户经理的佣金报表"""
        """
        month_end_sql="select month_end from D_DATE where ID=? "
        db.cursor.execute(month_end_sql, etldate)
        is_month_end=db.cursor.fetchall()
        if is_month_end[0][0] == 'Y': 
            info("dep.man_dep,depsal.man_dep_sal")
            depsal.man_dep_sal(etldate)
        """
    finally :
        db.closeDB()

def sum_dep_report(etldate):
    day = int(str(etldate)[6:8])
    if day <= 8:
        startdate = int(str(etldate)[0:6]+"01")
        lmend = int(util.daycalc(startdate,-1))
        lmstart = int(str(lmend)[0:6]+"01")
        msg = "dep.sum_dep_report,计算上个月报表:%d-%d"%(lmstart, lmend)
        info( msg )
        man_dep(lmstart, lmend)
        msg = msg + "调用结束"
        info( msg )

    startdate = int(str(etldate)[0:6]+"01")
    enddate = etldate
    msg = "dep.sum_dep_report,计算本月报表:%d-%d"%(startdate, etldate)
    info( msg )
    man_dep(startdate,etldate)
    msg = msg + "调用结束"
    info( msg )

if __name__=='__main__':
    arglen=len(sys.argv)
    print sys.argv 
    d1=datetime.now()
    if arglen == 2:
        etldate=int(sys.argv[1])
        sum_dep_report(etldate)
    else:
        print "please input python %s yyyyMMdd "%sys.argv[0]
