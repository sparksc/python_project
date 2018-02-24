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
from etl.star.model.odsfile import *
     
condecimal = getcontext()
"""
中间业务----只能到月末才开始跑
"""
def mid_bus(stardate,etldate):
    try:
        oneday=datetime.now()
        db = util.DBConnect()
        print "mid_bus:开始"
        while stardate<=etldate:
            sql_end="""
            select monthend_id from d_date where id=%s
            """%(stardate)
            db.cursor.execute(sql_end)
            date_end_1=db.cursor.fetchone()
            date_end=date_end_1[0]
            print date_end
            sql0="""
            DELETE FROM  MID_BUSINESS WHERE DATE_ID=?
            """
            db.cursor.execute(sql0,int(stardate))
            db.conn.commit()
            sql="""
            insert into MID_BUSINESS(date_id,mid_key1,mid_key2,org_code,sale_code,mid_type,sign_date,state,action)values
            (?,?,?,?,?,?,?,?,?)
            """
            db.cursor.executemany(sql,load_teller_imbs(stardate))
            db.conn.commit()
            insert_sql="""
            insert into MID_BUSINESS(date_id,mid_key1,mid_key2,org_code,sale_code,mid_type,sign_date,state,action)
            select * from
            (
             select a.open_date, a.net_cst_no,a.cst_no,OPEN_BRANCH_NO ,a.manage_code ,a.mid_type ,a.open_date1,'1' ,'I'
             from 
             (select id,open_date,net_cst_no||'-' ||'shou' net_cst_no,cst_no,OPEN_BRANCH_NO ,manage_code ,'手机银行' mid_type,open_date open_date1 from D_CUST_CONTRACT where BUSI_TYPE = '手机银行' and OPEN_date=?
              and SUB_TYPE ='专业版' 
              union all
              select id,open_date,net_cst_no||'-'||'qyi' net_cst_no,cst_no,OPEN_BRANCH_NO ,manage_code ,'企业网上银行' mid_type ,open_date open_date1 from D_CUST_CONTRACT where BUSI_TYPE = '企业网上银行' and OPEN_date=?
              union all
              select id,open_date,net_cst_no||'-'||'geyin' net_cst_no,cst_no,OPEN_BRANCH_NO ,manage_code ,'个人网上银行' mid_type ,open_date open_date1  from D_CUST_CONTRACT where BUSI_TYPE = '个人网上银行' and OPEN_date=?
              and SUB_TYPE ='专业版')a
             inner join F_CONTRACT_STATUS f on a.id=f.CONTRACT_ID
             and f.DATE_ID =? and F.STATUS IN ('正常','暂时冻结','停用','冻结','未激活') ------------状态f.date_id只取月末
             union all
             select open_date,id_number||'-'||'katong',cst_no,OPEN_BRANCH_NO ,manage_code ,'支付宝卡通' ,open_date,'1' ,'I' from D_CUST_CONTRACT where BUSI_TYPE = '支付宝卡通' and OPEN_date=?
             union all
             select open_date,id_number||'-'||'kuaijie',cst_no,OPEN_BRANCH_NO ,manage_code ,'支付宝快捷支付' ,open_date,'1' ,'I' from D_CUST_CONTRACT where BUSI_TYPE = '支付宝快捷支付' and OPEN_date=?
            )

            """
            db.cursor.execute(insert_sql,[int(stardate),int(stardate),int(stardate),int(date_end),int(stardate),int(stardate)])
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
        mid_bus(stardate,etldate)
        print "mid_bus",stardate,etldate,"完成",datetime.now()-d1
    else:
        print "please input python %s yyyyMMdd yyyyMMdd"%sys.argv[0]
