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
企业网银睡眠户报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        print filterstr,vlist
        sql ="""
            SELECT f.DATE_ID,m.THIRD_BRANCH_CODE,m.THIRD_BRANCH_NAME,m.SALE_CODE,m.SALE_NAME,d.CST_NAME,d.NET_CST_NO,d.CST_NO,d.ID_NUMBER,d.ID_TYPE,d.ACCT_NO,d.OPEN_DATE,f.STATUS,MAX(F.LAST_LOGON_DATE,LEFT(D.OPEN_DATE,8)),d.OPEN_BRANCH_NO FROM F_CONTRACT_STATUS F
            JOIN D_CUST_CONTRACT D ON F.CONTRACT_ID=D.ID
            JOIN D_SALE_MANAGE_RELA M ON M.MANAGE_ID=f.MANAGE_ID
            WHERE D.BUSI_TYPE='企业网上银行' AND F.STATUS IN ('正常','未激活','冻结')
            AND substr(D.OPEN_BRANCH_NO, 1, 3) = '966' AND (DAYS(TO_DATE(F.DATE_ID,'YYYYMMDD'))-DAYS(TO_DATE(MAX(F.LAST_LOGON_DATE,LEFT(D.OPEN_DATE,8)),'YYYYMMDD')))>180 %s
            """%(filterstr)
        print sql
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and m.THIRD_BRANCH_CODE in (%s) "%(vvv)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'m.SALE_CODE','m.THIRD_BRANCH_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return ["统计日期","机构号","机构名","员工号","员工名","客户名","客户号","客户内码","证件号","证件类型","付费帐号","开户时间","状态","最后登录时间","开户机构"]

    @property
    def page_size(self):
        return 15
