# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
"""
OCR系统差错率柜员排名情况
"""

class Query(ObjectQuery):
    def exp_str(self):
        return {"start_row":5,"start_col":1,"cols":13}

    def prepare_object(self):
        self.filterlist = ['DATE_ID','ORG_CODE','SALE_CODE']
        self.date_id=''
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        select date_id,org_code,org_name,sale_code,sale_name,long_cny,long_cnt,short_cny,short_cnt,together_cny,together_cnt,false_cny,false_cnt,id from cash_error_rate where 1=1 %s order by date_id,org_code
        """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i)
            for j in range(5,len(t)):
                if t[j] is None:t[j]=0
            rowlist.append(t)
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'DATE_ID':
                    filterstr = filterstr+" and left(DATE_ID,6) = %s"%(str(v)[:6])
                if k == 'ORG_CODE':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                if k == 'SALE_CODE':
                    filterstr = filterstr+" and SALE_CODE = ?"
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return[
        [{"name":"日期",'h':2},{"name":"机构号",'h':2},{"name":"机构名称",'h':2},{"name":"员工号",'h':2},{"name":"员工名",'h':2},{"name":"长款",'w':2},{"name":"短款",'w':2},{"name":"拼凑",'w':2},{"name":"假币",'w':2}],
         [{"name": u"长款面额",'h':1},{"name": u"长款张数",'h':1},{"name": u"短款面额",'h':1},{"name": u"短款张数",'h':1},{"name": u"拼凑面额",'h':1},{"name": u"拼凑张数",'h':1},{"name": u"假币面额",'h':1},{"name": u"假币张数",'h':1}]
        ]
    @property
    def page_size(self):
        return 10
