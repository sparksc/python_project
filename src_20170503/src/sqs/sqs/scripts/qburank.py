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
    国际业务部全省排名手工维护
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SYEAR','srank','remarks']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            SELECT syear,srank,remarks,id FROM Burank
            WHERE 1=1 %s order by SYEAR desc,id
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
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'SALE_CODE','ORG_CODE', None))
        return filterstr,vlist
    def column_header(self):
        return ["年份","全省排名","备注","操作"]

    @property
    def page_size(self):
        return 10
