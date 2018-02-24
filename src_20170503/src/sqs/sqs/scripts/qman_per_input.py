# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
"""
客户经理附加绩效佣金报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SYEAR','SMOUTH','STAFF_CODE','STAFF_NAME','ORG_CODE','ORG_NAME','SCORE']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT SYEAR, SMOUTH, ORG_CODE, ORG_NAME, STAFF_CODE, STAFF_NAME, SCORE/100.00, ID FROM YDW.M_MANAGER_ADD_SCO WHERE TYP='佣金' %s"""%(filterstr)

        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i)
            if t[6] is None:t[6]=0
            t[6]=self.amount_trans_dec(t[6])
            rowlist.append(t)
        return self.translate(rowlist,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ?"%k
                vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["统计年份","统计月份","机构号","机构名称","员工号","员工名称","附加效酬","操作"]

    @property
    def page_size(self):
        return 10
