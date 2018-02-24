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
支行人数手工维护
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SYEAR','ORG_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        SELECT HM.SYEAR,HM.ORG_CODE,BR.BRANCH_NAME,HM.ORG_COUNT,HM.REMARKS,HM.ID FROM HAND_MAINTAIN HM
        JOIN BRANCH BR ON HM.ORG_CODE=BR.BRANCH_CODE
        WHERE 1=1 %s ORDER BY HM.SYEAR,HM.ORG_CODE DESC
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
                if k == "ORG_CODE":
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr+" and HM.ORG_CODE in (%s)"%(vvv)
                else:
                    filterstr = filterstr+" and %s = ? "%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'ORG_CODE', None))
        return filterstr,vlist
    def column_header(self):
        return ["年份","机构号","机构名称","支行人数","备注","操作"]

    @property
    def page_size(self):
        return 10
