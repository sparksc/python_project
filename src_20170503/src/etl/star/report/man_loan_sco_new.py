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
客户经理贷款得分
"""
#对得分进行折比例
def sco_percent(sco,etldate):
    """计算当前月份应该所占比例"""
    month = str(etldate)[4:6]
    sco_end = float(sco) * (float(month) / 12.0)
    return sco_end

#对计划数折比例
def target_percent(target,etldate):
    """计算任务当前月应该完成数"""
    month = str(etldate)[4:6]
    tar_end = float(target) * (float(month) / 12.0)
    return tar_end

def man_loan_sco_new(stardate,etldate):
    try:
        db = util.DBConnect()
        while stardate<=etldate:
            sql1="""
        SELECT R.DATE_ID,R.ORG_CODE,R.SALE_CODE,SUM((NVL(R.PRI_THIS_AVG,0)-NVL(R.PRI_LAST_AVG,0))+(NVL(R.PUB_THIS_AVG,0)-NVL(R.PUB_LAST_AVG,0))),SUM(NVL(P.AVE_TARGET,0)) AS 日均贷款增加额指标,
             SUM(NVL(R.BAD_BAL,0)-NVL(R1.BAD_BAL,0)) AS 四级不良贷款,
             SUM(NVL(ROUND(R.TWO_CARD_BY_EBANK*1.0/ R.TWO_CARD_ALL ,2),0)) AS 两卡贷款客户电子渠道办贷率,
             SUM(NVL(V.TIMES,0)-NVL(P.AV,0)) AS 驻勤工作,
             SUM(NVL(R.PRI_ADD_BAL,0)+NVL(R.PUB_ADD_BAL,0)),SUM((NVL(P.ES_P_BASE,0)+NVL(P.ES_P_TARGET,0))) AS 扩面工作,
             SUM(NVL(R.PRI_ADD_NUM,0)+NVL(R.PUB_ADD_NUM,0)) AS 扩面新增管贷户,
             SUM(ROUND(CASE R.MIN_NUM WHEN 0 THEN 0 ELSE R.MIN_CRD_NUM*1.0/ R.MIN_NUM END ,2)),SUM(NVL(P.CRE__H_TARGET,0))AS 小额信用贷户数占比,
             SUM(NVL(R.TWO_THSI_NUM,0)-NVL(R.TWO_LAST_NUM,0)),SUM(NVL(P.CARD_TARGET,0)) AS 丰收两卡合同新增户数指标
       FROM REPORT_MANAGER_LOAN R
            LEFT JOIN (SELECT ORG_CODE,SALE_CODE,PRI_THIS_AVG,PUB_THIS_AVG,BAD_BAL FROM REPORT_MANAGER_LOAN WHERE DATE_ID=(SELECT L_YEAREND_ID FROM D_DATE WHERE ID=?)) R1 ON R1.SALE_CODE=R.SALE_CODE
            LEFT JOIN P_LOAN_NUM P ON R.ORG_CODE=P.BRANCH_CODE AND R.SALE_CODE=P.MANAGER_CODE AND TRIM(P.BDYEAR)=LEFT(R.DATE_ID,4)
            LEFT JOIN VILLAGE_INPUT V ON V.ORG_CODE=R.ORG_CODE AND V.STAFF_CODE=R.SALE_CODE AND LEFT(V.DATE_ID,4)=LEFT(R.DATE_ID,4)
       WHERE 1=1 AND  R.DATE_ID=? ---AND R.ORG_CODE IN ('966130','966080')
            GROUP BY R.DATE_ID,R.ORG_CODE,R.SALE_CODE
            """
            db.cursor.execute(sql1,etldate,etldate)
            row=db.cursor.fetchall()
            #print row
            """参数"""
            ''' 取得 日均贷款增加额得分参数'''
            sql2=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '日均贷款增加额得分参数'
            """
            db.cursor.execute(sql2.encode('utf-8'),etldate)
            row2=db.cursor.fetchall()
            #print row2
            stdc_avg=maxc_avg=minc_avg=0
            for i in row2:
                if i[0]=='标准分（分）':
                    stdc_avg=float(i[1])
                elif i[0]=='最高分（分）':
                    maxc_avg=float(i[1])
                elif i[0]=='最低分（分）':
                    minc_avg=float(i[1])
            #print stdc_avg,maxc_avg,minc_avg

            ''' 取得日均贷款增加额限制参数'''
            sql3=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '日均贷款增加额限制参数'
            """                                     #日均贷款增加额限制参数
            db.cursor.execute(sql3.encode('utf-8'),etldate)
            row3=db.cursor.fetchall()
            #print row3
            zb=df=0
            for i in row3:
                if i[0]=='指标额（亿元）':
                    zb=float(i[1])
                if i[0]=='得分':
                    df=float(i[1])
            #print zb,df

            ''' 取得 资产管理质量得分参数'''
            sql4=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '资产管理质量得分参数'
            """                                     #
            db.cursor.execute(sql4.encode('utf-8'),etldate)
            row4=db.cursor.fetchall()
            #print row4
            stdc_zc=maxc_zc=minc_zc=0
            for i in row4:
                if i[0]=='标准分（分）':
                    stdc_zc=float(i[1])
                elif i[0]=='最高分（分）':
                    maxc_zc=float(i[1])
                elif i[0]=='最低分（分）':
                    minc_zc=float(i[1])
            #print stdc_zc,maxc_zc,minc_zc
            
            sql5=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '四级不良贷款加扣分参数'
            """
            db.cursor.execute(sql5.encode('utf-8'),etldate)
            row5=db.cursor.fetchall()
            #print row5
            zc=0
            for i in row5:
                if i[0]=='得分（分/万元）':
                    zc=float(i[1])

            sql6=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '两卡贷款客户电子渠道办贷率奖励分值参数'
            """
            db.cursor.execute(sql6.encode('utf-8'),etldate)
            row6=db.cursor.fetchall()
            #print row6
            stdc_lk=max_lk=min_lk=kou_lk=0
            for i in row6:
                if i[0]=='最高奖励分值（分）':
                    max_lk=float(i[1])
                if i[0]=='扣减（分/%）':
                    kou_lk=float(i[1])
                if i[0]=='办贷率(%)':
                    stdc_lk=float(i[1])
                if i[0]=='最低奖励分值（分）':
                    min_lk=float(i[1])
            #print stdc_lk,max_lk,min_lk,kou_lk

            sql7=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '驻勤（驻村）工作扣分参数'
            ORDER BY D.DETAIL_VALUE DESC
            """
            db.cursor.execute(sql7.encode('utf-8'),etldate)
            row7=db.cursor.fetchall()
            #print row7
            zq_lk=0
            for i in row7:
                if i[0] == '扣减（分/次）':
                    zq_lk = float(i[1])
            #print zq_lk

            sql8=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '扩面工作得分参数'
            ORDER BY D.DETAIL_VALUE DESC
            """
            db.cursor.execute(sql8.encode('utf-8'),etldate)
            row8=db.cursor.fetchall()
            #print row8
            stdc_km=max_km=min_km=0
            for i in row8:
                if i[0] == '标准分（分）':
                    stdc_km=float(i[1])
                if i[0] == '最高分（分）':
                    max_km=float(i[1])
                if i[0] == '最低分（分）':
                    min_km=float(i[1])
                if i[0] == '纯对公客户经理对公户数增加奖励分数':
                    cdghs=float(i[1])
                if i[0] == '非纯对公客户经理对公户数增加奖励分数':
                    fcdgfs=float(i[1])
            #print stdc_km,max_km,min_km,cdghs,fcdgfs

            sql9=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '扩面工作管贷户数限制参数'
            ORDER BY D.DETAIL_VALUE DESC
            """
            db.cursor.execute(sql9.encode('utf-8'),etldate)
            row9=db.cursor.fetchall()
            #print row9
            km_min=km_xz=0
            for i in row9:
                if i[0] == '最低分（分）':
                    km_min=float(i[1])
                if i[0] == '管贷户数限制（户）':
                    km_xz=float(i[1])
            #print km_xz,km_min

            sql10=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '小额信用贷款户数占比指标得分参数'
            ORDER BY D.DETAIL_VALUE DESC
            """
            db.cursor.execute(sql10.encode('utf-8'),etldate)
            row10=db.cursor.fetchall()
            stdc_xe=max_xe=min_xe=0
            for i in row10:
                if i[0] == '标准分（分）':
                    stdc_xe=float(i[1])
                if i[0] == '最高分（分）':
                    max_xe=float(i[1])
                if i[0] == '最低分（分）':
                    min_xe=float(i[1])
            #print stdc_xe,max_xe,min_xe
    
            sql11=u"""
            SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
            JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
            JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
            WHERE T.TYPE_NAME LIKE '丰收两卡合同新增户数得分参数'
            """
            db.cursor.execute(sql11.encode('utf-8'),etldate)
            row11=db.cursor.fetchall()
            stdc_ht=max_ht=min_ht=0
            for i in row11:
                if i[0] == '标准分（分）':
                    stdc_ht=float(i[1])
                if i[0] == '最高分（分）':
                    max_ht=float(i[1])
                if i[0] == '最低分（分）':
                    min_ht=float(i[1])
                if i[0] == '纯对公客户经理新增贷款奖励分数':
                    xzjl =float(i[1])
            #print stdc_ht,max_ht,min_ht

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


            needtrans ={}
            i=0
            resultrow=[]
            if(len(row)>0):
                while True:
                    h1=row[i][0]
                    """h2是机构号"""
                    h2=str(row[i][1])
                    h3=str(row[i][2])
                    """h3是员工号"""
                    h4=row[i][3]
                    if row[i][4] == 0:
                        score_avg = stdc_avg       #没有设置目标任务时取标准分
                    else:
                        score_avg=(h4)/float(row[i][4])*stdc_avg
                        #print h3,h4,row[i][4],score_avg,maxc_avg,minc_avg,h4/100000000000.00,zb
                    score_avg = sco_percent(score_avg,etldate) #对于是金额的都是采取先计算得分再对得分折
                    if score_avg>maxc_avg:score_avg=maxc_avg
                    if score_avg<minc_avg:score_avg=minc_avg
                    if h4/100000000000.00 > zb:
                        if score_avg<df:
                            score_avg=df
                    qm1=int(score_avg*100)                      #日均贷款增加额指标

                    h5=row[i][5]
                    if h5 == 0:
                        score_zc = stdc_zc 
                    else:
                        score_zc = float(stdc_zc) - h5/1000000.00 * zc
                    if score_zc > maxc_zc: score_zc = maxc_zc
                    if score_zc < minc_zc: score_zc = minc_zc
                    qm2 = int(score_zc*100)                 #资产质量管理
                    if h3 == '9660480':
                        print qm2,h5/1000000.0*zc,stdc_zc

                    h6=row[i][6]
                    score_lk = 10 * ( h6 - float(stdc_lk)/100.00) + 3
                    if score_lk > max_lk : score_lk = max_lk
                    if score_lk < min_lk : score_lk = min_lk
                    qm3 = int(score_lk*100)                 #两卡贷款客户电子渠道办贷率
                    #print h3,qm3,h6
                   
                    h7=int(row[i][7])
                    if h7 >= 0:
                        score_zq = 0 
                    elif h7 < 0 :
                        score_zq =  h7 * zq_lk
                    qm4=int(score_zq)*100                            #驻勤工作
                    #print qm4,h7 ,zq_lk 

                    h8=row[i][8]
                    if row[i][9] == 0:
                        score_km = stdc_km
                    else :
                        score_km = stdc_km * (h8/float(row[i][9]))
                    score_km = sco_percent(score_km,etldate) #对于是金额的都是采取先计算得分再对得分折
                    h9=row[i][10]
                    if h9 >= km_xz:  #旬均管贷户数达550户,最低得9分 ,550和9都是参数
                        if score_km < km_min:
                            score_km=km_min
                    sql_km = """
                    SELECT NVL(R.PUB_NUM,0)-NVL(R1.PUB_NUM,0) FROM REPORT_MANAGER_LOAN R
                    JOIN REPORT_MANAGER_LOAN R1 ON R.SALE_CODE=R1.SALE_CODE AND R1.DATE_ID=(SELECT L_YEAREND_ID FROM D_DATE WHERE ID=%s)
                    WHERE R.DATE_ID=%s AND R.SALE_CODE='%s'
                    """%(etldate,etldate,str(h3))
                    db.cursor.execute(sql_km)
                    row_km=db.cursor.fetchall()
                    if len(row_km) == 1:
                        add_num = row_km[0][0]
                        if int(add_num) < 0:
                            add_num = 0
                    else:
                        add_num = 0
                    #print "****",add_num
                    if h3 in manage_list:   #纯公司类客户经理该项计算规则
                        score_km = score_km + add_num * cdghs
                    else:
                        score_km = score_km + add_num * fcdgfs
                    if score_km > max_km:score_km=max_km
                    if score_km < min_km:score_km=min_km
                    qm5=int(score_km*100)                   #扩面工作
                    #print qm5

                    h10=row[i][11]
                    if row[i][12] == 0:
                        score_xe = stdc_xe
                    else :
                        score_xe = stdc_xe * (h10/(target_percent(row[i][12],etldate)/10000.00))
                    if score_xe>max_xe:score_xe=max_xe
                    if score_xe<min_xe:score_xe=min_xe
                    qm6=int(score_xe*100)               #小额信用贷款户数占比指标
                    #print qm6

                    h11=row[i][13]
                    if row[i][14] == 0:
                        score_ht = stdc_ht
                    else:
                        score_ht = stdc_ht * (h11 / (target_percent(row[i][14],etldate)/100.00) )
                    if h3 in manage_list and float(score_km) == float(max_km):   #纯公司类客户经理该项计算规则
                        sql_pubnum="""
                        SELECT NVL(PUB_NUM,0)-NVL(PUB_LAST_NUM,0) FROM REPORT_MANAGER_LOAN WHERE DATE_ID=? AND SALE_CODE=?
                        """
                        db.cursor.execute(sql_pubnum,etldate,h3)
                        row_pubnum=db.cursor.fetchall()
                        if len(row_pubnum) == 1:
                            add_pubnum = row_pubnum[0][0]
                            if int(add_pubnum) < 0:
                                add_pubnum = 0
                        else:
                            add_pubnum = 0
                        score_ht = score_ht + add_pubnum * xzjl
                    if score_ht>max_ht:score_ht=max_ht
                    if score_ht<min_ht:score_ht=min_ht
                    qm7=int(score_ht*100)              #丰收两卡合同新增户数指标
                    #print qm7

                    score_all = qm1 + qm2 + qm3 + qm4 + qm5 + qm6 + qm7
                    resultrow.append((qm1,qm2,qm3,qm4,qm5,qm6,qm7,score_all,h1,h2,h3))
                    #print resultrow
                    i=i+1
                    if i>=len(row):
                        break
                    #print resultrow
            ''' 更新报表'''
            u_sql=u"""
            UPDATE REPORT_MANAGER_LOAN SET AVG_LOAN_SCO=?,ZX_SCO=?,TWO_CRAD_SCO=?,VILLAGE_SCO=?,LOAN_SCO=?,MIN_CARD_SCO=?,TWO_CARD_ADD=?,ALL_SCO=?  WHERE DATE_ID=? and ORG_CODE=? and SALE_CODE=? 
            """
            db.cursor.executemany(u_sql,resultrow)
            db.conn.commit()
            print stardate,"完成"
            stardate=int(util.daycalc(stardate,1))
    finally :
        db.closeDB()

if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen ==3:
        stardate=int(sys.argv[1])
        etldate=int(sys.argv[2])
        man_loan_sco_new(stardate,etldate)
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
