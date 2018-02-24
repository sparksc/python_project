#-*-coding:utf-8-*-

import sys
default_encoding = 'utf-8'

if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config
"""
CRM数据抽取
"""

class Query(ObjectQuery):
    def prepare_object(self):
        self.filterlist = ['org']
        filterstr, vlist = self.make_eq_filterstr()
        
        sql = u"""
        select distinct a.cust_no, a.CUST_IN_NO,a.MANAGER_NO,1,1,a.ORG_NO,a.ID from CUST_HOOK a 
        where a.TYP='贷款' and a.STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and a.HOOK_TYPE='管户' and left( a.MANAGER_NO,1)='9' and length(a.MANAGER_NO) = 7  %s
        union
        select distinct a.cust_no, a.CUST_IN_NO,a.MANAGER_NO,1,1,a.ORG_NO,a.ID from CUST_HOOK a
        left join (select distinct ORG_NO,CUST_IN_NO,ID from CUST_HOOK where TYP='贷款' and STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and HOOK_TYPE='管户') b on a.ORG_NO=b.ORG_NO and a.CUST_IN_NO=b.CUST_IN_NO
        where a.TYP='存款' and a.STATUS in ('待审批','已审批','预提交审批','正常','录入已审批') and a.HOOK_TYPE='管户' and b.CUST_IN_NO is null and left(a.MANAGER_NO,1)='9' and length(a.MANAGER_NO) = 7  %s
        """%(filterstr,filterstr)
        print sql
        if vlist:
           vlist2=[vlist[0],vlist[0]]
           row = self.engine.execute(sql,vlist2)
        else:
           row = self.engine.execute(sql,vlist)
        needtrans = {}
        return self.translate(row,needtrans)
       

    def make_eq_filterstr(self):
        filterstr = ""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                
                if k == 'org':
                    filterstr = filterstr + " and a.ORG_NO=?"
                    vlist.append(v.strip())
                '''
                elif k == 'NET_NAME':
                    filterstr = filterstr + " and NET_NAME like " + "'%'||"+ "?"+"||'%'" 
                    vlist.append(v.strip())
                elif k == 'MANAGER_NO':
                    filterstr = filterstr + " and manager_no=?"
                    vlist.append(v.strip())
                elif k == 'MANAGER_NAME':
                    filterstr = filterstr + "and MANAGER_NAME like " + "'%'||" + "?" + "||'%'"
                    vlist.append(v.strip())
                elif k == 'RB_COUNT':
                    filterstr = filterstr + " and rb_count=?"
                    vlist.append(v.strip())
                '''
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'a.ORG_NO', None))
        return filterstr, vlist
    def column_header(self):
        return ["客户号", "客户内码", "客户经理编号","主协办类型", "操作类型", "机构号"]
   
    @property
    def page_size(self):
        return 10
          
