# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
客户挂钩
"""

class Query(ObjectQuery):

    def prepare_object(self):
	#if( 'e_p_THIRD_ORG_CODE' in self.args):
	#    self.args.pop('e_p_THIRD_ORG_CODE')
        self.filterlist = ['CUST_NO']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""select cust_long_no,cust_name,cust_address,cust_no from D_CUST_INFO where 1=1 %s"""%(filterstr)

        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and CUST_LONG_NO = ?"
                vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["客户号","客户姓名","地址信息","客户内码"]
#
#    @property
#    def page_size(self):
#        return 10
