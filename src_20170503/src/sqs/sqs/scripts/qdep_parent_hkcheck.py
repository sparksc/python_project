# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
汇集户挂钩检查
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['account_no','org_no','typ']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select account_no
                from parent_hook
                where status not in ('失效') %s 
                group by account_no
                having sum(percentage)=100
                """%(filterstr)
        
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        print row
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                print k,v
                if k == 'account_no':
                    filterstr = filterstr + " and account_no = ? "  
                    vlist.append(v)
                elif k == 'org_no':
                    filterstr = filterstr + " and org_no = ? "  
                    vlist.append(v)
                elif k == 'typ':
                    filterstr = filterstr + " and typ = ? "  
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return [""]

    @property
    def page_size(self):
        return 10
