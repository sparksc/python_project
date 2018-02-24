# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
存款营销录入
"""

class Query(ObjectQuery):

    def prepare_object(self):
	#if( 'e_p_THIRD_ORG_CODE' in self.args):
	#    self.args.pop('e_p_THIRD_ORG_CODE')
        self.filterlist = ['DXXH','FJDXBH']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""SELECT A.GLDXBH,v.name,A.GLJE1,A.GLRQ1,A.GLRQ2,A.DK_TYPE,A.PARA_ID FROM T_ZJC_GSGX_DK A inner join STAFF_RELATION s on a.gldxbh = s.STAFF_CMS_CODE inner join F_USER v on s.staff_code  = v.user_name where A.glrq2 >to_char(current date,'yyyy-mm-dd') %s order by para_id"""%(filterstr)

        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        print row,'********************************************',vlist
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ?"%k
                vlist.append(v)
        return filterstr,vlist
#    def column_header(self):
#        return ["员工工号","员工姓名","管理比例","管理起始日期","管理结束日期","存款类型"]
#
#    @property
#    def page_size(self):
#        return 10
