# -*- coding:utf-8 -*-

from querybase import QueryBase, db2_pagination
"""
员工基本薪酬
"""

class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
	if self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is not None:
        	return "select tjrq,jgbh,jgmc,yggh,ygxm,je1,je2,je4,je5 from t_jgc_jxkh_yg_jcxc where tjrq='%s' and yggh=%s and jgbh=%s"%(arg,self.args.get("p_P_SALEID"),self.args.get("p_P_ORGID"))
	elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is None:
		return "select tjrq,jgbh,jgmc,yggh,ygxm,je1,je2,je4,je5 from t_jgc_jxkh_yg_jcxc where tjrq='%s' and yggh=%s"%(arg,self.args.get("p_P_SALEID"))
	elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is not None:
		return "select tjrq,jgbh,jgmc,yggh,ygxm,je1,je2,je4,je5 from t_jgc_jxkh_yg_jcxc where tjrq='%s' and jgbh=%s"%(arg,self.args.get("p_P_ORGID"))
	elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is not None:
		return "select tjrq,jgbh,jgmc,yggh,ygxm,je1,je2,je4,je5 from t_jgc_jxkh_yg_jcxc where yggh=%s and jgbh=%s"%(self.args.get("p_P_SALEID"),self.args.get("p_P_ORGID"))
	elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is not None:
		return "select tjrq,jgbh,jgmc,yggh,ygxm,je1,je2,je4,je5 from t_jgc_jxkh_yg_jcxc where jgbh=%s"%(self.args.get("p_P_ORGID"))
	elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is None:
		return "select tjrq,jgbh,jgmc,yggh,ygxm,je1,je2,je4,je5 from t_jgc_jxkh_yg_jcxc where jgbh=%s"%(self.args.get("p_P_SALEID"))
	elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is None:
		return "select tjrq,jgbh,jgmc,yggh,ygxm,je1,je2,je4,je5 from t_jgc_jxkh_yg_jcxc where tjrq='%s'"%(arg)

    def column_header(self):
        return ["统计日期", "机构号", "机构名称","员工工号","员工姓名","保障工资","津贴","岗位工资","基本薪酬汇总"]

