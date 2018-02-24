# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
机构指标查询
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['t_tjrq','t_jgbh']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select t.tjrq,t.jgbh,t.jgmc,t.je1,t.je2,t.je3,t.je19,t.je4,t.je5,t.je6,t.je7,t.je8,t.je9,t.je10,t.je11,t.hkl,t.je12,t.sjyhdhl,t.je15,t.je16,t.je17,t.je20 from t_jgc_jg_zb_qm t where 1=1 %s order by t.tjrq desc
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
        return ["统计日期","机构编号","机构名称","存款余额","贷款余额","本年存款净增","本年贷款净增","日均存款增加额","低成本存款净增","日均贷款增加额","个人贷款","企业贷款户数","五级不良率","表内外不良贷款下降额","易贷卡增量","活卡率","信用卡增量","手机银行动户率","企业网银户数","手机银行户数","电子银行使用替代率","贷款利息收入利息"]
     
    @property
    def page_size(self):
        return 15
