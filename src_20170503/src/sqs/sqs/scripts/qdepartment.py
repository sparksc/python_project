# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
部门机构查询
"""

class Query(ObjectQuery):
  
    def prepare_object(self):
        filterlist1 = ['branch_name','group_name']
        filterstr,vlist = self.make_eq_filterstr(filterlist1)
        sql1="""
        select bg.ID,b.BRANCH_NAME,g.GROUP_NAME,b.ROLE_ID,g.ID from BRANCH_GROUP bg
        join BRANCH b on b.ROLE_ID=bg.BRANCH_ID
        join "GROUP" g on g.ID=bg.GROUP_ID
        where 1=1 %s
        order by bg.id
        """%(filterstr)
        row = self.engine.execute(sql1,vlist).fetchall()
        print row
        needtrans={}
        return self.translate(row,needtrans)
        
    def make_eq_filterstr(self,filterlist):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in filterlist:
                filterstr = filterstr+" and %s = ? "%k
                vlist.append(v)
            
        return filterstr,vlist


    def column_header(self):
        return ["编号", "机构名称","部门名称","操作"]
    @property
    def page_size(self):    
        return 15
