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
客户经理信用卡业务绩效佣金报表 
"""
def com_card_sal(etldate):
    try:
        db=util.DBConnect()
        sql1="""
               select r.date_id,r.org_code,r.sale_code,
               ((nvl(r.this_num,0)-nvl(last_mon_num,0)) * 
               (select td.detail_value from t_para_detail td , T_PARA_TYPE tt ,T_PARA_HEADER th 
               where tt.type_key='XZDJK' and th.para_type_id=tt.id and td.PARA_ROW_ID=tt.id 
               and td.PARA_HEADER_ID=th.id and detail_key='price'))
               from REPORT_MANAGER_CREDITCARD r
               left join 
               ( select SALE_CODE,ORG_CODE,this_num last_mon_num from YDW.REPORT_MANAGER_CREDITCARD where date_id=(select l_monthend_id from d_date where id=%s))b
                on r.org_code=b.ORG_CODE and r.sale_code=b.sale_code
                 where r.date_id=%s
        """%(etldate,etldate)
        db.cursor.execute(sql1.encode('utf-8'))
        row1=db.cursor.fetchall()
        update_list=[]
       # rowlist=[]
        print row1
        #for i in row1:
         #   t=list(i[0:3])
          #  for j in i[3:]:
           #     if j is None:j=0
            #    if int(j) <0: j=0
             #   t.append(j)
           # rowlist.append(t)

        for i in row1:
            x = list(i)  #单位是元，不用再除100
            sal = x[3]
            x[3] =x[2]
            x[2] =x[1]
            x[1] =x[0]
            x[0] =long(sal)
            print x
            update_list.append(x)
        '''更新报表'''
        u_sql=u"""
        update REPORT_MANAGER_CREDITCARD set SALARY=? where DATE_ID=?and ORG_CODE=? and SALE_CODE=?
        """
        print update_list
        db.cursor.executemany(u_sql,update_list)
        db.conn.commit()
    finally:
        db.closeDB()

if __name__=='__main__':
    arglen=len(sys.argv)
    if arglen == 2:
        etldate=int(sys.argv[1])
        com_card_sal(etldate)
    else:
        print "please input python %s yyyyMMdd"%sys.argv[0]
