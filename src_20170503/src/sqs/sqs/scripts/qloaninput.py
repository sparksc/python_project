# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
百元贷款收息率
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['drrq','jgbh']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
                select drrq,jgbh,branch_name,bytdl,id from t_jgc_jxkh_lr_qm a
                inner join branch b on b.branch_code=jgbh
				where sjlx='7' %s 
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
		return ["统计日期", "机构编号","机构名称","收息率","操作"]

    @property
    def page_size(self):
        return 15
