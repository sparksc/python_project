# -*- coding:utf-8 -*-

from decimal import Decimal
from objectquery import ObjectQuery
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
"""
理财流水号详情
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SALE_CODE','CUST_NO','DATE','ORG']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
        select a.account_no,a.percentage,a.org_no,nvl(a.balance/100.00,0),a.status,d.user_name,d.name
        from account_hook a 
        join cust_hook t on t.CUST_IN_NO=a.cust_in_no
        join branch o on o.branch_code=a.org_no
        join f_user d on d.user_name=a.MANAGER_NO
        where a.typ='理财' and t.typ='理财' %s
	    """%(filterstr)
        print sql
        print vlist
        row = self.engine.execute(sql,vlist).fetchall()
        row = list(row)
        for i in range(0,len(row)):
            row[i] = list(row[i])
            row[i][3] = self.trans_dec(('%.2f' % row[i][3]))

        needtrans = {}
        return self.translate(row,needtrans)
    
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                #if k == 'DATE':
                #    filterstr = filterstr + " and f.date_id = ? " 
                #    vlist.append(v)
                if k == 'SALE_CODE':
                    filterstr = filterstr + " and t.manager_no = ? "
                    vlist.append(v)
                if k == 'CUST_NO':
                    filterstr = filterstr + " and t.cust_no = ? "
                    vlist.append(v)
                if k == 'ORG':
                    filterstr = filterstr + " and o.branch_code = ? "
                    vlist.append(v)
        return filterstr,vlist


    def column_header(self):
        return ["流水号","占比(%)", "机构号","余额","状态","员工号","员工名"]

    def trans_dec(self,num):
        tmp = Decimal(num)
        tmp = '{:,}'.format(tmp)
        return tmp
    @property
    def page_size(self):
        return 20
