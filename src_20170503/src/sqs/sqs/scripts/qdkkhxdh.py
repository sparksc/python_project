# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
存贷款客户核心号和信贷号
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['account_name','third_org_code','cust_seq','cust_seq2']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select account_name,third_org_code,b.BRANCH_NAME,cust_seq,cust_seq2,ID
            from LOAN_CUS_CORE_CREDIT
            inner join BRANCH b on BRANCH_CODE = third_org_code
            where 1=1 %s
	    """%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+"and %s = ?"%k 
                vlist.append(v) 
        return filterstr,vlist
   
    def column_header(self):
        return ["客户姓名","机构编号","机构名称","客户号","客户内码","操作"]

    @property
    def page_size(self):
        return 10
