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
四季度柜面入口营销考核
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['FROM_DATE_ID','END_DATE_ID', 'org']
        filterstr,vlist = self.make_eq_filterstr()
        sql = """
        SELECT  X.BRANCH_CODE, X.BRANCH_NAME, nvl(sum(CASE WHEN X.CNT = 0 THEN 1 END), 0), nvl(sum(CASE WHEN X.CNT = 1 THEN 1 END), 0), nvl(sum(CASE WHEN X.CNT = 2 THEN 1 END), 0), 
                nvl(sum(CASE WHEN X.CNT = 3 THEN 1 END), 0), nvl(sum(CASE WHEN X.CNT = 4 THEN 1 END), 0), nvl(sum(CASE WHEN X.CNT = 5 THEN 1 END), 0), nvl(sum(CASE WHEN X.CNT = 6 THEN 1 END), 0),
                nvl(sum(CASE WHEN X.CNT = 7 THEN 1 END), 0), nvl(sum(CASE WHEN X.CNT = 8 THEN 1 END), 0), nvl(sum(CASE WHEN X.CNT = 9 THEN 1 END), 0), nvl(sum(CASE WHEN X.CNT > 9 THEN 1 END), 0),
                nvl(sum(CNT), 0), X.AGE_FLAG
        FROM 
            (SELECT TRAN_BRANCH_CODE as BRANCH_CODE, BRANCH_NAME as BRANCH_NAME,CST_NO as CST_NO, AGE_FLAG as AGE_FLAG, sum(1) as CNT 
            FROM 
                (SELECT DATE_ID, TRAN_BRANCH_CODE, BRANCH_NAME, TELLER_JNO, CST_NO, CST_ID, 
                    (CASE WHEN ((days(to_date(?, 'YYYYMMDD')) - days(to_date(CST_ID, 'YYYYMMDD'))) / 365 >= 18 AND (days(to_date(?, 'YYYYMMDD')) - days(to_date(CST_ID, 'YYYYMMDD'))) / 365 <= 50) THEN 1 ELSE 0 END) as AGE_FLAG 
                FROM 
                    (SELECT DATE_ID, TRAN_BRANCH_CODE, BRANCH_NAME, TELLER_JNO, CST_NO, CST_ID, MBANK_CST_NO FROM 
                        (SELECT distinct F.DATE_ID as DATE_ID, A.OPEN_BRANCH_CODE as TRAN_BRANCH_CODE, B.BRANCH_NAME as BRANCH_NAME, F.TELLER_JNO as TELLER_JNO, 
                        A.CST_NO AS CST_NO, (CASE WHEN length(A.CST_ID) = 18 THEN '19'||substr(A.CST_ID, 10, 6) ELSE substr(A.CST_ID, 10, 8) END) as CST_ID 
                        FROM F_JRN_TRANSACTION F INNER JOIN D_JRN_TRANSACTION_TYPE DT on F.JRN_TRAN_TYPE_ID = DT.ID 
                        INNER JOIN D_ACCOUNT A ON A.ACCOUNT_NO = F.ACCT_NO
                        INNER JOIN BRANCH B on B.BRANCH_CODE = A.OPEN_BRANCH_CODE
                        WHERE F.DATE_ID >= ? AND F.DATE_ID <= ? AND %s DT.ANALYSIS_CHANNEL in ('TE', '柜面') AND DT.DIRECT = '借' AND DT.CASH_TRAN_FLAG = '转账' AND DT.REV_FLAG = '未抹账'
                        AND F.ACCT_NO is not null AND F.PEER_ACCT_NO is not null AND F.TEL_TRAN_CODE in ('001106', '001116', '004603', '003111', '003113')
                        AND A.CST_NO is not null AND left(A.CST_NO, 2) = '81' AND A.CST_ID is not null AND (length(A.CST_ID) = 18 OR length(A.CST_ID) = 21) AND A.CST_NO <> '81020910324')M
                    LEFT JOIN
                        (SELECT distinct d.CST_NO as MBANK_CST_NO FROM D_CUST_CONTRACT d, F_CONTRACT_STATUS f WHERE d.BUSI_TYPE =  '手机银行' AND d.ID = f.CONTRACT_ID AND f.DATE_ID = ? AND f.STATUS = '正常')N
                ON M.CST_NO = N.MBANK_CST_NO)Q where Q.MBANK_CST_NO is null)D
            GROUP BY D.TRAN_BRANCH_CODE, D.BRANCH_NAME, D.CST_NO, D.AGE_FLAG order by D.TRAN_BRANCH_CODE ASC)X
        GROUP BY X.BRANCH_CODE, X.BRANCH_NAME, X.AGE_FLAG
        """%(filterstr)
        print sql
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row:
            if int(i[14]) == 1:
                t=list(i[0:14])
                rowlist.append(t)    
        return self.translate(rowlist,needtrans)

    def make_eq_filterstr(self):
        filterstr = ""
        vlist = []
        from_date_id = 0
        end_date_id = 0
        for k,v in self.args.items():
            #if k == 'login_branch_no':
            #    bb = self.deal_branch_query_auth(v)
            #    if bb != False :
            #        filterstr = filterstr+" A.OPEN_BRANCH_CODE in ( %s ) AND"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" A.OPEN_BRANCH_CODE in ( %s ) AND "%(vvv)
                elif k == 'FROM_DATE_ID':
                    from_date_id = v
                elif k == 'END_DATE_ID':
                    end_date_id = v
                else: 
                    pass

        vlist.append(end_date_id)
        vlist.append(end_date_id)
        vlist.append(from_date_id)
        vlist.append(end_date_id)
        vlist.append(end_date_id)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'A.OPEN_BRANCH_CODE', None))
        return filterstr, vlist

    def column_header(self):
        return ["机构编号","机构名称","柜面交易0笔","柜面交易1笔","柜面交易2笔","柜面交易3笔","柜面交易4笔", "柜面交易5笔", "柜面交易6笔", "柜面交易7笔", "柜面交易8笔", "柜面交易9笔", "柜面交易9笔以上", "总笔数"]

    @property
    def page_size(self):
        return 15
