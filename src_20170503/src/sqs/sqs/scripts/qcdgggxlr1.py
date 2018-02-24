# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
贷款营销录入
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['GLDXBH','DXMC','DXBH','FJDXBH','NO_CHECK_STATUS','CHECK_STATUS','STATUS']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
            SELECT drrq,A.GLDXBH,v.name,fjdxbh,dxmc,b.branch_name,dxbh,A.GLJE1,A.GLRQ1,A.GLRQ2,gggx,status,check_status,A.PARA_ID 
            FROM T_ZJC_GSGX_CDK A 
            inner join Staff_relation s on a.gldxbh = s.STAFF_CMS_CODE
            inner join F_USER v on s.staff_code = v.user_name 
            inner join BRANCH b on b.BRANCH_CODE = jgbh
            where (glrq2 >to_char(current date,'yyyy-mm-dd') or check_status in ('0','2','3')) %s  
            order by a.PARA_ID desc
	    """%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={11:'CD_ST',12:'CD_CK_ST'}
        return self.translate(row,needtrans)
    
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k=='NO_CHECK_STATUS':
                    filterstr = filterstr+" and %s <> ?"%k[3:]
                else:
                    filterstr = filterstr+" and %s = ?"%k
                vlist.append(v)
        return filterstr,vlist


    def column_header(self):
        return ["维护日期","员工信贷号", "员工姓名","客户内码","客户名","机构","存款账号","归属比例","挂钩起始日期","挂钩结束日期","挂钩关系","状态","复核状态"]

    @property
    def page_size(self):
        return 10
