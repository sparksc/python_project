
# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
pos录入
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['ORG_NO', 'ATM_NO','STATUS']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
        select org_no,atm_no,typ,sub_typ,addr,status,end_date,id 
        from D_ATM where 1=1 %s order by id desc
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
                    filterstr = filterstr + " and org_no=?"
                    vlist.append(v.strip())
                elif k == 'ATM_NO':
                    filterstr = filterstr + " and atm_no=?"
                    vlist.append(v.strip())
                elif k == 'STATUS':
                    filterstr = filterstr + " and status=?"
                    vlist.append(v.strip())
        return filterstr,vlist
    def column_header(self):
        return ["机构号","机具编号","类型","附离","安装地址","状态","销户时间"]

    @property
    def page_size(self):
        return 10
