# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from utils import config
"""
员工所有业绩查询,包括客户挂钩和账号挂钩
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ["org", "manager_no"]
        filterstr,vlist = self.make_eq_filterstr()
        sql1 =u"""
                select a.id,branch_code,s.user_name,s.name,a.cust_no,d.cust_name,typ, percentage,'客户优先',a.cust_in_no
                from cust_hook a  
                left join branch o on o.branch_code=a.org_no
                left join f_user s on s.user_name=a.manager_no
                left join D_CUST_INFO d on d.cust_no=a.cust_in_no
                where a.status in ('正常') %s
                order by id desc
            """%(filterstr)
        row1 = self.engine.execute(sql1,vlist).fetchall()

        sql2 =u"""
                select a.id,a.org_no,s.user_name,s.NAME,a.ACCOUNT_NO,d.cust_name,a.TYP,a.PERCENTAGE,a.follow_cust,a.cust_in_no
                from account_hook a               
                left join branch o on o.branch_code=a.org_no
                left join f_user s on s.user_name=a.manager_no
                left join D_CUST_INFO d on d.cust_no=a.cust_in_no
                where a.follow_cust='账号优先' and a.status in ('正常') %s
                order by id desc
            """%(filterstr)
        row2 = self.engine.execute(sql2,vlist).fetchall()
        ebank_dict = {}
        row = []
        for r in row1:
            if r[6] == u'电子银行':
                if ebank_dict.get(r[9]) is not None:
                    continue
                else:
                    ebank_dict[r[9]] = 1
                    row.append(r)
            else:
                row.append(r)

        for r in row2:
            row.append(r)

        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and a.org_no in ( %s ) "%(vvv)
                elif k == 'manager_no':
                    filterstr = filterstr +" and a.manager_no = ? "
                    vlist.append(v)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['transfer'],'a.manager_no','a.org_no', None))
        return filterstr,vlist
    def column_header(self):
        return ["序号","机构号","员工号","员工名","客户号/账号","名称", "业务类型", "占比(%)", "优先级", "操作"]

    @property
    def page_size(self):
        return 15
