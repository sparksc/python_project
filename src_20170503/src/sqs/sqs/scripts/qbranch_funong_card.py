# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config

"""福农卡发卡量指标"""
class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['org_no', 'kyear']
        filterstr,vlist = self.make_eq_filterstr()
        sql = u"""
        SELECT F.KYEAR,F.ORG_NO,B.BRANCH_NAME,F.TARGET,F.REMARKS,F.ID 
        FROM FUNONG_CARD_TARGET F JOIN BRANCH B ON B.BRANCH_CODE=F.ORG_NO
        WHERE 1=1 %s
        ORDER BY F.KYEAR,F.ORG_NO
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
                    filterstr = filterstr + "and f.org_no in(%s) "%(vvv)
                else:
                    filterstr = filterstr + "and %s=?"%k
                    vlist.append(v)
        
        filterstr = "%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'f.org_no',None))
       
        return filterstr, vlist
    def column_header(self):
        return ["所属年份","机构号","机构名称","发卡量目标任务","备注","操作"]

    @property
    def page_size(self):
        return 10

