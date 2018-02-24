# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
正常客户挂钩
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['org_no', 'cust_no','manager_no','typ']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select a.id,org0_code,org0_name,sale_code,sale_name,cust_no,percentage,typ,a.start_date,a.end_date from cust_hook a  
                left join D_ORG o on o.org0_code=a.org_no
                left join D_SALES_TEMP s on s.sale_code=a.manager_no
                where status='正常' %s
                order by id desc
            """%(filterstr)
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
        return ["序号","机构号","机构名","员工号","员工名","客户号","分配比例","类型","挂钩起始日期","挂钩结束日期", "操作"]

    @property
    def page_size(self):
        return 15
