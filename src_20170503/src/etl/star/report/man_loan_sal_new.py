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
客户经理贷款佣金报表 除100000000.00
"""
'''
sum(nvl(PRI_LAST_STANDARD_NUM,0)) --对私户数上年年末 
sum(nvl(PUB_LAST_STANDARD_NUM,0)) --对公户数上年年末
sum(nvl(PRI_LAST_AVG,0))---对私管贷日均上年末
SUM(nvl(PUB_LAST_AVG,0)) ---对公管贷日均上年末
sum(nvl(round(b.pri_add_num),0)) ---对私增量户数
sum(nvl(round(b.pub_add_num),0)) -对公增量户数
sum(nvl((PRI_MONTH_AVG-PRI_LAST_AVG),0))-对私贷款日均增量
sum(nvl((PUB_MONTH_AVG-PUB_LAST_AVG),0))-对公贷款日均增量
sum(nvl(TWO_CARD_LOANRATE,0))-两卡贷款的户数
sum(nvl(PRI_ELEC_FILE_INFO,0))-对私电子档案
sum(nvl(PUB_ELEC_FILE_INFO,0))-对公电子档案
'''
def man_loan_sal(etldate):
    try :
        db = util.DBConnect()
        month_end_sql="""
        select month_end from D_DATE where ID=?
        """
        db.cursor.execute(month_end_sql,etldate)
        is_month_end=db.cursor.fetchall()
        print "aaaa",is_month_end
        if not bool(is_month_end):
            raise Exception(u"超出月末天数,请检查")
        elif is_month_end[0][0]=='Y':
            pass
        else:
            raise Exception(u"未到月末,无法执行")

        day_sql="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='管贷旬均天数选择' and h.HEADER_NAME in ('管贷旬均指标参数1(日)','管贷旬均指标参数2(日)','管贷旬均指标参数3(日)') order by int(d.DETAIL_VALUE)
        """
        db.cursor.execute(day_sql)
        day_row=db.cursor.fetchall()
        print day_row
        print type(day_row[0][0])
        if len(day_row)==3:
            day_row1=str(day_row[0][0]).zfill(2)
            day_row2=str(day_row[1][0]).zfill(2)
            day_row3=str(day_row[2][0]).zfill(2)
        else:
            raise Exception(u"旬均天数不对,请检查")

        month_sql='''
            select left(L_monthend_ID,6),left(id,6) from d_date where ID=?
        '''
        db.cursor.execute(month_sql,etldate)
        month=db.cursor.fetchall()    
        print month
        last_month=month[0][0]
        this_month=month[0][1]
        sql1="""
            select r.date_id,r.org_code,r.sale_code,
            sum(nvl(PRI_LAST_STANDARD_NUM,0)) as PRI_LAST_STANDARD_NUM,  
            sum(nvl(PUB_LAST_STANDARD_NUM,0)) as PUB_LAST_STANDARD_NUM,  
            sum(nvl(PRI_LAST_AVG,0)) as PRI_LAST_AVG ,  
            SUM(nvl(PUB_LAST_AVG,0)) as PUB_LAST_AVG,
            round(nvl(b.pri_add_num,0)) as pri_add_num,
            round(nvl(b.pub_add_num,0)) as pub_add_num,
            sum(nvl(PRI_MONTH_AVG,0)-nvl(PRI_LAST_AVG,0)) as PRI_add_MON_AVG, 
            sum(nvl(PUB_MONTH_AVG,0)-nvl(PUB_LAST_AVG,0))as PUB_add_MON_AVG,
            sum(case when (nvl(TWO_CARD_BY_EBANK,0)*1.0/nvl(TWO_CARD_ALL,1)) >=0.35 then TWO_CARD_BY_EBANK else 0 end) as TWO_CARD_LOANRATE ,
            sum(nvl(PRI_ELEC_FILE_INFO,0)) as PRI_ELEC_FILE_INFO,
            sum(nvl(PUB_ELEC_FILE_INFO,0)) as PUB_ELEC_FILE_INFO
            from report_manager_loan r
            left join
            (select  f.ORG_CODE,f.sale_code,(nvl(f.pri_this_add_num,0)-nvl(a.pri_last_add_num,0))/3 as pri_add_num,(nvl(f.pub_this_add_num,0)-nvl(a.pub_last_add_num,0))/3 as pub_add_num from 
            (select ORG_CODE, sale_code,sum(nvl(PRI_ADD_NUM,0)) as pri_this_add_num , sum(nvl(PUB_ADD_NUM,0)) as pub_this_add_num from REPORT_MANAGER_LOAN 
            where date_id in ('%s'||'%s','%s'||'%s','%s'||'%s') group by ORG_CODE,SALE_CODE  order by org_code)f 
            left join (select ORG_CODE,sale_code,sum(nvl(PRI_ADD_NUM,0)) as pri_last_add_num, sum(nvl(PUB_ADD_NUM,0)) as pub_last_add_num from REPORT_MANAGER_LOAN  
            where date_id in ('%s'||'%s','%s'||'%s','%s'||'%s') group by  ORG_CODE,SALE_CODE order by org_code)a
            on a.org_code=f.org_code and a.sale_code=f.sale_code )b
            on r.org_code=b.org_code and r.sale_code=b.sale_code 
            WHERE r.DATE_ID=?
            group by r.date_id,r.org_code,r.sale_code ,b.pri_add_num,b.pub_add_num order by r.org_code
        """%(this_month,day_row1,this_month,day_row2,this_month,day_row3,last_month,day_row1,last_month,day_row2,last_month,day_row3)
        db.cursor.execute(sql1,etldate)
        row=db.cursor.fetchall()
      #  rowlist=[]
      #  for i in row:
       #     t=list(i[0:3])
       #     for j in i[3:]:
       #         if j is None:j=0
        #        if j <0: j=0
         #       t.append(j)
         #   rowlist.append(t)
        print sql1
       # print rowlist

        '''参数'''
        '''取得管贷户数参数'''
        sql2="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='管贷户数计价参数' and h.HEADER_NAME='贷款管贷户数计价参数'
        """
        db.cursor.execute(sql2.encode('utf-8'))
        row2=db.cursor.fetchall()
        print "row2",row2
        num_price=int(Decimal(row2[0][0])*100000000)
        print "num_price",num_price 
        '''取管贷余额效酬参数'''
        sql3="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='管贷效酬计价参数' and h.HEADER_NAME='贷款管贷效酬计价参数'
        """
        db.cursor.execute(sql3.encode('utf-8'))
        row3=db.cursor.fetchall()
        print "row3",row3
        last_avg_price=int(Decimal(row3[0][0])*100)
        print "last_avg_price",last_avg_price
        '''取对私增户扩面效酬'''
        sql4="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='对私增户扩面效酬计价参数' and h.HEADER_NAME='贷款对私增户扩面效酬计价参数'
        """
        db.cursor.execute(sql4.encode('utf-8'))
        row4=db.cursor.fetchall()
        pri_add_price=int(Decimal(row4[0][0])*100000000)
        print "row4",row4
        print "pri_add_price",pri_add_price
        '''取对公增户扩面效酬'''
        sql5="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='对公增户扩面效酬计价参数' and h.HEADER_NAME='贷款对公增户扩面效酬计价参数'
         """

        db.cursor.execute(sql5.encode('utf-8'))
        row5=db.cursor.fetchall()
        print "row5",row5
        pub_add_price=int(Decimal(row5[0][0])*100000000)
        print "pub_add_price",pub_add_price
        """贷款日均增量效酬"""
        sql6="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='贷款日均增量效酬计价参数' and h.HEADER_NAME='贷款日均增量效酬计价参数'
        """
        db.cursor.execute(sql6.encode('utf-8'))
        row6=db.cursor.fetchall()
        print "row6",row6
        avg_add_price=int(Decimal(row6[0][0])*100)
        print "avg_add_price",avg_add_price
        """两卡贷款客户电子渠道效酬"""
        sql7='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='两卡贷款客户电子渠道办贷率计价参数' and h.HEADER_NAME='两卡单价'
        '''
        db.cursor.execute(sql7.encode('utf-8'))
        row7=db.cursor.fetchall()
        print "row7",row7
        two_card_price=int(Decimal(row7[0][0])*100000000)
        print "two_card_price",two_card_price
        """电子档案信息采集效酬"""
        sql8='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='电子档案信息采集计价参数' and h.HEADER_NAME='电子单价'
        '''
        db.cursor.execute(sql8.encode('utf-8'))
        row8=db.cursor.fetchall()
        print "row8",row8
        elec_info_price=int(Decimal(row8[0][0])*100000000)
        print "elec_info_price",elec_info_price
        '''对公贷款折合系数'''
        sql9='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='对公贷款户数折算参数' and h.HEADER_NAME='折合系数'
        '''
        db.cursor.execute(sql9.encode('utf-8'))
        row9=db.cursor.fetchall()
        print "row9",row9
        pub_to_pri_num=int(row9[0][0])
        print "pub_to_pri_num",pub_to_pri_num
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
            feed_list.append(int(x[3]*num_price+x[4]*pub_to_pri_num*num_price)) ##除以100000000
            feed_list.append(int(x[5]*last_avg_price+x[6]*last_avg_price)) ##除以100000000
            feed_list.append(int(x[7]*pri_add_price)) ##除100000000
            feed_list.append(int(x[8]*pub_add_price)) ##除以100000000
            feed_list.append(int(x[9]*avg_add_price+x[10]*avg_add_price)) ##除以100000000
            feed_list.append(int(x[11]*two_card_price)) ##除以100000000
            feed_list.append(int(x[12]*elec_info_price+x[13]*elec_info_price))##除以100000000
            feed_list=feed_list[3:]+feed_list[:3]
            num=num+1
            update_list.append(feed_list)
        print num,"条"
        '''
            更新报表
        '''
        u_sql="""
        update REPORT_MANAGER_LOAN set TOTAL_NUM_SAL=?,AVG_SAL=?,PRI_ADD_NUM_SAL=?
        ,PUB_ADD_NUM_SAL=?,ADD_AVG_ASL=?,TWO_CARD_LOANRATE_SAL=?,ELEC_FILE_INFO_SAL=? where date_id =? and org_code=?  and sale_code=? 
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
        man_loan_sal(etldate)
    else:
        print "please input python %s yyyyMMdd"%sys.argv[0]


