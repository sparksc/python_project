# -*- coding:utf-8 -*-

from querybase import QueryBase, db2_pagination


class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
        print self.args
        sql = "select id,group_name from GROUP"
        rs =[]
        if self.args is not None:
            sql+=" where"
            for k in self.args:
                if k!='total_count' and k!='page':
                    sql+=" %s=? and"%(k)
                    rs.append(self.args.get(k))
            sql+=" 1=1 order by id"
        print rs
        print sql
        return sql,rs
                        
    def column_header(self):
        return ["岗位编号", "岗位名称"]
