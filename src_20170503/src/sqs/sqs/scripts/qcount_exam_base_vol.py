# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
"""
业务量考核
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','ORG_CODE','SALE_CODE']
        self.date_id=''
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        select date_id,org_code,org_name,asscount_cnt,special_cnt,comcount_cnt,discount_cnt, mark,id from counter_exam_vol where 1=1 %s order by date_id,org_code
        """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i)
            if t[3] is None:
                t[3]=0
            if t[4] is None:
                t[4]=0
            if t[5] is None:
                t[5]=0
            if t[6] is None:
                t[6]=0
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
        return ["年月","机构号",'机构名','助理会计','特殊人员作管理岗统计人数','综合柜员','派遣柜员','备注',"操作"]

    @property
    def page_size(self):
        return 10
