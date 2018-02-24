# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from utils import config
"""
国际业务归属
"""
class Query(ObjectQuery):
    def group_by(self):
        return [0],(7,8),{0:[1]}
    def cancal_merge(self):
        return True

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE','count','CORPNAME','CUST_IN_NO',"IS_OPEN_NEW_WH"]
        self.mon_date=''
        self.count=""
        filterstr,vlist = self.make_eq_filterstr()
        sql_ebills="""
        select * from 
        (
        select 
        ORG_CODE,
        ORG_NAME,
        MONTH,           --0
        cust_in_no,      --33 
        CORPNAME,          --3中文名称
        SALE_CODE,         --4
        SALE_NAME,             --5
        round(sum(nvl(EXBPAMT,0)/1000000.00),2)+           -- '出口议付金额' 6
        round(sum(nvl(EXAGENTAMT,0)/1000000.00),2)+         -- '出口托收金额' 7
        round(sum(nvl(EXCLEANAMT,0)/1000000.00),2)+         -- '出口光票托收金额'8
        round(sum(nvl(NTCLEANAMT,0)/1000000.00),2)+         -- '非贸易光盘托收金额'9
        round(sum(nvl(EXINREMITAMT,0)/1000000.00),2)+       -- '出口汇入汇款金额'11
        round(sum(nvl(NTINREMITAMT,0)/1000000.00),2)+       -- '非贸易汇入汇款金额'12
        round(sum(nvl(IMOUTREMTIAMT,0)/1000000.00),2)+      -- '进口汇出汇款金额'14
        round(sum(nvl(NTOUTREMITAMT,0)/1000000.00),2)+      -- '非贸易汇出汇款金额'15
        round(sum(nvl(IMLCAMT,0)/1000000.00),2)+            -- '进口开证金额'17
        round(sum(nvl(IMICAMT,0)/1000000.00),2)+            -- '进口代收金额'18
        round(sum(nvl(FIINREMITAMT,0)/1000000.00),2)+       -- '资本项下汇入汇款金额'19
        round(sum(nvl(FIOUTREMITAMT,0)/1000000.00),2)+      -- '资本项下汇出汇款金额'20
        round(sum(nvl(LGAMT,0)/1000000.00),2)+              -- '保函金额'21
        round(sum(nvl(IMLGAMT,0)/1000000.00),2) total_set,          -- '进口保函金额'22
 

        round(sum(nvl(USANCEAMT,0)/1000000.00),2)+ --远期24 
        round(sum(nvl(SIGHTAMT,0)/1000000.00),2)+ --即期 25
        round(sum(nvl(CROSSBORDERAMT,0)/1000000.00),2) total_cross,--跨境26


        --round(sum(nvl(MONTHAMT,0)/1000000.00),2),--外币存款折人民币月日均28
        --round(sum(nvl(DAYAMT,0)/1000000.00),2),--外币存款折人民币年日均29
        --round(sum(nvl(BALANCE,0)/1000000.00),2), ---外币存款折人民币余额30 
        IS_OPEN_NEW_WH --31
        from 
        ebills_hook
        where 1=1 %s 
        group by MONTH,ORG_CODE,ORG_NAME,CORPNAME,SALE_CODE,SALE_NAME,IS_OPEN_NEW_WH,cust_in_no)
        where total_set!=0 or total_cross!=0
        order by MONTH,ORG_CODE,sale_name
        """%(filterstr)
        print sql_ebills
        row_ori = self.engine.execute(sql_ebills.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row_ori:
            t=list(i[0:7])
            for j in i[7:len(i)-1]:
                if j is None:j=0
                j=self.amount_trans_dec(j)
                t.append(j)
            t.append(i[len(i)-1])
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            print k,v
            if v and k in self.filterlist:
                if k == 'DATE_ID':
                    filterstr = filterstr +" and  MONTH = %s "%(int(str(v)[:6]))
                elif k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                elif k == 'SALE_CODE':
                    filterstr = filterstr +" and SALE_CODE = '%s' "%v
                elif k=='count':
                    self.count='%s'%v
                elif k=='CORPNAME':
                    filterstr= filterstr +" and CORPNAME like '%%%s%%' "%v
                elif k=='CUST_IN_NO':
                    filterstr=filterstr+" and CUST_IN_NO = '%s' "%v
                elif k=="IS_OPEN_NEW_WH":
                    if v=="是":
                        filterstr=filterstr+" and IS_OPEN_NEW_WH = '%s' "%(v)
                    elif v=="否":
                        filterstr=filterstr+" and IS_OPEN_NEW_WH != '是' "
                    else:
                        pass

                else: 
                    pass
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],"SALE_CODE",'ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return [
        [{"name": u"机构编号",'h':2},{"name": u"机构名称",'h':2}, {"name": u"统计月份",'h':2},{"name": u"客户内码",'h':2},{"name": u"客户名称",'h':2},{"name":u"员工号",'h':2},{"name":u"员工姓名",'h':2},{"name":u"结算量合计值",'h':2},{"name":u"结售汇量合计",'h':2},{"name":u"是否新开有效外汇账户",'h':2}]
    ]

    @property
    def page_size(self):
        return 15
