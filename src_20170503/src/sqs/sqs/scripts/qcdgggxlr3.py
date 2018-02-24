# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
存贷挂钩关系录入
"""

class Query(ObjectQuery):

    def prepare_object(self):
	#if( 'e_p_THIRD_ORG_CODE' in self.args):
	#    self.args.pop('e_p_THIRD_ORG_CODE')
        self.filterlist = ['FJDXBH']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""SELECT A.DXBH,A.DXXH,A.GLJE1,A.GLRQ1,A.GLRQ2,A.GGGX,A.STATUS,A.PARA_ID FROM T_ZJC_GSGX_CDK A where A.glrq2 >to_char(current date,'yyyy-mm-dd') %s """%(filterstr)

        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}#{5:'CKTYPE'}
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
        return ["存款账号","账号序号","挂钩比例","挂钩起始日期","挂钩结束日期","存贷挂钩关系","状态"]
#
#    @property
#    def page_size(self):
#        return 10
