# -*- coding:utf-8 -*-

from querybase import QueryBase, db2_pagination
"""
员工贷款归属关系查询
"""

class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
	sql="""
 select B.JGBH,
	TRIM(B.DXBH) DXBH,
	TRIM(B.GLDXBH) GLDXBH,
	TRIM(B.DXXH) DXXH,
	C.STAFF_NAME,
	TRIM(B.FJDXBH) FJDXBH,
	TRIM(B.dxmc) dxmc,
	B.GLJE1,
	TRIM(B.glrq1) GLRQ1,
	TRIM(B.glrq2) GLRQ2,
(case when a.balance_attr = '1' then -1*a.balance else a.balance end )*0.01  RQYE
FROM M_ACCOUNT A
INNER JOIN t_zjc_gsgx_dk b ON a.ACCOUNT_NO=b.dxbh and a.DEBIT_NO=b.dxxh
INNER JOIN STAFF_RELATION C ON B.GLDXBH=C.STAFF_CMS_CODE 
WHERE a.BALANCE>0 
AND A.ACCOUNT_STATUS<>'1'
and (
(substr(a.new_subj_code,1,4) in ( '1301','1302','1303','1304')  and a.account_classify='L') 
or 
(substr(a.new_subj_code,1,4) in ( '1305','1306')  and a.account_classify='I') 
)
AND B.glje1=100
	"""
	i=0
	print self.args
    rs =[]
	for k in self.args:
		if k=="e_p_P_DATE":
			continue
		val=self.args.get(k)
		if i==1:
			sql=sql+" where %s=?"%(k[4:])
            rs.append(val)
			i=0
		else:
			sql=sql+" and %s=?"%(k[4:])
            rs.append(val)
	sql=sql+" order by a.PARA_ID desc"
	return sql,rs
    def column_header(self):
        return ["机构编号","账号","客户经理编号","账号序号","客户经理姓名","客户姓名","客户号","归属比例","归属起始日期","归属结束日期","贷款余额"]
