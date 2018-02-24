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
import man_ebank_sal_new as ebanksal
import posatm as posatm
import man_ebank_sco_new as ebank_sco 
     
condecimal = getcontext()
"""
客户经理电子银行指标报表
"""
def man_dep(stardate,etldate):
    try:
        oneday=datetime.now()
        db = util.DBConnect()
        while stardate<=etldate:
            sql0 = """
            UPDATE YDW.REPORT_MANAGER_OTHER 
                SET  MB_LAST_NUM=0, MB_THIS_NUM=0, CB_LAST_NUM=0, CB_THIS_NUM=0, EPAY_LAST_NUM=0, EPAY_THIS_NUM=0, ETC_LAST_NUM=0, ETC_THIS_NUM=0, PB_LAST_NUM=0, PB_THIS_NUM=0, KT_LAST_NUM=0, KT_THIS_NUM=0, KJ_LAST_NUM=0, KJ_THIS_NUM=0, ADD_HIGH_POS_NUM=0, ADD_LOW_POS_NUM=0, FARM_SERV_HIGH_NUM=0, FARM_SERVICE_LOW_NUM=0, LAST_THIRD_DEPO_NUM=0, THIRD_DEPO_ADD_NUM=0, THIS_ADD_ETC_NUM=0, MB_ADD_NUM_SAL=0, CB_ADD_NUM_SAL=0, EPAY_ADD_NUM_SAL=0, ADD_HIGH_POS_SAL=0, ADD_LOW_POS_SAL=0, FARM_SERV_SAL=0, ADD_ETC_NUM_SAL=0, ADD_THIRD_DEPO_SAL=0, ALL_SCO=0, MB_ADD_SCO=0, CB_ADD_SCO=0, POS_ADD_SCO=0, BAD_ADD_SCO=0, ETC_ADD_SCO=0, EPAY_ADD_SCO=0, FRAM_SCO=0, POS_THIS_NUM=0, BASE_PAY=0, POSITION_PAY=0, BRANCH_NET_SAL=0, MANAGE_BUS_SAL=0, WORK_QUALITY_SAL=0, HIG_CIV_QUAL_SAL=0, JOB_SAT_SAL=0, DAY_DEP_COMP_PER=0, DAY_DEP_SAL=0, DAY_DEP_SEC_FEN=0, CREDIT_POOL=0, INTER_SET_SAL=0, SALE_VOC_SAL=0, ADD_EFC_CURSAL=0, ADD_FUNON_SAL=0, PER_CAR_DANERSAL=0, BUM_HOM_SAL=0, OTHER_ACHI_SAL=0, COMPRE_SAL=0, LABOR_COMP_SAL=0, PROV_FUND_SAL=0, SAFE_FAN_SAL=0, ALL_RISK_SAL=0, BAD_LOAN_PERSAL=0, FTP_ACH_SAL=0, COUNT_COMPLE_SAL=0, COUNT_COP_SSAL=0, HP_FINA_SAL=0, OTHER_SPEC_SAL1=0, OTHER_SPEC_SAL2=0, OTHER_SPEC_SAL3=0, OTHER_SPEC_SAL4=0, OTHER_SPEC_SAL5=0, BRANCH_SECO_FEN1=0, BRANCH_SECO_FEN2=0, BRANCH_SECO_FEN3=0, BRANCH_SECO_FEN4=0, OTHER_ACH_WAGES=0, OVER_WORK_SAL=0, OTHER_SAL1_DUAN=0, OTHER_SAL2=0, OTHER_SAL3_WEI=0, OTHER_SAL4_KE=0, OTHER_SAL5_GE=0, OTHER_SAL6=0, OTHER_SAL7=0, OTHER_SAL8=0, QJ_BAD_LOAN_SAL=0, ADD_FUNON_NUM=0, FLAG=0
                    WHERE DATE_ID=?
            """
            db.cursor.execute(sql0,int(stardate))
            db.conn.commit()

            sql="""
            SELECT COUNT(DISTINCT (CASE WHEN C.BUSI_TYPE='手机银行' AND F.SUB_TYPE='专业版' AND F.STATUS NOT IN ('已注销','注销')  THEN C.CST_NO END )), --手机银行户数
            COUNT(DISTINCT (CASE WHEN C.BUSI_TYPE='手机银行' AND F.SUB_TYPE='专业版' AND F.STATUS NOT IN ('已注销','注销') AND (DAYS(TO_DATE(F.DATE_ID,'YYYYMMDD'))-DAYS(TO_DATE(MAX(F.LAST_LOGON_DATE,LEFT(C.OPEN_DATE,8)),'YYYYMMDD')))<=180 THEN C.CST_NO  END )), --手机银行有效户数
            COUNT(DISTINCT (CASE WHEN C.BUSI_TYPE='个人网上银行' AND F.SUB_TYPE='专业版'  AND F.STATUS NOT IN ('已注销','注销')  THEN C.CST_NO END )), --个人银行户数
            COUNT(DISTINCT (CASE WHEN C.BUSI_TYPE='个人网上银行' AND F.SUB_TYPE='专业版'  AND F.STATUS NOT IN ('已注销','注销') AND (DAYS(TO_DATE(F.DATE_ID,'YYYYMMDD'))-DAYS(TO_DATE(MAX(F.LAST_LOGON_DATE,LEFT(C.OPEN_DATE,8)),'YYYYMMDD')))<=180 THEN C.CST_NO END )), --个人银行有效户数
            COUNT(DISTINCT (CASE WHEN C.BUSI_TYPE='企业网上银行' AND F.STATUS<>'销户' THEN C.CST_NO END)), --企业银行有效户数存量
            COUNT(DISTINCT (CASE WHEN C.BUSI_TYPE='企业网上银行' AND F.STATUS<>'销户' AND (DAYS(TO_DATE(F.DATE_ID,'YYYYMMDD'))-DAYS(TO_DATE(MAX(F.LAST_LOGON_DATE,LEFT(C.OPEN_DATE,8)),'YYYYMMDD')))<=180 THEN C.CST_NO END )), --企业银行有效户数现量
            SUM(CASE WHEN C.BUSI_TYPE='支付宝卡通' AND F1.STATUS IN ('签约成功','正常') THEN 1 ELSE 0 END ), --支付宝卡通有效户数存量
            COUNT(DISTINCT (CASE WHEN C.BUSI_TYPE='支付宝卡通' AND F.STATUS IN ('签约成功','正常') THEN C.CST_NO END )), --支付宝卡通有效户数现量
            SUM(CASE WHEN C.BUSI_TYPE='支付宝快捷支付' THEN 1 ELSE 0 END ), --支付宝快捷支付有效户数存量
            COUNT(DISTINCT (CASE WHEN C.BUSI_TYPE='支付宝快捷支付' THEN C.CST_NO END )), --支付宝快捷支付有效户数现量
            COUNT(DISTINCT (CASE WHEN C.BUSI_TYPE IN ('丰收e支付','新丰收e支付') AND F.STATUS<>'注销' THEN C.AGREMENT_NO END )), --丰收E支付户数
            COUNT(DISTINCT (CASE WHEN C.BUSI_TYPE IN ('丰收e支付','新丰收e支付') AND F.STATUS<>'注销' AND (DAYS(TO_DATE(F.DATE_ID,'YYYYMMDD'))-DAYS(TO_DATE(MAX(F.LAST_TRADE_DATE,LEFT(C.OPEN_DATE,8)),'YYYYMMDD')))<=180 THEN C.AGREMENT_NO END )), --丰收E支付有效户数现量
            SUM(CASE WHEN C.BUSI_TYPE='ETC' AND F1.STATUS IN ('签约成功','正常') THEN 1 ELSE 0 END), --ECT 存量
            COUNT(DISTINCT (CASE WHEN C.BUSI_TYPE='ETC' AND F.STATUS IN ('签约成功','正常') THEN C.NET_CST_NO END)),  --ETC 现量
            SUM (CASE WHEN C.BUSI_TYPE='第三方存管' AND F1.STATUS IN ('已签约') THEN 1 ELSE 0 END),  --存量
            COUNT(DISTINCT (CASE WHEN C.BUSI_TYPE='第三方存管' AND F.STATUS IN ('已签约') THEN C.ID_NUMBER END)),  --量
            F.DATE_ID,M.SALE_CODE
            FROM F_CONTRACT_STATUS F
            LEFT JOIN (SELECT CONTRACT_ID,STATUS,LAST_LOGON_DATE,LAST_TRADE_DATE FROM F_CONTRACT_STATUS F WHERE DATE_ID=(SELECT L_YEAREND_ID FROM D_DATE  WHERE ID=?) ) F1 ON F1.CONTRACT_ID=F.CONTRACT_ID
            JOIN D_CUST_CONTRACT C ON F.CONTRACT_ID=C.ID 
            JOIN D_DATE D ON F.DATE_ID=D.ID  
            JOIN D_DATE DD ON D.L_YEAREND_ID=DD.ID
            JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID --AND M.MANAGE_TYPE<>'机构管理' 
            WHERE F.DATE_ID =?    ----AND M.SALE_CODE IN ('9660160','X9660160')
            GROUP BY F.DATE_ID,M.SALE_CODE
            """
            sql1="""
            UPDATE YDW.REPORT_MANAGER_OTHER SET  MB_LAST_NUM=?, MB_THIS_NUM=?, PB_LAST_NUM=?, PB_THIS_NUM=?, CB_LAST_NUM=?, CB_THIS_NUM=?, KT_LAST_NUM=?, KT_THIS_NUM=?, KJ_LAST_NUM=?, KJ_THIS_NUM=?, EPAY_LAST_NUM=?, EPAY_THIS_NUM=?, ETC_LAST_NUM=?, ETC_THIS_NUM=?,LAST_THIRD_DEPO_NUM=?,THIRD_DEPO_ADD_NUM=?,FLAG=1 WHERE   DATE_ID=? AND  SALE_CODE=? 
            """
            db.cursor.execute(sql,int(stardate),int(stardate))
            row = db.cursor.fetchall()
            #print row
            resultrow=[]
            for i in row:
                t = list(i[0:])
                resultrow.append(t)
            #print resultrow
            db.cursor.executemany(sql1,resultrow)
            db.conn.commit()

            #更新ETC相关
            sql_e=u"""SELECT LEFT(L_YEAREND_ID,4) FROM D_DATE WHERE ID=?"""
            db.cursor.execute(sql_e,stardate)
            row_e=db.cursor.fetchall()
            last_year = row_e[0][0]
            sql_et=u"""
            SELECT COUNT(A.CUST_NET_NO),COUNT(B.CUST_NET_NO),CASE WHEN LENGTH(TRIM(A.TELLER_NO))<6 THEN A.ORG_NO ELSE A.TELLER_NO END ,A.ORG_NO
            FROM ETC_DATA A LEFT JOIN ETC_DATA B  ON A.CUST_NET_NO=B.CUST_NET_NO AND LEFT(B.DATE_ID,4)=?
             WHERE LEFT(A.DATE_ID,4)=(SELECT YEAR FROM D_DATE WHERE ID=?) GROUP BY A.TELLER_NO,A.ORG_NO
            """
            db.cursor.execute(sql_et,last_year,stardate)
            row_et=db.cursor.fetchall()
            u_sql_et = u"""
            UPDATE YDW.REPORT_MANAGER_OTHER SET ETC_THIS_NUM=?,ETC_LAST_NUM=?,FLAG=1 WHERE SALE_CODE=? AND ORG_CODE=? 
            """
            resultrow_et = []
            for i in row_et:
                t = list(i[0:])
                resultrow_et.append(t)
            #print resultrow_et
            db.cursor.executemany(u_sql_et,resultrow_et)
            db.conn.commit()



            """刷客户经理的佣金报表"""
            month_end_sql="""
            select month_end from D_DATE where ID=?
            """
            db.cursor.execute(month_end_sql,stardate)
            is_month_end=db.cursor.fetchall()
            if is_month_end[0][0]=='Y': 
                ebanksal.man_ebank_sal(etldate)
                posatm.man_posatm(stardate,stardate)
                #ebank_sco.man_ebank_sco_new(stardate,stardate)
            
            sql2="""
            DELETE FROM REPORT_MANAGER_OTHER WHERE DATE_ID=? AND FLAG=0
            """
            db.cursor.execute(sql2,int(stardate))
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
        man_dep(stardate,etldate)
        print stardate,"完成",datetime.now()-d1
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
