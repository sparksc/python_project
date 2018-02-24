# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
综合柜员本人按年考核绩效薪酬
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['tjrq','yggh']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je25,je26,je16,je18,je21,je22,gw 
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
        return ["统计日期", "考核周期", "考核类型","员工工号","员工姓名","机构编号","机构名称","网点存款存量维护绩效薪酬","网点存款增量绩效薪酬","新增手机银行活跃客户>绩效薪酬","新增企业网银活跃客户绩效薪酬","新增POS机活跃客户绩效薪酬1","新增POS机活跃客户绩效薪酬2","岗位号"]
    @property
    def page_size(self):
        return 15
