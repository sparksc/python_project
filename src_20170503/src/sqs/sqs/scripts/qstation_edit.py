# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
岗位查询
"""

class Query(ObjectQuery):
  
    def prepare_object(self):
        filterlist1 = ['type_name','group_name']
        filterstr,vlist = self.make_eq_filterstr(filterlist1)
        sql1="""
        select g.id,g.group_name,t.type_name,g.GROUP_TYPE_CODE,t.type_code 
        from group g 
        inner join group_type t on t.type_code=g.group_type_code
        where 1=1 %s
        order by g.id
        """%(filterstr)
        row = self.engine.execute(sql1,vlist).fetchall()
        needtrans={}
        resultrow=[]
        i=0
        if(len(row)>0):
            while True:
                r1=row[i][0]
                r2=row[i][1]
                r3=row[i][2]
                r4=row[i][3]
                r5=row[i][4]
                resultrow.append((r1,r2,r3,r4,r5))
                i=i+1
                if i>=len(row):
                    break
        return self.translate(resultrow,needtrans)
        
    def make_eq_filterstr(self,filterlist):
        filterstr =""
        vlist = []
        print(self.args.items(),">>>>>>>>>>>>>>>>>>")
        for k,v in self.args.items():
            if v and k in filterlist:
                if(k=='type_name'):
                    filterstr = filterstr+" and t.type_name = ? "
                    vlist.append(v)
                if(k=='group_name'):
                    filterstr = filterstr+" and g.group_name = ? "
                    vlist.append(v)
            
        return filterstr,vlist


    def column_header(self):
        return ["参数编号", "参数名称","参数类型","操作"]
    @property
    def page_size(self):    
        return 15
