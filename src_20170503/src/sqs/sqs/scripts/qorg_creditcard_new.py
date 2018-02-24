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
机构信用卡指标
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        select date_id,org_code ,org_name,
        sum(nvl(BAD_BAL,0) )/100.0,
        round((sum(nvl(BAD_BAL,0) )/ (case when sum(nvl(ALL_BAL,0))=0 then 1.00 else  (sum(nvl(ALL_BAL,0))*1.00) end))*100,2),
        sum(nvl(THIS_NUM,0)), 
        sum(nvl(THIS_NUM,0)-nvl(LAST_NUM ,0)),
        sum(nvl(BAD_ALL,0))/ 100.00 
        from REPORT_MANAGER_CREDITCARD 
        where 1=1 %s
        group by DATE_ID,ORG_CODE,org_name order by ORG_CODE
            """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print sql
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i[0:3])
            for j in i[3:]:
                if j is None:j=0
                j=self.amount_trans_dec(j)
                t.append(j)
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            print k,v
            #if k == 'login_branch_no':
            #    bb = self.deal_branch_query_auth(v)
            #    if bb != False :
            #        filterstr = filterstr+" and ORG_CODE in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return ["统计日期","机构编号","机构名称",'不良透支金额',"不良率(%)","发卡量","新增贷记卡","新增丰收贷记卡逾期本金"]

    @property
    def page_size(self):
        return 15
