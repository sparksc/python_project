# -*- coding:utf-8 -*-

import sys
import datetime
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
员工岗位历史查询
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['start_date','end_date','sale_code']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
            SELECT G.ID,G.START_DATE,G.END_DATE,SALE_CODE,SALE_NAME, G.PROPERTY,G.ORG_CODE,G.GROUP_HIS,G.POSITION_HIS ,G.DEG_LEVEL,G.POSITION_TYPE,
 G.SALE_FALG,G.WORKSTATUS,G.IS_TEST,G.IS_VIRIUAL
            FROM GROUP_HIS G
            WHERE 1=1 %s
            ORDER BY START_DATE
            """%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        print sql
        print filterstr
        print vlist
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and G.%s = ?"%k
                vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["开始日期","结束日期","员工号","员工名",'人员性质',"机构","部门","岗位",u'等级','客户经理类别','安全员标志','在职状态','试聘人员','虚拟柜员标志']

    @property
    def page_size(self):
        return 20
