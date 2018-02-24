# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['org_no', 'kyear']
        filterstr,vlist = self.make_eq_filterstr()
        print filterstr,vlist
        sql = u"""
        SELECT  %s,M.SECOND_BRANCH_CODE,M.SECOND_BRANCH_NAME,
            COUNT(DISTINCT CASE WHEN F.DATE_ID >= %s||'0101' AND F.DATE_ID<=%s||'0331' THEN D.CARD_NO END) AS CARD_NUM1,
            BIGINT(NVL(TA.TARGET,0)*(SELECT A.DETAIL_VALUE FROM T_PARA_DETAIL A WHERE A.DETAIL_KEY='WEIGHT' AND A.PARA_ROW_ID =
                (SELECT D.PARA_ROW_ID FROM T_PARA_TYPE Y JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=Y.ID JOIN T_PARA_DETAIL D ON H.ID=D.PARA_HEADER_ID
                WHERE Y.TYPE_NAME='福农卡支行考核参数' AND D.DETAIL_VALUE='支行第一季度考核比例'))/ 100) AS FIRST_TAR1, 
            COUNT(DISTINCT CASE WHEN F.DATE_ID >= %s||'0401' AND F.DATE_ID<=%s||'0630' THEN D.CARD_NO END) AS CARD_NUM2,
            BIGINT(NVL(TA.TARGET,0)*(SELECT A.DETAIL_VALUE FROM T_PARA_DETAIL A WHERE A.DETAIL_KEY='WEIGHT' AND A.PARA_ROW_ID =
                (SELECT D.PARA_ROW_ID FROM T_PARA_TYPE Y JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=Y.ID JOIN T_PARA_DETAIL D ON H.ID=D.PARA_HEADER_ID
                WHERE Y.TYPE_NAME='福农卡支行考核参数' AND D.DETAIL_VALUE='支行第二季度考核比例'))/ 100) AS FIRST_TAR2, 
            COUNT(DISTINCT CASE WHEN F.DATE_ID >= %s||'0701' AND F.DATE_ID<=%s||'0931' THEN D.CARD_NO END) AS CARD_NUM3,
            BIGINT(NVL(TA.TARGET,0)*(SELECT A.DETAIL_VALUE FROM T_PARA_DETAIL A WHERE A.DETAIL_KEY='WEIGHT' AND A.PARA_ROW_ID =
                (SELECT D.PARA_ROW_ID FROM T_PARA_TYPE Y JOIN T_PARA_HEADER H ON H.PARA_TYPE_ID=Y.ID JOIN T_PARA_DETAIL D ON H.ID=D.PARA_HEADER_ID
                WHERE Y.TYPE_NAME='福农卡支行考核参数' AND D.DETAIL_VALUE='支行第三季度考核比例'))/ 100) AS FIRST_TAR3,
            COUNT(DISTINCT CASE WHEN F.DATE_ID >= %s||'1001' AND F.DATE_ID<=%s||'1231' THEN D.CARD_NO END) AS CARD_NUM4,
            BIGINT(NVL(TA.TARGET,0)) AS FIRST_TAR4
        FROM F_CREDIT_CARD_STATUS F
            JOIN D_CREDIT_CARD D ON D.ID = F.CARD_ID 
            JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID
            JOIN FUNONG_CARD_TARGET TA ON TA.KYEAR=%s AND TA.ORG_NO=M.SECOND_BRANCH_CODE
            JOIN D_CUST_INFO I ON D.CST_NO=I.CUST_NO
        WHERE 1=1 AND F.STATUS NOT IN('持卡人请求关闭', '呆账核销', '呆账核销清户', '销卡代码', '新卡激活，旧卡失效') AND D.PRODUCT IN ('0632','福农卡966')
        AND F.DUE_DATE >= %s||'01'  AND D.OPEN_DATE <= %s||'1231' 
        AND SUBSTR(I.CUST_LONG_NO,4,20) NOT IN (SELECT CCRD15TO18(ID_NUMBER) FROM F_USER WHERE WORK_STATUS='在职' AND LENGTH(ID_NUMBER)>10)
        %s
        GROUP BY  M.SECOND_BRANCH_CODE,M.SECOND_BRANCH_NAME,TA.TARGET
        """%(self.year,self.year,self.year,self.year,self.year,self.year,self.year,self.year,self.year,self.year,self.year,self.year,filterstr)
        print sql
        row = self.engine.execute(sql, vlist).fetchall()
        needtrans = {}
        rowlist=[]
        for i in row:
            t=list(i[0:3])
            t.append(i[4])
            t.append(i[3])
            per1 = round((float(i[3])/float(i[4]))*100 ,2)
            t.append(per1)
            t.append(i[6])
            t.append(i[5])
            per2 = round((float(i[5])/float(i[6]))*100 ,2)
            t.append(per2)
            t.append(i[8])
            t.append(i[7])
            per3 = round((float(i[7])/float(i[8]))*100 ,2)
            t.append(per3)
            tar_4 = int(int(i[10]) - int(i[8]) - int(i[6]) - int(i[4]))
            t.append(tar_4)
            t.append(i[9])
            per4 = round((float(i[9])/float(tar_4))*100 ,2)
            t.append(per4)
            rowlist.append(t)
        return self.translate(rowlist,needtrans)

    def make_eq_filterstr(self):
        filterstr = ""
        self.year = ''
        vlist = []
        for k, v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org_no':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr + "and M.SECOND_BRANCH_CODE in(%s) "%(vvv)
                elif k == 'kyear':
                    #filterstr = filterstr + "and %s=?"%k
                    self.year = str(v)[0:4]
        
        filterstr = "%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'M.SECOND_BRANCH_CODE',None))
       
        return filterstr, vlist
    def column_header(self):
        return [
            [{'name':'统计年份','h':2},{'name':'机构号','h':2},{'name':'机构名称','h':2},{'name':'第一季度','w':3},{'name':'第二季度','w':3},{'name':'第三季度','w':3},{'name':'第四季度','w':3}],        
            [{'name':'目标任务','h':1},{'name':'发卡量','h':1},{'name':'完成比例','h':1},{'name':'目标任务','h':1},{'name':'发卡量','h':1},{'name':'完成比例','h':1},{'name':'目标任务','h':1},{'name':'发卡量','h':1},{'name':'完成比例','h':1},{'name':'目标任务','h':1},{'name':'发卡量','h':1},{'name':'完成比例','h':1}]
        ]


    @property
    def page_size(self):
        return 10

