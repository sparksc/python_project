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
        self.filterlist = ['SYEAR','org','USER_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        print u'',filterstr,vlist
        sql ="""
            select tt.syear,b.BRANCH_CODE,b.BRANCH_NAME,tt.USER_CODE,fu.NAME,
                tt.COUNT_RDATA,tt.COUNT_CSCORE,tt.COUNT_WEIGHT,tt.COUNT_SCORE,
                tt.LEVEL_RDATA,tt.LEVEL_CSCORE,tt.LEVEL_WEIGHT,tt.LEVEL_SCORE,
                tt.CIVIL_RDATA,tt.CIVIL_CSCORE,tt.CIVIL_WEIGHT,tt.CIVIL_SCORE,
                tt.ERROR_RDATA,tt.ERROR_CSCORE,tt.ERROR_WEIGHT,tt.ERROR_SCORE,
                tt.SATIS_RDATA,tt.SATIS_CSCORE,tt.SATIS_WEIGHT,tt.SATIS_SCORE,
                tt.WYEAR_RDATA,tt.WYEAR_CSCORE,tt.WYEAR_WEIGHT,tt.WYEAR_SCORE,
                tt.EDU_RDATA,tt.EDU_CSCORE,tt.EDU_WEIGHT,tt.EDU_SCORE,
                tt.BYEAR_RDATA,tt.BYEAR_CSCORE,tt.BYEAR_WEIGHT,tt.BYEAR_SCORE,
                tt.EXTRA_SCORE,tt.VIOLATE_SCORE,tt.TOTAL_SCORE,tt.SYS_LEVEL,tt.ADJ_LEVEL,tt.LAST_LEVEL,tt.ID
                from teller_table tt 
                join F_USER fu on fu.USER_NAME = tt.USER_CODE 
                join USER_BRANCH ub on ub.USER_ID = fu.ROLE_ID 
                join branch b on ub.BRANCH_ID = b.ROLE_ID
                where 1=1 %s
                order by tt.SYEAR desc, tt.user_code
            """%(filterstr)
        print u'sql语句：',sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        rowlist=[]
        
        return self.translate(row,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr+"and b.BRANCH_CODE in(%s)"%(vvv)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'tt.USER_CODE','b.BRANCH_CODE', None))
        print u'',filterstr,vlist
        return filterstr,vlist  
    def column_header(self):
        return [
                [{"name":"统计年份","h":2},{"name":"机构编号","h":2},{"name":"机构名称","h":2},{"name":"员工编号","h":2},{"name":"员工姓名","h":2},{"name":"业务量（笔）","w":4},{"name":"市办业务知识技能达标（级）","w":4},{"name":"优质文明服务（分）","w":4},{"name":"业务差错率（‰）","w":4},{"name":"客户满意度（%）","w":4},{"name":"行龄（年）","w":4},{"name":"文化程度","w":4},{"name":"临柜工作经验（年）","w":4},{"name":"附加分项","h":2},{"name":"违规积分附加扣分项","h":2},{"name":"综合得分","h":2},{"name":"系统测算等级","h":2},{"name":"调整等级","h":2},{"name":"等级" ,"h":2}]
                
                ,[{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"分值","h":1},{"name":"权重","h":1},{"name":"得分","h":1}]
        ]
    @property
    def page_size(self):
        return 10
