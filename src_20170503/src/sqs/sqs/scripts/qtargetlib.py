# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
指标库
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = []
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
			select pei_freq,type,name,object_type,desc,data_src,pei_id from pe_pei_def  
			where 1=1 %s
			order by pei_id
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
		return ["指标周期", "指标类型","指标名称","对象类型","指标描述","数据来源","操作"]

    @property
    def page_size(self):
        return 15
