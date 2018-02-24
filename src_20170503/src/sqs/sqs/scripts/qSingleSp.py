# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
单笔分润移交查询
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['id','from_teller_no','to_teller_no','hook_typ','status','typ']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select id,account_no,from_teller,to_teller,percentage,balance,status,note 
                from HOOK_SINGLE_MOVE
                where 1=1 %s
                order by id
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
        return ["批次号","账户","移交柜员", "接收柜员", "占比", "账户余额","状态", "审批备注"]

    @property
    def page_size(self):
        return 15
