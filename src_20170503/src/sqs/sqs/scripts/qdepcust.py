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
存款 客户号
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CST_TYP','CUST_NO','MANAGER_NO','ORG_NO','STATUS','NOTE']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT c.ORG_NO, d.BRANCH_NAME, c.manager_no, s.name,CASE WHEN left(c.cust_in_no,2)='81' THEN '对私' WHEN left(c.cust_in_no,2)='82' THEN '对公' END SIGN, c.CUST_NO, i.CUST_NAME,c.percentage,nvl(c.balance/100.00,0),nvl(c.add_avg_balance/100.00,0),NOTE,c.ID 
                 FROM YDW.CUST_HOOK c
                 JOIN BRANCH d on d.branch_code=c.org_no 
                 JOIN F_USER s on s.user_name=c.manager_no
                 JOIN D_CUST_INFO i on i.cust_no=c.cust_in_no
                 WHERE typ='存款' and s.name is not null and status in ('正常','已审批','预提交审批','待审批') %s ORDER BY ID DESC"""%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        row = list(row)
        for i in range(0,len(row)):
            row[i] = list(row[i])
            row[i][8] =self.trans_dec('%.2f' % row[i][8])
            row[i][9] =self.trans_dec('%.2f' % row[i][9])
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():

            if v and k in self.filterlist:
                if k == 'ORG_NO':
                    vvv = self.dealfilterlist(v)
                    if self.top_branch_no not in vvv:
                        filterstr = filterstr +" and c.org_no in( %s ) "%(vvv)
                elif k == 'CUST_NO':
                    filterstr = filterstr + " and c.cust_no = ? "
                    vlist.append(v)
                elif k == 'NOTE':
                    filterstr = filterstr + " and note like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                elif k == 'MANAGER_NO':
                    filterstr = filterstr + " and manager_no = ? "
                    vlist.append(v)
                elif k == 'CST_TYP':
                    if v == u'对公':
                        filterstr = filterstr + " and  left(c.cust_in_no,2)='82' "
                    elif v == u'对私':
                        filterstr = filterstr + " and  left(c.cust_in_no,2)='81' "
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'manager_no','c.org_no', None))
        return filterstr,vlist
    def column_header(self):
        return ["机构号","机构名","员工号","员工名","公私类型","客户号","客户名","占比(%)","余额(元)","当前日均(元)","地址信息"]

    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        xxx = '{:,}'.format(tmp)
        return xxx
    @property
    def page_size(self):
        return 10
