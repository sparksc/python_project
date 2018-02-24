# -*- coding:utf-8 -*-

from querybase import QueryBase, db2_pagination
"""
综合柜员按季考核绩效薪酬
"""

class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
        print self.args
	if self.args.get("p_P_DATE") is not None:
                arg=str(self.args.get("p_P_DATE"))[0:4]+'-'+str(self.args.get("p_P_DATE"))[4:6]+'-'+str(self.args.get("p_P_DATE"))[6:8]
        if self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is not None:
                return "select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je15,je17,je20,je27,je24,gw from t_jgc_jxkh_jx_qm where tjrq='%s' and yggh=%s and jgbh=%s"%(arg,self.args.get("p_P_SALEID"),self.args.get("p_P_ORGID"))
        elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is None:
                return "select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je15,je17,je20,je27,je24,gw from t_jgc_jxkh_jx_qm where tjrq='%s' and yggh=%s"%(arg,self.args.get("p_P_SALEID"))
        elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is not None:
                return "select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je15,je17,je20,je27,je24,gw from t_jgc_jxkh_jx_qm where tjrq='%s' and jgbh=%s"%(arg,self.args.get("p_P_ORGID"))
        elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is not None:
                return "select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je15,je17,je20,je27,je24,gw from t_jgc_jxkh_jx_qm where yggh=%s and jgbh=%s"%(self.args.get("p_P_SALEID"),self.args.get("p_P_ORGID"))
        elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is not None:
                return "select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je15,je17,je20,je27,je24,gw from t_jgc_jxkh_jx_qm where jgbh=%s"%(self.args.get("p_P_ORGID"))
        elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is None:
                return "select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je15,je17,je20,je27,je24,gw from t_jgc_jxkh_jx_qm where jgbh=%s"%(self.args.get("p_P_SALEID"))
        elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is None:
                return "select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je15,je17,je20,je27,je24,gw from t_jgc_jxkh_jx_qm where tjrq='%s'"%(arg)
    def column_header(self):
        return ["统计日期", "考核周期", "考核类型","员工工号","员工姓名","机构编号","机构名称","新增手机银行绩效薪酬","新增企业网银绩效薪酬","新增POS机绩效薪酬","电银替代率绩效薪酬","计件业务量绩效薪酬","岗位号"]

    @property
    def page_size(self):
        return 10
