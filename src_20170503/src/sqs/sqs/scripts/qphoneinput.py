# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
手机e银行录入
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['yggh','drrq','jgbh']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
                select drrq,jgbh,branch_name,yggh,ygxm,sj_fzs,sj_hys,eyh,eyhhy,id from t_jgc_jxkh_lr_qm a
                inner join branch b on b.branch_code=jgbh
				where sjlx='4' %s 
				order by drrq desc 
	    """%(filterstr)
        
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
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
		return ["维护日期", "机构编号","机构名称","员工工号","员工姓名","手机发展数","手机活跃数","e银行","e银行活跃数","操作"]

    @property
    def page_size(self):
        return 15
