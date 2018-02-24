# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
"""
柜员扣罚手工录入
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','ORG_CODE','SALE_CODE']
        self.date_id=''
        filterstr,vlist = self.make_eq_filterstr()
        sql_date='select seasonend_id from d_date where id=%s'%(self.date_id)
        row_date = self.engine.execute(sql_date.encode('utf-8'),vlist).fetchone()
        if int(self.date_id) != int(row_date[0]):
            return (u"未到月末,不能查看")
        sql ="""
        select date_id,org_code,ORG_NAME,ATM_NO,NOT_WORK_DAYS,id from report_branch_manch_hander where 1=1 %s order by DATE_ID,ORG_CODE
       
        """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i)
           # for k in [5,6]:
           #     if t[k] is None:
           #         t[k]=0
           #     else:
           #         t[k]=self.amount_trans_dec(t[k])
            rowlist.append(t)
        return self.translate(rowlist,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'DATE_ID':
                    filterstr = filterstr+" and %s = ?"%k
                    self.date_id=int(v)
                    vlist.append(v)
                if k == 'ORG_CODE':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                if k == 'SALE_CODE':
                    filterstr = filterstr+" and SALE_CODE = ?"
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["统计日期","机构号","机构名称","机具号","未正常运行的天数","操作"]

    @property
    def page_size(self):
        return 10
