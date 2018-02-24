# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
查询所有页面
"""

class Query(ObjectQuery):
 
    def prepare_object(self):
        self.filterlist = ['m_name']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
             SELECT m.id,m.name,m.location,m.parent_id from menu m where 1=1 %s
             order by m.id 
            """%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        print(sql)
        print(vlist)
        return self.translate(row,needtrans)
    def make_eq_filterstr(self):
        filterstr = ""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s like"%(k.replace('_','.'))+" '%'||"+"?"+"||'%'"
                vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["ID","名字","location","parentID","操作"]
    @property
    def page_size(self):
        return 15
