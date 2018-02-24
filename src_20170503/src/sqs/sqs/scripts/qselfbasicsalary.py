# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
本人基本薪酬
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['t_tjrq','t_yggh']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select t.tjrq,t.jgbh,t.jgmc,t.yggh,t.ygxm,t.je1,t.je2,t.je4,t.je5 from t_jgc_jxkh_yg_jcxc t where 1=1 %s order by t.yggh desc
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
                vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["统计日期", "机构号", "机构名称","员工工号","员工姓名","保障工资","津贴","岗位工资","基本薪酬汇总"]
    @property
    def page_size(self):
        return 15
