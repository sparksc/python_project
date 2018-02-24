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
        self.filterlist = ['ACCOUNT_NO','MANAGER_NO','HOOK_TYPE','TYP','SRC','STATUS','ORG_NO']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select distinct c.etl_date,d.branch_name,c.MANAGER_NO,s.name,c.account_no,a.cst_name,c.hook_type,c.percentage,c.start_date,c.end_date,c.status,c.id,c.manager_no
                from account_hook c
                left join branch d on d.branch_code=c.org_no
                left join f_user s on s.user_name=c.manager_no
                left join d_account a on a.account_no=c.account_no
                where c.HOOK_TYPE = ? and c.typ = '存款' %s order by id
                """%(filterstr)
	print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        vlist = [u"存贷挂钩"]
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and c.%s = ?"%k
                vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        #return ["维护日期","机构号","机构名","员工号","员工名","账号","类型","占比","认定方式","管理起始日期","管理结束日期","状态","操作"]
        return ["维护日期","机构","员工号","营销员工","账号","账号名称","营销类型","管理比例%","开始日期","结束日期","关系状态"]

    @property
    def page_size(self):
        return 10
