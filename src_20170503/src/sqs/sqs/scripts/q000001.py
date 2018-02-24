# -*- coding:utf-8 -*-

from querybase import QueryBase, db2_pagination


class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
        print self.args
        return u"select * from menu"
        # return u"select * from menu where name like ? and id=?", [u"%储蓄%", 3]

    def column_header(self):
        return ["A", "B", "C"]

    @property
    def page_size(self):
        return 3
