# -*- coding:utf-8 -*-

from decimal import Decimal
from objectquery import ObjectQuery
"""
获得存款客户号下
待手工认定的客户号优先的存款帐号
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['cust_no','date_id','org_no']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
                select a.account_no
                from F_BALANCE f
                join d_account c on c.id=f.account_id
                join account_hook a on a.ACCOUNT_NO=c.account_no
                join cust_hook t on t.CUST_IN_NO=f.CST_NO
                join d_org o on o.ID=f.ORG_ID
                where f.ACCT_TYPE=1 and a.status='待手工' and date_id=20150103 %s
                """%(filterstr)
        print sql
        print vlist
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans = {}
        return self.translate(row,needtrans)
    
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'cust_no':
                    filterstr = filterstr + " and t.cust_no = ? "
                    vlist.append(v)
                if k == 'org_no':
                    filterstr = filterstr + " and o.org0_code = ? "
                    vlist.append(v)
        return filterstr,vlist


    def column_header(self):
        return [" "]

    @property
    def page_size(self):
        return 20
