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
考核数据结果查询
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID', 'org', 'CHECK_DATE_ID']
        filterstr1, filterstr2, vlist = self.make_eq_filterstr()
        #sql ="""
        # select q.DATE_ID, q.ORG_NO, q.CUST_IN_NO, q.CUST_NO, q.CUST_NAME, q.ACCOUNT_NO, q.TEL_NO, q.CNT, d.SUB_TYPE, d.OPEN_BRANCH_NO, d.NET_CST_NO, d.STATUS 
        # from QUARTER_TERM_SALE_MBANK q
        # left join (select d.CST_NO, f.SUB_TYPE, d.OPEN_BRANCH_NO, d.NET_CST_NO, f.STATUS from D_CUST_CONTRACT d  join F_CONTRACT_STATUS f on f.CONTRACT_ID = d.ID where d.BUSI_TYPE = '手机银行' AND f.SUB_TYPE = '专业版' and f.STATUS in ('冻结','停用','暂时冻结','正常') %s) d on d.CST_NO = q.CUST_IN_NO
        # where 1=1 %s
        # order by d.NET_CST_NO
        #"""%(filterstr1, filterstr2)
        sql ="""
        select q.DATE_ID, q.ORG_NO, q.CUST_IN_NO, q.CUST_NO, q.CUST_NAME, q.ACCOUNT_NO,q.CNT, nvl(info.tel_core,'') as tel_core ,
        nvl(info.cust_address,'') as cust_address,nvl(info.cust_credit_address,'') as cust_credit_address,decode(nvl(d.sj_cst_id,''),'','否','是') as sj_flag
        from QUARTER_TERM_SALE_MBANK q
        left join d_cust_info info on q.CUST_IN_NO=info.cust_no
        left join (select distinct  '101'||CCRD15TO18(trim(substr(cst_id,4,20)))  as sj_cst_id from MB_PB_ACCINF where  ACTION<>'D' and MAIF_STT<>'5' and MAIF_SIGNFLAG='2'
        and CST_ID is not null AND (length(CST_ID) = 18 OR length(CST_ID) = 21) and left(CST_ID,3) = '101'  %s) d 
        on d.sj_cst_id = q.CUST_NO
        where 1=1 %s 
         order by q.org_no,q.cnt desc 
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
        return ["考核日期", "机构号","客户内码","客户号","客户名称", "账号", "笔数", "联系电话","核心地址","信贷地址","开通手机银行专业版"]

    @property
    def page_size(self):
        return 15
