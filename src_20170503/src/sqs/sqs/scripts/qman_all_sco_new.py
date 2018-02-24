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
客户经理绩效得分
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        """
        存款
        """
        sql1 ="""
           SELECT DATE_ID,ORG_CODE,ORG_NAME,SALE_CODE,SALE_NAME,DEP_SCORE/100.00 FROM REPORT_MANAGER_DEP 
           where 1=1 %s
           ORDER BY DATE_ID,ORG_CODE,SALE_CODE desc
            """%(filterstr)
        row1 = self.engine.execute(sql1.encode('utf-8'),vlist).fetchall()

        """
        贷款
        """
        sql2 ="""
            SELECT DATE_ID,ORG_CODE,ORG_NAME,SALE_CODE,SALE_NAME, ALL_SCO/100.00 
            FROM  REPORT_MANAGER_LOAN WHERE 1=1 %s
            ORDER BY DATE_ID,ORG_CODE,SALE_CODE desc
            """%(filterstr)
        row2 = self.engine.execute(sql2.encode('utf-8'),vlist).fetchall()

        """
        电子银行
        """
        sql3 ="""
            SELECT DATE_ID,ORG_CODE,ORG_NAME,SALE_CODE,SALE_NAME, ALL_SCO / 100.00
            FROM REPORT_MANAGER_OTHER WHERE 1=1 %s 
            ORDER BY DATE_ID,ORG_CODE,SALE_CODE desc
            """%(filterstr)
        row3 = self.engine.execute(sql3.encode('utf-8'),vlist).fetchall()
        '''
        附加得分
        '''
        sql5 ="""
            SELECT SYEAR||SMOUTH, ORG_CODE, ORG_NAME, STAFF_CODE, STAFF_NAME, sum(SCORE/100.00) FROM YDW.M_MANAGER_ADD_SCO WHERE TYP='得分' %s group by SYEAR, SMOUTH, ORG_CODE, ORG_NAME, STAFF_CODE, STAFF_NAME
            """%(self.addsal)
        row5 = self.engine.execute(sql5.encode('utf-8')).fetchall()
        print sql5

        """
        先进行员工信息汇总 日期,机构号,机构名称,柜员号,柜员名称
        """
        tellerlist=[]
        for a in row1:
            t = []
            t.insert(0, a[0])   #日期
            t.insert(1, a[1])   #机构号
            t.insert(2, a[2])   #机构名称
            t.insert(3, a[3])   #柜员号
            t.insert(4, a[4])   #柜员名称
            tellerlist.append(t)

        for a in row2:
            t = []
            is_exist = False
            for x in tellerlist:
                if x[1] == a[1] and x[3] == a[3]:
                    is_exist = True
            if is_exist == False: 
                t.insert(0, a[0])
                t.insert(1, a[1])
                t.insert(2, a[2])
                t.insert(3, a[3])
                t.insert(4, a[4])
                tellerlist.append(t)
            
        for a in row3:
            t = []
            is_exist = False
            for x in tellerlist:
                if x[1] == a[1] and x[3] == a[3]:
                    is_exist = True
            if is_exist == False: 
                t.insert(0, a[0])
                t.insert(1, a[1])
                t.insert(2, a[2])
                t.insert(3, a[3])
                t.insert(4, a[4])
                tellerlist.append(t)

        for a in row5:
            t = []
            is_exist = False
            for x in tellerlist:
                if x[1] == a[1] and x[3] == a[3]:
                    is_exist = True
            if is_exist == False: 
                t.insert(0, a[0])
                t.insert(1, a[1])
                t.insert(2, a[2])
                t.insert(3, a[3])
                t.insert(4, a[4])
                tellerlist.append(t)

        rowlist=[]
        for t in tellerlist:
            jgh = t[1]
            ygh = t[3]

            rt=[]
            for i in t:
                rt.append(i)
            total = 0
            total, rt=self.find_same(jgh,ygh,total,row1,rt,1)
            total, rt=self.find_same(jgh,ygh,total,row2,rt,1)
            total, rt=self.find_same(jgh,ygh,total,row3,rt,1)
            total, rt=self.find_same(jgh,ygh,total,row5,rt,1)           

            rt.insert(11, total)

            rowlist.append(tuple(rt))

        needtrans ={}
        row = []
        for i in rowlist:
            t=list(i)
            for j in range(6,10):
                if t[j] is None:t[j]=0
                t[j]=self.amount_trans_dec(t[j])
            row.append(t)    
        return self.translate(row,needtrans)    
    
    def find_same(self,jgh,ygh,total, rowlist,rt,t):

        is_exist = False
        for x in rowlist:
            if jgh==x[1] and ygh==x[3]:
                for i in range(5,len(x)):
                    rt.append(x[i])
                    if x[i] is not None:
                        total = total + x[i]
                    is_exist = True

        if is_exist == False:
            for j in range(t):
                rt.append(0)        
        return total, rt        

    def make_eq_filterstr(self):
        filterstr =""
        self.addsal=""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                    self.addsal=self.addsal+" and ORG_CODE in (%s)"%(vvv)
                elif k == 'DATE_ID':
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
                    v1=v[:4]
                    v2=v[4:6]
                    print v1, v2
                    self.addsal=self.addsal+" and  SYEAR= '%s' and SMOUTH='%s'"%(v1,v2)
                    self.date_id = v 
                elif k=='SALE_CODE':
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
                    self.addsal=self.addsal+" and STAFF_CODE='%s'"%v
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'SALE_CODE','ORG_CODE', None))
        self.addsal ="%s and %s"%(self.addsal,self.get_auth_sql(config.DATATYPE['query'],'STAFF_CODE','ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return ["统计日期","机构号","机构名称","员工号","员工名称","存款业务得分","贷款业务得分","电子银行业务得分","附加分","绩效总得分"]
                                                                                    
    @property
    def page_size(self):
        return 15
