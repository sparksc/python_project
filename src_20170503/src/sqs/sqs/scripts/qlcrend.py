# -*- coding:utf-8 -*-

import sys
from decimal import Decimal
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
理财待认定
"""

class Query(ObjectQuery):

    def prepare_object(self):

        self.filterlist = ['CUST_NO','ORG_NO','NOTE','CST_TYP','YD','LD','CUST_NAME','hide']
        filterstr,vlist,filterstr2,vlist2 = self.make_eq_filterstr()
        sql1 =u"""
                select c.id,c.org_no,o.branch_name, c.cust_no,i.cust_name,c.percentage,nvl(balance/100.00,0) bal,nvl(add_avg_balance/100.00,0) pdt,c.note, c.cust_in_no
                from cust_hook c
                join branch o on o.branch_code=c.org_no
                join d_cust_info i on i.cust_no=c.cust_in_no
                where c.typ='理财' and c.status='待手工' %s
                order by c.id desc
               """%(filterstr)
        print sql1
        row1 = self.engine.execute(sql1,vlist).fetchall()

        row = list(row1)
        for i in range(0,len(row)):
            row[i] = list(row[i])
            row[i][5] =self.trans_dec('%.2f' % row[i][5])
            row[i][6] =self.trans_dec('%.2f' % row[i][6])

        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr,filterstr2 ="",""
        vlist,vlist2 = [],[]
        for k,v in self.args.items():
            #if k == 'login_teller_no':
            #    if self.deal_teller_query_auth(v) == True:
            #        filterstr = filterstr+" and c.manager_no = '%s'"%v
            if k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False :
                    filterstr = filterstr+" and c.org_no in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'ORG_NO':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and c.org_no in ( %s ) "%(vvv)
                elif k == 'CUST_NO':
                    filterstr = filterstr + " and c.cust_no =? "
                    vlist.append(v)
                elif k == 'NOTE':
                    filterstr = filterstr + " and c.note like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                elif k == 'LD':
                    filterstr = filterstr + " and balance/1000000 >= ? "
                    vlist.append(v)
                elif k == 'hide':
                    filterstr = filterstr + 'and c.hide = ?'
                    vlist.append(v.strip())
                elif k == 'YD':
                    filterstr = filterstr + " and add_avg_balance/1000000 >= ? "
                    vlist2.append(v)
                elif k=='CUST_NAME':
                    filterstr = filterstr + " and i.CUST_NAME like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                
        return filterstr,vlist,filterstr2,vlist2
    def column_header(self):
        return ["机构号","机构名","客户号","客户名","占比(%)","总购买金额(元)","当前日均(元)","地址信息","操作"]
    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        tmp = '{:,}'.format(tmp)
        return tmp

    @property
    def page_size(self):
        return 10
