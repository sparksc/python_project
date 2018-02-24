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
柜员等级评定指标手工维护
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SYEAR','ORG_CODE','USER_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
             select ul.SYEAR,ul.ORG_CODE,b.BRANCH_NAME,ul.USER_CODE,fu.NAME,ul.TASK_LEVEL,ul.CIVILIZED_SERVICE,ul.TASK_ERRORRATE,ul.CUST_SATISFACTION,ul.WORK_YEAR,ul.BANKTERM_YEAR,ul.VIOLATION_SCORE,ul.REMARKS,ul.ID 
                from USER_LEVEL ul,BRANCH b,F_USER fu
                where b.BRANCH_CODE = ul.ORG_CODE and fu.USER_NAME=ul.USER_CODE %s                             
                order by ul.SYEAR desc,ul.ID
             """%(filterstr)
        print sql
         
        
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
       
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        print self.args.items()
        for k,v in self.args.items(): 
            if v and k in self.filterlist:
                if k == 'ORG_CODE':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr+"and ul.ORG_CODE in(%s)"%(vvv)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)           
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'ul.USER_CODE','ul.ORG_CODE', None))

        return filterstr,vlist
    def column_header(self):
        return ["年份","机构号","机构名称","员工号","员工姓名","市办业务知识技能达标(级)","优质文明服务扣分(分)","业务差错率(‰)","客户满意度(%)","行龄(年)","临柜工作经验(年)","违规积分(分)","备注","操作"]

    @property
    def page_size(self):
        return 10
