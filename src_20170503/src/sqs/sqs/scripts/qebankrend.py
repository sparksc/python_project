# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
电子银行待认定
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['NOTE','CUST_NO','CUST_NAME','MANAGER_NO','TYP','SRC','ORG_NO','STATUS','hide']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
        select org_no,o.branch_name,c.cust_no,d.cust_name,note,c.cust_in_no,c.id
        from cust_hook c
        join branch o on o.branch_code=c.org_no
        join d_cust_info d on d.cust_no=c.cust_in_no
        where typ='电子银行' and c.status='待手工' %s
        """%(filterstr)
        print sql
        print vlist
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False :
                    filterstr = filterstr+" and c.org_no in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'ORG_NO':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and c.org_no in( %s ) "%(vvv)
                elif k == 'CUST_NO':
                    filterstr = filterstr + " and c.cust_no = ? "
                    vlist.append(v)
                elif k == 'hide':
                    filterstr = filterstr + " and c.hide = ? "
                    vlist.append(v)
                elif k == 'NOTE':
                    filterstr = filterstr + " and note like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                elif k == 'CUST_NAME':
                    filterstr = filterstr + " and CUST_NAME like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["机构号","机构名","客户号","客户名","地址信息","操作"]

    @property
    def page_size(self):
        return 10
