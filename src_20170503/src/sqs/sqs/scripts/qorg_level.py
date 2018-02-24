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
网点业务经营管理等级报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['SYEAR','org']
        filterstr,vlist = self.make_eq_filterstr()
        print u'',filterstr,vlist
        sql ="""
            select ol.syear,ol.org_code,b.BRANCH_NAME,                    
                ol.yjc_rdata,ol.yjc_cscore,ol.yjc_weight,ol.yjc_score,
                ol.rjc_rdata,ol.rjc_cscore,ol.rjc_weight,ol.rjc_score,
                ol.yjd_rdata,ol.yjd_cscore,ol.yjd_weight,ol.yjd_score,
                ol.ebc_rdata,ol.ebc_cscore,ol.ebc_weight,ol.ebc_score,
                ol.ebr_rdata,ol.ebr_cscore,ol.ebr_weight,ol.ebr_score,
                ol.dkc_rdata,ol.dkc_cscore,ol.dkc_weight,ol.dkc_score,
                ol.wdg_rdata,ol.wdg_cscore,ol.wdg_weight,ol.wdg_score,
                ol.sbl_rdata,ol.sbl_cscore,ol.sbl_weight,ol.sbl_score,
                ol.total_score,ol.sys_level,ol.adj_level,ol.last_level,ol.id
            from org_level as ol 
            join branch b on b.branch_code = ol.org_code
            where 1=1 %s
            order by ol.SYEAR desc,ol.ORG_CODE asc
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
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'b.BRANCH_CODE', None))
        print u'',filterstr,vlist
        return filterstr,vlist  
    def column_header(self):
        return [
                [{"name":"统计年份","h":2},{"name":"机构编号","h":2},{"name":"机构名称","h":2},{"name":"年度日均存款总量（亿元）","w":4},{"name":"人均日均存款量（万元）","w":4},{"name":"年度日均贷款总量（亿元）","w":4},{"name":"电子银行开户数（户）","w":4},{"name":"电子银行替代率（%）","w":4},{"name":"贷款户数（户）","w":4},{"name":"网点贷款户日均存贷挂钩率（%）","w":4},{"name":"四级不良贷款率（%）","w":4},{"name":"综合得分","h":2},{"name":"系统测算等级","h":2},{"name":"调整等级","h":2},{"name":"管理等级" ,"h":2}]
                
                ,[{"name":"实绩","h":1},{"name":"等级值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"等级值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"等级值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"等级值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"等级值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"等级值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"等级值","h":1},{"name":"权重","h":1},{"name":"得分","h":1},{"name":"实绩","h":1},{"name":"等级值","h":1},{"name":"权重","h":1},{"name":"得分","h":1}]
        ]
    @property
    def page_size(self):
        return 10
