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
考核数据结果汇总查询
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID', 'org', 'CHECK_DATE_ID']
        filterstr1, filterstr2, vlist = self.make_eq_filterstr()
        #sql ="""
        #select h.date_id,h.org_no,j.branch_name,h.task,h.done from (
        #select DATE_ID,org_no,count(1) as task,sum(case when a.net_cst_no is null then 0 else 1 end) as done from (
        #select  q.DATE_ID, q.ORG_NO, q.CUST_IN_NO, q.CUST_NO, q.CUST_NAME, q.ACCOUNT_NO, q.TEL_NO, q.CNT, d.SUB_TYPE, d.OPEN_BRANCH_NO, d.NET_CST_NO, d.STATUS 
        #from QUARTER_TERM_SALE_MBANK q
        #left join (select  d.CST_NO, f.SUB_TYPE, d.OPEN_BRANCH_NO, d.NET_CST_NO, f.STATUS from D_CUST_CONTRACT d  join F_CONTRACT_STATUS f on f.CONTRACT_ID = d.ID where d.BUSI_TYPE = '手机银行' and f.SUB_TYPE='专业版'
        #        and f.STATUS in ('冻结','停用','暂时冻结','正常') %s) d on d.CST_NO = q.CUST_IN_NO
        #where 1=1 %s 
        #order by d.NET_CST_NO
        #) a group by DATE_ID,org_no
        #) h join branch j on h.org_no=j.branch_code
        #"""%(filterstr1, filterstr2)
        sql ="""
        select h.date_id,h.org_no,j.branch_name,h.task,h.done from (
        select DATE_ID,org_no,count(1) as task,sum(case when a.sj_cst_id is null then 0 else 1 end) as done from (
        select  q.DATE_ID, q.ORG_NO, q.CUST_IN_NO, q.CUST_NO, q.CUST_NAME, q.ACCOUNT_NO, q.TEL_NO, q.CNT, d.sj_cst_id
        from QUARTER_TERM_SALE_MBANK q
        left join (select distinct  '101'||CCRD15TO18(trim(substr(cst_id,4,20)))  as sj_cst_id from MB_PB_ACCINF where ACTION<>'D' and MAIF_STT<>'5' and MAIF_SIGNFLAG='2'
        and CST_ID is not null AND (length(CST_ID) = 18 OR length(CST_ID) = 21) and left(CST_ID,3) = '101'  %s) d on d.sj_cst_id = q.CUST_NO
        where 1=1 %s 
        ) a group by DATE_ID,org_no
        ) h join branch j on h.org_no=j.branch_code
        """%(filterstr1, filterstr2)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print "0000000000000000000000000", sql
        needtrans ={}
        return self.translate(list(row),needtrans)    

    def make_eq_filterstr(self):
        filterstr1 =""
        filterstr2 =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr2 = filterstr2 +" and q.ORG_NO in ( %s ) "%(vvv)
                elif k == 'DATE_ID':
                    filterstr2 = filterstr2+" and q.DATE_ID = ?"
                    vlist.append(v)
                elif k == 'CHECK_DATE_ID':
                    filterstr1 = filterstr1+" and DATE_ID = ?"
                    vlist.append(v)
                else: 
                    pass
        filterstr2 ="%s and %s"%(filterstr2,self.get_auth_sql(config.DATATYPE['query'],'None','a.ORG_NO', None))
        return filterstr1,filterstr2,vlist

    def column_header(self):
        return ["考核日期", "机构号","机构名称","计划笔数", "完成笔数"]

    @property
    def page_size(self):
        return 15
