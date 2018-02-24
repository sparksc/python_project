# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
参数类型查看
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['type_status','type_name','type_key','type_module']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
            select type_module,TYPE_NAME,type_key, TYPE_DETAIL, TYPE_STATUS,ID
            from T_PARA_TYPE
            where 1=1 %s
            order by type_module,id
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
        return ["模块","参数名","参数key", "参数说明", "参数状态","id","操作"]

    @property
    def page_size(self):
        return 15
