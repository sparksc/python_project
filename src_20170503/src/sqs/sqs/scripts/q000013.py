# -*- coding:utf-8 -*-

from querybase import QueryBase, db2_pagination
"""
机构指标查询
"""

class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
	if self.args.get("p_P_DATE") is not None:
		arg=str(self.args.get("p_P_DATE"))[0:4]+'-'+str(self.args.get("p_P_DATE"))[4:6]+'-'+str(self.args.get("p_P_DATE"))[6:8]
	if self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is not None:
        	return "select tjrq,jgbh,jgmc,je1,je2,je3,je19,je4,je5,je6,je7,je8,je9,je10,je11,hkl,je12,sjyhdhl,je15,je16,je17,je20 from t_jgc_jg_zb_qm where tjrq='%s' and yggh=%s and jgbh=%s"%(arg,self.args.get("p_P_SALEID"),self.args.get("p_P_ORGID"))
	elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is None:
		return "select tjrq,jgbh,jgmc,je1,je2,je3,je19,je4,je5,je6,je7,je8,je9,je10,je11,hkl,je12,sjyhdhl,je15,je16,je17,je20 from t_jgc_jg_zb_qm where tjrq='%s' and yggh=%s"%(arg,self.args.get("p_P_SALEID"))
	elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is not None:
		return "select tjrq,jgbh,jgmc,je1,je2,je3,je19,je4,je5,je6,je7,je8,je9,je10,je11,hkl,je12,sjyhdhl,je15,je16,je17,je20 from t_jgc_jg_zb_qm where tjrq='%s' and jgbh=%s"%(arg,self.args.get("p_P_ORGID"))
	elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is not None:
		return "select tjrq,jgbh,jgmc,je1,je2,je3,je19,je4,je5,je6,je7,je8,je9,je10,je11,hkl,je12,sjyhdhl,je15,je16,je17,je20 from t_jgc_jg_zb_qm where yggh=%s and jgbh=%s"%(self.args.get("p_P_SALEID"),self.args.get("p_P_ORGID"))
	elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is not None:
		return "select tjrq,jgbh,jgmc,je1,je2,je3,je19,je4,je5,je6,je7,je8,je9,je10,je11,hkl,je12,sjyhdhl,je15,je16,je17,je20 from t_jgc_jg_zb_qm where jgbh=%s"%(self.args.get("p_P_ORGID"))
	elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is None:
		return "select tjrq,jgbh,jgmc,je1,je2,je3,je19,je4,je5,je6,je7,je8,je9,je10,je11,hkl,je12,sjyhdhl,je15,je16,je17,je20 from t_jgc_jg_zb_qm where jgbh=%s"%(self.args.get("p_P_SALEID"))
	elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is None:
		return "select tjrq,jgbh,jgmc,je1,je2,je3,je19,je4,je5,je6,je7,je8,je9,je10,je11,hkl,je12,sjyhdhl,je15,je16,je17,je20 from t_jgc_jg_zb_qm where tjrq='%s'"%(arg)


    def column_header(self):
        return ["统计日期","机构编号","机构名称","存款余额","贷款余额","本年存款净增","本年贷款净增","日均存款增加额","低成本存款净增","日均贷款增加额","个人贷款","企业贷款户数","五级不良率","表内外不良贷款下降额","易贷卡增量","活卡率","信用卡增量","手机银行动户率","企业网银户数","手机银行户数","电子银行使用替代率","贷款利息收入利息"]
