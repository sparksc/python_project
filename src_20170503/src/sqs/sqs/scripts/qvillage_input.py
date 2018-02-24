# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
"""
驻勤（驻村）工作手工录入
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','ORG_CODE','STAFF_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT DATE_ID,ORG_CODE,ORG_NAME,STAFF_CODE,STAFF_NAME,TIMES,ID FROM VILLAGE_INPUT WHERE 1=1 %s ORDER BY DATE_ID,ORG_CODE,STAFF_CODE"""%(filterstr)
        print 'sql =',sql
        print 'vlist =',vlist
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'DATE_ID':
                    if len(v) == 8:
                        filterstr = filterstr+" and %s <= ?"%k
                    vlist.append(v)
                if k == 'ORG_CODE':
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
                if k == 'STAFF_CODE':
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["统计日期","机构号","机构名称","员工号","员工名称","驻勤（驻村）工作","操作"]

    @property
    def page_size(self):
        return 10
