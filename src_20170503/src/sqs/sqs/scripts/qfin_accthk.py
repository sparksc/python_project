# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
"""
理财
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['FIN_ACCOUNT_NO','CUST_LONG_NO','ACCOUNT_NO']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select d.FIN_ACCOUNT_NO,c.CUST_NAME,c.CUST_ADDRESS,d.CST_NO,(select ORG0_CODE from D_ORG where id = x.org_id) from D_ACCOUNT d 
            join F_BALANCE x on x.account_id=d.id and x.acct_type=8 and x.date_id =(SELECT MAX(DATE_ID) FROM F_BALANCE_CHECK)
            join D_CUST_INFO c on d.CST_NO=c.CUST_NO        
            where d.ACCT_TYPE=8 and d.ACCOUNT_CLASS='理财账户' %s
            """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
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
        return ["理财账号","客户姓名","地址信息"]
#
#    @property
#    def page_size(self):
#        return 10
