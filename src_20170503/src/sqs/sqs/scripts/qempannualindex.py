# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
员工按年指标
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['t_tjrq','t_yggh','t_jgbh']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select t.tjrq,t.khlx,t.tjzq,t.jgbh,t.jgmc,t.yggh,t.ygxm,t.je37,t.je38,t.je39,t.je1,t.je2,t.je35,t.je3,t.je4,t.je42,t.je41,t.je44,t.je6,t.je7,t.je8,t.je9,t.je10,t.je11,t.je12,t.je34,t.je18,t.je16,t.je21,t.je22,t.je25,t.je26,t.je36 from t_jgc_jxkh_zb_qm t where 1=1 %s order by t.yggh desc
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
        return ["统计日期","考核类型", "统计周期", "机构编号","机构名称","员工工号","员工姓名","非营销人员日均存款余额","非营销人员日均存款存量","非营销人员日均存款增量","日均自营存款存量余额","日均自营存款增量余额","当前日均自营存款(时点)","日均派生存款存量余额","日均派生存款增量余额","日均分配存款增量","日均分配存款存量","日均存款余额","贷款利差收入","贷款户数扩面存量(日均50万以下)","贷款户数扩面增量(日均50万以下)","贷款户数扩面存量(日均50万以上)","贷款户数扩面增量(日均50万以上)","不良贷款余额","不良贷款下降额","上年末不良贷款额","新增企业网银活跃客户","新增手机银行活跃客户","新增POS机活跃客户1","新增POS机活跃客户2","上年网点人均日均存款存量","网点人均日均存款增量","当前网点人均日均存款"]

    @property
    def page_size(self):
        return 15
