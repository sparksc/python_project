# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
"""
电子银行详情
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SALE_CODE','CUST_NO','DATE','ORG','CUST_IN_NO']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
            select net_cst_no, cust_no, busi_type, org_no,user_name,name from ebank_info
            where 1=1 %s
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
                if k == 'SALE_CODE':
                    filterstr = filterstr + " and user_name = ? "
                    vlist.append(v)
                if k == 'CUST_NO':
                    filterstr = filterstr + " and cust_no = ? "
                    vlist.append(v)
                if k == 'CUST_IN_NO':
                    filterstr = filterstr + " and cust_in_no = ? "
                    vlist.append(v)
                if k == 'ORG':
                    filterstr = filterstr + " and org_no = ? "
                    vlist.append(v)
        return filterstr,vlist


    def column_header(self):
        return ["标识号", "客户号", "电子银行子类型","机构号","营销员工号","营销员工名"]

    @property
    def page_size(self):
        return 30
