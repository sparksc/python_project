# -*- coding:utf-8 -*-

from querybase import QueryBase, db2_pagination
"""
综合柜员本人按年考核绩效薪酬
"""

class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
        print self.args
	if self.args.get("p_P_DATE") is not None:
                arg=str(self.args.get("p_P_DATE"))[0:4]+'-'+str(self.args.get("p_P_DATE"))[4:6]+'-'+str(self.args.get("p_P_DATE"))[6:8]
        if self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is not None:
                return "select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je25,je26,je16,je18,je21,je22,gw from t_jgc_jxkh_jx_qm where tjrq='%s' and yggh=%s and jgbh=%s"%(arg,self.args.get("p_P_SALEID"),self.args.get("p_P_ORGID"))
        elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is None:
                return "select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je25,je26,je16,je18,je21,je22,gw from t_jgc_jxkh_jx_qm where tjrq='%s' and yggh=%s"%(arg,self.args.get("p_P_SALEID"))
        elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is not None:
                return "select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je25,je26,je16,je18,je21,je22,gw from t_jgc_jxkh_jx_qm where tjrq='%s' and jgbh=%s"%(arg,self.args.get("p_P_ORGID"))
        elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is not None:
                return "select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je25,je26,je16,je18,je21,je22,gw from t_jgc_jxkh_jx_qm where yggh=%s and jgbh=%s"%(self.args.get("p_P_SALEID"),self.args.get("p_P_ORGID"))
        elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is not None:
                return "select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je25,je26,je16,je18,je21,je22,gw from t_jgc_jxkh_jx_qm where jgbh=%s"%(self.args.get("p_P_ORGID"))
        elif self.args.get("p_P_DATE") is None and self.args.get("p_P_SALEID") is not None and self.args.get("p_P_ORGID") is None:
                return "select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je25,je26,je16,je18,je21,je22,gw from t_jgc_jxkh_jx_qm where jgbh=%s"%(self.args.get("p_P_SALEID"))
        elif self.args.get("p_P_DATE") is not None and self.args.get("p_P_SALEID") is None and self.args.get("p_P_ORGID") is None:
                return "select tjrq,khlx,tjzq,yggh,ygxm,jgbh,jgmc,je25,je26,je16,je18,je21,je22,gw from t_jgc_jxkh_jx_qm where tjrq='%s'"%(arg)





    def column_header(self):
        return ["统计日期", "考核周期", "考核类型","员工工号","员工姓名","机构编号","机构名称","网点存款存量维护绩效薪酬","网点存款增量绩效薪酬","新增手机银行活跃客户绩效薪酬","新增企业网银活跃客户绩效薪酬","新增POS机活跃客户绩效薪酬1","新增POS机活跃客户绩效薪酬2","岗位号"]

    @property
    def page_size(self):
        return 10
