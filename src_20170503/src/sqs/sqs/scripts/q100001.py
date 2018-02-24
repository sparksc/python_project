# -*- coding:utf-8 -*-

from objectquery import ObjectQuery


class Query(ObjectQuery):

    def prepare_object(self):
        rows = self.engine.execute(
            "select * from menu order by id asc").fetchall()
        return [list(row) for row in rows]

    def column_header(self):
        return ["A", "B", "C"]

    @property
    def page_size(self):
        """

        """
        return 3

    def object_to_json(self, src_object):
        """
        对象如果不能使用默认JSON序列化的方法，请覆盖此方法
        """
        return ObjectQuery.object_to_json(self, src_object)
