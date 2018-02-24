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
客户经理存款
"""

class Query(ObjectQuery):
    def group_by(self):
        return [0],(7,8,9,10)
    def prepare_object(self):
        self.filterlist = ['FROM_DATE_ID', 'END_DATE_ID', 'org','SALE_CODE']
        self.kaishi=''
        self.jiesu=''
        filterstr,vlist = self.make_eq_filterstr()
        sql="""
        (SELECT b.parent_name,%s,%s,M.THIRD_BRANCH_CODE,M.THIRD_BRANCH_NAME,M.SALE_CODE,M.SALE_NAME,COUNT(DISTINCT D.CARD_NO) AS CARD_NUM,(nvl(A.SSFY,0)) as 实收费用,(nvl(A.YSFY,0)) as 应收费用
            FROM F_CREDIT_CARD_STATUS F
            JOIN D_CREDIT_CARD D ON D.ID = F.CARD_ID 
            JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID
            LEFT JOIN D_CUST_INFO I ON D.CST_NO=I.CUST_NO
            LEFT JOIN (
                SELECT AH.MANAGER_NO,COUNT(DISTINCT FT.CARD_NO) AS CARD_NUM ,
                SUM(CASE WHEN T.ABS_NAME='还款冲应收费用' THEN F.AMOUNT ELSE 0 END)/ 100.00 AS SSFY,
                SUM(CASE WHEN T.ABS_NAME='按日贷款手续费' THEN F.AMOUNT ELSE 0 END)/ 100.00 AS YSFY
                FROM F_TRANSACTION F
                INNER JOIN D_TRANSACTION_TYPE T ON T.ID = F.TRAN_TYPE_ID AND T.IS_EMPLOYEE  !='是'
                INNER JOIN D_TRANSACTION  FT  ON FT.ID = F.TRAN_ID 
                INNER JOIN D_ORG O ON O.ID = F.ORG_ID    
                INNER JOIN D_ACCOUNT2 A ON A.ID = F.ACCOUNT_ID
                INNER JOIN ACCOUNT_HOOK AH ON  AH.CARD_NO = A.CARD_NO AND AH.SUB_TYP='福农卡'
                INNER JOIN V_STAFF_INFO V ON V.USER_NAME = AH.MANAGER_NO
                WHERE T.ABS_NAME IN ('还款冲应收费用','按日贷款手续费') AND F.DATE_ID>= %s AND F.DATE_ID<= %s
                GROUP  BY O.ORG0_CODE,O.ORG0_NAME,AH.MANAGER_NO,V.NAME
                ) A on A.MANAGER_NO=m.SALE_CODE
            join (SELECT B.BRANCH_CODE CHILD_CODE,B.BRANCH_NAME,A.BRANCH_CODE PARENT_CODE,A.BRANCH_NAME PARENT_NAME,A.BRANCH_LEVEL FROM BRANCH A
            JOIN BRANCH B ON A.ROLE_ID=B.PARENT_ID WHERE A.BRANCH_LEVEL='支行')B ON M.THIRD_BRANCH_CODE=B.CHILD_CODE
            WHERE F.DATE_ID>= %s AND F.DATE_ID<= %s AND F.STATUS NOT IN('持卡人请求关闭','呆账核销','呆账核销清户','销卡代码','新卡激活，旧卡失效') AND D.PRODUCT IN ('0632','福农卡966')
            AND F.DUE_DATE>= %s AND D.OPEN_DATE<= %s AND UPPER(CCRD15TO18(TRIM(SUBSTR(I.CUST_LONG_NO,4,20)))) NOT IN (SELECT UPPER(CCRD15TO18(ID_NUMBER)) FROM F_USER WHERE WORK_STATUS='在职' AND LENGTH(ID_NUMBER)>10)
            %s
            GROUP BY  M.THIRD_BRANCH_CODE,M.THIRD_BRANCH_NAME,M.SALE_CODE,M.SALE_NAME,A.SSFY,A.YSFY,b.parent_name)
          """%(self.kaishi,self.jiesu,self.kaishi,self.jiesu,self.kaishi,self.jiesu,str(self.kaishi)[0:6],self.kaishi,filterstr)
        print sql
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()

        sql1=u"""
        SELECT A.DETAIL_VALUE FROM T_PARA_DETAIL A WHERE A.DETAIL_KEY='WEIGHT' AND A.PARA_ROW_ID =
            (
            SELECT D.PARA_ROW_ID FROM T_PARA_TYPE Y JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=Y.ID JOIN T_PARA_DETAIL D ON H.ID=D.PARA_HEADER_ID
            WHERE Y.TYPE_NAME='福农卡支行考核参数' AND D.DETAIL_VALUE='客户经理奖励金额参数'
            )
        """
        per = self.engine.execute(sql1.encode('utf-8')).fetchall()
        #print "percent:",per
        if len(per[0]) == 1:
            per = float(per[0][0])/100.00
        else:
            per = 0

        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i[0:8])
            for j in i[8:]:
                if j is None:j=0
                j=self.amount_trans_dec(j)
                t.append(j)
            t.append(str(round(float(i[8])*per,2)))
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and M.THIRD_BRANCH_CODE in ( %s ) "%(vvv)
                elif k == 'FROM_DATE_ID':
                    #filterstr = filterstr +" and f.date_id >= %s "%v
                    self.kaishi=int(v)
                    vlist.append(v)
                elif k == 'END_DATE_ID':
                    #filterstr = filterstr +" and f.date_id <= %s "%v
                    self.jiesu=int(v)
                    vlist.append(v)
                elif k == 'SALE_CODE':
                    filterstr = filterstr +" and M.SALE_CODE = '%s' "%v
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'M.SALE_CODE','M.THIRD_BRANCH_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return ["支行汇总","开始时间","结束时间","机构号","机构名称", "客户经理号","客户经理名称","福农卡期间发卡量","期间实收总费用","期间应收总费用","期间奖励金额"]

    @property
    def page_size(self):
        return 15
