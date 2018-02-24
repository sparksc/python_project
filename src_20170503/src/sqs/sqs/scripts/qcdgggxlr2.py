# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
存贷挂钩关系录入
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['FJDXBH']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""select b.branch_name,fjdxbh,dxmc,gldxbh,f.name,glrq1,glrq2,dk_type from T_ZJC_GSGX_DK a inner join BRANCH b on b.branch_code=a.jgbh inner join STAFF_RELATION s on s.staff_cms_code = a.gldxbh inner join F_USER f on f.user_name = s.staff_code where 1=1 %s order by para_id"""%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={7:'DKTYPE'}
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
        return ["机构","客户内码","客户姓名","员工信贷号","员工姓名","管理开始日期","管理结束日期","挂钩类型"]
#
#    @property
#    def page_size(self):
#        return 10
