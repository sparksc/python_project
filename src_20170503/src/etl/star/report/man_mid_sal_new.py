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
reload(sys)
sys.setdefaultencoding('utf-8')
condecimal = getcontext()
"""
客户经理中间业务佣金报表
"""
'''
'''
def man_ebank_sal(etldate):
    try :
        db = util.DBConnect()
        sql1="""
        select a.date_id,a.org_code,a.sale_code,
        nvl(a.THIRD_DEPO_ADD_NUM,0)-nvl(b.THIRD_DEPO_ADD_NUM,0),
        nvl(a.THIS_ADD_ETC_NUM,0)-nvl(b.THIS_ADD_ETC_NUM,0)
        from      
        (select date_id, ORG_CODE,SALE_CODE,
        sum(nvl(THIRD_DEPO_ADD_NUM,0)) as THIRD_DEPO_ADD_NUM ,
        sum(nvl(ETC_THIS_NUM,0)) as THIS_ADD_ETC_NUM
        from REPORT_MANAGER_OTHER where date_id =?
        group by date_id,org_code,sale_code )a
        left join 
        (select date_id, ORG_CODE,SALE_CODE,
        sum(nvl(THIRD_DEPO_ADD_NUM,0)) as THIRD_DEPO_ADD_NUM,
        sum(nvl(ETC_THIS_NUM,0)) as THIS_ADD_ETC_NUM
        from REPORT_MANAGER_OTHER where date_id =(select L_monthend_ID from d_date where ID=%s)
        group by date_id,org_code,sale_code 
        )b
        on a.date_id=b.date_id and a.org_code=b.org_code and a.sale_code=b.sale_code
        """%(etldate)
        print sql1
        db.cursor.execute(sql1,etldate)
        row=db.cursor.fetchall()
        print row
      #  rowlist=[]
       # for i in row:
        #    t=list(i[0:3])
         #   for j in i[3:]:
          #      if j is None:j=0
           #     if j <0: j=0
            #    t.append(j)
           # rowlist.append(t)

        '''参数'''
        '''新增第三方存管'''
        sql2="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='股票第三方存管计价参数' and h.HEADER_NAME='单价（元/户）'
        """
        db.cursor.execute(sql2.encode('utf-8'))
        row2=db.cursor.fetchall()
        print "row2",row2
        num_add_third=int(Decimal(row2[0][0])*100)
        print "num_add_third",num_add_third
        '''新增ETC存管'''
        sql3="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='新增ETC计价参数' and h.HEADER_NAME='单价（元/户）'
        """
        db.cursor.execute(sql3.encode('utf-8'))
        row3=db.cursor.fetchall()
        print "row3",row3
        num_add_etc=int(Decimal(row3[0][0])*100)
        print "num_add_etc",num_add_etc
        '''开始计算佣金'''
        feed_list=[]
        update_list=[]
        num=0
        for i in row:
            x=list(i)
            feed_list=[]
            feed_list.append((x[0]))
            feed_list.append((x[1]))
            feed_list.append((x[2]))
            feed_list.append(int(x[3])*num_add_third) ##除以100
            feed_list.append(int(x[4])*num_add_etc) ##除以100
            feed_list=feed_list[3:]+feed_list[:3]
            num=num+1
            update_list.append(feed_list)
        print num,"条"
        '''
            更新报表
        '''
        u_sql="""
        update REPORT_MANAGER_OTHER set ADD_THIRD_DEPO_SAL=? ,ADD_ETC_NUM_SAL=? where date_id =? and org_code=? and sale_code=? 
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
        man_ebank_sal(etldate)
    else:
        print "please 输入 python %s yyyyMMdd(如20160630)"%sys.argv[0]


