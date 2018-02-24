# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery

"""
客户经理机构信用卡业务绩效佣金报表
"""

class Query(ObjectQuery):
 
    def prepare_object(self):
        self.filterlist = ['ORG0_CODE']
        self.filterlist1 = ['DATE_ID1']
        self.filterlist2 = ['DATE_ID2']
        self.filterlist3 = ['SALE_CODE']
        global ym
        filterstr3,filterstr1,filterstr2,filterstr,vlist1,vlist2,ym = self.make_eq_filterstr()
        
        sql =u"""
                SELECT o.ORG0_CODE,o.ORG0_NAME,t.SALE_CODE,t.SALE_NAME,count(1) AS 发卡量 FROM F_CREDIT_CARD_STATUS f
                INNER JOIN D_CREDIT_CARD d ON d.ID=f.CARD_ID 
                INNER JOIN D_ORG o ON o.ORG0_CODE=d.OPEN_BRANCH_CODE %s
                INNER JOIN D_TELLER t ON t.SALE_CODE=d.MANAGE_CODE %s
                WHERE STATUS NOT IN( '持卡人请求关闭','销卡代码','新卡激活，旧卡失效','呆账核销','呆账核销清户') %s 
                GROUP BY o.ORG0_CODE,o.ORG0_NAME,t.SALE_CODE,t.SALE_NAME
                ORDER BY o.ORG0_CODE
                """%(filterstr,filterstr3,filterstr1)
          
        row = self.engine.execute(sql.encode('utf-8'),vlist1).fetchall()
        print (row)
        sql1 =u"""
                 SELECT o.ORG0_CODE,o.ORG0_NAME,t.SALE_CODE,t.SALE_NAME,count(1) AS 发卡量 FROM F_CREDIT_CARD_STATUS f
                 INNER JOIN D_CREDIT_CARD d ON d.ID=f.CARD_ID 
                 INNER JOIN D_ORG o ON o.ORG0_CODE=d.OPEN_BRANCH_CODE %s
                 INNER JOIN D_TELLER t ON t.SALE_CODE=d.MANAGE_CODE %s
                 WHERE STATUS NOT IN( '持卡人请求关闭','销卡代码','新卡激活，旧卡失效','呆账核销','呆账核销清户') %s 
                 GROUP BY o.ORG0_CODE,o.ORG0_NAME,t.SALE_CODE,t.SALE_NAME
                 ORDER BY o.ORG0_CODE
                 """%(filterstr,filterstr3,filterstr2)
        row1 = self.engine.execute(sql1.encode('utf-8'),vlist2).fetchall()
        
        sql4=u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where  TYPE_KEY='xzyh'
            """
        row4 = self.engine.execute(sql4.encode('utf-8')).fetchall()
        i=0
        rr=[]
        while True:
            c = (int(row[i][4])-int(row1[i][4]))*int(row4[0][1])
            rr.append((ym,row[i][0],row[i][1],row[i][2],row[i][3],c))
            i+=1
            if i>=len(row1):
                break
        needtrans ={}
        print rr
        return self.translate(rr,needtrans)
    def make_eq_filterstr(self):
        filterstr = ""
        filterstr1 = ""
        filterstr2 = ""
        filterstr3 = ""
        vlist1 = []
        vlist2 = []
        global yy
        for k,v in self.args.items():
            if v and k in self.filterlist1:
                k[:-1] == 'DATE_ID'
                filterstr1 = filterstr1+" and %s = ? "%(k[:-1])      
                vlist1.append(v)
                yy = v[0:6] 
       
        for k,v in self.args.items():
            if v and k in self.filterlist2:
                k[:-1] == 'DATE_ID'
                filterstr2 = filterstr2+" and %s = ? "%(k[:-1])
                vlist2.append(v)

        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ? "%k
                vlist1.append(v)
                vlist2.append(v)
               
        return filterstr3,filterstr1,filterstr2,filterstr,vlist1,vlist2,yy
    def column_header(self):
        return ["统计月份","机构号","机构名","客户号","客户名","发卡量效酬"]
    @property
    def page_size(self):
        return 15
