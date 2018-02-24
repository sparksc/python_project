# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
存款 客户号
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CUST_NO','MANAGER_NO','ORG_NO','STATUS']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT c.start_date, c.ORG_NO, d.BRANCH_NAME, c.manager_no, s.name, c.CUST_NO, i.CUST_NAME, c.balance, c.percentage, NOTE, c.ID 
                 FROM YDW.CUST_HOOK c
                 LEFT JOIN BRANCH d on d.branch_code=c.org_no 
                 LEFT JOIN F_USER s on s.user_name=c.manager_no
                 LEFT JOIN D_CUST_INFO i on i.cust_long_no=c.cust_no
                 LEFT JOIN D_CUST_CONTRACT dc on dc.CST_NO=c.CUST_IN_NO
                 WHERE typ='存款' and status in ('正常','已审批') %s ORDER BY ID"""%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'ORG_NO':
                    vvv = self.dealfilterlist(v)
                    if self.top_branch_no not in vvv:
                        filterstr = filterstr +" and c.org_no in( %s ) "%(vvv)
                elif k == 'CUST_NO':
                    filterstr = filterstr + " and c.cust_no = ?  "
                    vlist.append(v)
                elif k == 'NOTE':
                    filterstr = filterstr + " and note like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                elif k == 'MANAGER_NO':
                    filterstr = filterstr + " and manager_no = ? "
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["管理开始日期","机构号","机构名","员工号","员工名","客户号","客户名","余额","占比(%)","地址信息"]

    @property
    def page_size(self):
        return 10
