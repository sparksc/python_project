# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
信用卡录入
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['ACCOUNT_NO','MANAGER_NO','SRC','SUB_TYP','STATUS']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select c.etl_date,c.org_no,d.org0_name,c.manager_no,s.sale_name,c.account_no,c.sub_typ,c.src,c.start_date,c.end_date,c.status,c.id
                from account_hook c
                left join d_org d on d.org0_code=c.org_no
                left join d_sales_temp s on s.sale_code=c.manager_no
                where typ='信用卡' %s 
                order by id
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
        return ["维护日期","机构号","机构名","员工号","员工名","卡号","类型","认定方式","管理起始日期","管理结束日期","状态","操作"]

    @property
    def page_size(self):
        return 10
