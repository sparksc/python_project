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
柜员等级报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','ORG_CODE','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        print u'',filterstr,vlist
        sql ="""
        SELECT  DATE_ID, ORG_CODE, ORG_NAME, FARMERSFILE_TARGETPER, FARMCREDIT_GRADEPER, MINCAR_CUSJUDPER, HUIPU_FASTCARPER, PALN_OBJVILNUM, 
        CARDCIR_OFFADDNUM, BUMBUS_ADDNUM, YEARPLAN_ADDLOANNUM, CREDITLOAN_BLANCEPER, CREDITLOAN_PERNUMPER ,REMARK,ID
        FROM YDW.PUHUI_BRANCH_TARGET_HANDER
        where 1=1  %s order by ORG_CODE
            """%(filterstr)
        print u'sql语句：',sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i)
            for j in range(2,len(i)-1):
                if t[j]==None:
                    t[j]=0
                if j==13:
                    t[j]=""
            rowlist.append(t)
        return self.translate(rowlist,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():

            if v and k in self.filterlist:
                if k == 'ORG_CODE':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr+"and ORG_CODE in (%s)"%(vvv)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'SALE_CODE','ORG_CODE', None))
        print u'',filterstr,vlist
        return filterstr,vlist  
    def column_header(self):
        return ['年份','机构号','机构名称','农户建档目标（%）','农户信用等级评定率指标（%）','小微专车客户评价覆盖面指标%','普惠快车客户评价覆盖面指标%','计划指标村数','卡类有效循环合同新增张数指标','丰收创业卡新增 张数指标','年度计划新增个人贷款户数指标','30万（含）以下信用贷款余额占比指标','30万（含）以下信用贷款户数占比指标','备注','操作']
    @property
    def page_size(self):
        return 10
