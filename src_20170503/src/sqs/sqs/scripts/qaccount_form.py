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
助理会计等级报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SYEAR','org','ORG_CODE','USER_CODE','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select tt.syear,b.BRANCH_CODE,b.BRANCH_NAME,tt.USER_CODE,fu.NAME,
                tt.COUNT_RDATA,tt.COUNT_CSCORE,tt.COUNT_WEIGHT,tt.COUNT_SCORE,
                tt.MIS_RDATA,tt.MIS_CSCORE,tt.MIS_WEIGHT,tt.MIS_SCORE,
                tt.BALL_RDATA,tt.BALL_CSCORE,tt.BALL_WEIGHT,tt.BALL_SCORE,
                tt.BASIC_RDATA,tt.BASIC_CSCORE,tt.BASIC_WEIGHT,tt.BASIC_SCORE,
                tt.YRANK_RDATA,tt.YRANK_CSCORE,tt.YRANK_WEIGHT,tt.YRANK_SCORE,
                tt.WRONG_RDATA,tt.WRONG_CSCORE,tt.WRONG_WEIGHT,tt.WRONG_SCORE,
                tt.COMP_RDATA,tt.COMP_CSCORE,tt.COMP_WEIGHT,tt.COMP_SCORE,
                tt.SKILL_RDATA,tt.SKILL_CSCORE,tt.SKILL_WEIGHT,tt.SKILL_SCORE,
                tt.EDU_RDATA,tt.EDU_CSCORE,tt.EDU_WEIGHT,tt.EDU_SCORE,
                tt.EXPER_RDATA,tt.EXPER_CSCORE,tt.EXPER_WEIGHT,tt.EXPER_SCORE,
                tt.EXTRA_SCORE,tt.TOTAL_SCORE,tt.SYS_LEVEL,tt.ADJ_LEVEL,tt.LAST_LEVEL,tt.ID
                from account_form tt
                join F_USER fu on fu.USER_NAME = tt.USER_CODE
                join USER_BRANCH ub on ub.USER_ID = fu.ROLE_ID
                join branch b on ub.BRANCH_ID = b.ROLE_ID
                where 1=1 %s
                order by tt.SYEAR desc, tt.user_code
           """%(filterstr)
        print sql
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        '''
        rowlist=[]
        for i in row:
            t=list(i[0:4])
            for j in i[4:]:
                if j is None:j=0
                j=self.trans_dec(j)
                t.append(j)
            rowlist.append(t)
        '''
        return self.translate(row,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and b.BRANCH_CODE in ( %s ) "%(vvv)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'tt.USER_CODE','b.BRANCH_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return [
            [{"name":"统计年份","h":2},{"name":"机构号","h":2},{"name":"机构名","h":2},{"name":"员工号","h":2},{"name":"员工名","h":2},{"name":"支行（部）网点数量（个）","w":4},{"name":"支行（部）差错率（名）","w":4},{"name":"支行（部）业务总量（名）","w":4},{"name":"支行（部）会计基础等级（级）","w":4},{"name":"助理会计行龄（年）","w":4},{"name":"支行（部）内勤人均违规积分分值排名","w":4},{"name":"支行（部）电子银行替代率完成率排名（名）","w":4},{"name":"助理会计市办业务知识技能达标（级）","w":4},{"name":"助理会计文化程度","w":4},{"name":"助理会计工作经验","w":4},{"name":"附加分项","h":2},{"name":"综合得分","h":2},{"name":"系统测算等级","h":2},{"name":"调整等级","h":2},{"name":"等级","h":2},{'name':'操作','h':2}],
            [{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1}]
            ]
    def trans_dec(self,num):
        tmp = num
        #tmp = '{:,}'.format(tmp)
        return tmp

    @property
    def page_size(self):
        return 15
