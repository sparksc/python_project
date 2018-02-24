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
信用卡
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CUST_NO','MANAGER_NO','ORG_NO','STATUS','NOTE']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT c.ORG_NO, d.BRANCH_NAME, c.manager_no, s.name, c.ACCOUNT_NO, i.CUST_NAME,NOTE, c.ID 
                 FROM YDW.ACCOUNT_HOOK c
                 LEFT JOIN BRANCH d on d.branch_code=c.org_no 
                 LEFT JOIN F_USER s on s.user_name=c.manager_no
                 LEFT JOIN D_CUST_INFO i on i.cust_no=c.cust_in_no
                 WHERE typ='信用卡' and status in ('正常','已审批','预提交审批','待审批') %s ORDER BY ID"""%(filterstr)
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
                    vvv = self.dealfilterlist(v)
                    if self.top_branch_no not in vvv:
                        filterstr = filterstr +" and c.org_no in( %s ) "%(vvv)
                elif k == 'CUST_NO':
                    filterstr = filterstr + " and c.account_no =? "
                    vlist.append(v)
                elif k == 'NOTE':
                    filterstr = filterstr + " and note like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                elif k == 'MANAGER_NO':
                    filterstr = filterstr + " and manager_no = ? "
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'manager_no','c.org_no', None))
        return filterstr,vlist
    def column_header(self):
        return ["机构号","机构名","员工号","员工名","卡号","客户名","地址信息"]

    def trans_dec(self,num):
        tmp = Decimal(num)
        tmp = '{:,}'.format(tmp)
    @property
    def page_size(self):
        return 10
