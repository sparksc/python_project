# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
员工按季考核绩效薪酬
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['t_tjrq','t_yggh','t_jgbh']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select t.tjrq,t.khlx,t.tjzq,t.yggh,t.ygxm,t.jgbh,t.jgmc,t.je15,t.je17,t.je20,t.je27,t.je24,t.je37,t.je38,nvl(t.je15,0)+nvl(t.je17,0)+nvl(t.je20,0)+nvl(t.je27,0)+nvl(t.je24,0)+nvl(t.je37,0)+nvl(t.je38,0) as hz,t.gw from t_jgc_jxkh_jx_qm t where 1=1 %s order by t.yggh desc
	    """%(filterstr)
        print(sql)
        print(vlist)
        needtrans={}
        row = self.engine.execute(sql,vlist).fetchall()
        return self.translate(row,needtrans)
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ?"%(k.replace('_','.',1))
                if(k=='t_tjrq'):
                    vlist.append(str(v)[0:4]+'-'+str(v)[4:6]+'-'+str(v)[6:8])
                else:
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["统计日期", "考核周期", "考核类型","员工工号","员工姓名","机构编号","机构名称","新增手机银行绩效薪酬","新增企业网银绩效薪酬","新增POS机绩效薪酬","电银替代率绩效薪酬","计件业务量绩效薪酬","支行行长二次分配薪酬","基础业务量二次分配绩效薪酬","汇总薪酬","岗位号"]

    @property
    def page_size(self):
        return 15
