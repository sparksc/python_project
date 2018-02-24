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
客户经理信用卡指标报表
"""
def man_creditcard(stardate,etldate):
    try:
        oneday=datetime.now()
        db = util.DBConnect()
        while stardate<=etldate:
            sql0 = """
            UPDATE YDW.REPORT_MANAGER_CREDITCARD 
                SET  LAST_NUM=0, THIS_NUM=0, BAD_BAL=0, ALL_BAL=0, BAD_ALL=0, SALARY=0, PPL_BAL=0, FLAG=0
                    WHERE DATE_ID=?
            """
            db.cursor.execute(sql0,int(stardate))
            db.conn.commit()
            sql="""
            ------DELETE FROM REPORT_MANAGER_CREDITCARD WHERE DATE_ID = ?
            """
            """
            客户经理发卡量现量 THIS_NUM 
            """
            sql1="""
            SELECT COUNT(*),F.DATE_ID, M.SALE_CODE
            FROM F_CREDIT_CARD_STATUS F
            JOIN D_CREDIT_CARD D ON D.ID = F.CARD_ID 
            JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID
            WHERE F.DATE_ID = ? AND F.STATUS NOT IN('持卡人请求关闭', '呆账核销', '呆账核销清户', '销卡代码', '新卡激活，旧卡失效')  AND F.DUE_DATE >= ?  AND D.OPEN_DATE <= ? 
            GROUP BY F.DATE_ID, M.SALE_CODE
            """
            sql2="""
            UPDATE REPORT_MANAGER_CREDITCARD  SET THIS_NUM=?,FLAG=1 WHERE DATE_ID=?   AND SALE_CODE=?
            """
            #db.cursor.execute(sql,int(stardate))
            yearmonth=str(stardate)[0:6]
            print yearmonth
            db.cursor.execute(sql1,int(stardate),int(yearmonth),int(stardate))
            row2=db.cursor.fetchall()
            #print row2
            resultrows2=[]
            for i in row2:
                t=list(i[0:])
                resultrows2.append(t)
                #print resultrows2 
            db.cursor.executemany(sql2,resultrows2)
            """
            客户经理发卡量存量 LAST_NUM
            """
            sql3="""
            SELECT COUNT(*), M.SALE_CODE
            FROM F_CREDIT_CARD_STATUS F
            JOIN D_CREDIT_CARD D ON D.ID = F.CARD_ID 
            JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID
            WHERE F.DATE_ID = (SELECT L_YEAREND_ID FROM D_DATE  WHERE ID=?) AND F.STATUS NOT IN('持卡人请求关闭', '呆账核销', '呆账核销清户', '销卡代码', '新卡激活，旧卡失效')  AND F.DUE_DATE >= (SELECT LEFT(L_YEAREND_ID,6) FROM D_DATE  WHERE ID=?)  AND D.OPEN_DATE <= (SELECT L_YEAREND_ID FROM D_DATE  WHERE ID=?)
            GROUP BY F.DATE_ID, M.SALE_CODE
            """
            sql4="""
            UPDATE REPORT_MANAGER_CREDITCARD SET LAST_NUM=?,FLAG=1 WHERE  SALE_CODE=? AND DATE_ID=? 
            """
            db.cursor.execute(sql3,int(stardate),int(stardate),int(stardate))
            row3=db.cursor.fetchall()
            #print row3
            resultrow3=[]
            for i in row3:
                t=list(i[0:])
                t.append(int(stardate))
                resultrow3.append(t)
                #print resultrow3
            db.cursor.executemany(sql4,resultrow3)
            
            """
            --构造全量处理不良
            """
            sql5="""
            DELETE FROM CREDIT_BAD_DATE 
            """
            sql6="""
            INSERT INTO YDW.CREDIT_BAD_DATE(DATE_ID, THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME, ACCOUNT_NO, OPEN_DATE, STATUS) 
            SELECT FF.DATE_ID, NVL(M.THIRD_BRANCH_CODE,MM.THIRD_BRANCH_CODE) , NVL(M.THIRD_BRANCH_NAME, MM.THIRD_BRANCH_NAME), NVL(M.SALE_CODE, MM.SALE_CODE), NVL(M.SALE_NAME, MM.SALE_NAME), B.ACCOUNT_NO, NVL(B.OPEN_DATE, BB.OPEN_DATE), FF.STATUS FROM D_CREDIT_CARD B
            JOIN D_CREDIT_CARD BB ON B.ACCOUNT_NO = BB.ACCOUNT_NO
            JOIN (SELECT ACCOUNT_NO, MIN(OPEN_DATE) AS MIN_OPEN_DATE, MIN(OPEN_DATE || ISS_SERIAL) AS ISS FROM D_CREDIT_CARD GROUP BY ACCOUNT_NO) A ON A.ACCOUNT_NO = B.ACCOUNT_NO AND B.OPEN_DATE || B.ISS_SERIAL = A.ISS   --
            JOIN (SELECT ACCOUNT_NO, MAX(OPEN_DATE || ISS_SERIAL) AS ISS FROM D_CREDIT_CARD GROUP BY ACCOUNT_NO) AA ON AA.ACCOUNT_NO = BB.ACCOUNT_NO AND BB.OPEN_DATE || BB.ISS_SERIAL = AA.ISS
            JOIN F_CREDIT_CARD_STATUS FF ON BB.ID = FF.CARD_ID AND FF.DATE_ID = ?  --最后卡的状态
            JOIN D_SALE_MANAGE_RELA MM ON FF.MANAGE_ID=MM.MANAGE_ID
            LEFT JOIN F_CREDIT_CARD_STATUS F ON B.ID = F.CARD_ID AND F.DATE_ID = A.MIN_OPEN_DATE  --最早发卡人
            LEFT JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID   --默认
            """
            db.cursor.execute(sql5)
            db.cursor.execute(sql6,int(stardate))
            """不良 BAD_BAL"""
            sql7="""
            SELECT    SUM(CASE WHEN F.MTHS_ODUE > 300 THEN F.STM_BALFRE+F.STM_BALINT+F.STM_BALMP+F.BAL_FREE +F.BAL_INT+F.BAL_MP ELSE 0 END) BAD_BAL,--不良透支金额
            SUM(F.STM_BALFRE+F.STM_BALINT+F.STM_BALMP+F.BAL_FREE +F.BAL_INT+F.BAL_MP) ALL_BAL,  --总额(少分期)
            F.DATE_ID , A.SALE_CODE
            FROM F_CREDIT_BAD_20161031 F
            JOIN CREDIT_BAD_DATE A ON F.ACCOUNT_NO = A.ACCOUNT_NO AND A.STATUS NOT IN ('持卡人请求关闭','呆账核销','呆账核销清户') 
            WHERE F.DATE_ID = ? AND ( -F.BAL_FREE + (CASE WHEN F.BAL_INT_FLAG='-' THEN F.BAL_INT ELSE -F.BAL_INT END) -F.STM_BALFRE  + (CASE WHEN F.STMBALINT_FLAG='-' THEN F.STM_BALINT ELSE -F.STM_BALINT END) -F.BAL_MP - F.STM_BALMP ) < 0
            GROUP BY F.DATE_ID,A.SALE_CODE
            """
            db.cursor.execute(sql7,int(stardate))
            row7=db.cursor.fetchall()
            #print row7
            resultrow7=[]
            for i in row7:
                t=list(i[0:])
                resultrow7.append(t)
            sql8="""
            UPDATE REPORT_MANAGER_CREDITCARD SET BAD_BAL=? , ALL_BAL=?,FLAG=1 WHERE DATE_ID=?  AND SALE_CODE=?
            """
            db.cursor.executemany(sql8,resultrow7)
            """
            --新增不良  BAD_ALL
            """
            sql9="""
            SELECT SUM(F.BAL_FREE - (CASE WHEN F.BAL_INT_FLAG='-' THEN F.BAL_INT ELSE -F.BAL_INT END) + F.STM_BALFRE  - (CASE WHEN F.STMBALINT_FLAG='-' THEN F.STM_BALINT ELSE -F.STM_BALINT END) + F.BAL_MP + F.STM_BALMP),
            F.DATE_ID ,A.SALE_CODE
            FROM F_CREDIT_BAD_20161031 F 
            JOIN CREDIT_BAD_DATE A ON F.ACCOUNT_NO = A.ACCOUNT_NO AND A.STATUS NOT IN ('持卡人请求关闭','呆账核销','呆账核销清户')
            WHERE F.DATE_ID = ? 
            AND A.OPEN_DATE>= (select YEARBEG_ID from D_DATE where id = ?) AND F.MTHS_ODUE>=100  --大于年初 
            GROUP BY F.DATE_ID, A.SALE_CODE
            """
            db.cursor.execute(sql9,int(stardate),int(stardate))
            row9=db.cursor.fetchall()
            #print row9
            resultrow9=[]
            for i in row9:
                t=list(i[0:])
                resultrow9.append(t)
            sql10="""
            UPDATE REPORT_MANAGER_CREDITCARD SET BAD_ALL=?,FLAG=1  WHERE DATE_ID=? AND SALE_CODE=?
            """
            db.cursor.executemany(sql10,resultrow9)
            """
            --分期 PPL_BAL
            """
            sql11="""
            SELECT SUM(REM_PPL),F.DATE_ID, A.SALE_CODE  FROM F_CREDIT_MPUR_20161031 F
            LEFT JOIN CREDIT_BAD_DATE A ON F.ACCOUNT_NO = A.ACCOUNT_NO
            WHERE F.DATE_ID = ? 
            GROUP BY F.DATE_ID, A.SALE_CODE
            """
            db.cursor.execute(sql11,int(stardate))
            row11=db.cursor.fetchall()
            #print row11
            resultrow11=[]
            for i in row11:
                t=list(i[0:])
                resultrow11.append(t)
            sql12="""
            UPDATE REPORT_MANAGER_CREDITCARD SET PPL_BAL=?,FLAG=1  WHERE DATE_ID=?  AND SALE_CODE=?
            """
            db.cursor.executemany(sql12,resultrow11)
            db.conn.commit()

            sql13="""
            DELETE FROM REPORT_MANAGER_CREDITCARD WHERE DATE_ID=? AND FLAG=0
            """
            db.cursor.execute(sql13,int(stardate))
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
        man_creditcard(stardate,etldate)
        print stardate,"完成",datetime.now()-d1
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
