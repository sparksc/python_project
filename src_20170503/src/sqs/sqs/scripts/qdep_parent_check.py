# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
"""
汇集户账户信息检查
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['ACCOUNT_NO']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select i.cust_long_no, i.cust_name, i.cust_address, i.cust_no, d.open_branch_code
            from d_account d 
            inner join d_cust_info i on i.cust_no=d.cst_no
            where d.account_class='汇集户' %s
            """%(filterstr)

        print sql
        print filterstr
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and d.account_no = ?"
                vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["客户号","客户姓名","地址信息","客户内码"]
#
#    @property
#    def page_size(self):
#        return 10
