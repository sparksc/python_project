# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
机具挂钩
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CUST_NO','MANAGER_NO','TYP','SRC','ORG_NO','STATUS']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT c.ORG_NO, d.BRANCH_NAME,s.user_name, s.NAME, c.CUST_NO, i.merchant_NAME,i.merchant_addr, c.STATUS, c.ID 
                 FROM YDW.CUST_HOOK c
                 JOIN branch d on d.branch_code=c.org_no 
                 JOIN f_user s on s.user_name=c.manager_no
                 JOIN D_POS i on i.merchant_no = c.cust_no and i.pos_no = c.cust_in_no
                 WHERE 1=1 and c.status in ('录入待审批') %s ORDER BY ID"""%(filterstr)
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
        return ["机构号","机构名","员工号","员工名","商户号","商户名","地址信息","状态","操作"]    #为了方便复用,表头由js传入

    @property
    def page_size(self):
        return 10
