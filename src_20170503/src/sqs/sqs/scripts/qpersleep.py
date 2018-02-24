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
个人网银睡眠户报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            SELECT f.DATE_ID,m.THIRD_BRANCH_CODE,m.THIRD_BRANCH_NAME,m.SALE_CODE,m.SALE_NAME,d.CST_NAME,d.NET_CST_NO,d.CST_NO,d.ID_NUMBER,d.OPEN_DATE,d.OPEN_BRANCH_NO,d.MOBILE_NO,f.STATUS,MAX(F.LAST_LOGON_DATE,LEFT(D.OPEN_DATE,8))  
            FROM F_CONTRACT_STATUS F
            JOIN D_CUST_CONTRACT D ON F.CONTRACT_ID=D.ID
            JOIN D_SALE_MANAGE_RELA M ON M.MANAGE_ID=F.MANAGE_ID
            WHERE D.BUSI_TYPE='个人网上银行' AND F.STATUS IN ('正常','暂时冻结','冻结') AND F.SUB_TYPE IN( '专业版','大众版')
            AND SUBSTR(D.OPEN_BRANCH_NO,1,3)='966' AND (DAYS(TO_DATE(F.DATE_ID,'YYYYMMDD'))-DAYS(TO_DATE(MAX(F.LAST_LOGON_DATE,LEFT(D.OPEN_DATE,8)),'YYYYMMDD')))>180 %s
            """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print sql
        needtrans ={}
        return self.translate(row,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            print k,v
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
        return ["统计日期","机构号","机构名","员工号","员工名","客户名","客户号","客户内码","身份证号","办理日期","办理机构","电话","状态","最后登录时间"]


    @property
    def page_size(self):
        return 15
