# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config

"""
存款客户号转移数据
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['cust_no','ORG_NO','manager_no','note','status','cst_typ','ld','notnote']
        filterstr,vlist,filterstr2,vlist2 = self.make_eq_filterstr()
        sql1 =u"""
        select 
        sum(nvl(balance/100.00,0)),sum(nvl(add_avg_balance/100.00,0)),count(*)
        from cust_hook c
        join f_user u on u.user_name=c.manager_no
        join branch o on o.branch_code=c.org_no
        join d_cust_info i on i.cust_no=c.cust_in_no
        where c.typ='存款' %s 
               """%(filterstr)
        row1 = self.engine.execute(sql1,vlist).fetchall()

        row = list(row1)
        for i in range(0,len(row)):
            row[i] = list(row[i])
            if row[i][0] is  None:
                row[i][0]=0
            row[i][0] =self.trans_dec('%.2f' % row[i][0])
            if row[i][1] is  None:
                row[i][1]=0
            row[i][1] =self.trans_dec('%.2f' % row[i][1])

        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr,filterstr2 ="",""
        vlist,vlist2 = [],[]
        for k,v in self.args.items():

            if v and k in self.filterlist:
                if k == 'ORG_NO':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and c.org_no in ( %s ) "%(vvv)
                elif k == 'note':
                    filterstr = filterstr + " and c.note like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                elif k == 'notnote':
                    for n1 in v.split(","):
                        filterstr = filterstr + " and c.note not like " + " '%'||"+"?"+"||'%' "
                        vlist.append(n1)
                else:
                    filterstr = filterstr+" and c.%s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['transfer'],'c.manager_no','c.org_no', None))        
        return filterstr,vlist,filterstr2,vlist2
    def column_header(self):
        return ["机构号","机构名","员工号","员工名","公私类型","客户号","客户名","占比(%)","余额(元)","当前日均(元)","地址信息"]

    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        xxx = '{:,}'.format(tmp)
        return xxx
    @property
    def page_size(self):
        return 10
