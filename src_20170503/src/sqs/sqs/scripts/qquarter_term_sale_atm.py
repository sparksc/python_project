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
            SELECT X.BRANCH_CODE, X.BRANCH_NAME, nvl(sum(CASE WHEN X.CNT >= 1200 THEN 1 END), 0), nvl(sum(CASE WHEN (X.CNT > 1800 AND X.CNT <= 2400) THEN 1 END), 0), 
                nvl(sum(CASE WHEN X.CNT > 2400 THEN 1 END), 0) 
            FROM 
				(SELECT
                    B.BRANCH_CODE   AS BRANCH_CODE,
                    B.BRANCH_NAME   AS BRANCH_NAME,
				    A.ATM_NO        AS ATM_NO,
					SUM(1)/((days(to_date(?, 'YYYYMMDD')) - days(to_date(?, 'YYYYMMDD')) + 1) / 30)  AS CNT  
				FROM
					F_JRN_TRANSACTION F 
					INNER JOIN D_ATM A 
					ON F.TERMINAL_CODE=A.ATM_NO 
                    INNER JOIN BRANCH B
                    ON A.ORG_NO = B.BRANCH_CODE
					INNER JOIN D_JRN_TRANSACTION_TYPE DT 
					ON F.JRN_TRAN_TYPE_ID=DT.ID
				    INNER JOIN D_DATE D
				    ON D.ID = F.DATE_ID
				WHERE
	                D.ID >= ? and D.ID <= ? and %s
					F.SALE_ROLE='存款对账登记簿' AND
                    --F.TRAN_BRANCH_CODE LIKE '966%%' AND
                    A.TYP in ('取', '存取') AND
				    A.SUB_TYP = '附' AND
					DT.ANALYSIS_CHANNEL IN ('CA', 'NA', 'UA')
				GROUP BY
                    B.BRANCH_CODE,
                    B.BRANCH_NAME,
	                A.ATM_NO
				ORDER BY B.BRANCH_CODE ASC)X
            GROUP BY X.BRANCH_CODE, X.BRANCH_NAME
            """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i)
            ##需要对查询出的数据进行处理
            atm_count = self.get_atm_counts_by_org_no(t[0])
            t.insert(3, atm_count)
            t.insert(4, round(float(t[2])/float(atm_count)*100, 2))
            t.insert(6, round(float(t[5])/float(atm_count)*100, 2))
            t.insert(8, round(float(t[7])/float(atm_count)*100, 2))

            rowlist.append(t)    
        return self.translate(rowlist,needtrans)

    def get_atm_counts_by_org_no(self, org_no):
        sql = """ select count(*) from D_ATM M  where M.ORG_NO = ? and M.TYP in ('取', '存取') AND M.SUB_TYP = '附' """
        atm_count = self.engine.execute(sql, [org_no]).fetchall()[0]
        return int(atm_count[0])

    def make_eq_filterstr(self):
        filterstr = ""
        vlist = []
        from_date_id = 0
        end_date_id = 0
        for k,v in self.args.items():
            #if k == 'login_branch_no':
            #    bb = self.deal_branch_query_auth(v)
            #    if bb != False :
            #        filterstr = filterstr+" A.ORG_NO in ( %s ) and"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" A.ORG_NO in ( %s ) and "%(vvv)
                elif k == 'FROM_DATE_ID':
                    from_date_id = v
                elif k == 'END_DATE_ID':
                    end_date_id = v
                else: 
                    pass

        vlist.append(int(end_date_id))
        vlist.append(int(from_date_id))
        vlist.append(int(from_date_id))
        vlist.append(int(end_date_id))
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'A.ORG_NO', None))
        return filterstr, vlist

    def column_header(self):
        return ["机构编号","机构名称","交易1200笔以上ATM数量","布放ATM机总数量","有效率1","交易1800-2400笔ATM数量","有效率2", "交易2400笔以上ATM数量","有效率3"]

    @property
    def page_size(self):
        return 15
