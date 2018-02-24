# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
存款营销录入
"""

class Query(ObjectQuery):

    def prepare_object(self):
	#if( 'e_p_THIRD_ORG_CODE' in self.args):
	#    self.args.pop('e_p_THIRD_ORG_CODE')
        self.filterlist = ['ACCOUNT_NO']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""select ACCOUNT_NO,ACCOUNT_CLASSIFY,ACCOUNT_NAME,CUST_SEQ, THIRD_ORG_NAME, OPEN_DATE,CLOSE_DATE,ACCOUNT_SBSQ from M_ACCOUNT where substr(SUBJ_CODE,1,4)  in ('2001','2002','2003','2004','2005','2006','2007','2011','2014','2017') %s"""%(filterstr)

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
        return ["存款账号","存款类型","客户姓名","客户号","开户机构","开户日期","销户日期","账号序号"]
#
#    @property
#    def page_size(self):
#        return 10
