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
保证金查询页面 by cchen 2017-03-26
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
            select a.org_no,a.manager_no,a.percentage,a.status,a.account_no,b.cust_name,a.note,a.follow_cust,a.balance/100.00,a.add_avg_balance/100.00 from (
            select * from account_hook where typ='存款' and left(ACCOUNT_NO,2)='28' and PERCENTAGE=100 and length(MANAGER_NO)!=6 
            ) a ,d_cust_info b where a.cust_in_no=b.cust_no %s
            """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i[0:8])
            for j in i[8:]:
                if j is None:j=0
                j=self.amount_trans_dec(j)
                t.append(j)
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_NO in ( %s ) "%(vvv)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)

        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'SALE_CODE','ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return ["机构编号","员工编号","占比","状态","账户","客户名","地址信息","优先级","余额","账户日均"]

    def trans_dec(self,num):
        tmp = Decimal(num)/Decimal(100)
        tmp = '{:,}'.format(tmp)
        return tmp

    @property
    def page_size(self):
        return 15
