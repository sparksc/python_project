# -*- coding:utf-8 -*-

from decimal import Decimal
from objectquery import ObjectQuery
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
"""
客户号查询详情
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['ID','ORG','MANAGER','TYP']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
            select a.ACCOUNT_NO,a.PERCENTAGE,a.org_no, s.user_name,s.name,nvl(a.BALANCE/100.00,0) bal,nvl(a.add_avg_balance/100.00,0)
            from account_hook a
            join cust_hook t on a.cust_in_no=t.cust_in_no and t.org_no = a.org_no
            join f_user s on s.user_name=a.manager_no 
            join branch o on o.branch_code=a.org_no
            where a.status in ('正常','已审批','预提交审批','待审批') and a.follow_cust='客户号优先' %s
            """%(filterstr)
        print sql
        print vlist
        row = self.engine.execute(sql,vlist).fetchall()
        row = list(row)
        for i in range(0,len(row)):
            row[i] = list(row[i])
            row[i][5] = self.trans_dec(('%.2f' % row[i][5]))
            row[i][6] = self.trans_dec(('%.2f' % row[i][6]))

        needtrans = {}
        return self.translate(row,needtrans)
    
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'ID':
                    filterstr = filterstr + " and t.id = ? "
                    vlist.append(v)
                if k == 'ORG':
                    filterstr = filterstr + " and o.branch_code = ? "
                    vlist.append(v)
                if k == 'MANAGER':
                    filterstr = filterstr + " and a.manager_no = ? "
                    vlist.append(v)
                if k == 'TYP':
                    filterstr = filterstr + " and t.typ = ? and a.typ = ?"
                    vlist.append(v)
                    vlist.append(v)
        return filterstr,vlist


    def column_header(self):
        return ["账户号/流水号","占比(%)", "机构号","员工号","员工名","余额(元)","当前日均(元)"]

    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        tmp = '{:,}'.format(tmp)
        return tmp
    @property
    def page_size(self):
        return 20
