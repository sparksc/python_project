# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from utils import config

"""
导入的考核数据查询
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID', 'org']
        filterstr, vlist = self.make_eq_filterstr()
        sql ="""
        select q.DATE_ID, q.ORG_NO, q.CUST_IN_NO,  q.CUST_NAME, q.CUST_NO,q.ACCOUNT_NO,  q.CNT,nvl(info.tel_core,'') as tel_core ,
        nvl(info.cust_address,'') as cust_address,nvl(info.cust_credit_address,'') as cust_credit_address from quarter_term_sale_mbank q left join d_cust_info info on q.cust_in_no=info.cust_no where 1=1  %s  order by q.org_no,q.CNT desc
        """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print "0000000000000000000000000", sql
        needtrans ={}
        return self.translate(list(row),needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and q.ORG_NO in ( %s ) "%(vvv)
                elif k == 'DATE_ID':
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
                else: 
                    pass
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'None','q.ORG_NO', None))
        return filterstr,vlist

    def column_header(self):
        return ["考核日期", "机构号","客户内码","客户名称","客户号", "账号", "笔数","电话号码","核心地址","信贷地址"]

    @property
    def page_size(self):
        return 15
