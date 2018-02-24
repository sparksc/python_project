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
import loan_duty as loanduty
import loan_old as loanold
import man_loan_sco_new as loan_sco 
     
condecimal = getcontext()
"""
客户经理贷款指标报表
"""
def man_loan(stardate,etldate):
    try:
        oneday=datetime.now()
        db = util.DBConnect()
        while stardate<=etldate:
            sql0="""
            UPDATE YDW.REPORT_MANAGER_LOAN 
            SET  PRI_NUM=0, PUB_NUM=0, PRI_LAST_AVG=0, PUB_LAST_AVG=0, PRI_THIS_AVG=0, PUB_THIS_AVG=0, PRI_ADD_NUM=0, PUB_ADD_NUM=0, PRI_ADD_BAL=0, PUB_ADD_BAL=0, MIN_CRD_NUM=0, MIN_NUM=0, MIN_CRD_BAL=0, MIN_BAL=0, BAD_NUM=0, BAD_BAL=0, OUT_NUM=0, OUT_BAL=0, TWO_LAST_NUM=0, TWO_THSI_NUM=0, PRI_LAST_STANDARD_NUM=0, PUB_LAST_STANDARD_NUM=0, PRI_THIS_MON_AVG=0, PUB_THIS_MON_AVG=0, TWO_CARD_LOANRATE=0, PRI_ELEC_FILE_INFO=0, PUB_ELEC_FILE_INFO=0, TOTAL_NUM_SAL=0, AVG_SAL=0, PRI_ADD_NUM_SAL=0, PUB_ADD_NUM_SAL=0, ADD_AVG_ASL=0, TWO_CARD_LOANRATE_SAL=0, ELEC_FILE_INFO_SAL=0, PRI_MONTH_AVG=0, PUB_MONTH_AVG=0, MONTH_AVG=0, PRI_PDT=0, PUB_PDT=0, PRI_THIS_STANDARD_NUM=0, PUB_THIS_STANDARD_NUM=0, PRI_BAL=0, PUB_BAL=0, ALL_SCO=0, TWO_CARD_BY_EBANK=0, TWO_CARD_ALL=0, AVG_LOAN_SCO=0, ZX_SCO=0, TWO_CRAD_SCO=0, VILLAGE_SCO=0, LOAN_SCO=0, MIN_CARD_SCO=0, TWO_CARD_ADD=0, DSZRYE=0, DGZRYE=0, DSZRYE1=0, DGZRYE1=0, DSYSLX=0, DGYSLX=0, DSGGYE=0, DGGGYE=0, DAILY_AVE_LOAN=0, FOR_GRAD_BAD=0,DSGGRJ=0,DGGGRJ=0,FLAG=0,PRI_LAST_BAL=0,PUB_LAST_BAL=0,PRI_LAST_NUM=0,PUB_LAST_NUM=0
            WHERE   DATE_ID=?
            """
            db.cursor.execute(sql0,int(stardate))
            db.conn.commit()
            sql="""
            SELECT COUNT(DISTINCT (CASE WHEN LEFT(F.CST_NO,2)='81' AND F.BALANCE>0 THEN F.CST_NO END)),--对私管贷户数
            COUNT(DISTINCT (CASE WHEN LEFT(F.CST_NO,2)='82' AND F.BALANCE>0 THEN F.CST_NO END)),--对公管贷户数
            COUNT(DISTINCT (CASE WHEN LEFT(F.CST_NO,2)='81' AND F1.BALANCE>( SELECT D.DETAIL_VALUE*100 FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID  JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME='管贷客户户数指贷款余额参数' AND H.HEADER_NAME='管贷客户户数指贷款余额(元)' ) THEN F.CST_NO END)),--管贷余额大于等于5000元的对私客户户数(上年年末)
            COUNT(DISTINCT (CASE WHEN LEFT(F.CST_NO,2)='82' AND F1.BALANCE>( SELECT D.DETAIL_VALUE*100 FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID  JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME='管贷客户户数指贷款余额参数' AND H.HEADER_NAME='管贷客户户数指贷款余额(元)' ) THEN F.CST_NO END)),--管贷余额大于等于5000元的对公客户户数(上年年末)
            COUNT(DISTINCT (CASE WHEN LEFT(F.CST_NO,2)='81' AND F.BALANCE>( SELECT D.DETAIL_VALUE*100 FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME='管贷客户户数指贷款余额参数' AND H.HEADER_NAME='管贷客户户数指贷款余额(元)' ) THEN F.CST_NO END)),--管贷余额当前大于等于5000元的对私客户户数
            COUNT(DISTINCT (CASE WHEN LEFT(F.CST_NO,2)='82' AND F.BALANCE>( SELECT D.DETAIL_VALUE*100 FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME='管贷客户户数指贷款余额参数' AND H.HEADER_NAME='管贷客户户数指贷款余额(元)' ) THEN F.CST_NO END)),--管贷余额当前大于等于5000元的对公客户户数
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' THEN F1.YEAR_PDT*M.PERCENT/ 100 ELSE 0 END)/ DD.YEAR_DAYS),--对私存量日均
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' THEN F1.YEAR_PDT*M.PERCENT/ 100 ELSE 0 END)/ DD.YEAR_DAYS),--对公存量日均
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' THEN F.YEAR_PDT*M.PERCENT/ 100 ELSE 0 END)/ D.BEG_YEAR_DAYS),--对私现量日均
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' THEN F.YEAR_PDT*M.PERCENT/ 100 ELSE 0 END)/ D.BEG_YEAR_DAYS),--对公现量日均
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' AND F.ACCT_TYPE=4 THEN ( CASE WHEN SUBSTR(DATE_ID,5,2)!='01'THEN (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0))*M.PERCENT/ 100 ELSE NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 END ) ELSE 0 END)/ D.BEG_MONTH_DAYS),--对私当月贷款日均
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' AND F.ACCT_TYPE=4 THEN ( CASE WHEN SUBSTR(DATE_ID,5,2)!='01'THEN (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0))*M.PERCENT/ 100 ELSE NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 END ) ELSE 0 END)/ D.BEG_MONTH_DAYS),--对公当月贷款日均
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='81' THEN ( CASE WHEN SUBSTR(DATE_ID,5,2)!='01'THEN (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0))*M.PERCENT/ 100 ELSE NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 END ) ELSE 0 END)/ D.BEG_MONTH_DAYS) AS DSYLJ,--对私月日均
            BIGINT(SUM(CASE WHEN LEFT(F.CST_NO,2)='82' THEN ( CASE WHEN SUBSTR(DATE_ID,5,2)!='01'THEN (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0))*M.PERCENT/ 100 ELSE NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 END ) ELSE 0 END)/ D.BEG_MONTH_DAYS) AS DGYLJ,--对公月日均
            BIGINT(SUM(CASE WHEN SUBSTR(DATE_ID,5,2)!='01' THEN (NVL(F.YEAR_PDT,0)-NVL(F2.YEAR_PDT,0))*M.PERCENT/ 100 ELSE NVL(F.YEAR_PDT,0)*M.PERCENT/ 100 END )/ D.BEG_MONTH_DAYS) AS YLJ,--月日均
            COUNT(DISTINCT (CASE WHEN T.GUA_TP_NAME='信用' AND F.BALANCE>0 AND F.BALANCE<=30000000 THEN F.CST_NO END)),--小额信用贷款户数
            COUNT(DISTINCT (CASE WHEN F.BALANCE>0 AND F.BALANCE<=30000000 THEN F.CST_NO END)),--小额贷款户数
            SUM(CASE WHEN T.GUA_TP_NAME='信用' AND F.BALANCE<=30000000 THEN F.BALANCE ELSE 0 END),--小额信用贷款余额
            SUM(CASE WHEN F.BALANCE<=30000000 THEN F.BALANCE ELSE 0 END),--小额贷款余额
            COUNT(DISTINCT (CASE WHEN S.GRADE_FOUR IN ('逾期','呆滞','呆账') AND F.BALANCE>0 THEN F.CST_NO END)),--资产不良贷款户数
            SUM(CASE WHEN S.GRADE_FOUR IN ('逾期','呆滞','呆账') AND (F.BALANCE>0 OR F.OUT_BALANCE>0)  THEN (F.BALANCE+F.OUT_BALANCE) ELSE 0 END),--资产不良贷款余额
            COUNT(DISTINCT (CASE WHEN F.OUT_BALANCE>0 THEN F.CST_NO END)),--核销贷款户数
            SUM(CASE WHEN F.OUT_BALANCE>0 THEN F.OUT_BALANCE ELSE 0 END), --核销贷款余额
            SUM(CASE WHEN LEFT(F.CST_NO,2)='81' AND F.BALANCE>0 THEN F.BALANCE END),--对私余额
            SUM(CASE WHEN LEFT(F.CST_NO,2)='82' AND F.BALANCE>0 THEN F.BALANCE END),--对公余额      
            SUM(CASE WHEN LEFT(F.CST_NO,2)='81' AND F1.BALANCE>0 THEN F1.BALANCE END),--对私余额存量
            SUM(CASE WHEN LEFT(F.CST_NO,2)='82' AND F1.BALANCE>0 THEN F1.BALANCE END),--对公余额存量  
            COUNT(DISTINCT (CASE WHEN LEFT(F.CST_NO,2)='81' AND F1.BALANCE>0 THEN F1.CST_NO END)),--对私管贷户数
            COUNT(DISTINCT (CASE WHEN LEFT(F.CST_NO,2)='82' AND F1.BALANCE>0 THEN F1.CST_NO END)),--对公管贷户数
            F.DATE_ID,M.SALE_CODE
            FROM F_BALANCE F
            LEFT JOIN (SELECT ACCOUNT_ID,YEAR_PDT,BALANCE,CST_NO FROM F_BALANCE F WHERE DATE_ID=(SELECT L_YEAREND_ID FROM D_DATE WHERE ID=?) AND ACCT_TYPE=4)F1 ON F1.ACCOUNT_ID=F.ACCOUNT_ID
            LEFT JOIN (SELECT ACCOUNT_ID,YEAR_PDT,BALANCE FROM F_BALANCE F WHERE DATE_ID=(SELECT L_MONTHEND_ID FROM D_DATE WHERE ID=?) AND ACCT_TYPE=4) F2 ON F2.ACCOUNT_ID=F.ACCOUNT_ID
            JOIN D_LOAN_ACCOUNT A ON F.ACCOUNT_ID=A.ID AND A.CCY='CNY'
            JOIN D_ACCOUNT_TYPE T ON F.ACCOUNT_TYPE_ID=T.ID 
            JOIN D_ACCOUNT_STATUS S ON F.ACCOUNT_STATUS_ID=S.ID
            JOIN D_DATE D ON F.DATE_ID=D.ID  
            JOIN D_DATE DD ON D.L_YEAREND_ID=DD.ID
            JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID  --AND M.MANAGE_TYPE='机构管理' 
            WHERE F.ACCT_TYPE=4   AND F.DATE_ID =?  -----AND M.SALE_CODE IN ('9660160','X9660160')
            GROUP BY F.DATE_ID,M.SALE_CODE,D.BEG_YEAR_DAYS,DD.YEAR_DAYS,D.BEG_MONTH_DAYS,D.MONTH_DAYS
            """
            sql1=u"""
            UPDATE YDW.REPORT_MANAGER_LOAN SET  PRI_NUM=?, PUB_NUM=?, PRI_LAST_STANDARD_NUM=?,PUB_LAST_STANDARD_NUM=?,PRI_THIS_STANDARD_NUM=?,PUB_THIS_STANDARD_NUM=?,PRI_LAST_AVG=?, PUB_LAST_AVG=?, PRI_THIS_AVG=?, PUB_THIS_AVG=?,PRI_THIS_MON_AVG=?,PUB_THIS_MON_AVG=?, PRI_MONTH_AVG=?,PUB_MONTH_AVG=?,MONTH_AVG=?, MIN_CRD_NUM=?, MIN_NUM=?, MIN_CRD_BAL=?, MIN_BAL=?, BAD_NUM=?, BAD_BAL=?, OUT_NUM=?, OUT_BAL=?,PRI_BAL=?,PUB_BAL=?,FLAG=1,PRI_LAST_BAL=?,PUB_LAST_BAL=?,PRI_LAST_NUM=?,PUB_LAST_NUM=? WHERE   DATE_ID=? AND SALE_CODE=?
            """
            db.cursor.execute(sql,int(stardate),int(stardate),int(stardate))
            row=db.cursor.fetchall()
            resultrow=[]
            for i in row:
                t=list(i[0:])
                resultrow.append(t)
            #print resultrow
            db.cursor.executemany(sql1,resultrow)
            """对公扩面管贷户数.管贷余额 """
            sql3="""
            SELECT COUNT(DISTINCT CST_NO),SUM(PUB_ADD_BAL), ORG_CODE,SALE_CODE FROM(
                SELECT  M.THIRD_BRANCH_CODE ORG_CODE,M.SALE_CODE ,F.CST_NO,
            SUM(F.BALANCE) PUB_ADD_BAL
            FROM F_BALANCE  F 
            JOIN D_ACCOUNT A ON F.ACCOUNT_ID=A.ID
            JOIN D_SALE_MANAGE_RELA M ON M.MANAGE_ID=F.MANAGE_ID
            WHERE F.DATE_ID=?
            AND F.ACCT_TYPE IN(4,7) AND F.BALANCE>0 
            GROUP BY M.THIRD_BRANCH_CODE,M.SALE_CODE,F.CST_NO
            HAVING SUM(F.BALANCE)>100000000 AND LEFT(F.CST_NO,2)='82'
            )
            GROUP BY ORG_CODE,SALE_CODE
            """
            """对私扩面管贷户数.管贷余额 """
            sql4="""
            SELECT COUNT(DISTINCT CST_NO),SUM(PUB_ADD_BAL),ORG_CODE,SALE_CODE  FROM(
            SELECT  M.THIRD_BRANCH_CODE ORG_CODE,M.SALE_CODE ,F.CST_NO,
            SUM(F.BALANCE) PUB_ADD_BAL
            FROM F_BALANCE  F 
            JOIN D_ACCOUNT A ON F.ACCOUNT_ID=A.ID
            JOIN D_SALE_MANAGE_RELA M ON M.MANAGE_ID=F.MANAGE_ID
            WHERE F.DATE_ID=?
            AND F.ACCT_TYPE IN(4,7) AND F.BALANCE>0 
            GROUP BY M.THIRD_BRANCH_CODE,M.SALE_CODE,F.CST_NO
            HAVING (SUM(F.BALANCE)<=100000000 and sum(f.balance)>500000  AND LEFT(F.CST_NO,2)='82') OR LEFT(F.CST_NO,2)='81'
            )
            GROUP BY ORG_CODE,SALE_CODE
            """
            """两卡电子渠道办贷率 """
            sql5=u"""
            SELECT     COUNT(DISTINCT CASE WHEN J.CHANNELDESC IN ('自助终端','网银') THEN F.CST_NO END), --通过电子渠道办贷的户数      -----前端上除以下，显示两卡电子渠道办贷率
            COUNT(DISTINCT F.CST_NO ),                                                            --总户数
            F.DATE_ID,M.THIRD_BRANCH_CODE,M.SALE_CODE
            FROM F_BALANCE F
            JOIN D_LOAN_ACCOUNT A ON F.ACCOUNT_ID=A.ID AND A.CCY='CNY' AND LOAN_PROD_CODE IN ('51118','51154','51155','51156')
            JOIN D_ACCOUNT_TYPE T ON F.ACCOUNT_TYPE_ID=T.ID 
            JOIN D_ACCOUNT_STATUS S ON F.ACCOUNT_STATUS_ID=S.ID
            JOIN D_DATE D ON F.DATE_ID=D.ID  
            JOIN F_T_LOAN_JRNL J ON A.ID=J.ACCT_ID AND J.TRANS_DATE_ID>=D.YEARBEG_ID AND J.TRANS_DATE_ID<=D.YEAREND_ID
            JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID AND LENGTH(M.SALE_CODE)=7--AND M.MANAGE_TYPE='机构管理' 
            WHERE F.ACCT_TYPE=4   AND F.DATE_ID =? 
            GROUP BY F.DATE_ID,M.THIRD_BRANCH_CODE,M.THIRD_BRANCH_NAME,M.SALE_CODE,M.SALE_NAME,D.BEG_MONTH_DAYS--,DD.YEAR_DAYS
            ORDER BY SALE_CODE
            """
            """丰收两卡合同现量,丰收两卡合同存量"""
            sql6=u"""
            SELECT COUNT( DISTINCT(F.CONTRACT_ID)),         ---现在有效
            COUNT( DISTINCT(F1.CONTRACT_ID)),               ----去年存量
            F.DATE_ID,D.OPEN_BRANCH_NO,M.SALE_CODE
            FROM F_CONTRACT_STATUS F
            LEFT JOIN  ( SELECT * FROM  F_CONTRACT_STATUS  F WHERE F.DATE_ID=(SELECT L_YEAREND_ID FROM D_DATE WHERE ID=?)  )  F1 ON F.CONTRACT_ID=F1.CONTRACT_ID
            LEFT JOIN D_CUST_CONTRACT D ON F.CONTRACT_ID=D.ID
            JOIN D_ORG O ON D.OPEN_BRANCH_NO = O.ORG0_CODE
            JOIN D_MANAGE DM ON F.MANAGE_ID=DM.ID
            JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID 
            WHERE D.BUSI_TYPE = '贷款合同' AND F.STATUS IN ('发放','暂停','有效') AND F.DATE_ID = ? AND  D.SUB_TYPE IN ('51118','51154','51155','51156') 
            GROUP BY F.DATE_ID,D.OPEN_BRANCH_NO,M.SALE_CODE
            """
            
            db.cursor.execute(sql3,int(stardate))
            row3=db.cursor.fetchall()
            resultrow3=[]
            for i in row3:
                t=list(i[0:])
                t.append(int(stardate))
                resultrow3.append(t)
            #print resultrow3
            """更新对公扩面管贷户数.管贷余额 """
            u_sql3="""
            UPDATE REPORT_MANAGER_LOAN  SET PUB_ADD_NUM=? ,PUB_ADD_BAL=?,FLAG=1 WHERE ORG_CODE=? and SALE_CODE=? and DATE_ID=?
            """
            db.cursor.executemany(u_sql3,resultrow3)

            db.cursor.execute(sql4,int(stardate))
            row4=db.cursor.fetchall()
            resultrow4=[]
            for i in row4:
                t=list(i[0:])
                t.append(int(stardate))
                resultrow4.append(t)
            #print resultrow4
            """更新对私扩面管贷户数.管贷余额 """
            u_sql4="""
            UPDATE REPORT_MANAGER_LOAN  SET PRI_ADD_NUM= ?,PRI_ADD_BAL= ?,FLAG=1 WHERE ORG_CODE=? and SALE_CODE=? and DATE_ID=?
            """
            db.cursor.executemany(u_sql4,resultrow4)
            
            db.cursor.execute(sql5.encode('utf-8'),int(stardate))
            row5=db.cursor.fetchall()
            #print row5
            resultrow5=[]
            for i in row5:
                t=list(i[0:])
                resultrow5.append(t)
            #print resultrow5
            """ """
            u_sql5="""
            UPDATE REPORT_MANAGER_LOAN  SET TWO_CARD_BY_EBANK= ?,TWO_CARD_ALL=?,FLAG=1 WHERE  DATE_ID=?  and ORG_CODE=? and SALE_CODE=?
            """
            db.cursor.executemany(u_sql5,resultrow5)
            
            db.cursor.execute(sql6.encode('utf-8'),int(stardate),int(stardate))
            row6=db.cursor.fetchall()
            #print row6
            resultrow6=[]
            for i in row6:
                t=list(i[0:])
                resultrow6.append(t)
            #print resultrow6
            """ """
            u_sql6="""
            UPDATE REPORT_MANAGER_LOAN  SET TWO_THSI_NUM= ?, TWO_LAST_NUM=?,FLAG=1  WHERE  DATE_ID=?  and ORG_CODE=? and SALE_CODE=?
            """
            db.cursor.executemany(u_sql6,resultrow6)

            db.conn.commit()

            sql7="""
            DELETE FROM REPORT_MANAGER_LOAN WHERE DATE_ID=? AND FLAG=0 
            """
            db.cursor.execute(sql7,int(stardate))
            db.conn.commit()
            
            """贷款责任"""
            loanduty.man_loan(stardate,stardate)
            """刷客户经理的佣金报表"""
            month_end_sql="""
            select month_end from D_DATE where ID=?
            """
            db.cursor.execute(month_end_sql,stardate)

            is_month_end=db.cursor.fetchall()
            if is_month_end[0][0]=='Y': 
                loansal.man_loan_sal(stardate)
                loanold.loan_old(stardate,stardate)
                #loan_sco.man_loan_sco_new(stardate,stardate)
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
