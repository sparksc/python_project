# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config

"""
客户挂钩录入审批
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CUST_NO','MANAGER_NO','TYP','STATUS']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT c.ID, c.ETL_DATE, c.ORG_NO, d.ORG0_NAME, c.MANAGER_NO, s.NAME as user_NAME, c.CUST_NO, i.CUST_NAME, c.TYP,c.STATUS
                 FROM YDW.CUST_HOOK c
                 LEFT JOIN D_ORG d on d.org0_code=c.org_no 
                 LEFT JOIN f_user s on s.user_name=c.manager_no
                 LEFT JOIN D_CUST_INFO i on i.cust_no=c.cust_in_no
                 WHERE 1=1 %s ORDER BY ID"""%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and c.%s = ?"%k
                vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],"c.MANAGER_NO",'ORG_NO', None))
        return filterstr,vlist
    def column_header(self):
        return ["机构号","机构名","员工号","员工名","客户号","客户名","类型","状态"]

    @property
    def page_size(self):
        return 10
