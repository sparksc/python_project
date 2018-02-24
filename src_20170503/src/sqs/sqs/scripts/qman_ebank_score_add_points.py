# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config

class Query(ObjectQuery):
    def exp_str(self):
        return {"start_row":4,"start_col":1,"cols":7}

    def prepare_object(self):
        self.filterlist = ['org_no', 'kyear', 'user_name']
        filterstr,vlist = self.make_eq_filterstr()
        sql = u"""
        SELECT M.KYEAR,M.ORG_NO,B.BRANCH_NAME,M.USER_NAME,F.NAME,M.ADD_POINTS,M.REMARKS,M.ID FROM MAN_EBANK_ADD_POINTS M ,BRANCH B,F_USER F 
        WHERE 1=1 %s AND B.BRANCH_CODE=M.ORG_NO AND F.USER_NAME=M.USER_NAME
        ORDER BY M.KYEAR ,M.ORG_NO,M.USER_NAME
        """%(filterstr)

        print sql
        row = self.engine.execute(sql, vlist).fetchall()
        needtrans = {}
        return self.translate(row, needtrans)

    def make_eq_filterstr(self):
        filterstr = ""
        vlist = []
        for k, v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org_no':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr + "and m.org_no in(%s) "%(vvv)
                elif k == 'user_name':
                    filterstr = filterstr + "and m.user_name in(%s) "%v
                else:
                    filterstr = filterstr + "and %s=?"%k
                    vlist.append(v)
        
        filterstr = "%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'m.user_name','m.org_no',None))
       
        return filterstr, vlist
    def column_header(self):
        return ["所属年份","机构号","机构名称","员工号","员工名称","附加分","备注","操作"]

    @property
    def page_size(self):
        return 15

