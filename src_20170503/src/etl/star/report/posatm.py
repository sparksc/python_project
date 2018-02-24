# -*- coding:utf-8 -*-
import os,sys
import DB2  
import csv
import multiprocessing
import os, time, random  
import etl.base.util as util
from decimal import *
from etl.base.conf import Config
from datetime import datetime,timedelta
from multiprocessing import Process,Queue,Pool
     
condecimal = getcontext()
"""
客户经理posatm
"""
def man_posatm(stardate,etldate):
    try:
        oneday=datetime.now()
        db = util.DBConnect()
        while stardate<=etldate:
            yearmonth=str(stardate)[0:6]
            print yearmonth
            """FARM_SERV_HIGH_NUM ---高服务点"""
            sql="""
            MERGE INTO REPORT_MANAGER_OTHER A
            USING (SELECT POS_MON_DATE,POS_ORG_NO,POS_MANAGER_NO,SUM(HIGH_POS_NUM) TOTAL_NUM
            FROM ((SELECT MON_DATE POS_MON_DATE,ORG_NO POS_ORG_NO,MANAGER_NO POS_MANAGER_NO, COUNT(1) HIGH_POS_NUM
            FROM (SELECT DISTINCT B.MON_DATE,F.ORG_NO,F.MANAGER_NO,F.MERCHANT_NO,F.POS_NO,NVL(B.MON_TRAN_NUM,0) MON_TRAN_NUM
            FROM (SELECT C.ORG_NO,C.MANAGER_NO,A.MERCHANT_NO,A.POS_NO,CASE WHEN A.END_DATE IS NULL THEN 20991231 ELSE A.END_DATE END POS_END_DATE
            FROM D_POS A ----客户经理名下的所有POS编号
            LEFT JOIN CUST_HOOK C ON C.CUST_NO=A.MERCHANT_NO AND  C.CUST_IN_NO=A.POS_NO
            WHERE  C.TYP='POS'  AND C.SUB_TYP='助农'  AND C.STATUS IN ('待审批','已审批','预提交审批','正常','录入已审批'))F
            LEFT JOIN (SELECT  ORG_NO,MANAGER_NO,MERCHANT_NO,POS_NO,LEFT(DATE_ID,6) MON_DATE,SUM(TRAN_NUM) MON_TRAN_NUM,COUNT(1) TRAN_DAYS   ----一个月中客户经理名下一个POS交易次数达到要求的(每一条记录代表每一个月独一无二POS产生的笔数)
            FROM F_POS_TRAN_NUM  WHERE LEFT(DATE_ID,6)= ? GROUP BY ORG_NO,MANAGER_NO,MERCHANT_NO,POS_NO,LEFT(DATE_ID,6) )B ---!!!!要加POS台数要求
            ON F.MERCHANT_NO=B.MERCHANT_NO AND F.POS_NO=B.POS_NO AND F.MANAGER_NO=B.MANAGER_NO
            WHERE ? <=POS_END_DATE     )P      ---这是?是参数
            WHERE  P.MON_TRAN_NUM>=60   ----这里的MON_DATE参数要改成变量
            GROUP BY P.MON_DATE,P.ORG_NO,P.MANAGER_NO)
            UNION ALL
            (SELECT F.MON_DATE ATM_MON_DATE,F.ORG_NO ATM_ORG_NO,F.MANAGER_NO ATM_MANAGER_NO,COUNT(1) HIGH_ATM_NUM -----每月客户经理名下的台数
            FROM (SELECT DISTINCT   MON_DATE,ATM_NO,C.ORG_NO,C.MANAGER_NO,NVL(MON_TRAN_NUM,0) MON_TRAN_NUM--找到对应的客户经理(这是客户经理名下每一台独一无二ATM一个月中交易的次数)
            FROM ( SELECT DISTINCT MON_ID MON_DATE,A.ATM_NO,MON_TRAN_NUM,CASE WHEN A.END_DATE IS NULL THEN 20991231 ELSE END_DATE END END_DATE
             FROM D_ATM A    ---找到对应的机器号
             LEFT JOIN (SELECT LEFT(D_ATM_DATE_ID,6) MON_ID,D_ATM_ID,SUM(D_ATM_TRAN_NUM) MON_TRAN_NUM FROM 
             F_ATM_TRAN_NUM WHERE LEFT(D_ATM_DATE_ID,6)=?
             GROUP BY LEFT(D_ATM_DATE_ID,6),D_ATM_ID  ) MON_ATM_TRAN_NUM---一个月中客户经理下这个机器交易次数达到要求的
             ON A.ID=MON_ATM_TRAN_NUM.D_ATM_ID ) MON_ATM
             LEFT JOIN CUST_HOOK C ON MON_ATM.ATM_NO=C.CUST_IN_NO WHERE  C.TYP='机具' AND C.SUB_TYP='助农终端'  
             AND  C.STATUS IN ('待审批','已审批','预提交审批','正常','录入已审批') AND ? <MON_ATM.END_DATE     ) F       ----?是参数
             WHERE F.MON_TRAN_NUM>=60  GROUP BY F.MON_DATE,F.ORG_NO,F.MANAGER_NO))A
             GROUP BY POS_MON_DATE,POS_ORG_NO,POS_MANAGER_NO)PP
             ON(LEFT(A.DATE_ID,6)=PP.POS_MON_DATE AND A.ORG_CODE=PP.POS_ORG_NO AND A.SALE_CODE=PP.POS_MANAGER_NO)
             WHEN MATCHED THEN UPDATE SET A.FARM_SERV_HIGH_NUM=PP.TOTAL_NUM,FLAG=1
            """
            """低服务活点率 """
            sql1="""
            MERGE INTO REPORT_MANAGER_OTHER A   USING (SELECT  POS_MON_DATE,POS_ORG_NO,POS_MANAGER_NO,SUM(HIGH_POS_NUM) TOTAL_NUM
            FROM ((SELECT %s  POS_MON_DATE,ORG_NO POS_ORG_NO,MANAGER_NO POS_MANAGER_NO, COUNT(1) HIGH_POS_NUM
            FROM (SELECT DISTINCT B.MON_DATE,F.ORG_NO,F.MANAGER_NO,F.MERCHANT_NO,F.POS_NO,NVL(B.MON_TRAN_NUM,0) MON_TRAN_NUM
            FROM (SELECT C.ORG_NO,C.MANAGER_NO,A.MERCHANT_NO,A.POS_NO,CASE WHEN A.END_DATE IS NULL THEN 20991231 ELSE A.END_DATE END POS_END_DATE
            FROM D_POS A ----客户经理名下的所有POS编号
            LEFT JOIN CUST_HOOK C ON C.CUST_NO=A.MERCHANT_NO AND  C.CUST_IN_NO=A.POS_NO
            WHERE  C.TYP='POS'  AND C.SUB_TYP='助农'  AND C.STATUS IN ('待审批','已审批','预提交审批','正常','录入已审批') )F
            LEFT JOIN 
            (SELECT  ORG_NO,MANAGER_NO,MERCHANT_NO,POS_NO,LEFT(DATE_ID,6) MON_DATE,SUM(TRAN_NUM)  MON_TRAN_NUM,COUNT(1) TRAN_DAYS   ----一个月中客户经理名下一个POS交易次数达到要求的(每一条记录代表每一个月独一无二POS产生的笔数)
            FROM F_POS_TRAN_NUM  WHERE LEFT(DATE_ID,6)= %s GROUP BY ORG_NO,MANAGER_NO,MERCHANT_NO,POS_NO,LEFT(DATE_ID,6)  )B    ---!!!!要加POS台数要求
            ON F.MERCHANT_NO=B.MERCHANT_NO AND F.POS_NO=B.POS_NO AND F.MANAGER_NO=B.MANAGER_NO
            WHERE %s <=POS_END_DATE    )P       ---这是s是参数
            WHERE  P.MON_TRAN_NUM<60   ----这里的MON_DATE参数要改成变量注意是
            GROUP BY P.MON_DATE,P.ORG_NO,P.MANAGER_NO)
            UNION ALL
            ( SELECT %s ATM_MON_DATE,F.ORG_NO ATM_ORG_NO,F.MANAGER_NO ATM_MANAGER_NO,COUNT(1) HIGH_ATM_NUM -----每月客户经理名下的台数
            FROM (SELECT DISTINCT   MON_DATE,ATM_NO,C.ORG_NO,C.MANAGER_NO,NVL(MON_TRAN_NUM,0) MON_TRAN_NUM--找到对应的客户经理(这是客户经理名下每一台独一无二ATM一个月中交易的次数)
            FROM( SELECT DISTINCT MON_ID MON_DATE,A.ATM_NO,MON_TRAN_NUM,CASE WHEN A.END_DATE IS NULL THEN 20991231 ELSE END_DATE END END_DATE
             FROM D_ATM A    ---找到对应的机器号
             LEFT JOIN (SELECT LEFT(D_ATM_DATE_ID,6) MON_ID,D_ATM_ID,SUM(D_ATM_TRAN_NUM) MON_TRAN_NUM FROM 
             F_ATM_TRAN_NUM WHERE LEFT(D_ATM_DATE_ID,6)= %s 
             GROUP BY LEFT(D_ATM_DATE_ID,6),D_ATM_ID  ) MON_ATM_TRAN_NUM---一个月中客户经理下这个机器交易次数达到要求的
             ON A.ID=MON_ATM_TRAN_NUM.D_ATM_ID ) MON_ATM
             LEFT JOIN CUST_HOOK C
             ON MON_ATM.ATM_NO=C.CUST_IN_NO WHERE  C.TYP='机具' AND C.SUB_TYP='助农终端' AND C.STATUS IN ('待审批','已审批','预提交审批','正常','录入已审批') AND %s<MON_ATM.END_DATE) F
             WHERE F.MON_TRAN_NUM<60   GROUP BY F.MON_DATE,F.ORG_NO,F.MANAGER_NO))A
             GROUP BY POS_MON_DATE,POS_ORG_NO,POS_MANAGER_NO)PP
             ON LEFT(A.DATE_ID,6)=PP.POS_MON_DATE AND A.ORG_CODE=PP.POS_ORG_NO AND A.SALE_CODE=PP.POS_MANAGER_NO
             WHEN MATCHED THEN UPDATE SET A.FARM_SERVICE_LOW_NUM=PP.TOTAL_NUM,FLAG=1
            """%(yearmonth,yearmonth,stardate,yearmonth,yearmonth,stardate)
            db.cursor.execute(sql,(yearmonth),(stardate),(yearmonth),(stardate))
            db.cursor.execute(sql1)
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
        print stardate,etldate
        man_posatm(stardate,etldate)
        print "posatm",stardate,etldate,"完成",datetime.now()-d1
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
