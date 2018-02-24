# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
查询账户以及密码
"""

class Query(ObjectQuery):
 
    def prepare_object(self):
        self.filterlist = ['USER_NAME','NAME']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select u.USER_NAME,u.NAME,o.BRANCH_NAME,p.CREDENTIAL,u.ROLE_ID,f.FACTOR_ID,o.ROLE_ID from F_USER u
            join USER_BRANCH b on b.USER_ID=u.ROLE_ID
            join BRANCH o on o.ROLE_ID=b.BRANCH_ID
            join FACTOR f on f.USER_ID=u.ROLE_ID
            join PASSWORD p on p.FACTOR_ID=f.FACTOR_ID
            where 1=1 %s order by u.ROLE_ID
            """%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        print(sql)
        print(vlist)
        return self.translate(row,needtrans)
    def make_eq_filterstr(self):
        filterstr = ""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s like"%(k)+" '%'||"+"?"+"||'%'"
                vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["员工号","姓名","所属机构","操作"]
    @property
    def page_size(self):
        return 15
