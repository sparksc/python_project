# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
我的工作台业绩查询
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID', 'org']
        filterstr,vlist = self.make_eq_filterstr()
        sql = """
            select status, count(*) from account_hook where status in ('待手工', '待审批', '录入待审批')  group by status 
            """
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i)
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)

    def make_eq_filterstr(self):
        filterstr = ""
        vlist = []
        from_date_id = 0
        end_date_id = 0
        for k,v in self.args.items():
            if k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False :
                    filterstr = filterstr+" A.ORG_NO in ( %s ) and"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" A.ORG_NO in ( %s ) and "%(vvv)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)

        return filterstr, vlist

    def column_header(self):
        return ["状态","笔数"]

    @property
    def page_size(self):
        return 10
