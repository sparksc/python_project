# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
员工本人按季指标
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['t_tjrq','t_yggh']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select t.tjrq,t.khlx,t.tjzq,t.jgbh,t.jgmc,t.yggh,t.ygxm,t.je17,t.je15,t.je20 from t_jgc_jxkh_zb_qm t where 1=1 %s order by t.jgbh desc
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
        return ["统计日期","考核类型", "考核周期", "机构编号","机构名称","员工工号","员工姓名","新增企业网银","新增手机银行","新增POS机"]

    @property
    def page_size(self):
        return 15
