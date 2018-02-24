# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
存款审批
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['ACCOUNT_NO','MANAGER_NO','TYP','STATUS', 'BATCH_ID']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                (SELECT ah.ID, MANAGER_NO, ACCOUNT_NO,d.cust_name, ORG_NO, PERCENTAGE, ah.TYP,ah.STATUS 
                FROM YDW.ACCOUNT_HOOK ah 
                JOIN YDW.CUST_HOOK_BATCH ch on ah.batch_id = ch.id
                left JOIN d_cust_info d on d.cust_no=ah.cust_in_no
                WHERE 1=1 %s ORDER BY ah.ID)
                UNION
                (SELECT ah.ID, MANAGER_NO, ah.CUST_NO,d.cust_name, ORG_NO, PERCENTAGE,  ah.TYP,ah.STATUS 
                FROM YDW.CUST_HOOK ah
                JOIN YDW.CUST_HOOK_BATCH ch on ah.batch_id = ch.id  
                left JOIN d_cust_info d on d.cust_no=ah.cust_in_no 
                WHERE 1=1 %s ORDER BY ah.ID)
                """%(filterstr,filterstr)
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
                if k == 'BATCH_ID':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ch.id = ? "
                    vlist.append(v)
                    vlist.append(v)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["编号","员工号","账号/客户号","客户名","机构编号","分配比例","类型","状态"]

    @property
    def page_size(self):
        return 10
