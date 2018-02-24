# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
"""
OCR系统差错率机构排名情况
"""

class Query(ObjectQuery):
    def exp_str(self):
        return {"start_row":5,"start_col":1,"cols":9}

    def prepare_object(self):
        self.filterlist = ['DATE_ID','ORG_CODE','SALE_CODE']
        self.date_id=''
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        select date_id,org_code,org_name,scan_bus_cnt,inform_cnt,adjust_cnt,total_cnt,rete_error,pai_rank,id from ocr_org_rate_error where 1=1 %s order by date_id,org_code
        """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i)
            for j in range(3,len(t)-2):
                if t[j] is None:t[j]=0
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
        [{"name":"年月",'h':2},{"name":"机构号",'h':2},{"name":"机构名称",'h':2},{"name":"扫描业务凭证",'h':2},{"name":"差错笔数",'w':3},{"name":"差错率",'h':2},{"name":"排名",'h':2}],
         [{"name": u"告知类",'h':1},{"name": u"整改类",'h':1},{"name": u"合计",'h':1}]
        ]
    @property
    def page_size(self):
        return 10
