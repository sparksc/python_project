# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
参数类型查看
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['report_name']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
            select REPORT_NAME,REPORT_SCRIPT,REPORT_URL,REPORT_USER,ID
            from T_REPORT_MAG
            where 1=1 %s
            order by REPORT_NAME,id
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
        return ["报表名称","报表脚本","父菜单名称","员工工号筛选状态","操作"]

    @property
    def page_size(self):
        return 15
