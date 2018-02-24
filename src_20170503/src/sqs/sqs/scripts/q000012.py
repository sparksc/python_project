# -*- coding:utf-8 -*-

from querybase import QueryBase, db2_pagination
"""
本人基本薪酬
"""

class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
	if self.args.get("p_P_DATE") is not None:
		arg=str(self.args.get("p_P_DATE"))[0:4]+'-'+str(self.args.get("p_P_DATE"))[4:6]+'-'+str(self.args.get("p_P_DATE"))[6:8]
	if self.args.get("p_P_DATE") is not None:
        	return "select tjrq,jgbh,jgmc,yggh,ygxm,je1,je2,je4,je5 from t_jgc_jxkh_yg_jcxc where tjrq='%s'"%(arg)
    def column_header(self):
        return ["统计日期", "机构号", "机构名称","员工工号","员工姓名","保障工资","津贴","岗位工资","基本薪酬汇总"]

