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
四季度柜面入口营销考核基础数据导出
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['FROM_DATE_ID','END_DATE_ID', 'org']
        filterstr,vlist,l_date = self.make_eq_filterstr()
        sql = """
            --机构号,机构名称,客户内码,账号,交易笔数,客户名称,客户号,电话号码,核心地址,信贷地址 
        select %s, x.tran_branch_code as BRANCH_CODE, x.BRANCH_NAME,x.CST_NO,x.ACCOUNT_NO, x.CNT,  info.cust_name , '101'||x.sfz as sfz ,nvl(info.tel_core,'') as tel_core ,
        nvl(info.cust_address,'') as cust_address,nvl(info.cust_credit_address,'') as cust_credit_address from (
        select h.* from (
        select TRAN_BRANCH_CODE,BRANCH_NAME,ACCOUNT_NO,CST_NO,sfz,count(1) as CNT  from (
        SELECT distinct F.DATE_ID as DATE_ID, A.OPEN_BRANCH_CODE as TRAN_BRANCH_CODE, B.BRANCH_NAME as BRANCH_NAME, F.TELLER_JNO as TELLER_JNO,
        F.ACCT_NO as ACCOUNT_NO,
        a.CST_NO,
        CCRD15TO18(trim(substr(a.cst_id,4,20))) as sfz
        FROM F_JRN_TRANSACTION F 
        INNER JOIN D_JRN_TRANSACTION_TYPE DT on F.JRN_TRAN_TYPE_ID = DT.ID 
        INNER JOIN D_ACCOUNT A ON A.ACCOUNT_NO = F.ACCT_NO
        INNER JOIN BRANCH B on B.BRANCH_CODE = A.OPEN_BRANCH_CODE
        WHERE F.DATE_ID >= ? AND F.DATE_ID <= ? 
        %s AND DT.ANALYSIS_CHANNEL in ('TE', '柜面') AND DT.DIRECT = '借' AND DT.CASH_TRAN_FLAG = '转账'
        --AND DT.REV_FLAG = '未抹账'
        AND F.ACCT_NO is not null AND F.PEER_ACCT_NO is not null 
        AND F.SYS_TRAN_CODE in ('410150','722110','740020','742020') 
        AND A.CST_NO is not null AND left(A.CST_NO, 2) = '81' AND A.CST_ID is not null AND (length(A.CST_ID) = 18 OR length(A.CST_ID) = 21) and left(a.CST_ID,3) = '101'
        AND A.CST_NO <> '81020910324'
        ) where ((days(to_date(?, 'YYYYMMDD')) - days(to_date(substr(sfz, 7, 8), 'YYYYMMDD'))) / 365) between 18 and 50
        group by TRAN_BRANCH_CODE,BRANCH_NAME,ACCOUNT_NO,CST_NO,sfz      
        ) h left join
        (
        select distinct  CCRD15TO18(trim(substr(cst_id,4,20)))  as sj_cst_id from MB_PB_ACCINF where date_id=? and ACTION<>'D' and MAIF_STT<>'5' and MAIF_SIGNFLAG='2'
        and CST_ID is not null AND (length(CST_ID) = 18 OR length(CST_ID) = 21) and left(CST_ID,3) = '101'
        ) j on h.sfz=j.sj_cst_id where j.sj_cst_id is null
        ) x left join D_CUST_INFO info on x.CST_NO = info.cust_no
        with ur
        """%(l_date, filterstr)
        print sql
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr = ""
        vlist = []
        from_date_id = 0
        end_date_id = 0
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and A.OPEN_BRANCH_CODE in ( %s )  "%(vvv)
                elif k == 'FROM_DATE_ID':
                    from_date_id = v
                elif k == 'END_DATE_ID':
                    end_date_id = v
                else: 
                    pass

        vlist.append(from_date_id)
        vlist.append(end_date_id)
        vlist.append(end_date_id)
        vlist.append(end_date_id)

        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'A.OPEN_BRANCH_CODE', None))
        print filterstr
        return filterstr, vlist,end_date_id

    def column_header(self):
        return ["考核日期", "机构号","机构名称","客户内码","账号","交易笔数","客户名称","客户号","电话号码","核心地址","信贷地址"]

    @property
    def page_size(self):
        return 15
