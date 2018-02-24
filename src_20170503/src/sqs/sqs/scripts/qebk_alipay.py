# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config
"""
电子银行 - 支付宝快捷支付
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CUST_NO','MANAGER_NO','ORG_NO','STATUS','NOTE']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
        select c.org_no,o.branch_name,c.manager_no,u.name,f.NET_CST_NO,c.cust_no,d.cust_name,note,nvl(d.TEL_CORE,'无') as tel_no,f.BUSI_TYPE,f.sub_type,f.open_date,f.STATUS
        from cust_hook c 
        join branch o on o.branch_code=c.org_no
        join f_user u on u.user_name=c.manager_no
        join d_cust_info d on d.cust_no=c.cust_in_no
        join ebank_info f on  c.CUST_NO=f.CUST_NO and c.ORG_NO=f.ORG_NO 
        where c.typ='电子银行' and c.status in ('正常','待审批','预提交审批','已审批') and f.BUSI_TYPE='支付宝快捷支付' %s
        """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        #print row
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
                    filterstr = filterstr + " and c.cust_no = ? " #+ " '%'||"+"?"+"||'%' "
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
        return ["机构号","机构名","员工号","员工名","卡号","客户号","客户名","地址信息","手机号","类型","子类型","办理日期","状态"]

    @property
    def page_size(self):
        return 10
