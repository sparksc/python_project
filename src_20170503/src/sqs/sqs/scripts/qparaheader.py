# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
参数类型查看
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['para_type_id','header_name','header_key','header_detail','header_type','header_status','header_order']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
            select header_name,header_key,header_type,header_detail,header_order,header_status,ID
            from T_PARA_header
            where 1=1 %s
            order by header_order
	    """%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)
    
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ? "%k
                vlist.append(v)
        return filterstr,vlist

    def column_header(self):
        return ["属性名","属性key","数据类型", "说明","属性顺序", "参数状态","操作"]

    @property
    def page_size(self):
        return 15
