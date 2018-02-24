# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
员工本人按年考核绩效薪酬
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['t_tjrq','t_yggh']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select t.tjrq,t.khlx,t.tjzq,t.yggh,t.ygxm,t.jgbh,t.jgmc,t.je36,t.je1,t.je2,t.je6,t.je7,t.je8,t.je11,t.je25,t.je26,t.je16,t.je18,t.je21,t.je22,t.gw from t_jgc_jxkh_jx_qm t where 1=1 %s order by t.yggh desc
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
        return ["统计日期", "考核周期", "考核类型","员工工号","员工姓名","机构编号","机构名称","非营销人员日均存款增量绩效薪酬","日均存款存量绩效薪酬","日均存款增量绩效薪酬","贷款利差收入绩效薪酬","贷款增户扩面存量绩效薪酬","贷款增户扩面增量绩效薪酬","不良绩效薪酬","网点存款存量维护绩效薪酬","网点存款增量绩效薪酬","新增手机银行活跃客户绩效薪酬","新增企业网银活跃客户绩效薪酬","新增POS机活跃客户绩效薪酬1","新增POS机活跃客户绩效薪酬2","岗位号"]
    @property
    def page_size(self):
        return 15
