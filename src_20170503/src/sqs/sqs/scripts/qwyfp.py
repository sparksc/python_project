# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config
"""
网银分配界面
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['cust_no','cust_name','note','org']
        filterstr,vlist = self.make_eq_filterstr()

        sql1 =u"""
                select a.id,org0_code,org0_name,org0_code,a.cust_no,d.cust_name,dc.open_date,note from EBANK_ORG a
                join D_ORG o on o.org0_code=a.org_no
                join d_cust_info d on d.cust_no= a.cust_in_no
                join d_cust_contract dc on a.CUST_NET_NO = dc.NET_CST_NO and CLOSE_DATE=30001231 and dc.BUSI_TYPE  = '企业网上银行'
                where status='待分配' and typ='电子银行' and sub_typ='企业网上银行' %s
                order by id desc
            """%(filterstr)
        print sql1 
        row = self.engine.execute(sql1,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
             if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and org0_code in (%s) "%(vvv)
                elif k == 'cust_no':
                    filterstr = filterstr+" and a.cust_no = ?"
                    vlist.append(v)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'org0_code', None))
        return filterstr,vlist
    def column_header(self):
        return ["序号","机构号","机构名","员工号","客户号","客户名称","开户日期","地址",""]

    @property
    def page_size(self):
        return 15
