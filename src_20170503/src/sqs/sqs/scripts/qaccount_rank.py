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
助理会计等级评定指标手工维护
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SYEAR','ORG_CODE','USER_CODE','CREDENTIAL_CODE','org']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select es.SYEAR,es.ORG_CODE,b.BRANCH_NAME,es.USER_CODE,fu.NAME,es.MIS_RANK,es.BASIC_RANK,es.RYEAR,es.SCORE_RANK,es.REPLEACE_RANK,es.SKILL,es.EXPERIENCE,es.REMARKS,es.ID 
                from ACCOUNT_RANK es,BRANCH b,F_USER fu 
                where b.BRANCH_CODE = es.ORG_CODE and fu.USER_NAME=es.USER_CODE %s order by es.SYEAR desc, es.ID
             """%(filterstr)
        print sql

        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        ''' 
        rowlist=[]
        for i in row:
            t=list(i)
            if t[3] is None:t[3]=0
            t[3]=self.amount_trans_dec(t[3])

            if t[4] is None:t[4]=0
            t[4]=self.amount_trans_dec(t[4])
            rowlist.append(t)
        '''
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        print self.args.items()
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'ORG_CODE':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and es.ORG_CODE in (%s) "%(vvv)
                else:
                    filterstr = filterstr+"and %s = ?"%k
                    vlist.append(v)           
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'es.USER_CODE','es.ORG_CODE', None))

        return filterstr,vlist
    def column_header(self):
        return ["年份","机构号","机构名称","员工号","员工名","支行（部）业务差错率排名","支行（部）会计基础等级","助理会计行龄","支行（部）内勤人均违规积分分值排名","支行（部）电子银行替代率完成率排名","助理会计业务知识技能达标","助理会计工作经验","备注","操作"]
    @property
    def page_size(self):
        return 10
