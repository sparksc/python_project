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

#对得分进行折比例
def sco_percent(sco,etldate):
    """计算当前月份应该所占比例"""
    month = str(etldate)[4:6]
    sco_end = float(sco) * (float(month) / 12.0)
    return sco_end
"""
客户经理存款得分
"""
def man_dep_sco_new(stardate,etldate):
    try:
        db = util.DBConnect()
        while stardate<=etldate:
            sql1="""
            SELECT R.DATE_ID,R.ORG_CODE,R.SALE_CODE,SUM(R.THIS_AVG-NVL(R.LAST_AVG,0)),nvl(P.TARGET,0)
            FROM REPORT_MANAGER_DEP R
            JOIN P_DEP_NUM P ON R.ORG_CODE=P.THIRD_ORG_CODE AND R.SALE_CODE=P.MANAGER_CODE
            WHERE 1=1 AND  R.DATE_ID=?
            GROUP BY R.DATE_ID,R.ORG_CODE,R.SALE_CODE,R.SALE_NAME,P.TARGET
            """
            db.cursor.execute(sql1,stardate)
            row=db.cursor.fetchall()
            print row
            """参数"""
            ''' 取得 标准分，最高分，最低分'''
            sql4=u"""
            select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
            join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
            join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
            where t.TYPE_NAME='新增日均存款得分'
            """
            db.cursor.execute(sql4.encode('utf-8'),stardate)
            row4=db.cursor.fetchall()
            print row4
            stdc=maxc=minc=0
            for i in row4:
                if i[0]=='标准分':
                    stdc=int(i[1])
                elif i[0]=='最高分':
                    maxc=int(i[1])
                elif i[0]=='最低分':
                    minc=int(i[1])
            print stdc,maxc,minc
            needtrans ={}
            i=0
            resultrow=[]
            if(len(row)>0):
                while True:
                    h1=row[i][0]
                    """h3是机构号"""
                    h2=row[i][1]
                    h3=row[i][2]
                    """h4是员工号"""
                    h5=row[i][3]
                    if row[i][4] == 0:
                        score = maxc #没有设置目标任务时取最高分
                    else:
                        score=(h5)/float(row[i][4])*stdc
                        print row[i][4],score,h5
                    score = sco_percent(score,etldate)
                    print "****",score
                    if score>maxc:score=maxc
                    if score<minc:score=minc
                    qm1=int(score*100)
                    resultrow.append((qm1,h1,h2,h3))
                    print resultrow
                    i=i+1
                    if i>=len(row):
                        break
                    #print resultrow
            ''' 更新报表'''
            u_sql=u"""
            UPDATE REPORT_MANAGER_DEP SET DEP_SCORE=? WHERE DATE_ID=? and ORG_CODE=? and SALE_CODE=? 
            """
            db.cursor.executemany(u_sql,resultrow)
            db.conn.commit()
            print stardate,"完成"
            stardate=int(util.daycalc(stardate,1))
    finally :
        db.closeDB()

if __name__=='__main__':
    arglen=len(sys.argv)
    print arglen
    if arglen ==3:
        stardate=int(sys.argv[1])
        etldate=int(sys.argv[2])
        man_dep_sco_new(stardate,etldate)
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
