# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
客户挂钩审批
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CUST_NO','MANAGER_NO','TYP','STATUS']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT ID,ETL_DATE, MANAGER_NO, CUST_NO, ORG_NO, PERCENTAGE, START_DATE, END_DATE, TYP,SRC,STATUS FROM YDW.CUST_HOOK WHERE 1=1 %s ORDER BY ID"""%(filterstr)
        print sql 
        print vlist 
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
        return ["编号","维护日期","员工工号","客户号","机构编号","分配比例","管理起始日期","管理结束日期","类型","自动认定","状态"]

    @property
    def page_size(self):
        return 10
