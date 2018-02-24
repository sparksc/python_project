# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
绩效合约查看
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['pe_object','user_name','pe_freq','date']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
				select pe_type,b.branch_name,u.name,pe_freq,date,score,id
				from pe_contract pe
                inner join branch b on pe.pe_object=b.branch_code
				inner join f_user u on pe.pe_pic=u.role_id
				where 1=1 %s
				order by pe.id desc 
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
		return ["考核类型", "考核对象","负责人","考核周期","合约日期","合约总分","合约查看"]

    @property
    def page_size(self):
        return 15
