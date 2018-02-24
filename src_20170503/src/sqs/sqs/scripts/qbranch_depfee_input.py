# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
"""
网点存款存量维护费手工录入
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['ORG_CODE','BE_YEAR']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT ORG_CODE, ORG_NAME, BE_YEAR, FEE, ID    FROM YDW.DEP_STOCK_MTF_INPUT WHERE INPUT_LEVEL='branch' %s"""%(filterstr)

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
        return ["机构号","机构名称","所属年份","存款存量维护费金额","操作"]

    @property
    def page_size(self):
        return 10
