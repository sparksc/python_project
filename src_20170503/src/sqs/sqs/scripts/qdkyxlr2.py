# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
贷款营销录入
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['GLDXBH','DXMC','DXBH','FJDXBH']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
            SELECT DRRQ,A.GLDXBH,v.name,TRIM(B.debit_no) AS ZHXH,TRIM(A.DXBH) as DXBH,B.ACCOUNT_NAME HM,B.CUST_SEQ KHNM,jgbh,A.GLJE1,A.GLRQ1,A.GLRQ2,A.DK_TYPE,A.PARA_ID 
            FROM T_ZJC_GSGX_DK A 
            inner join M_ACCOUNT B on  A.DXBH=B.ACCOUNT_NO AND A.DXXH=B.DEBIT_NO and B.BALANCE<>0 and substr(B.SUBJ_CODE,1,4)  in ('1301','1302','1303','1304','1305','1306') 
            inner join Staff_relation s on a.gldxbh = s.STAFF_CMS_CODE
            inner join F_USER v on s.staff_code = v.user_name 
            inner join BRANCH b on b.BRANCH_CODE = jgbh
            where A.glrq2 >to_char(current date,'yyyy-mm-dd') %s  
            order by a.PARA_ID desc
	    """%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={11:'DKTYPE'}
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
        return ["维护日期","员工信贷号", "员工姓名", "合同号","客户账号","客户名","客户内码","机构编号","归属比例","归属起始日期","归属结束日期","营销类型"]

    @property
    def page_size(self):
        return 10
