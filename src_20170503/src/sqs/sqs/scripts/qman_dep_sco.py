# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
客户经理存款得分
"""

class Query(ObjectQuery):
 
    def prepare_object(self):
        filterlist1 = ['year','month','BRANCH_CODE','SALE_CODE']
        filterlist2 = ['year','jgbhh','SALE_CODE']
        global ny 
        filterstr,vlist,ny = self.make_eq_filterstr(filterlist1)
        filterstr2,vlist2,ny2 = self.make_eq_filterstr(filterlist2)
        sql1="""
        SELECT THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME, MONTH_DAYS, YEAR_DAYS, sum(sun_balance) 
        FROM YDW.M_COM_DEP
        where ACCT_TYPE ='1' %s
        group by THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME, MONTH_DAYS, YEAR_DAYS
        """%(filterstr)
        row = self.engine.execute(sql1,vlist).fetchall()
        
        sql2="""
        SELECT THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME, sum(sun_balance) 
        FROM YDW.M_COM_DEP
        where ACCT_TYPE ='1' %s
        group by THIRD_BRANCH_CODE, THIRD_BRANCH_NAME, SALE_CODE, SALE_NAME
        """%(filterstr2)
        row2 = self.engine.execute(sql2,vlist2).fetchall()
        """参数"""
        ''' 客户经理考核增量'''
        sql3=u"""
        select MANAGER_CODE,BASE,TARGET from P_DEP_NUM 
            """
        row3 = self.engine.execute(sql3.encode('utf-8')).fetchall()
        ''' 取得 标准分，最高分，最低分'''
        sql4=u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_NAME='新增日均存款得分'
            """
        row4 = self.engine.execute(sql4.encode('utf-8')).fetchall()
        stdc=maxc=minc=0
        for i in row4:
            if i[0]==u'标准分':
                stdc=int(i[1])
            elif i[0]==u'最高分':
                maxc=int(i[1])
            elif i[0]==u'最低分':
                minc=int(i[1])
        needtrans ={}
        i=0
        resultrow=[]
        if(len(row)>0):
            month_days=row[0][4]
            year_days=row[0][5]
            while True:
                h2=row[i][0]
                """r2是机构号"""
                h3=row[i][1]
                h4=row[i][2]
                """r4是员工号"""
                h5=row[i][3]
                c1=c2=0.00
                for mm in row2:
                    if(h2==mm[0] and h4==mm[2]):
                        c1=float(row[i][6])/month_days
                        c2=float(mm[4])/year_days
                        r1=float(c2)
                        r2=float(c1-c2)
                        break
                score = (r2)/float(row3[0][2])*stdc
                if score>maxc:score=maxc
                if score<minc:score=minc
                qm1=round(score,2)
                resultrow.append((ny/100,ny%100,h2,h3,h4,h5,qm1,qm1))
                i=i+1
                if i>=len(row):
                    break
        return self.translate(resultrow,needtrans)


    def make_eq_filterstr(self,filterlist):
        filterstr =""
        vlist = []
        global ymday
        for k,v in self.args.items():
            if(k=='S_DATE'):
                ymday=v
            if v and k in filterlist:
                if(k=='BRANCH_CODE'):
                    filterstr = filterstr+" and THIRD_BRANCH_CODE = ? "
                    vlist.append(v)
                if(k=='SALE_CODE'):
                    filterstr = filterstr+" and SALE_CODE = ? "
                    vlist.append(v)
        if(len(ymday)!=8):
            ymday='10000101'
        for k in filterlist:
            if(k=='year'):
                v=int(ymday)/100/100
                filterstr = filterstr+" and %s = ? "%k
                vlist.append(v)
            if(k=='month'):
                v=int(ymday)/100%100
                filterstr = filterstr+" and %s = ? "%k
                vlist.append(v)
            
        return filterstr,vlist,int(ymday)/100

    def column_header(self):
        return ["统计年份","统计月份","机构号","机构名称","员工号","员工名称","新增日均存款得分","存款绩效得分"]
    @property
    def page_size(self):
        return 15
