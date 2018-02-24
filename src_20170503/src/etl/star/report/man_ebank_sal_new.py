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
客户经理电子银行佣金报表
"""
'''
nvl(sum(b.MB_THIS_NUM -a.mb_this_num),0), --手机银行有效户数
nvl(sum(b.CB_THIS_NUM -a.cb_this_num),0), --新增企业网银有效户数
nvl(sum(b.EPAY_THIS_NUM -a.epay_this_num),0),--新增有效丰收e支付
nvl(sum(b.ADD_HIGH_POS_NUM),0), --新增POS(高扣率)
nvl(sum(b.ADD_LOW_POS_NUM),0), --新增POS(低扣率)
nvl(sum(b.FARM_SERV_HIGH_NUM),0),--助农服务点月活点指标(达到60%以上)
nvl(sum(b.FARM_SERVICE_LOW_NUM),0)--助农服务点月活点指标(未达到60%以上)
'''
def man_ebank_sal(etldate):
    try :
        db = util.DBConnect()
        sql1="""
        select b.date_id,b.org_code,b.sale_code,
        (nvl(b.mb_this_num,0)-nvl(a.mb_this_num,0)),
        (nvl(b.cb_this_num,0)-nvl(a.cb_this_num,0)),
        (nvl(b.epay_this_num,0)-nvl(a.epay_this_num,0)),
        (nvl(b.ADD_HIGH_POS_NUM,0)-nvl(a.ADD_HIGH_POS_NUM,0)),
        (nvl(b.ADD_LOW_POS_NUM,0)-nvl(a.ADD_LOW_POS_NUM,0)),
        b.FARM_SERV_HIGH_NUM,
        b.FARM_SERVICE_LOW_NUM  
        from
        (select date_id, ORG_CODE,SALE_CODE,
        sum(nvl(mb_this_num,0)+nvl(PB_THIS_NUM,0)) as mb_this_num ,
        sum(nvl(cb_this_num,0)) as cb_this_num,
        sum(nvl(epay_this_num,0))as epay_this_num,
        sum(nvl(ADD_HIGH_POS_NUM,0))as ADD_HIGH_POS_NUM,
        sum(nvl(ADD_LOW_POS_NUM,0))as ADD_LOW_POS_NUM,
        sum(nvl(FARM_SERV_HIGH_NUM,0))/ count (1) as FARM_SERV_HIGH_NUM, --取的是这个月的总值,不是每天
        sum(nvl(FARM_SERVICE_LOW_NUM,0))/ count (1) as FARM_SERVICE_LOW_NUM
        from REPORT_MANAGER_OTHER where date_id =?
        group by date_id,org_code,sale_code )b
        left join 
        (select date_id, ORG_CODE,SALE_CODE,
        sum(nvl(mb_this_num,0)+nvl(PB_THIS_NUM,0)) as mb_this_num ,
        sum(nvl(cb_this_num,0)) as cb_this_num,
        sum(nvl(epay_this_num,0))as epay_this_num,
        sum(nvl(ADD_HIGH_POS_NUM,0))as ADD_HIGH_POS_NUM,
        sum(nvl(ADD_LOW_POS_NUM,0))as ADD_LOW_POS_NUM
        from REPORT_MANAGER_OTHER where date_id =(select L_monthend_ID from d_date where ID=%s)
        group by date_id,org_code,sale_code )a
        on b.org_code=a.org_code and b.sale_code=a.sale_code 
        """%(etldate)
        #print sql1
        db.cursor.execute(sql1,etldate)
        row=db.cursor.fetchall()
        #print row
       # row=[]
        #for i in row:
         #   t=list(i[0:3])
          #  for j in i[3:]:
           #     if j is None:j=0
            #    if j <0: j=0
             #   t.append(j)
          #  rowlist.append(t)

        '''参数'''
        '''新增手机银行参数'''
        sql2="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='新增手机银行有效户数计价参数' and h.HEADER_NAME='新增手机银行有效户数计价参数'
        """
        db.cursor.execute(sql2.encode('utf-8'))
        row2=db.cursor.fetchall()
        #print "row2",row2
        num_add_mobile=int(Decimal(row2[0][0])*100)
        #print "num_add_mobile",num_add_mobile 
        '''新增企业网银有效户数效酬参数'''
        sql3="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='新增企业网银有效户数计价参数' and h.HEADER_NAME='新增企业网银有效户数计价参数'
        """
        db.cursor.execute(sql3.encode('utf-8'))
        row3=db.cursor.fetchall()
        #print "row3",row3
        num_add_cb=int(Decimal(row3[0][0])*100)
        #print "num_add_cb",num_add_cb
        '''新增有效丰收e支付效酬'''
        sql4="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='新增有效丰收e支付计价参数' and h.HEADER_NAME='新增有效e支付效酬计价参数'
        """
        db.cursor.execute(sql4.encode('utf-8'))
        row4=db.cursor.fetchall()
        num_add_epay=int(Decimal(row4[0][0])*100)
        #print "row4",row4
        #print "num_add_epay",num_add_epay
        '''
         新增贷记卡效酬参数
        '''
        #sql5='''
        #select d.DETAIL_VALUE from T_PARA_TYPE t
        #join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        #join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        #where t.TYPE_NAME='新增贷记卡计价参数' and h.HEADER_NAME='新增贷记卡效酬计价参数'
        #'''
        #db.cursor.execute(sql5.encode('utf-8'))
        #row5=db.cursor.fetchall()
       # num_add_credit=int(Decimal(row5[0][0])*100)
       # print "row5",row5
        #print "num_add_credit",num_add_credit

        '''
        新增POS机(高扣率)
        '''
        sql6='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='新拓展POS机效酬计价参数' and h.HEADER_NAME='新拓展pos机1单价'
        '''
        db.cursor.execute(sql6.encode('utf-8'))
        row6=db.cursor.fetchall()
        num_high_pos=int(Decimal(row6[0][0])*100)
        #print "row6",row6
        #print "num_high_pos",num_high_pos
        '''
        新增POS机(抵扣率)
        '''
        sql7='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='新拓展POS机效酬计价参数' and h.HEADER_NAME='新拓展pos机2单价'
        '''
        db.cursor.execute(sql7.encode('utf-8'))
        row7=db.cursor.fetchall()
        num_low_pos=int(Decimal(row7[0][0])*100)
        #print "row7",row7
        #print "num_low_pos",num_low_pos
        
        '''
        助农服务点
        '''
        sql8='''
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='助农服务点月活点指标计价参数' and h.HEADER_NAME='助农-价格'
        '''
        db.cursor.execute(sql8.encode('utf-8'))
        row8=db.cursor.fetchall()
        farm_price=int(Decimal(row8[0][0])*100)
        #print "row8",row8
        #print "farm_price",farm_price
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
            feed_list.append(int(x[3])*num_add_mobile) ##除以100
            feed_list.append(int(x[4])*num_add_cb) ##除以100
            feed_list.append(int(x[5])*num_add_epay) ##除100
            feed_list.append(int(x[6])*num_high_pos) ##除100
            feed_list.append(int(x[7])*num_low_pos) ##除100
            if int(x[8])==0 and int(x[9])==0:
                pass
            elif (int(x[8])*1.0)/(int(x[8])+int(x[9]))>=0.6:
                x[9]=0
            else:
                pass
            feed_list.append(int(x[8])*farm_price-int(x[9])*farm_price)##除100
            feed_list=feed_list[3:]+feed_list[:3]
            num=num+1
            update_list.append(feed_list)
        print num,"条"
        '''
            更新报表
        '''
        u_sql="""
        update REPORT_MANAGER_OTHER set MB_ADD_NUM_SAL=?,CB_ADD_NUM_SAL=?,EPAY_ADD_NUM_SAL=? ,ADD_HIGH_POS_SAL=?,ADD_LOW_POS_SAL=?,FARM_SERV_SAL=? where date_id =? and org_code=? and sale_code=? 
        """
        db.cursor.executemany(u_sql,update_list)
        db.conn.commit()

        sql10="""
        SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
        JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
        JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
        WHERE T.TYPE_NAME LIKE '%客户经理新增福农卡效酬参数%'
        """
        db.cursor.execute(sql10.encode('utf-8'))
        row10=db.cursor.fetchall()
        #print row10
        std_fn=0
        for i in row10:
            if i[0]=='单价（元/张）':
                std_fn=float(i[1])
        #print std_fn,"客户经理新增福农卡效酬参数"

        sql11="""
        SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
        JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
        JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
        WHERE T.TYPE_NAME LIKE '%客户经理推荐人保公司办理车险业务效酬%'
        """
        db.cursor.execute(sql11.encode('utf-8'))
        row11=db.cursor.fetchall()
        #print row11
        std_rb=0
        for i in row11:
            if i[0]=='单价（元/张）':
                std_rb=float(i[1])
        #print std_rb,"客户经理推荐人保公司办理车险业务效酬"

        sql12="""
        SELECT H.HEADER_NAME,D.DETAIL_VALUE FROM T_PARA_TYPE T
        JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=T.ID
        JOIN T_PARA_DETAIL D ON D.PARA_HEADER_ID=H.ID
        WHERE T.TYPE_NAME LIKE '%新增丰收家（丰收购）效酬参数%'
        """
        db.cursor.execute(sql12.encode('utf-8'))
        row12=db.cursor.fetchall()
        #print row12
        std_one=std_two=0
        for i in row12:
            if i[0]=='一个平台上线单价（元/户）':
                std_one=float(i[1])
            if i[0]=='两个平台上线单价（元/户）':
                std_two=float(i[1])
        #print std_one,std_two,"新增丰收家（丰收购）效酬参数"
        sql13="""
        SELECT SYEAR,ORG_CODE,USER_CODE,ONLINE_HOME,ONLINE_BUY,ONLINE_TWO,COUNTS FROM ADDHARVEST  WHERE SYEAR= %s
        """%(int(str(etldate)[0:4]))
        db.cursor.execute(sql13)
        row13=db.cursor.fetchall()
        #print row13
        i=0
        resultrow1=[]
        if(len(row13)>0):
            while True:
                h1=etldate    #date_id
                h2=row13[i][1]    #ORG_CODE
                h3=row13[i][2]    #SALE_CODE
                h4=row13[i][3]    #丰收家上线人数
                h5=row13[i][4]    #丰收购上线人数
                h6=row13[i][5]    #两家上线人数
                h7=row13[i][6]    #推荐人保户数
                qm11=int(int(h4)*std_one*100)
                qm12=int(int(h5)*std_one*100)
                qm13=int(int(h6)*std_two*100)
                qm14=int(int(h7)*std_rb*100)
                qm15 = qm11 + qm12 +qm13  #新增丰收家（丰收购）效酬
                resultrow1.append((qm15,qm14,int(h1),h2,h3))
                i=i+1
                if i>=len(row13):
                    break
        ''' 更新报表'''
        u_sql1=u"""
        UPDATE REPORT_MANAGER_OTHER SET BUM_HOM_SAL=? ,PER_CAR_DANERSAL=?  WHERE DATE_ID=? and ORG_CODE=? and SALE_CODE=? 
        """
        #print resultrow1
        db.cursor.executemany(u_sql1,resultrow1)

        sql14=u"""
        SELECT COUNT(*), M.SALE_CODE FROM F_CREDIT_CARD_STATUS F  JOIN D_CREDIT_CARD D ON D.ID = F.CARD_ID  JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID
        JOIN F_USER F1 ON F1.USER_NAME = M.SALE_CODE  JOIN D_CUST_INFO I ON SUBSTR(I.CUST_LONG_NO,4,20) = F1.ID_NUMBER
        WHERE F.DATE_ID = %s AND F.STATUS NOT IN('持卡人请求关闭', '呆账核销', '呆账核销清户', '销卡代码', '新卡激活，旧卡失效')  AND D.PRODUCT IN ('0632','福农卡966')
        AND F.DUE_DATE >= (SELECT LEFT(L_YEAREND_ID,6) FROM D_DATE  WHERE ID=%s)  AND D.OPEN_DATE <=%s 
        GROUP BY F.DATE_ID, M.SALE_CODE
        """%(etldate,etldate,etldate)
        db.cursor.execute(sql14)
        row14=db.cursor.fetchall()
        #print row14
        i=0
        resultrow2=[]
        if(len(row14)>0):
            while True:
                h1=row14[i][0]
                h2=row14[i][1]
                qm16=int(int(h1)*std_rb*100)
                resultrow2.append((qm16,h2,etldate))
                i=i+1
                if i>=len(row14):
                    break
        u_sql2=u"""
        UPDATE REPORT_MANAGER_OTHER SET ADD_FUNON_SAL=?   WHERE  SALE_CODE=? AND  DATE_ID=? 
        """
        #print resultrow2
        db.cursor.executemany(u_sql2,resultrow2)

        
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


