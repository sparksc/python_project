# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
"""
"""

class Query(ObjectQuery):
    def exp_str(self):
        return {"start_row":5,"start_col":1,"cols":6}

    def prepare_object(self):
        self.filterlist = ['DATE_ID','ORG_CODE','SALE_CODE']
        self.date_id=''
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        select date_id,sale_code,sale_name,org_code,org_name,mark,id from counter_reason where 1=1 %s order by date_id,org_code
        """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i)
            rowlist.append(t)
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'DATE_ID':
                    filterstr = filterstr+" and DATE_ID = %s"%(str(v)[:6])
                if k == 'ORG_CODE':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                if k == 'SALE_CODE':
                    filterstr = filterstr+" and SALE_CODE = ?"
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return[
        [{"name":"年月",'h':2},{"name":"员工号",'h':2},{"name":"员工名",'h':2},{"name":"机构号",'h':2},{"name":"机构名称",'h':2},{"name":"具体事件描述",'h':2}]
        ]
    @property
    def page_size(self):
        return 10
