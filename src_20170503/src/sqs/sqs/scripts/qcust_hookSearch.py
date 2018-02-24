# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
正常客户挂钩
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['org_no','cust_no','manager_no','hook_type','status','typ']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""select org_no,hook_type,cust_no,manager_no,start_date,end_date,percentage,status from cust_hook 
                where status='正常' %s
                order by org_no
        """%(filterstr)
        
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
        return filterstr,vlist
    def column_header(self):
        return ["机构","营销类型","客户号","客户经理","起始日期","结束日期","管理比例", "关系状态"]

    @property
    def page_size(self):
        return 15
