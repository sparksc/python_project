# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config

"""
批量任务查询
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['from_teller_no','is_cust','to_teller_no','hook_typ','deal_status','typ','to_branch_no']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select id, from_teller_no,u.name, to_teller_no,u2.name, hook_typ, typ, total_count,total_amount, deal_status 
                from cust_hook_batch c
                join f_user u on u.user_name=c.from_teller_no
                join f_user u2 on u2.user_name=c.to_teller_no
                join branch b on b.branch_code=c.to_branch_no
                where 1=1 %s
                order by id desc
        """%(filterstr)
        
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
                filterstr = filterstr+" and %s = ?"%k
                vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'to_branch_no', None))
        return filterstr,vlist
    def column_header(self):
        return ["批次号", "移交柜员","移交柜员名", "接收柜员","接收柜员名", "挂钩类型", "业务类型", "总笔数","总金额","审批状态"]

    @property
    def page_size(self):
        return 15
