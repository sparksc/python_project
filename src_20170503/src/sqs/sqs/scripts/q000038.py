# -*- coding:utf-8 -*-
#核心工号关系维护新增查询可添加关系用户

from querybase import QueryBase, db2_pagination


class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
        print self.args
        return u"select f.user_name,f.name from f_user f where f.user_name not in (select staff_code from staff_relation)"

    def column_header(self):
        return ["A", "B", "C"]

    @property
    def page_size(self):
        return 3
