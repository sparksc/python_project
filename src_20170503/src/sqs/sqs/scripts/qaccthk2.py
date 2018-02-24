# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
账户挂钩
"""

class Query(ObjectQuery):

    def prepare_object(self):
	#if( 'e_p_THIRD_ORG_CODE' in self.args):
	#    self.args.pop('e_p_THIRD_ORG_CODE')
        self.filterlist = ['ACCOUNT_NO','CARD_NO']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""select d.account_no,d.cst_no,d.cst_name,nvl(f.CUST_ADDRESS,f.CUST_CREDIT_ADDRESS) from D_ACCOUNT d
                left join d_cust_info f on f.cust_no=d.cst_no
                left join d_credit_card c on c.account_no=d.account_no
                where 1=1 %s """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'ACCOUNT_NO':
                    filterstr = filterstr+" and d.account_no = ?"
                    vlist.append(v)
                elif k == 'CARD_NO':
                    filterstr = filterstr+" and c.card_no = ?"
                    vlist.append(v)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["账号","客户号","客户姓名"]
#
#    @property
#    def page_size(self):
#        return 10
