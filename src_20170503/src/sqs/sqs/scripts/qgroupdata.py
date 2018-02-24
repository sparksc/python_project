# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
    数据权限 
"""
class Query(ObjectQuery):
    def prepare_object(self):
        filterlist =['group_name','data_type','auth_type']
        filterstr,vlist = self.make_eq_filterstr(filterlist)
        sql =u"""
        select f.id,f.group_id,g.group_name,f.data_type,f.auth_type
        from group_data f
        join group g on g.id=f.group_id
        where 1=1 %s 
        order by g.group_name
        """%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans = {3:"data_type",4:"auth_type"}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self,filterlist):
        filterstr =u""
        vlist=[]
        for k,v in self.args.items():
            if k == 'group_name':
                filterstr=filterstr+"and g.%s = ?"%k
                vlist.append(v)
            if k == 'data_type':
                filterstr=filterstr+"and f.%s = ?"%k
                vlist.append(v)
            if k == 'auth_type':
                filterstr=filterstr+"and f.%s = ?"%k
                vlist.append(v)
        return filterstr,vlist

    def column_header(self):
        return ["岗位名称","数据类型","权限类型","操作"]

    @property
    def page_size(self):
        return 15
                

