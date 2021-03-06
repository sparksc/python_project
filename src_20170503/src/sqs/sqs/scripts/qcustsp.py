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
        sql =u"""SELECT c.ID, c.ETL_DATE, c.ORG_NO, d.BRANCH_NAME, c.MANAGER_NO, s.name, CASE WHEN left(i.cust_no,2)='81' THEN '对私' WHEN left(i.cust_no,2)='82' THEN '对公' END SIGN, c.CUST_NO, i.CUST_NAME,c.NOTE, c.TYP, c.PERCENTAGE,c.STATUS,c.CUST_IN_NO 
                 FROM YDW.CUST_HOOK c
                 LEFT JOIN BRANCH d on d.branch_code=c.org_no 
                 LEFT JOIN v_staff_info s on s.user_name=c.manager_no
                 LEFT JOIN D_CUST_INFO i on i.cust_no=c.cust_in_no
                 WHERE 1=1 %s ORDER BY ID"""%(filterstr)
        print sql
        print vlist
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
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],"manager_no",'ORG_NO', None))
        return filterstr,vlist
    def column_header(self):
        for k,v in self.args.items():
            if k=='TYP' and v=='存款':
                return ["机构号","机构名","员工号","员工名","公私标志","客户号","客户名","地址","类型","分配比例","状态"]
            elif k=='TYP' and v=='理财':    
                return ["机构号","机构名","员工号","员工名","公私标志","客户号","客户名","地址","类型","分配比例","状态"]
        return ["机构号","机构名","员工号","员工名","公私标志","客户号","客户名","地址","类型","分配比例","状态"]

    @property
    def page_size(self):
        return 100
