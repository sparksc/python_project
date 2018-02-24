# -*- coding:utf-8 -*-

from decimal import Decimal
from objectquery import ObjectQuery
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
"""
存款帐号详情
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SALE_CODE','ORG','CUST_IN_NO','TYP']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
            select a.ACCOUNT_NO,a.PERCENTAGE,a.org_no, o.branch_name, nvl(a.BALANCE/100.00,0) bal,a.status 
            from account_hook a
            join branch o on o.branch_code=a.org_no
            where   a.status='录入待审批' and a.follow_cust='客户号优先' %s
            """%(filterstr)
        print sql
        print vlist
        row = self.engine.execute(sql,vlist).fetchall()
        row = list(row)
        for i in range(0,len(row)):
            row[i] = list(row[i])
            row[i][4] = self.trans_dec(('%.2f' % row[i][4]))

        needtrans = {}
        return self.translate(row,needtrans)
    
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'CUST_IN_NO':
                    filterstr = filterstr + " and a.cust_in_no = ? "
                    vlist.append(v)
                if k == 'ORG':
                    filterstr = filterstr + " and o.branch_code = ? "
                    vlist.append(v)
                if k == 'SALE_CODE':
                    filterstr = filterstr + " and a.manager_no = ? "
                    vlist.append(v)
                if k == 'TYP':
                    filterstr = filterstr + " and a.typ = ? "
                    vlist.append(v) 

        return filterstr,vlist


    def column_header(self):
        return ["账户","占比(%)", "机构号","机构名","余额","状态"]

    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        tmp = '{:,}'.format(tmp)
        return tmp
    @property
    def page_size(self):
        return 20
