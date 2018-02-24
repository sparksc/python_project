# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config

"""
账户挂钩审批
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['ACCOUNT_NO','MANAGER_NO','TYP','STATUS']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select a.ID,ETL_DATE,ORG_NO,ORG0_NAME,MANAGER_NO,s.name,ACCOUNT_NO,TYP,STATUS 
                from account_hook a
                left join D_ORG o on o.org0_code=a.org_no
                left join f_user s on s.user_name=a.MANAGER_NO
                WHERE 1=1 %s
                ORDER BY ID"""%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():

            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ?"%k
                vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],"c.MANAGER_NO",'ORG_NO', None))
        return filterstr,vlist
    def column_header(self):
        for k,v in self.args.items():
            if k=='TYP' and v=='信用卡':
                return ["机构号","机构名","推广员工号","推广员工名","卡号","类型","状态"]
            elif k=='TYP':
                return ["机构号","机构名","员工号","员工名","账号","类型","状态"]
        return ["机构号","机构名","员工号","员工名","账号","类型","状态"]

    @property
    def page_size(self):
        return 10
