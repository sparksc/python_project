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
客户经理存款佣金报表  记住除以100000000.00
LAST_AVG 存款存量含理财
MONTH_AVG 月日均含理财
"""
def man_dep_sal(etldate):
    try :
        db = util.DBConnect()
        sql1="""
        SELECT DATE_ID,ORG_CODE,SALE_CODE, SUM(nvl(LAST_AVG,0)),SUM(nvl(MONTH_AVG,0)-nvl(LAST_AVG,0))
        FROM YDW.REPORT_MANAGER_DEP
        join V_STAFF_INFO on SALE_CODE= USER_NAME
        WHERE DATE_ID = ?
        GROUP BY DATE_ID,ORG_CODE,SALE_CODE
        """
        db.cursor.execute(sql1,etldate)
        row=db.cursor.fetchall()
        #rowlist=[]
        #print row
        #for i in row:
           # t=list(i[0:3])
            #for j in i[3:]:
             #   if j is None:j=0
              #  if j <0: j=0
               # t.append(j)
           # rowlist.append(t)
        #print row
        """参数"""
        ''' 取得 非客户经理存量日均存款计价参数'''
        sql2=u"""
            select d.DETAIL_VALUE from T_PARA_TYPE t
            join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
            join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
            where TYPE_NAME='非客户经理存量日均存款计价参数' and HEADER_NAME='存量日均存款计价参数'
            """
        db.cursor.execute(sql2.encode('utf-8')) 
        row2=db.cursor.fetchall()
        last_price=int(Decimal(row2[0][0])*100)
        print last_price
        ''' 取得 新增日均存款计价参数'''
        sql3=u"""
            select d.DETAIL_VALUE from T_PARA_TYPE t
            join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
            join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
            where TYPE_NAME='新增日均存款计价参数' and HEADER_NAME='新增日均存款计价参数'
            """
        db.cursor.execute(sql3.encode('utf-8'))
        row3=db.cursor.fetchall()
        add_price=int(Decimal(row3[0][0])*100)
        print add_price
        ''' 取得 客户经理存款存量维护费'''
        sql4=u"""
        SELECT ORG_CODE,STAFF_CODE, FEE  FROM YDW.DEP_STOCK_MTF_INPUT 
        WHERE INPUT_LEVEL='manager' and BE_YEAR=(
        select YEAR-1 from D_DATE where ID= ?)
        """
        db.cursor.execute(sql4,etldate)
        row4=db.cursor.fetchall()
        '''开始计算佣金'''
        feedict={}
        for i in row4:
            feedict[(i[0],i[1])]=i[2]
        update_list=[]
        for i in row:
            x=list(i)
            key=(x[1],x[2])
            if key in feedict:              #除100000000
                x[3]=feedict.get(key)*1000000
            else: 
                x[3]= x[3]*last_price
            x[4]=x[4]*add_price    
            x=x[3:]+x[:3]
            update_list.append(x)
        ''' 更新报表'''
        u_sql=u"""
        update REPORT_MANAGER_DEP set TRY_LAST_AVG_SAL=?,TRY_ADD_AVG_SAL=? where DATE_ID=? and ORG_CODE=? and SALE_CODE=?
        """
        db.cursor.executemany(u_sql,update_list)
        db.conn.commit()
    finally :
        db.closeDB()

if __name__=='__main__':
    arglen=len(sys.argv)
    print arglen
    if arglen ==2:
        etldate=int(sys.argv[1])
        man_dep_sal(etldate)
    else:
        print "please input python %s yyyyMMdd"%sys.argv[0]


