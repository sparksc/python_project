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
        sql_date='select MONTHEND_ID from d_date where id=%s'%(self.date_id)
        row_date = self.engine.execute(sql_date.encode('utf-8'),vlist).fetchone()
        if int(self.date_id) != int(row_date[0]):
            return (u"未到月末,不能查看")
        sql ="""select date_id,org_code,org_name,assess_man_num ,max(ID) from report_manager_workquality_hander WHERE 1=1 and assess_man_num is not null %s   group by (date_id,org_code,org_name,assess_man_num)  order by org_code"""%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        rowlist=[]
#        for i in row:
#            t=list(i)
#            if t[5] is None:
#                t[5]=0
#            else:
#                t[5]=self.amount_trans_dec(t[5])
#            rowlist.append(t)
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            print k,v
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
        return ["统计日期","机构号","机构名称","参与考核人数","操作"]

    @property
    def page_size(self):
        return 10
