# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config
"""
etc分配界面
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['cust_no','org','cust_name']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select a.id,branch_code,branch_name,manager_no,a.cust_no,d.cust_name,typ 
                from cust_hook a  
                join d_cust_info d on d.cust_no=a.cust_in_no
                join branch o on o.branch_code=a.org_no
                where status='待分配' and typ='电子银行' and sub_typ='ETC' %s
                order by id desc
            """%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        print sql
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            print k,v
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and branch_code in (%s) "%(vvv)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'manager_no','branch_code', None))
        return filterstr,vlist
    def column_header(self):
        return ["序号","机构号","机构名","员工号","客户号","客户名","类型",""]

    @property
    def page_size(self):
        return 15
