# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
查询用户
"""

class Query(ObjectQuery):
 
    def prepare_object(self):
        self.filterlist = ['USER_NAME','NAME','DEPARTMENT','org','JOB','MANAGERTYPE']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select u.USER_NAME,u.NAME,u.BRANCH_NAME,u.DEPARTMENT,u.JOB,u.MANAGERTYPE,u.CREDENTIAL,u.ROLE_ID,u.FACTOR_ID,u.BRANCH_ID,u.ORG from V_STAFF_INFO u
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
                 if k == 'org':
                      vvv = self.dealfilterlist(v)
                      filterstr = filterstr +" and ORG in ( %s ) "%(vvv)
                 elif k == 'NAME':
                      filterstr = filterstr+" and name like"+" '%'||"+"?"+"||'%'"
                      vlist.append(v)
                 else :
                      filterstr = filterstr+" and %s = ?"%k
                      vlist.append(v)
                      
        return filterstr,vlist
    def column_header(self):
        return ["员工号","姓名","所属机构","部门","职务","类别","操作"]
    @property
    def page_size(self):
        return 15
