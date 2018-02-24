# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from utils import config
"""
客户层面转移
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ["ORG_NO", "manager_no", "cust_no","typ","status","note","notnote"]
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
            select c.id,org_no,o.branch_name,c.manager_no,u.name,c.cust_no,d.cust_name,note
            from cust_hook c
            join branch o on o.branch_code=c.org_no
            join f_user u on u.user_name=c.manager_no
            join d_cust_info d on d.cust_no=c.cust_in_no
            where typ='电子银行' %s
            """%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'note':
                    filterstr = filterstr + " and note like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                elif k == 'notnote':
                    for n1 in v.replace("，",",").split(","):
                        filterstr = filterstr + " and c.note not like " + " '%'||"+"?"+"||'%' "
                        vlist.append(n1)
                elif k == 'org_no' or k == 'ORG_NO':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and c.org_no in ( %s ) "%(vvv)
                else:
                    filterstr = filterstr+" and c.%s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['transfer'],'c.manager_no','c.org_no', None))
        return filterstr,vlist
    def column_header(self):
        return ["序号","机构号","机构名","员工号","员工名","客户号","客户名","地址信息","操作"]

    @property
    def page_size(self):
        return 15
