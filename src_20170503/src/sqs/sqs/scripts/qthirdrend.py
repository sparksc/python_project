# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
第三方待认定
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CUST_NO','NOTE','ORG_NO','CUST_NAME','hide']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                SELECT a.START_DATE,a.ORG_NO,o.ORG0_NAME,a.CUST_NO,c.CUST_NAME,a.NOTE,a.ID
                FROM CUST_HOOK a
                JOIN D_CUST_INFO c ON c.cust_no=a.cust_in_no
                JOIN D_ORG o ON a.ORG_NO=o.ORG0_CODE
                WHERE a.TYP='第三方存管' and a.STATUS='待手工' %s
                ORDER BY a.ID DESC
                 """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False:
                    filterstr = filterstr+" and a.org_no in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'ORG_NO':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and a.org_no in( %s ) "%(vvv)
                elif k == 'CUST_NO':
                    filterstr = filterstr + " and a.cust_no = '%s'"%v                    
                elif k == 'CUST_NAME':
                    filterstr = filterstr + " and c.cust_name = '%s'"%v
                elif k == 'hide':
                    filterstr = filterstr + " and a.hide = ? "
                    vlist.append(v)
                elif k == 'NOTE':
                    filterstr = filterstr + " and a.note like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["日期","机构号","机构名","客户号","客户名","地址信息","操作"]

    @property
    def page_size(self):
        return 10
