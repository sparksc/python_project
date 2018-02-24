# -*- coding:utf-8 -*-

from querybase import QueryBase, db2_pagination
"""
综合柜员本人按季考核指标
"""

class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
	if self.args.get("p_P_DATE") is not None:
                arg=str(self.args.get("p_P_DATE"))[0:4]+'-'+str(self.args.get("p_P_DATE"))[4:6]+'-'+str(self.args.get("p_P_DATE"))[6:8]
        if self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is not None:
                return "select tjrq,tjzq,khlx,jgbh,jgmc,yggh,ygxm,je17,je15,je20,je24,je33 from t_jgc_jxkh_zb_qm where tjrq='%s' and yggh=%s and jgbh=%s"%(arg,self.args.get("p_P_SALEID"),self.args.get("p_P_ORGID"))
        elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is None:
                return "select tjrq,tjzq,khlx,jgbh,jgmc,yggh,ygxm,je17,je15,je20,je24,je33 from t_jgc_jxkh_zb_qm where tjrq='%s' and yggh=%s"%(arg,self.args.get("p_P_SALEID"))
        elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is not None:
                return "select tjrq,tjzq,khlx,jgbh,jgmc,yggh,ygxm,je17,je15,je20,je24,je33 from t_jgc_jxkh_zb_qm where tjrq='%s' and jgbh=%s"%(arg,self.args.get("p_P_ORGID"))
        elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is not None:
                return "select tjrq,tjzq,khlx,jgbh,jgmc,yggh,ygxm,je17,je15,je20,je24,je33 from t_jgc_jxkh_zb_qm where yggh=%s and jgbh=%s"%(self.args.get("p_P_SALEID"),self.args.get("p_P_ORGID"))
        elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is not None:
                return "select tjrq,tjzq,khlx,jgbh,jgmc,yggh,ygxm,je17,je15,je20,je24,je33 from t_jgc_jxkh_zb_qm where jgbh=%s"%(self.args.get("p_P_ORGID"))
        elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is None:
                return "select tjrq,tjzq,khlx,jgbh,jgmc,yggh,ygxm,je17,je15,je20,je24,je33 from t_jgc_jxkh_zb_qm where jgbh=%s"%(self.args.get("p_P_SALEID"))
        elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is None:
                return "select tjrq,tjzq,khlx,jgbh,jgmc,yggh,ygxm,je17,je15,je20,je24,je33 from t_jgc_jxkh_zb_qm where tjrq='%s'"%(arg)
    def column_header(self):
        return ["统计日期","考核周期","考核类型","机构编号","机构名称","员工工号","员工姓名","新增企业网银","新增手机银行","新增POS机","折后业务量","业务量"]
