# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from utils import config
"""
存款归属单笔维护
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ["ORG_NO","org_no", "manager_no","note", "account_no","typ","status","follow_cust"]
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select a.id,branch_code,branch_name,user_name,name,account_no,i.cust_name,note from account_hook a  
                join branch o on o.branch_code=a.org_no
                join f_user s on s.user_name=a.manager_no
                LEFT JOIN D_CUST_INFO i on i.cust_no=a.cust_in_no
                where 1=1 %s
                order by id desc
            """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'ORG_NO':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and o.branch_code in ( %s ) "%(vvv)
                elif k == 'org_no':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and o.branch_code in ( %s ) "%(vvv)
                elif k == 'note':
                    filterstr = filterstr + " and note like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['transfer'],'a.manager_no','a.org_no', None))
        return filterstr,vlist
    def column_header(self):
        return ["序号","机构号","机构名","员工号","员工名","卡号","客户名","地址信息","操作"]

    @property
    def page_size(self):
        return 15
