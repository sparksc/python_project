# -*- coding:utf-8 -*-
#核心工号关系维护新增查询可添加关系用户

from querybase import QueryBase, db2_pagination


class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
        print self.args
        return u"select f.user_name,f.name,d.dict_value,f.role_id from f_user f inner join dict_data d on d.dict_type ='WS' and d.dict_key = f.work_status order by f.role_id"

    def column_header(self):
        return ["员工工号", "员工姓名", "工作状态"]

    @property
    def page_size(self):
        return 10
