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
刷柜员业务量需要的表
"""
def m_teller_tran(stardate,etldate):
    try:
        oneday=datetime.now()
        db = util.DBConnect()
        while int(stardate)<=int(etldate):
            print 'm_teller_tran,"柜员业务量折算率"',stardate
            sql0="""
            DELETE FROM M_TELLER_TRAN WHERE DATE_ID=?
            """
            db.cursor.execute(sql0,int(stardate))
            sql1="""
            DELETE FROM M_CASH_TRAN_AMOUNT WHERE DATE_ID=?
            """
            db.cursor.execute(sql1,int(stardate))
            sql2="""
            DELETE FROM M_CASH_TRAN_CNT WHERE DATE_ID=?
            """
            db.cursor.execute(sql2,int(stardate))
            
            sql3="""
            DELETE FROM F_PST_FLOW_DISCOUNT  WHERE DATE_ID=?
            """
            db.cursor.execute(sql3,int(stardate))
            db.conn.commit()

            date_list=[]
            sql_pst="""
            insert into F_PST_FLOW_DISCOUNT
            select d.id date_id,f.*,0 as discount from 
            (
             select
             b.BRANCH_CODE,
             fu.USER_NAME,--1
             fu.NAME, --2  
             max(case when gt.TYPE_NAME='职务' then g.id end) as PST_ID,
             max(case when gt.TYPE_NAME='职务' then g.group_type_code end) as PST_CODE,
             max(case when gt.TYPE_NAME='职务' then g.group_name end) as PST_NAME 
             from F_USER fu
             left join USER_BRANCH ub on ub.USER_ID=fu.ROLE_ID
             left join BRANCH b on b.ROLE_ID=ub.BRANCH_ID
             left join USER_GROUP ug on ug.USER_ID=fu.ROLE_ID 
             left join "GROUP" g on g.ID=ug.GROUP_ID
             left join GROUP_TYPE gt on gt.TYPE_CODE=g.GROUP_TYPE_CODE
             where 1=1  and is_virtual='否' and gt.type_code!='5000'         
             group by fu.USER_NAME,fu.NAME,b.BRANCH_CODE) F,d_date  d
            where  d.id=? and   PST_NAME is not null and branch_code is not null
            """
            db.cursor.execute(sql_pst,int(stardate))
            db.conn.commit()


            sql="""
            insert into M_TELLER_TRAN(DATE_ID,YM,TRAN_BRANCH_CODE,TRAN_TELLER_CODE,SALE_NAME,SALE_ROLE,PST_ID,PST_CODE,PST_NAME,PST_DISCOUNT,TEL_TRAN_CODE,TRANNAME,TRAN_DISCOUNT,CNY_AMOUNT,CNT,TRADE_CNT,DISCOUNT_CNT)
            ( SELECT 
              F.DATE_ID, D.YM, F.TRAN_BRANCH_CODE, F.TRAN_TELLER_CODE, P.SALE_NAME, F.SALE_ROLE, P.PST_ID, P.PST_CODE, P.PST_NAME, P.DISCOUNT AS PST_DISCOUNT, F.TEL_TRAN_CODE, F.TRANNAME, F.DISCOUNT AS TRAN_DISCOUNT, SUM(F.CNY_AMOUNT)*0.01 AS CNY_AMOUNT, SUM(1) AS CNT, 
              SUM(1*F.DISCOUNT) TRADE_CNT, SUM(1*F.DISCOUNT*(1+nvl(P.DISCOUNT,0))) DISCOUNT_CNT 
              FROM 
              ( 
               SELECT DATE_ID,ORIGINAL_JNO,TELLER_JNO,CHILD_JNO,SALE_ROLE,TEL_TRAN_CODE,TRANNAME, NVL(DISCOUNT,0) AS DISCOUNT , TRAN_DATE,TRAN_BRANCH_CODE,TRAN_TELLER_CODE,AUTH_TELLER_CODE1,AUTH_TELLER_CODE2,CHECK_TELLER_CODE,CNY_AMOUNT 
               FROM 

               ( SELECT F.DATE_ID,F.ORIGINAL_JNO,F.TELLER_JNO,F.CHILD_JNO,F.SALE_ROLE,F.TEL_TRAN_CODE,TD.TRANNAME,TD.DISCOUNT, F.TRAN_DATE,F.TRAN_BRANCH_CODE,F.TRAN_TELLER_CODE,F.AUTH_TELLER_CODE1,F.AUTH_TELLER_CODE2,F.CHECK_TELLER_CODE,F.CNY_AMOUNT, ROW_NUMBER() OVER (PARTITION BY F.DATE_ID,F.ORIGINAL_JNO,F.TELLER_JNO,F.TEL_TRAN_CODE,F.TRAN_DATE ORDER BY F.DATE_ID,F.ORIGINAL_JNO,F.TELLER_JNO,F.TEL_TRAN_CODE,F.CHILD_JNO) RN 
                 FROM 
                 YDW.F_JRN_TRANSACTION F 
                 LEFT JOIN F_TRADE_DISCOUNT TD ON F.DATE_ID =TD.DATE_ID AND F.TEL_TRAN_CODE=TD.TRANID 
                 WHERE F.SALE_ROLE='录入柜员'
                 AND F.date_id=? 
               ) 
               WHERE RN=1 AND TEL_TRAN_CODE NOT IN ('413091','731220','无','00413091','00731220') 


               UNION ALL 
               SELECT F.DATE_ID,F.ORIGINAL_JNO,F.TELLER_JNO,F.CHILD_JNO,F.SALE_ROLE,F.TEL_TRAN_CODE,TD.TRANNAME, NVL(TD.DISCOUNT,0) AS DISCOUNT , F.TRAN_DATE,F.TRAN_BRANCH_CODE,F.TRAN_TELLER_CODE,F.AUTH_TELLER_CODE1,F.AUTH_TELLER_CODE2,F.CHECK_TELLER_CODE,F.CNY_AMOUNT 
               FROM 
               YDW.F_JRN_TRANSACTION F 
               INNER JOIN YDW.D_JRN_TRANSACTION_TYPE D ON F.JRN_TRAN_TYPE_ID=D.ID 
               LEFT JOIN F_TRADE_DISCOUNT TD ON F.DATE_ID =TD.DATE_ID AND F.TEL_TRAN_CODE=TD.TRANID 
               WHERE 
               F.TEL_TRAN_CODE IN ('413091','731220','00413091','00731220') AND D.MAIN_JRNL_FLAG<>'非主流水交易' AND F.SALE_ROLE='录入柜员' -----1
               AND F.date_id=? 

              UNION ALL 
              SELECT F.DATE_ID,F.ORIGINAL_JNO,F.TELLER_JNO,F.CHILD_JNO,F.SALE_ROLE,F.TEL_TRAN_CODE,TD.TRANNAME, NVL(TD.DISCOUNT,0) AS DISCOUNT, F.TRAN_DATE,F.TRAN_BRANCH_CODE,F.TRAN_TELLER_CODE,F.AUTH_TELLER_CODE1,F.AUTH_TELLER_CODE2,F.CHECK_TELLER_CODE, F.CNY_AMOUNT 
              FROM 
              YDW.F_JRN_TRANSACTION F LEFT JOIN F_TRADE_DISCOUNT TD ON F.DATE_ID =TD.DATE_ID 
              AND F.TEL_TRAN_CODE=TD.TRANID 
              WHERE F.SALE_ROLE LIKE '复核柜员%' 
              AND F.date_id=?

              UNION ALL
              SELECT F.DATE_ID,F.ORIGINAL_JNO,F.TELLER_JNO,F.CHILD_JNO,F.SALE_ROLE,F.TEL_TRAN_CODE,TD.TRANNAME, 
              CASE WHEN TD.DISCOUNT IS NOT NULL AND TD.DISCOUNT <> 0 THEN 1 ELSE 0 END AS DISCOUNT, F.TRAN_DATE,F.TRAN_BRANCH_CODE,F.TRAN_TELLER_CODE,F.AUTH_TELLER_CODE1,F.AUTH_TELLER_CODE2,
              F.CHECK_TELLER_CODE,F.CNY_AMOUNT 
              FROM 
              YDW.F_JRN_TRANSACTION F LEFT JOIN F_TRADE_DISCOUNT TD ON F.DATE_ID =TD.DATE_ID AND F.TEL_TRAN_CODE=TD.TRANID 
              WHERE F.SALE_ROLE LIKE '授权柜员%'  
              AND F.date_id=?

              UNION ALL 
              SELECT F.DATE_ID,F.ORIGINAL_JNO,F.TELLER_JNO,F.CHILD_JNO,F.SALE_ROLE,F.TEL_TRAN_CODE,TD.TRANNAME, NVL(TD.DISCOUNT,0) AS DISCOUNT, F.TRAN_DATE,F.TRAN_BRANCH_CODE,F.TRAN_TELLER_CODE,F.AUTH_TELLER_CODE1,F.AUTH_TELLER_CODE2,F.CHECK_TELLER_CODE,F.CNY_AMOUNT 
              FROM 
              YDW.F_JRN_TRANSACTION F LEFT JOIN F_TRADE_DISCOUNT TD ON F.DATE_ID =TD.DATE_ID AND F.TEL_TRAN_CODE=TD.TRANID 
              WHERE F.SALE_ROLE ='网银录入柜员'  
              AND F.date_id=?

              UNION ALL 
              SELECT F.DATE_ID,F.ORIGINAL_JNO,F.TELLER_JNO,F.CHILD_JNO,F.SALE_ROLE,F.TEL_TRAN_CODE,TD.TRANNAME, 
              CASE WHEN TD.DISCOUNT IS NOT NULL AND TD.DISCOUNT <> 0 THEN 1 ELSE 0 END AS DISCOUNT, F.TRAN_DATE,F.TRAN_BRANCH_CODE,F.TRAN_TELLER_CODE,F.AUTH_TELLER_CODE1,F.AUTH_TELLER_CODE2,
              F.CHECK_TELLER_CODE,F.CNY_AMOUNT 
              FROM 
              YDW.F_JRN_TRANSACTION F LEFT JOIN F_TRADE_DISCOUNT TD ON F.DATE_ID =TD.DATE_ID AND F.TEL_TRAN_CODE=TD.TRANID 
              WHERE F.SALE_ROLE = '网银授权柜员' 
              AND F.date_id=?

              UNION ALL 
              SELECT F.DATE_ID,F.ORIGINAL_JNO,F.TELLER_JNO,F.CHILD_JNO,F.SALE_ROLE,F.TEL_TRAN_CODE,TD.TRANNAME, NVL(TD.DISCOUNT,0) AS DISCOUNT, F.TRAN_DATE,F.TRAN_BRANCH_CODE,F.TRAN_TELLER_CODE,F.AUTH_TELLER_CODE1,F.AUTH_TELLER_CODE2,F.CHECK_TELLER_CODE,F.CNY_AMOUNT 
              FROM YDW.F_JRN_TRANSACTION F 
              LEFT JOIN F_TRADE_DISCOUNT TD ON F.DATE_ID =TD.DATE_ID AND F.TEL_TRAN_CODE=TD.TRANID 
              WHERE F.SALE_ROLE ='理财录入柜员' 
              AND F.date_id=?

              UNION ALL 
                SELECT F.DATE_ID, '0' AS ORIGINAL_JNO, '0' AS TELLER_JNO, '0' AS CHILD_JNO, F.SALE_ROLE, F.TRAN_CODE, TD.TRANNAME, NVL(TD.DISCOUNT, 0) AS DISCOUNT, F.DATE_ID, F.TRAN_BRANCH_CODE, F.TELLER_CODE AS TRAN_TELLER_CODE, '无' AS AUTH_TELLER_CODE1, '无' AS AUTH_TELLER_CODE2, F.REVIEW_TELLER_CODE AS CHECK_TELLER_CODE, F.AMOUNT AS CNY_AMOUNT 
                FROM 
                YDW.F_CIS_TRAN F LEFT JOIN F_TRADE_DISCOUNT TD ON F.DATE_ID = TD.DATE_ID AND F.TRAN_CODE = TD.TRANID 
                WHERE 
               F.SALE_ROLE = '录入柜员' AND STATUS = '00' 
               AND F.DATE_ID=?

              UNION ALL 
               SELECT F.DATE_ID, '0' AS ORIGINAL_JNO, '0' AS TELLER_JNO, '0' AS CHILD_JNO, F.SALE_ROLE, F.TRAN_CODE, TD.TRANNAME, NVL(TD.DISCOUNT, 0) AS DISCOUNT, F.DATE_ID, F.TRAN_BRANCH_CODE, F.TELLER_CODE AS TRAN_TELLER_CODE, '无' AS AUTH_TELLER_CODE1, '无' AS AUTH_TELLER_CODE2, F.REVIEW_TELLER_CODE AS CHECK_TELLER_CODE, F.AMOUNT AS CNY_AMOUNT 
                FROM 
                YDW.F_CIS_TRAN F LEFT JOIN F_TRADE_DISCOUNT TD ON F.DATE_ID = TD.DATE_ID AND F.TRAN_CODE = TD.TRANID 
               WHERE F.SALE_ROLE = '复核柜员1' AND STATUS = '00' 
               AND F.DATE_ID=?

              ) F 
              INNER JOIN D_DATE D ON F.DATE_ID=D.ID 
              INNER JOIN F_PST_FLOW_DISCOUNT P ON P.SALE_CODE=F.TRAN_TELLER_CODE   
              AND P.DATE_ID=F.DATE_ID
              AND F.date_id=?
              GROUP BY F.DATE_ID,D.YM,F.TRAN_BRANCH_CODE,F.TRAN_TELLER_CODE,P.PST_ID,P.PST_CODE,P.SALE_NAME,F.SALE_ROLE,P.PST_NAME,P.DISCOUNT,F.TEL_TRAN_CODE,F.TRANNAME,F.DISCOUNT
              ) 
            """
            for i in range(sql.count("?")):
                date_list.append(int(stardate))
            db.cursor.execute(sql,date_list)

            sql_amount="""
             insert into M_CASH_TRAN_AMOUNT(DATE_ID,YM,TEL_TRAN_CODE,TRANNAME,TRAN_BRANCH_CODE,TRAN_TELLER_CODE,SALE_NAME,PST_ID,PST_CODE,PST_NAME,PST_DISCOUNT,DIRECT,CNY_AMOUNT,D_CNY_AMOUNT,C_CNY_AMOUNT,MIN_LIMIT_CNT,TOTAL_LIMIT_CNT) 
            (  SELECT F.DATE_ID,     
            substr(f.date_id,1,6) ym,     
            F.TEL_TRAN_CODE,     
            T.TRANNAME,    
            F.TRAN_BRANCH_CODE,     
            F.TRAN_TELLER_CODE,     
            P.SALE_NAME,    
            P.PST_ID,   
            P.PST_CODE,   
            P.PST_NAME,    
            P.DISCOUNT AS PST_DISCOUNT,    
            D.DIRECT,    
            SUM(F.CNY_AMOUNT*0.01) AS CNY_AMOUNT,   
            SUM( CASE WHEN D.DIRECT='借' THEN F.CNY_AMOUNT*0.01 ELSE 0 END) AS D_CNY_AMOUNT,     
            SUM( CASE WHEN D.DIRECT='贷' THEN F.CNY_AMOUNT*0.01 ELSE 0 END) AS C_CNY_AMOUNT ,
            SUM(CASE WHEN F.TEL_TRAN_CODE IN ('001103','1103','1105','001105','001113','1113','001114','1114','004601','4601','004602','4602','004605','4605','004606','4606')  and d.ANALYSIS_CHANNEL in ('柜面', 'TE') 
            and f.AMOUNT<1000000 THEN 1 ELSE 0 END ) AS min_limit_cnt,

            SUM(CASE WHEN F.TEL_TRAN_CODE IN ('001103','1103','1105','001105','001113','1113','001114','1114','004601','4601','004602','4602','004605','4605','004606','4606')  and d.ANALYSIS_CHANNEL in ('柜面', 'TE') THEN 1 ELSE 0 END ) AS total_limit_cnt

            FROM 
                YDW.F_JRN_TRANSACTION F 
                INNER JOIN YDW.D_JRN_TRANSACTION_TYPE D ON F.JRN_TRAN_TYPE_ID=D.ID 
                INNER JOIN F_PST_FLOW_DISCOUNT P ON P.SALE_CODE=F.TRAN_TELLER_CODE AND P.DATE_ID=F.DATE_ID 
                LEFT JOIN D_TRADE T ON T.TRANID=F.TEL_TRAN_CODE 
            WHERE 
                F.SALE_ROLE='录入柜员' AND F.TEL_TRAN_CODE NOT IN ('006213','6213','无','6253','006253','6218','006218') 
                AND D.CASH_TRAN_FLAG='现金' AND D.DIRECT<>'无' AND exists ( SELECT ACCOUNT_NO FROM D_ACCOUNT a WHERE CST_NAME='库存现金' and f.ACCT_NO=a.ACCOUNT_NO )    
                AND F.CNY_AMOUNT > 0 
                AND F.DATE_ID=?
            GROUP BY F.DATE_ID ,F.TEL_TRAN_CODE,T.TRANNAME,F.TRAN_BRANCH_CODE, F.TRAN_TELLER_CODE,P.PST_ID,P.PST_CODE,P.SALE_NAME,P.PST_NAME,P.DISCOUNT ,D.DIRECT )
            """
            db.cursor.execute(sql_amount,int(stardate))

            sql_cnt="""
            insert into M_CASH_TRAN_CNT(DATE_ID,YM,TEL_TRAN_CODE,TRANNAME,TRAN_BRANCH_CODE,TRAN_TELLER_CODE,SALE_NAME,PST_ID,PST_CODE,PST_NAME,PST_DISCOUNT,TRAN_DISCOUNT,CNT,D_CNT,C_CNT) 
            (
            SELECT 
            DATE_ID,  
            SUBSTR(DATE_ID,1,6) YM,  
            TEL_TRAN_CODE,  
            TRANNAME,   
            TRAN_BRANCH_CODE,   
            TRAN_TELLER_CODE,  
            SALE_NAME,   
            PST_ID,   
            PST_CODE,  
            PST_NAME, 
            PST_DISCOUNT,  
            TRAN_DISCOUNT,   
            SUM(1) AS CNT,   
            SUM(CASE WHEN DIRECT='借' THEN 1 ELSE 0 END) AS D_CNT,   
            SUM(CASE WHEN DIRECT='贷' THEN 1 ELSE 0 END) AS C_CNT 
            FROM
            ( SELECT F.DATE_ID,    F.TRAN_DATE,    SUBSTR(F.DATE_ID,1,6) YM,    F.ORIGINAL_JNO,    F.TELLER_JNO,    F.TEL_TRAN_CODE,    T.TRANNAME,    F.TRAN_BRANCH_CODE,    F.TRAN_TELLER_CODE, P.SALE_NAME,    P.PST_ID,    P.PST_CODE,    P.PST_NAME,    P.DISCOUNT AS PST_DISCOUNT,    T.DISCOUNT AS TRAN_DISCOUNT,    D.DIRECT 
              FROM 
              YDW.F_JRN_TRANSACTION F 
              INNER JOIN YDW.D_JRN_TRANSACTION_TYPE D ON F.JRN_TRAN_TYPE_ID=D.ID 
              INNER JOIN F_PST_FLOW_DISCOUNT P ON P.SALE_CODE=F.TRAN_TELLER_CODE AND P.DATE_ID=F.DATE_ID 
              LEFT JOIN F_TRADE_DISCOUNT T ON T.TRANID=F.TEL_TRAN_CODE AND T.DATE_ID = F.DATE_ID 
              WHERE D.CASH_TRAN_FLAG='现金' AND D.DIRECT<>'无' 
                AND exists 
                ( SELECT ACCOUNT_NO FROM D_ACCOUNT a WHERE CST_NAME='库存现金' and f.ACCT_NO=a.ACCOUNT_NO )    
                AND F.CNY_AMOUNT > 0 
                AND F.DATE_ID=?
              GROUP BY 
                F.DATE_ID , F.TRAN_DATE, F.ORIGINAL_JNO, F.TELLER_JNO, F.TEL_TRAN_CODE,T.TRANNAME,F.TRAN_BRANCH_CODE, F.TRAN_TELLER_CODE,P.PST_ID,P.PST_CODE,P.SALE_NAME,P.PST_NAME,P.DISCOUNT , T.DISCOUNT, D.DIRECT )    
            GROUP BY DATE_ID, TEL_TRAN_CODE, TRANNAME,TRAN_BRANCH_CODE,TRAN_TELLER_CODE,SALE_NAME,PST_ID, PST_CODE, PST_NAME,PST_DISCOUNT,TRAN_DISCOUNT )
            """
            db.cursor.execute(sql_cnt,int(stardate))
            db.conn.commit()
            
            """理财"""
            licai="""
            insert into M_TELLER_TRAN(DATE_ID,YM,TRAN_BRANCH_CODE,TRAN_TELLER_CODE,SALE_NAME,SALE_ROLE,PST_ID,PST_CODE,PST_NAME,PST_DISCOUNT,TEL_TRAN_CODE,TRANNAME,TRAN_DISCOUNT,CNY_AMOUNT,CNT,TRADE_CNT,DISCOUNT_CNT)
            select tran_date,left(tran_date,6) YM,TRAN_BRANCH_CODE,TRAN_TELLER_CODE,SALE_NAME,'理财录入柜员',PST_ID,PST_CODE,PST_NAME,ft.DISCOUNT,
            fm.tel_tran_code,td.TRANNAME,td.DISCOUNT,0 as CNY_AMOUNT,SUM(1) AS CNT, SUM(1*td.DISCOUNT) TRADE_CNT, SUM(1*td.DISCOUNT*(1+nvl(ft.DISCOUNT,0))) DISCOUNT_CNT 
            from 
            FMS_TRANS_LOG fm
            join F_PST_FLOW_DISCOUNT ft on fm.TRAN_TELLER_CODE = ft.SALE_CODE and ft.date_id=fm.TRAN_DATE
            left join F_TRADE_DISCOUNT TD  ON fm.tran_date = TD.DATE_ID AND Fm.tel_tran_code = TD.TRANID
            where TRAN_DATE=?
            group by tran_date,TRAN_BRANCH_CODE,TRAN_TELLER_CODE,TEL_TRAN_CODE,SALE_NAME,PST_ID,PST_CODE,PST_NAME,ft.DISCOUNT,fm.tel_tran_code,td.TRANNAME,td.DISCOUNT
            """
            db.cursor.execute(licai,int(stardate))
            db.conn.commit()
            print stardate,"完成",datetime.now()- oneday
            stardate=int(util.daycalc(stardate,1))
    finally :
        db.cursor.execute("refresh table M_ORG_DATE_FLAT")
        db.closeDB()

if __name__=='__main__':
    arglen=len(sys.argv)
    print sys.argv 
    d1=datetime.now()
    if arglen ==3:
        stardate=int(sys.argv[1])
        etldate=int(sys.argv[2])
        print stardate,etldate
        m_teller_tran(stardate,etldate)
        print "m_teller_tran",stardate,etldate,"完成",datetime.now()-d1
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
