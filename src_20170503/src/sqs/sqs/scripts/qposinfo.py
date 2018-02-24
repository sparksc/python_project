# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
POS录入查询POS信息
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['merchant_no', 'pos_no', 'org_no']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT install_date, org_no, merchant_no, merchant_name, pos_no, typ, merchant_addr from D_POS  d WHERE d.status = '正常' %s
                 """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                 filterstr = filterstr+" and %s = ?"%k
                 vlist.append(v)
        return filterstr,vlist

    def column_header(self):
        return ["日期","机构号","商户号", "商户名", "终端号", "类型","地址信息"]

    @property
    def page_size(self):
        return 10
