# -*- coding:utf-8 -*-

from querybase import QueryBase, db2_pagination


class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
        return "select * from f_user"

    def column_header(self):
        return ["ROLE_ID", "USER_NAME", "NAME"]
