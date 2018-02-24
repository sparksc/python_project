# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
客户经理本人按年考核指标
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['tjrq','yggh']
        filterstr,vlist = self.make_eq_filterstr()
   

        sql ="""
            select tjrq,tjzq,khlx,jgbh,jgmc,yggh,ygxm,je1,je2,je35,je3,je4,je6,je7,je8,je9,je10,je11,je12,je34,je18,je16,je21,je22 
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
        return ["统计日期","考核周期","考核类型","机构编号","机构名称","员工工号","员工姓名","日均自营存款存量余额","日均自营存款增量余额","当前日均自营存款(时点)","日均派生存款存量余额","日均派生存款增量余额","贷款利差收入","贷款户数扩面存量(日均50万以下)","贷款户数扩面增量(日均50万以下)","贷款户数扩面存量(日均50万以上)","贷款户数扩面增量(日均50万以上)","不良贷款余额","不良贷>款下降额","上年末不良贷款额","新增企业网银活跃客户","新增手机银行活跃客户","新增POS机活跃客户1","新增POS机活跃客户2"]
    
    @property
    def page_size(self):
        return 15
