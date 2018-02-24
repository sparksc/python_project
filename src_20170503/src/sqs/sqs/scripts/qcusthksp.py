# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
客户挂钩审批
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CUST_NO','MANAGER_NO','TYP','STATUS']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT c.ID, c.ETL_DATE, c.ORG_NO, d.ORG0_NAME, c.MANAGER_NO, s.SALE_NAME, CASE WHEN left(c.cust_no,2)='81' THEN '对私' WHEN left(c.cust_no,2)='82' THEN '对公' END SIGN, c.CUST_NO, i.CUST_NAME, c.TYP, c.PERCENTAGE, c.SRC, c.START_DATE, c.END_DATE, c.STATUS
                 FROM YDW.CUST_HOOK c
                 LEFT JOIN D_ORG d on d.org0_code=c.org_no 
                 LEFT JOIN D_SALES_TEMP s on s.sale_code=c.manager_no
                 LEFT JOIN D_CUST_INFO i on i.cust_no=c.cust_no
                 WHERE 1=1 %s ORDER BY ID"""%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and c.%s = ?"%k
                vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["编号","维护日期","机构编号","机构名称","员工号","员工名称","公私标志","客户号","客户名","类型","分配比例","认定方式","管理起始日期","管理结束日期","状态"]

    @property
    def page_size(self):
        return 10
