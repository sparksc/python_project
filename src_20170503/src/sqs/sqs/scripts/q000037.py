# -*- coding:utf-8 -*-
#存贷款流失参数
from querybase import QueryBase, db2_pagination


class Query(QueryBase):

    @db2_pagination()
    def prepare_sql(self):
        print self.args
        sql = """select s2.name,s2.user_name,s1.staff_sop_code,s1.staff_cms_code,d1.dict_value,d2.dict_value,d3.dict_value,d4.dict_value,s1.id from staff_relation s1 left join f_user s2 on s1.staff_code=s2.user_name inner join dict_data d1 on d1.dict_type = 'IS_KHJL' and d1.dict_key = s1.is_khjl inner join dict_data d2 on d2.dict_type = 'IS_ZHGY' and d2.dict_key = s1.is_zhgy inner join dict_data d3 on d3.dict_type = 'IS_KJZG' and d3.dict_key = s1.is_kjzg inner join dict_data d4 on d4.dict_type = 'IS_ZHHZ' and d4.dict_key = s1.is_zhhz """
       # print type(unicode(self.args.get('ygxm')))
       # print unicode(self.args.get('ygxm'))
       # print self.args.get('ygxm')
        rs =[]
        if self.args is not None:
            sql+=""" where"""
            for k in self.args:
                if k!='total_count' and k!='page':
                    sql+=" %s=? and"%(k)
                    rs.append(self.args.get(k))
            sql+=" 1=1 order by s1.id"
#        if self.args.get('ygxm'):
#            sql+=""" s2.name = ? and"""
#            rs.append()
#        if self.args.get('yggh'):
#            sql+=""" s2.user_name = '"""+self.args.get('yggh')+"""' and"""
#        if self.args.get('hxgh'):
#            sql+=""" s1.staff_sop_code = '"""+self.args.get('hxgh')+"""' and"""
#        if self.args.get('xdgh'):
#            sql+=""" s1.staff_cms_code = '"""+self.args.get('xdgh')+"""' and"""
#        sql+=""" 1=1 order by s1.id"""
        print rs
        print sql
        return sql,rs
    def column_header(self):
        return ["员工姓名", "员工工号", "核心工号","信贷工号","是否客户经理","是否综合柜员","是否会计主管","是否支行行长"]

    @property
    def page_size(self):
        return 10 
