# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
综合柜员本人按年考核指标
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['tjrq','yggh']
        print(self.filterlist)
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select tjrq,tjzq,khlx,jgbh,jgmc,yggh,ygxm,je25,je26,je36,je21,je22,je16,je18
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
        return ["统计日期","考核周期","考核类型","机构编号","机构名称","员工工号","员工姓名","上年网点人均日均存款存量","网点人均日均存款增量","当前网点日均人均存款存>量","新增POS机活跃客户1","新增POS机活跃客户2","新增手机银行活跃客户","新增企业网银活跃客户"]
    @property
    def page_size(self):
        return 15
