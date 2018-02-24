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
客户经理电子银行绩效得分
"""
#对计划数折比例
def target_percent(target,etldate):
    """计算任务当前月应该完成数"""
    month = str(etldate)[4:6]
    tar_end = float(target) * (float(month) / 12.0)
    return tar_end

#对私类贷款客户有效手机银行绑定率
def man_pri_loan_ebank(db,stardate):
    sql_e=u"""
    SELECT M.SALE_CODE,ROUND(COUNT(DISTINCT CASE WHEN LEFT(C.CST_NO,2)='81' THEN F.CST_NO END)*1.00/ COUNT(DISTINCT CASE WHEN LEFT(F.CST_NO,2)='81' THEN F.CST_NO END),2),M.THIRD_BRANCH_CODE
    FROM F_BALANCE F 
    JOIN D_LOAN_ACCOUNT D ON F.ACCOUNT_ID=D.ID
    JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID
    JOIN D_CUST_INFO I ON F.CST_NO= I.CUST_NO
    LEFT JOIN (SELECT C.CST_NO FROM F_CONTRACT_STATUS F
    JOIN D_CUST_CONTRACT C ON C.ID=F.CONTRACT_ID
    WHERE F.DATE_ID=? AND F.STATUS IN ('正常','暂时冻结','停用','冻结') 
     AND C.BUSI_TYPE LIKE '手机银行' ) C ON F.CST_NO=C.CST_NO 
     WHERE F.DATE_ID=? AND F.ACCT_TYPE='4' AND LENGTH(TRIM(I.CUST_LONG_NO))>15  AND LEFT(F.CST_NO,2)='81' AND LEFT(I.CUST_LONG_NO,3)='101' AND LEFT(I.CUST_LONG_NO,4)<>'1010'
     AND ((DAYS(TO_DATE(SUBSTR(CHAR(F.DATE_ID),1,4),'YYYY'))-DAYS(TO_DATE(SUBSTR(CCRD15TO18(TRIM(SUBSTR(I.CUST_LONG_NO,4,20))) , 7,4),'YYYY'))) / 365)<50    
     GROUP BY M.SALE_CODE,M.THIRD_BRANCH_CODE
    """
    db.cursor.execute(sql_e.encode('utf-8'),stardate,stardate)
    row_e=db.cursor.fetchall()
    pri_ebank = {}
    for i in range(len(row_e)):
        pri_ebank[row_e[i][0]+row_e[i][2]]= row_e[i][1]
        u_sql0=u"""
        UPDATE REPORT_MANAGER_OTHER SET MB_PERCENT=? WHERE DATE_ID=? AND SALE_CODE=? AND ORG_CODE=?
        """
        db.cursor.execute(u_sql0,str(row_e[i][1]),stardate,row_e[i][0],row_e[i][2])
        db.conn.commit()
    return pri_ebank 

#公司类贷款客户有效网上银行绑定率
def man_pub_loan_ebank(db,stardate):
    sql_e = u"""
    SELECT M.SALE_CODE,ROUND(COUNT(DISTINCT CASE WHEN LEFT(C.CST_NO,2)='82'  THEN F.CST_NO END)*1.00/ DECODE(COUNT(DISTINCT CASE WHEN LEFT(F.CST_NO,2)='82'  THEN F.CST_NO END),0,1,COUNT(DISTINCT CASE WHEN LEFT(F.CST_NO,2)='82'THEN F.CST_NO END)) ,2),M.THIRD_BRANCH_CODE
    FROM F_BALANCE F 
    JOIN D_LOAN_ACCOUNT D ON F.ACCOUNT_ID=D.ID
    JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID
    JOIN D_CUST_INFO I ON F.CST_NO= I.CUST_NO
    LEFT JOIN (SELECT C.CST_NO FROM F_CONTRACT_STATUS F
    JOIN D_CUST_CONTRACT C ON C.ID=F.CONTRACT_ID
    WHERE F.DATE_ID=? AND F.STATUS IN ('正常','未激活','冻结') 
     AND C.BUSI_TYPE LIKE '企业网上银行'     AND C.OPEN_BRANCH_NO LIKE '966%' ) C ON F.CST_NO=C.CST_NO
     WHERE F.DATE_ID=? AND F.ACCT_TYPE='4' 
     GROUP BY M.SALE_CODE,M.THIRD_BRANCH_CODE
    """
    db.cursor.execute(sql_e.encode('utf-8'),stardate,stardate)
    row_e=db.cursor.fetchall()
    pub_loan= {}
    for i in range(len(row_e)):
        pub_loan[row_e[i][0]+row_e[i][2]]= row_e[i][1]
        u_sql0=u"""
        UPDATE REPORT_MANAGER_OTHER SET PUB_PERCENT=? WHERE DATE_ID=? AND SALE_CODE=? AND ORG_CODE=?
        """
        db.cursor.execute(u_sql0,str(row_e[i][1]),stardate,row_e[i][0],row_e[i][2])
        db.conn.commit()
    return pub_loan 

def man_ebank_sco_new(stardate,etldate):
    try:
        db = util.DBConnect()
        while stardate<=etldate:
            u_sql0=u"""
            UPDATE REPORT_MANAGER_OTHER SET MB_ADD_SCO=0,CB_ADD_SCO=0,POS_ADD_SCO=0,BAD_ADD_SCO=0,ETC_ADD_SCO=0,EPAY_ADD_SCO=0,FRAM_SCO=0,MB_PERCENT_SAL=0,PUB_PERCENT_SAL=0,ALL_SCO=0 WHERE DATE_ID=? 
            """
            db.cursor.execute(u_sql0,stardate)
            db.conn.commit()
            sql0=u"""SELECT LEFT(L_YEAREND_ID,4) FROM D_DATE WHERE ID=?"""
            db.cursor.execute(sql0,stardate)
            row0=db.cursor.fetchall()
            last_year = row0[0][0]
            #print last_year 
            pri_ebank = man_pri_loan_ebank(db,stardate)
            #print pri_ebank
            pub_loan = man_pri_loan_ebank(db,stardate)
            #print pub_loan 
            sql1="""
            SELECT R.DATE_ID,R.ORG_CODE,R.SALE_CODE,SUM((NVL(R.MB_THIS_NUM,0)-NVL(R1.MB_THIS_NUM,0))) AS 新增手机银行户数,NVL(P.TAR_SJ,0),
             SUM( NVL(R.CB_THIS_NUM,0)-NVL(R1.CB_THIS_NUM,0)) AS 新增企业网银,NVL(P.TAR_WY,0),
             SUM(NVL(R.POS_THIS_NUM,0)-R1.POS_THIS_NUM) AS 新拓展POS机,NVL(P.TAR_POS,0),
             SUM(NVL(RMC.BAD_ALL/1000000.0,0)) AS 新增丰收贷记卡逾期本金,
             SUM((NVL(ET.ETC_NUM,0))) AS 新增ETC指标得分,NVL(P.TAR_ETC,0),
             SUM((NVL(R.EPAY_THIS_NUM,0)-NVL(R1.EPAY_THIS_NUM,0))) AS 新增有效丰收E支付,NVL(P.TAR_EPAY,0),
             SUM((NVL(R.FARM_SERV_HIGH_NUM,0))) AS 助农服务点月活点指标达到60,SUM((NVL(R.FARM_SERVICE_LOW_NUM,0))) 
             FROM REPORT_MANAGER_OTHER  R
              JOIN ( SELECT DATE_ID, ORG_CODE,SALE_CODE,NVL((MB_THIS_NUM),0) AS MB_THIS_NUM ,NVL((CB_THIS_NUM),0) AS CB_THIS_NUM,NVL((EPAY_THIS_NUM),0) AS EPAY_THIS_NUM, 
                    NVL((ETC_THIS_NUM),0) AS ETC_THIS_NUM,NVL(POS_THIS_NUM,0) AS POS_THIS_NUM
               FROM REPORT_MANAGER_OTHER WHERE DATE_ID =(SELECT L_YEAREND_ID FROM D_DATE WHERE ID=?) 
               GROUP BY DATE_ID,ORG_CODE,SALE_CODE,MB_THIS_NUM,CB_THIS_NUM,EPAY_THIS_NUM,ETC_THIS_NUM,POS_THIS_NUM ) R1 ON R1.SALE_CODE=R.SALE_CODE AND R1.ORG_CODE=R.ORG_CODE
              JOIN P_EBANK_NUM   P ON R.ORG_CODE=P.THIRD_ORG_CODE AND R.SALE_CODE=P.MANAGER_CODE
              LEFT JOIN (SELECT A.TELLER_NO,(COUNT(A.CUST_NET_NO) - COUNT(B.CUST_NET_NO)) AS ETC_NUM  FROM ETC_DATA A LEFT JOIN ETC_DATA B  ON A.CUST_NET_NO=B.CUST_NET_NO 
                    AND LEFT(B.DATE_ID,4)=? WHERE LEFT(A.DATE_ID,4)=(SELECT YEAR FROM D_DATE WHERE ID=?)
                GROUP BY A.TELLER_NO) ET ON ET.TELLER_NO=R.SALE_CODE
              JOIN REPORT_MANAGER_CREDITCARD RMC ON RMC.SALE_CODE=R.SALE_CODE AND RMC.DATE_ID=R.DATE_ID
              WHERE 1=1 AND R.DATE_ID=?
              GROUP BY R.DATE_ID,R.ORG_CODE,R.SALE_CODE,P.TAR_SJ,P.TAR_WY,P.TAR_POS,RMC.BAD_ALL,P.TAR_ETC,P.TAR_EPAY  
            """
            db.cursor.execute(sql1,stardate,last_year,stardate,stardate)
            row=db.cursor.fetchall()
            #print row
            """参数"""
            ''' 取得手机银行 标准分，最高分，最低分'''
            sql2=u"""
            select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
            join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
            join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
            where t.TYPE_NAME='新增手机银行有效户数得分参数'
            """
            db.cursor.execute(sql2.encode('utf-8'),stardate)
            row2=db.cursor.fetchall()
            #print row2
            std_mb=max_mb=min_mb=0
            for i in row2:
                if i[0]=='标准分（分）':
                    std_mb=float(i[1])
                elif i[0]=='最高分（分）':
                    max_mb=float(i[1])
                elif i[0]=='最低分（分）':
                    min_mb=float(i[1])
            print "shouji",std_mb,max_mb,min_mb

            ''' 取得企业网银 标准分，最高分，最低分'''
            sql3=u"""
            select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
            join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
            join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
            where t.TYPE_NAME='新增企业网银有效户数得分参数'
            """
            db.cursor.execute(sql3.encode('utf-8'),stardate)
            row3=db.cursor.fetchall()
            #print row3
            std_wy=max_wy=min_wy=0
            for i in row3:
                if i[0]=='标准分':
                    std_wy=float(i[1])
                elif i[0]=='最高分':
                    max_wy=float(i[1])
                elif i[0]=='最低分':
                    min_wy=float(i[1])
            print std_wy,max_wy,min_wy

            ''' 取得pos机 标准分，最高分，最低分'''
            sql4=u"""
            select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
            join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
            join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
            where t.TYPE_NAME='新拓展pos机得分参数'
            """
            db.cursor.execute(sql4.encode('utf-8'),stardate)
            row4=db.cursor.fetchall()
            #print row4
            std_pos=max_pos=min_pos=0
            for i in row4:
                if i[0]=='标准分':
                    std_pos=float(i[1])
                elif i[0]=='最高分':
                    max_pos=float(i[1])
                elif i[0]=='最低分':
                    min_pos=float(i[1])
            print std_pos,max_pos,min_pos

            ''' 取得新增丰收贷记卡逾期本金得分 标准分，最高扣分'''
            sql5=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '新增丰收贷记卡逾期本金得分参数'
            """
            db.cursor.execute(sql5.encode('utf-8'),stardate)
            row5=db.cursor.fetchall()
            #print row5
            std_card=max_card=0
            for i in row5:
                if i[0]=='每万元扣分':
                    std_card=float(i[1])
                elif i[0]=='最高分':
                    max_card=float(i[1])
            print std_card,max_card

            ''' 取得新增ETC指标得分'''
            sql6=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '新增ETC得分参数'
            """
            db.cursor.execute(sql6.encode('utf-8'),stardate)
            row6=db.cursor.fetchall()
            #print row6
            std_etc=max_etc=min_etc=0
            for i in row6:
                if i[0]=='标准分':
                    std_etc=float(i[1])
                elif i[0]=='最高分':
                    max_etc=float(i[1])
                elif i[0]=='最低分':
                    min_etc=float(i[1])
            print std_etc,max_etc,min_etc

            ''' 取得新增有效e支付得分'''
            sql7=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '新增有效丰收e支付得分参数'
            """
            db.cursor.execute(sql7.encode('utf-8'),stardate)
            row7=db.cursor.fetchall()
            #print row7
            std_ep=max_ep=min_ep=0
            for i in row7:
                if i[0]=='标准分':
                    std_ep=float(i[1])
                elif i[0]=='最高分':
                    max_ep=float(i[1])
                elif i[0]=='最低分':
                    min_ep=float(i[1])
            print std_ep,max_ep,min_ep

            ''' 取得助农服务点月活点指标得分参数'''
            sql8=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '助农服务点月活点率得分参数'
            """
            db.cursor.execute(sql8.encode('utf-8'),stardate)
            row8=db.cursor.fetchall()
            #print row8
            std_zn=max_zn=min_zn=0
            for i in row8:
                if i[0]=='标准分':
                    std_zn=float(i[1])
                elif i[0]=='最高分':
                    max_zn=float(i[1])
                elif i[0]=='最低分':
                    min_zn=float(i[1])
            print std_zn,max_zn,min_zn


            ''' 取得助农服务点月活点指标限制参数'''
            sql9=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '助农服务点月活点指标限制参数'
            """
            db.cursor.execute(sql9.encode('utf-8'),stardate)
            row9=db.cursor.fetchall()
            #print row9
            plan=0
            for i in row9:
                if i[0]=='完成率标准(%)':
                    plan=float(i[1])
            print plan 

            ''' 取得对私类贷款客户有效手机银行绑定率参数'''
            sql10=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '对私类贷款客户有效手机银行绑定率参数'
            """
            db.cursor.execute(sql10.encode('utf-8'))
            row10=db.cursor.fetchall()
            #print row10
            std_pri=max_pri=min_pri=plan_pri=per_pri=0
            for i in row10:
                if i[0]=='标准分':
                    std_pri=float(i[1])
                elif i[0]=='最高分':
                    max_pri=float(i[1])
                elif i[0]=='最低分':
                    min_pri=float(i[1])
                elif i[0]=='贷款客户有效手机银行绑定率':
                    plan_pri=float(i[1])
                elif i[0]=='每超(减)百分点奖(扣)分':
                    per_pri=float(i[1])
            print std_pri,max_pri,min_pri,plan_pri,per_pri

            ''' 取得公司类贷款客户有效网上银行绑定率参数'''
            sql11=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '公司类贷款客户有效网上银行绑定率参数'
            """
            db.cursor.execute(sql11.encode('utf-8'))
            row11=db.cursor.fetchall()
            #print row11
            std_pub=max_pub=min_pub=plan_pub=per_pub=0
            for i in row11:
                if i[0]=='标准分':
                    std_pub=float(i[1])
                elif i[0]=='最高分':
                    max_pub=float(i[1])
                elif i[0]=='最低分':
                    min_pub=float(i[1])
                elif i[0]=='公司类贷款客户有效网上银行绑定率':
                    plan_pub=float(i[1])
                elif i[0]=='每超(减)百分点奖(扣)分':
                    per_pub=float(i[1])
            print std_pub,max_pub,min_pub,plan_pub,per_pub

            sql12=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '纯公司类贷款客户经理'
            ORDER BY D.DETAIL_VALUE DESC
            """
            db.cursor.execute(sql12.encode('utf-8'),etldate)
            row12=db.cursor.fetchall()
            manage_list=[]
            for i in row12:
                if i[0] == '客户经理':
                    manage_list.append(i[1])
            #print manage_list

            i=0
            resultrow=[]
            if(len(row)>0):
                while True:
                    h1=row[i][0]    #date_id
                    h2=row[i][1]    #ORG_CODE
                    h3=row[i][2]    #SALE_CODE
                    h4=row[i][3]    #MB_THIS_NUM手机银行
                    if row[i][4] == 0:       #TAR_SJ为空，则取0
                        score = 0
                    else:
                        score=(h4)/float(target_percent(row[i][4],stardate))*std_mb
                    if score>max_mb:score=max_mb
                    if score<min_mb:score=min_mb
                    qm1=int(score*100)          #手机银行得分
                    h5=row[i][5]
                    if row[i][6] == 0:
                        scorew= 0 
                    else:
                        scorew=(h5)/float(target_percent(row[i][6],stardate))*std_wy
                    if scorew>max_wy:scorew=max_wy
                    if scorew<min_wy:scorew=min_wy
                    qm2=int(scorew*100)          #企业网银得分

                    h6=row[i][7] 
                    if row[i][8] == 0:
                        scorep = 0 
                    else :
                        scorep=(h6)/float(target_percent(row[i][8],stardate))*std_pos
                    if scorep>max_pos:scorep=max_pos
                    if scorep<min_pos:scorep=min_pos
                    qm3=int(scorep*100)          #新拓展pos机得分
                    #print "**********",h3,h6,qm2,row[i][8]

                    h7=row[i][9]
                    scored = 0
                    if h7 == 0:
                        scored = 0
                    else:
                        scored = 0-h7*std_card
                    if scored<max_card:scored=max_card
                    qm4=int(scored*100)          #新增逾期丰收贷记卡逾期本金得分

                    h8=row[i][10]
                    if row[i][11] == 0:
                        scoree = 0 
                    else :
                        scoree = (h8)/float(target_percent(row[i][11],stardate))*std_etc
                    if scoree > max_etc:scoree=max_etc
                    if scoree < min_etc:scoree=min_etc
                    qm5=int(scoree*100)          #新增ETC指标得分

                    h9=row[i][12]
                    if row[i][13] == 0:
                        scorep = 0 
                    else :
                        scorep = (h9)/float(target_percent(row[i][13],stardate))*std_ep
                    if scorep > max_ep :scorep=max_ep
                    if scorep < min_ep :scorep=min_ep
                    qm6=int(scorep*100)         #新增有效丰收e支付得分
                    
                    h10=row[i][14]
                    h11=row[i][15]
                    if int(h11) !=  0:
                        #print h10,h11
                        scorzn = 10*((float(h10)/(float(h10)+float(h11))*100-plan))/100 + std_zn
                        #print scorzn,h10/h11,h3
                        #print h11,scorzn
                    else:
                        scorzn = 0 
                    if scorzn>max_zn:scorzn=max_zn
                    if scorzn<min_zn:scorzn=min_zn
                    #print h3,h10,h11,scorzn,std_zn,max_zn
                    qm7=int(scorzn*100)        #助农服务点月平均活点率得分
                    
                    mb_percent = pri_ebank.get((h3+h2),plan_pri/100.00)
                    scorsj = 100 * per_pri *(mb_percent - plan_pri/100.00) + std_pri
                    if scorsj>max_pri:scorsj=max_pri
                    if scorsj<min_pri:scorsj=min_pri
                    qm8=int(scorsj*100)        #对私类客户贷款有效手机银行绑定率
                    #print mb_percent,scorsj,max_pri,min_pri,h3+h2,qm8

                    qm9=0
                    if h3 in manage_list:
                        pu_percent = pub_loan.get((h3+h2),plan_pub/100.00)
                        scorpu = 100 * per_pub *(pu_percent - plan_pub/100.00) + std_pub
                        if scorpu>max_pub:scorpu=max_pub
                        if scorpu<min_pub:scorpu=min_pub
                        qm9=int(scorpu*100)     #公司类贷款客户有效网上银行绑定率
                        #print pu_percent,scorpu,max_pub,min_pub,h3+h2,qm9

                    qm_add = 0
                    sql_add = u"""
                    SELECT NVL(ADD_POINTS,0) FROM MAN_EBANK_ADD_POINTS WHERE KYEAR=? AND ORG_NO=? AND USER_NAME=?
                    """
                    db.cursor.execute(sql_add.encode('utf-8'),str(stardate)[0:4],h2,h3)
                    row_add=db.cursor.fetchall()
                    #print row_add
                    if len(row_add) == 1: 
                        qm_add = row_add[0]
                        #print qm_add
                    

                    qm10 = qm1 + qm2 + qm3 + qm4 + qm5 + qm7 + qm8 + qm9
                    resultrow.append((qm1,qm2,qm3,qm4,qm5,qm6,qm7,qm8,qm9,qm10,h1,h2,h3))
                    #print resultrow
                    i=i+1
                    if i>=len(row):
                        break
            ''' 更新报表'''
            u_sql=u"""
            UPDATE REPORT_MANAGER_OTHER SET MB_ADD_SCO=?,CB_ADD_SCO=?,POS_ADD_SCO=?,BAD_ADD_SCO=?,ETC_ADD_SCO=?,EPAY_ADD_SCO=?,FRAM_SCO=?,MB_PERCENT_SAL=?,PUB_PERCENT_SAL=?,ALL_SCO=?,FLAG=1 WHERE DATE_ID=? and ORG_CODE=? and SALE_CODE=? 
            """
            db.cursor.executemany(u_sql,resultrow)
            db.conn.commit()
            print stardate,"完成"
            stardate=int(util.daycalc(stardate,1))
    finally :
        db.closeDB()


if __name__=='__main__':
    arglen=len(sys.argv)
    print sys.argv 
    if arglen ==3:
        stardate=int(sys.argv[1])
        etldate=int(sys.argv[2])
        man_ebank_sco_new(stardate,etldate)
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
