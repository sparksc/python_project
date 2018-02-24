# -*- coding:utf-8 -*-

import sys
from decimal import Decimal
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
                select a.ID,a.ETL_DATE,a.ORG_NO,o.BRANCH_NAME,a.MANAGER_NO,s.NAME,a.ACCOUNT_NO,i.CUST_NAME,nvl(a.BALANCE/100.00,0)  bal,a.NOTE,a.TYP,a.PERCENTAGE,a.STATUS 
                from account_hook a
                left join branch o on o.branch_code=a.org_no
                LEFT JOIN v_staff_info s on s.user_name=a.manager_no
                LEFT JOIN D_CUST_INFO i on i.cust_no=a.cust_in_no
                WHERE a.follow_cust='账号优先' and a.status='录入待审批' %s
                ORDER BY ID"""%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()

        row = list(row)
        for i in range(0,len(row)):
            row[i] = list(row[i])
            row[i][8] = self.trans_dec(('%.2f' % row[i][8]))

        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():

            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ?"%k
                vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],"a.manager_no",'a.ORG_NO', None))
        return filterstr,vlist
    def column_header(self):
        for k,v in self.args.items():
            if k=='TYP' and v=='存款':
                return ["机构号","机构名","员工号","员工名","账号","账户名","余额","地址","类型","分配比例","状态"]
            elif k=='TYP' and v=='理财':    
                return ["机构号","机构名","员工号","员工名","流水号","客户名","购买金额","地址","类型","分配比例","状态"]
        return ["机构号","机构名","员工号","员工名","账号","账户名","余额","地址","类型","分配比例","状态"]

    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        tmp = '{:,}'.format(tmp)
        return tmp

    @property
    def page_size(self):
        return 10
