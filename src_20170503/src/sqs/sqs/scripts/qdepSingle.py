# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
存款账户单笔分润转移
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['manager_no','org_no','typ']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select a.etl_date,o.org0_code,o.org0_name,s.SALE_CODE,s.SALE_NAME,d.ACCOUNT_NO,d.CST_NAME,(a.PERCENTAGE - nvl(h.PER,0)) PER,f.BALANCE bal,note,a.id
                from f_balance f
                join d_account d on d.ID=f.ACCOUNT_ID
                join account_hook a on a.ACCOUNT_NO=d.ACCOUNT_NO
                join d_sales_temp s on s.SALE_CODE=a.manager_no
                join d_org o on o.id=f.org_id
                left join (select move_id,sum(percentage) per from HOOK_SINGLE_MOVE group by move_id) h on h.move_id=a.id 
                where a.TYP='存款' and a.status='正常' and f.DATE_ID=20150104 and f.ACCT_TYPE=1 %s
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
                filterstr = filterstr+" and %s = ?"%k
                vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["日期","机构号","机构名","员工号","员工名","帐号","客户名","占比(%)","余额","地址信息"]

    @property
    def page_size(self):
        return 10
