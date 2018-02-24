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
国际业务部业务经营管理等级报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SYEAR']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        SELECT IL.SYEAR,IL.ORG_CODE,BR.BRANCH_NAME,IL.RANKING,IL.SYS_LEVEL,IL.ADJ_LEVEL,IL.LAST_LEVEL,IL.ID FROM INTERNATIONAL_LEVEL IL 
        JOIN BRANCH BR ON IL.ORG_CODE=BR.BRANCH_CODE
        WHERE 1=1 %s
        ORDER BY IL.SYEAR DESC
        """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        rowlist=[]
        
        return self.translate(row,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():

            if v and k in self.filterlist:
                    filterstr = filterstr+" and IL.%s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'BR.BRANCH_CODE', None))
        return filterstr,vlist  
    def column_header(self):
        return [
                [{"name":"统计年份","h":2},{"name":"机构编号","h":2},{"name":"机构名称","h":2},{"name":"全省排名","h":2},{"name":"系统测算等级","h":2},{"name":"调整等级","h":2},{"name":"管理等级" ,"h":2},{"name":"操作","h":2}]
        ]
    @property
    def page_size(self):
        return 10
