# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
更改主办客户经理
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['cust_no','org_no','typ']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select o.branch_code,o.branch_name,typ,i.cust_long_no,i.cust_name,percentage,d.user_name,d.name                                                                     
                from cust_hook c
                join d_cust_info i on i.cust_no=c.cust_in_no
                join branch o on o.branch_code=c.org_no
                join f_user d on d.user_name=c.manager_no
                where hook_type='管户' and left(cust_in_no,2)='82' and percentage<>100 and status in ('正常') %s
            """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if k == 'login_teller_no':
                if self.deal_teller_query_auth(v) == True:
                    filterstr = filterstr+" and c.manager_no = '%s'"%v
            elif k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False :
                    filterstr = filterstr+" and org_no in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org_no':
                    filterstr = filterstr +" and c.org_no = ? "
                    vlist.append(v)
                elif k == 'cust_no':
                    filterstr = filterstr + " and c.cust_no = ? "
                    vlist.append(v)
                elif k == 'typ':
                    filterstr = filterstr + " and c.typ = ? "
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["机构号","机构名","类型","客户号","客户名","占比(%)","主办客户经理员工号","主办客户经理姓名"]

    @property
    def page_size(self):
        return 10
