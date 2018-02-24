# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
员工机构岗位查看
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['branch_name','group_name','user_name','startdate','enddate']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
			select u.user_name,u.name,y.branch_name,g.group_name,z.startdate,z.enddate,z.id from f_user u 
            inner join User_Branch x on x.user_id=u.role_id 
            inner join Branch y on y.role_id=x.branch_id
            inner join User_Group z on z.user_id=u.role_id
			inner join Group g on g.id=z.group_id
			where 1=1 %s
			order by u.role_id
	    """%(filterstr)
        
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)
    
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            print '------------------'
            print k,v
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ?"%k
                vlist.append(v)
        return filterstr,vlist


    def column_header(self):
		return ["用户编号", "用户名称","机构","岗位","开始时间","结束时间","操作"]

    @property
    def page_size(self):
        return 15
