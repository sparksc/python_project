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
        self.filterlist = ['CUST_NO', 'CUST_IN_NO', 'MANAGER_NO','TYP','SRC','ORG_NO','STATUS']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT c.id, c.ORG_NO, d.ORG0_NAME,s.user_name, s.NAME, c.CUST_NO, i.addr, c.PERCENTAGE,c.STATUS
                 FROM YDW.CUST_HOOK c
                 LEFT JOIN D_ORG d on d.org0_code=c.org_no 
                 LEFT JOIN f_user s on s.user_name=c.manager_no
                 LEFT JOIN D_ATM i on i.atm_no = c.cust_in_no
                 WHERE c.typ = '机具' and c.status = '待手工' %s ORDER BY ID"""%(filterstr)
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
        return ["序号", "机构号","机构名","员工号","员工名","终端号","地址信息","比例(%)","状态", "操作"]

    @property
    def page_size(self):
        return 10
