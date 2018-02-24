# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
客户经理存款绩效佣金报表
"""

class Query(ObjectQuery):
  
    def prepare_object(self):
        filterlist1 = ['year','month','jgbhh','ygghh']
        filterlist2 = ['year','jgbhh','ygghh']
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
        sql3=u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_key='FJCRC'
        """
        row3 = self.engine.execute(sql3.encode('utf-8')).fetchall()
        for i in row3:
            if i[0]==u'存量日均存款计价参数':
                cs1=float(i[1])
            else:
                cs1=0
        sql4=u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_key='XZRJCK'
        """
        row4 = self.engine.execute(sql4.encode('utf-8')).fetchall()
        for i in row4:
            if i[0]==u'新增日均存款计价参数':
                cs2=float(i[1])
            else:
                cs2=0.00
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
                        r1=round(float(c2*cs1/10000/100),2)
                        r2=round(float((c1-c2)*cs2/10000/100),2)
                        break
                resultrow.append((ny,h2,h3,h4,h5,r1,r2,round(r1+r2,2)))
                i=i+1
                if i>=len(row):
                    break


        return self.translate(resultrow,needtrans)
        
    def make_eq_filterstr(self,filterlist):
        filterstr =""
        vlist = []
        global ymday
        for k,v in self.args.items():
            if(k=='tdate'):
                ymday=v
            if v and k in filterlist:
                if(k=='jgbhh'):
                    filterstr = filterstr+" and THIRD_BRANCH_CODE = ? "
                    vlist.append(v)
                if(k=='ygghh'):
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
        return ["统计月份","机构号","机构名称","员工号","员工名称","存量日均存款效酬","新增日均存款效酬","存款总效酬"]

    @property
    def page_size(self):    
        return 15
