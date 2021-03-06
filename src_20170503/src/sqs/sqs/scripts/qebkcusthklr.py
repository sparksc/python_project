# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
客户挂钩
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CUST_NO','MANAGER_NO','TYP','SRC','ORG_NO','STATUS']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT c.ORG_NO, d.ORG0_NAME,u.USER_NAME, u.NAME, c.CUST_NO, i.CUST_NAME, i.cust_address,c.STATUS, max(c.ID)
                 FROM YDW.CUST_HOOK c
                 JOIN D_ORG d on d.org0_code=c.org_no 
                 JOIN F_USER u on u.user_name=c.manager_no
                 JOIN D_CUST_INFO i on i.cust_no=c.cust_in_no
                 WHERE 1=1 and c.status in ('录入待审批') %s  
                 GROUP BY c.ORG_NO, d.ORG0_NAME,u.USER_NAME, u.NAME, c.CUST_NO, i.CUST_NAME, i.cust_address,c.STATUS
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
                filterstr = filterstr+" and c.%s = ?"%k
                vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["机构号","机构名","员工号","员工名","客户号","客户名","地址信息","状态","操作"]

    @property
    def page_size(self):
        return 10
