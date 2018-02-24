# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
存款营销录入
"""

class Query(ObjectQuery):

    def prepare_object(self):
	#if( 'e_p_THIRD_ORG_CODE' in self.args):
	#    self.args.pop('e_p_THIRD_ORG_CODE')
        self.filterlist = ['JGBH','GLDXBH','CK_TYPE','DXBH','DXMC']
        filterstr,vlist = self.make_eq_filterstr()
        sql =""" 
SELECT  DRRQ,A.GLDXBH,v.name,TRIM(A.DXBH) as DXBH,TRIM(B.ACCOUNT_SBSQ) AS ZHXH,B.ACCOUNT_NAME HM,B.THIRD_ORG_CODE jgbh,B.CUST_SEQ KHNM,A.GLJE1,A.GLRQ1,A.GLRQ2,A.CK_TYPE,A.PARA_ID FROM T_ZJC_GSGX_CK A inner join M_ACCOUNT B on  A.DXBH=B.ACCOUNT_NO AND A.DXXH=B.ACCOUNT_SBSQ and B.BALANCE<>0 and substr(B.SUBJ_CODE,1,4)  in ('2001','2002','2003','2004','2005','2006','2007','2011','2014','2017') inner join F_USER v on a.gldxbh = v.user_name where A.glrq2 >to_char(current date,'yyyy-mm-dd') %s  order by a.PARA_ID desc
    """%(filterstr)

        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={11:'CKTYPE'}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ?"%k
                vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["维护日期","员工工号","员工姓名","存款账号","账号序号","客户姓名","机构编号","客户号","分配比例","管理起始日期","管理结束日期","营销类型","操作"]

    @property
    def page_size(self):
        return 10
