# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
存款审批
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['ACCOUNT_NO','MANAGER_NO','TYP','STATUS']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select a.ID,ETL_DATE,ORG_NO,ORG0_NAME,MANAGER_NO,SALE_NAME,ACCOUNT_NO,TYP,PERCENTAGE,SRC,a.START_DATE,a.END_DATE,STATUS 
                from account_hook a
                left join D_ORG o on o.org0_code=a.org_no
                left join D_SALES_TEMP s on s.SALE_CODE=a.MANAGER_NO
                WHERE 1=1 %s
                ORDER BY ID"""%(filterstr)
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
        return ["编号","维护日期","机构号","机构名","员工号","员工名","账号","类型","分配比例","认定方式","管理起始日期","管理结束日期","状态"]

    @property
    def page_size(self):
        return 10
