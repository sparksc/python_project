# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
综合柜员本人按季考核绩效薪酬
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['tjrq','yggh']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je15,je17,je20,je27,je24,gw 
            from t_jgc_jxkh_jx_qm
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
                filterstr = filterstr+" and %s = ? "%k 
                vlist.append(v) 
        return filterstr,vlist
    def column_header(self):
        return ["统计日期", "考核周期", "考核类型","员工工号","员工姓名","机构编号","机构名称","新增手机银行绩效薪酬","新增企业网银绩效薪酬","新增POS机绩效薪酬","电银>替代率绩效薪酬","计件业务量绩效薪酬","岗位号"]
    @property
    def page_size(self):
        return 15
