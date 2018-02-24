# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
综合柜员本人按季考核指标
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['tjrq','yggh']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select tjrq,tjzq,khlx,jgbh,jgmc,yggh,ygxm,je17,je15,je20,je24,je33 
            from t_jgc_jxkh_zb_qm 
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
        return ["统计日期","考核周期","考核类型","机构编号","机构名称","员工工号","员工姓名","新增企业网银","新增手机银行","新增POS机","折后业务量","业务量"]
    @property
    def page_size(self):
        return 15
