# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
流水号
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['account_no','MANAGER_NO','cust_no','cust_name']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT c.ORG_NO, d.BRANCH_NAME, c.manager_no, s.name, c.ACCOUNT_NO,u.cust_long_no,u.CUST_NAME, c.percentage,c.note,case when follow_cust='账号优先' then '流水号优先' else '客户号优先' end, c.ID 
                 FROM YDW.ACCOUNT_HOOK c
                 JOIN BRANCH d on d.branch_code=c.org_no 
                 JOIN F_USER s on s.user_name=c.manager_no
                 join d_cust_info u on u.cust_no=c.cust_in_no
                 WHERE typ='理财' and follow_cust='客户号优先' and c.status='正常' and name is not null %s ORDER BY ID"""%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if k == 'login_teller_no':
                if self.deal_teller_transfer_auth(v) == True:
                    filterstr = filterstr+" and c.manager_no = '%s'"%v
            elif k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False:
                    filterstr = filterstr+" and c.org_no in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'ORG_NO':
                    vvv = self.dealfilterlist(v)
                    if self.top_branch_no not in vvv:
                        filterstr = filterstr +" and c.org_no in( %s ) "%(vvv)
                elif k == 'account_no':
                    filterstr = filterstr + " and c.account_no = ? "
                    vlist.append(v)
                elif k == 'cust_no':
                    filterstr = filterstr + " and u.cust_long_no = ? " 
                    vlist.append(v)
                elif k == 'MANAGER_NO':
                    filterstr = filterstr + " and manager_no = ? "
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["机构号","机构名","员工号","员工名","流水号","客户号","客户名","占比(%)","地址信息","优先级"]

    @property
    def page_size(self):
        return 10
