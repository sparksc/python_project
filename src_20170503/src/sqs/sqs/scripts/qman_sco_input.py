# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config
"""
客户经理附加分报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SYEAR','SMOUTH','STAFF_CODE','STAFF_NAME','ORG_CODE','ORG_NAME','SCORE']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT SYEAR, SMOUTH, ORG_CODE, ORG_NAME,STAFF_CODE, STAFF_NAME, SCORE/100.00, ID FROM YDW.M_MANAGER_ADD_SCO WHERE TYP='得分' %s"""%(filterstr)

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
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'staff_code','ORG_CODE', None))
        return filterstr,vlist
    def column_header(self):
        return ["统计年份","统计月份","机构号","机构名称","员工号","员工名称","附加分","操作"]

    @property
    def page_size(self):
        return 10
