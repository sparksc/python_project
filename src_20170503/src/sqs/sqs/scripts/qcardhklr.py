# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
账户挂钩
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['ACCOUNT_NO','MANAGER_NO','TYP','SRC','STATUS','ORG_NO','FOLLOW_CUST','SUB_TYP']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select c.etl_date,c.org_no,d.branch_name,c.manager_no,s.name,c.account_no,c.percentage,c.status,c.src,c.id
                from account_hook c
                left join branch d on d.branch_code=c.org_no
                left join f_user s on s.user_name=c.manager_no
                where 1=1 and status in ('正常') %s  order by id
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
        return filterstr,vlist
    def column_header(self):
        return ["日期","机构号","机构名","员工号","员工名","卡号","占比(%)","状态","是否补录","操作"]

    @property
    def page_size(self):
        return 10
