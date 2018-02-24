# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
客户经理贷款指标报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            SELECT DATE_ID, ORG_CODE, ORG_NAME, SALE_CODE, SALE_NAME, PRI_NUM, PUB_NUM, PRI_LAST_AVG, PUB_LAST_AVG, PRI_THIS_AVG-PRI_LAST_AVG, PUB_THIS_AVG-PUB_LAST_AVG, PUB_ADD_NUM, PRI_ADD_NUM, PRI_ADD_BAL, PUB_ADD_BAL,case MIN_NUM when 0 then 0 else MIN_CRD_NUM*1.0/ MIN_NUM end, case MIN_BAL when 0 then 0 else MIN_CRD_BAL*1.0/ MIN_BAL end, BAD_NUM, BAD_BAL,OUT_NUM,OUT_BAL,TWO_THSI_NUM-TWO_LAST_NUM,0,0 
            FROM YDW.REPORT_MANAGER_LOAN
            WHERE 1=1 %s 
            """%(filterstr)
#        暂时只展示表头
#        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        row = []
        print sql
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i)
            for j in [7,8,9,10,13,14,18,20]:
                if t[j] is None:t[j]=0
                t[j]=self.trans_dec(t[j])
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if k == 'login_teller_no':
                if self.deal_teller_query_auth(v) == True:
                    filterstr = filterstr+" and SALE_CODE = '%s'"%v
            elif k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False:
                    filterstr = filterstr+" and ORG_CODE in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        return filterstr,vlist

    def column_header(self):
        return ["统计日期","机构号","机构名称","员工号","员工名称","贷款模拟利润金额","分配贷款日均余额","不良分配责任贷款日均余额","增户扩面存量客户数","增户扩面增量客户数"]
    def trans_dec(self,num):
        tmp = Decimal(num)/Decimal(100)
        tmp = '{:,}'.format(tmp)
        return tmp
    @property
    def page_size(self):
        return 15

