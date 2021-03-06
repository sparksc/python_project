# -*- coding:utf-8 -*-

from querybase import QueryBase, db2_pagination
"""
员工按年指标
"""

class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
	if self.args.get("p_P_DATE") is not None:
		arg=str(self.args.get("p_P_DATE"))[0:4]+'-'+str(self.args.get("p_P_DATE"))[4:6]+'-'+str(self.args.get("p_P_DATE"))[6:8]
	if self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is not None:
        	return "select tjrq,khlx,tjzq,jgbh,jgmc,yggh,ygxm,je37,je38,je39,je1,je2,je35,je3,je4,je6,je7,je8,je9,je10,je11,je12,je34,je18,je16,je21,je22,je25,je26,je36 from t_jgc_jxkh_zb_qm where tjrq='%s' and yggh=%s and org_code=%s"%(arg,self.args.get("p_P_SALEID"),self.args.get("p_P_ORGID"))
	elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is None:
		return "select tjrq,khlx,tjzq,jgbh,jgmc,yggh,ygxm,je37,je38,je39,je1,je2,je35,je3,je4,je6,je7,je8,je9,je10,je11,je12,je34,je18,je16,je21,je22,je25,je26,je36 from t_jgc_jxkh_zb_qm where tjrq='%s' and yggh=%s"%(arg,self.args.get("p_P_SALEID"))
	elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is not None:
		return "select tjrq,khlx,tjzq,jgbh,jgmc,yggh,ygxm,je37,je38,je39,je1,je2,je35,je3,je4,je6,je7,je8,je9,je10,je11,je12,je34,je18,je16,je21,je22,je25,je26,je36 from t_jgc_jxkh_zb_qm where tjrq='%s' and org_code=%s"%(arg,self.args.get("p_P_ORGID"))
	elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is not None:
		return "select tjrq,khlx,tjzq,jgbh,jgmc,yggh,ygxm,je37,je38,je39,je1,je2,je35,je3,je4,je6,je7,je8,je9,je10,je11,je12,je34,je18,je16,je21,je22,je25,je26,je36 from t_jgc_jxkh_zb_qm where yggh=%s and org_code=%s"%(self.args.get("p_P_SALEID"),self.args.get("p_P_ORGID"))
	elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is not None:
		return "select tjrq,khlx,tjzq,jgbh,jgmc,yggh,ygxm,je37,je38,je39,je1,je2,je35,je3,je4,je6,je7,je8,je9,je10,je11,je12,je34,je18,je16,je21,je22,je25,je26,je36 from t_jgc_jxkh_zb_qm where org_code=%s"%(self.args.get("p_P_ORGID"))
	elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is None:
		return "select tjrq,khlx,tjzq,jgbh,jgmc,yggh,ygxm,je37,je38,je39,je1,je2,je35,je3,je4,je6,je7,je8,je9,je10,je11,je12,je34,je18,je16,je21,je22,je25,je26,je36 from t_jgc_jxkh_zb_qm where yggh=%s"%(self.args.get("p_P_SALEID"))
	elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is None:
		return "select tjrq,khlx,tjzq,jgbh,jgmc,yggh,ygxm,je37,je38,je39,je1,je2,je35,je3,je4,je6,je7,je8,je9,je10,je11,je12,je34,je18,je16,je21,je22,je25,je26,je36 from t_jgc_jxkh_zb_qm where tjrq='%s'"%(arg)

    def column_header(self):
        return ["统计日期","考核类型", "统计周期", "机构编号","机构名称","员工工号","员工姓名","非营销人员日均存款余额","非营销人员日均存款存量","非营销人员日均存款增量","日均自营存款存量余额","日均自营存款增量余额","当前日均自营存款(时点)","日均派生存款存量余额","日均派生存款增量余额","日均分配存款增量","日均分配存款存量","日均存款余额","贷款利差收入","贷款户数扩面存量(日均50万以下)","贷款户数扩面增量(日均50万以下)","贷款户数扩面存量(日均50万以上)","贷款户数扩面增量(日均50万以上)","不良贷款余额","不良贷款下降额","上年末不良贷款额","新增企业网银活跃客户","新增手机银行活跃客户","新增POS机活跃客户1","新增POS机活跃客户2","上年网点人均日均存款存量","网点人均日均存款增量","当前网点人均日均存款"]
