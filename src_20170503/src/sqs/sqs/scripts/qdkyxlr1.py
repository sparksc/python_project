# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
贷款营销录入
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DEBIT_NO','CUST_SEQ']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""SELECT ACCOUNT_NO,ACCOUNT_CLASSIFY,ACCOUNT_NAME,DEBIT_NO,CUST_SEQ,THIRD_ORG_NAME,OPEN_DATE,CLOSE_DATE FROM M_ACCOUNT WHERE BALANCE!=0  and substr(subj_code,1,4) in ('1301','1302','1303','1304','1305','1306') %s order by account_no"""%(filterstr)

        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={1:'M_A_C'}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ?"%k
                vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["账号","账号类型","客户姓名","合同号","客户内码","开户机构","开户日期","销户日期"]

    @property
    def page_size(self):
        return 10
