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
        filterstr,vlist = self.make_eq_filterstr()
        sql = """
            select manager_no, count(*), sum(balance)/100.00 from account_hook where %s status = '正常' group by manager_no
            """ %(filterstr)
        print sql
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
        for k,v in self.args.items():
            if k == 'login_teller_no':
                #if self.deal_teller_query_auth(v) == True:
                filterstr = filterstr+" manager_no = '%s' and "%v
            elif k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False :
                    filterstr = filterstr+" org_no in ( %s ) and"%bb

        return filterstr, vlist

    def column_header(self):
        return ["员工号","笔数","金额"]

    @property
    def page_size(self):
        return 10
