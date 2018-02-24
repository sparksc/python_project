# -*- coding:utf-8 -*-
# 存贷款流失参数
from querybase import QueryBase, db2_pagination


class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
        print self.args
        return "select dict_data.dict_value,jyje,para_id from T_JGC_JXKH_CS_LIUSHI inner join dict_data on dict_type = 'CORD' and T_JGC_JXKH_CS_LIUSHI.sjlx = dict_data.dict_key order by para_id"

    def column_header(self):
        return ["数据类型", "金额", "操作"]

    @property
    def page_size(self):
        return 15
