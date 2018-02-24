# -*- coding:utf-8 -*-

from querybase import QueryBase, db2_pagination
"""
员工存款归属关系查询
"""

class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
	sql="""
	SELECT  B.THIRD_ORG_CODE jgbh,D.org_name,A.GLDXBH,C.POSITION_NAME,B.ACCOUNT_NAME HM,B.CUST_SEQ KHNM,TRIM(A.DXBH)as DXBH,A.DXXH,
B.CCY BZ,B.BALANCE*0.01 RQYE,A.GLJE1,A.CK_TYPE,A.GLRQ1,A.GLRQ2,D.ORG_CODE ORG_CODE
FROM T_ZJC_GSGX_CK A inner join M_ACCOUNT B on  A.DXBH=B.ACCOUNT_NO AND A.DXXH=B.ACCOUNT_SBSQ and B.BALANCE>0
and  B.SUBJ_CODE in ('2011','2012','2014','20141','20151','2017','2051','2111','21111','2151','21511','2155','2511','25111','2431')  
inner join  VIEW_RSXXB C  on A.GLDXBH=C.STAFF_CODE left join ORGANIZATION d on a.JGBH=d.ORG_CODE  
	"""
	"""
where  (B.THIRD_ORG_CODE in `csjg` or B.THIRD_ORG_CODE in (select csjg from view_rsxxb where staff_code =`j_username`))
	"""
	i=1
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
        return ["机构编号","机构名称","员工工号","员工姓名","客户姓名","客户号","存款账号机","账号序号","币种","日切余额","分配比例","存款类型","管理起始日期","管理结束日期"]
