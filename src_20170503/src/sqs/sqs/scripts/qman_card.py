# -*- coding:utf-8 -*-

import sys
import datetime
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
客户经理信用卡业务报表
"""

class Query(ObjectQuery):
  
    def prepare_object(self):
        filterlist1 = ['month1','jgbhh','ygghh']
        filterlist2 = ['month2','jgbhh','ygghh']
        filterlist3 = ['month3','jgbhh','ygghh']
        filterstr,vlist,ny = self.make_eq_filterstr(filterlist1)
        filterstr2,vlist2,ny2 = self.make_eq_filterstr(filterlist2)
        filterstr3,vlist3,ny32 = self.make_eq_filterstr(filterlist3)
        sql1="""
        SELECT ORG0_CODE, ORG0_NAME, SALE_CODE, SALE_NAME, fakaliang
        FROM YDW.M_COM_CARD
        where 1=1 %s
        """%(filterstr)
        row = self.engine.execute(sql1,vlist).fetchall()
        sql2="""
        SELECT ORG0_CODE, ORG0_NAME, SALE_CODE, SALE_NAME, fakaliang
        FROM YDW.M_COM_CARD
        where 1=1 %s
        """%(filterstr2)
        row2 = self.engine.execute(sql2,vlist2).fetchall()
        sql3="""
        select org0_code,org0_name,sale_code,sale_name,sum(buliangl1) as x, sum(buliangl2) as x2
        from m_com_card2
        where 1=1 %s
        group by org0_code,org0_name,sale_code,sale_name
        """%(filterstr3)
        row3 = self.engine.execute(sql3,vlist3).fetchall()
        print(row3,">>>>>>>>>>>>>>>")
        needtrans ={}
        i=0
        resultrow=[]
        if(len(row)>0):
            while True:
                r1=ny
                r2=row[i][0]
                r3=row[i][1]
                r4=row[i][2]
                """r4员工号"""
                r5=row[i][3]
                q1=row[i][4]
                r7=q2=0
                q4=0.000
                q5=1.00
                for mm in row2:
                    if(r4==mm[2] and r2==mm[0]):
                        q2=int(mm[4])
                        break
                for mm in row3:
                    if(r4==mm[2] and r2==mm[0]):
                        q4=float(mm[4])
                        q5=float(mm[5])
                        break
                r6=int(q1)-int(q2)
                if q5>0:
                    r7=q4/q5

                resultrow.append((r1,r2,r3,r4,r5,r6,round(r7,2),0,0))
                    
                i=i+1
                if i>=len(row):
                    break
        return self.translate(resultrow,needtrans)
        
    def make_eq_filterstr(self,filterlist):
        filterstr =""
        vlist = []
        global yearmonthday
        for k,v in self.args.items():
            if(k=='tdate'):
                if(len(v)!=8):
                    v='10000101'
                yearmonthday=int(v)
                yy = int(v[0:4])
                ym = int(v[0:6])
                dd = int(v[6:8])
                date = datetime.datetime.strptime(v,'%Y%m%d')
                ladate = date - datetime.timedelta(days=dd)
                #lastdate是上个月月末
                lastdate=int(ladate.strftime('%Y%m%d'))
            if v and k in filterlist:
                if(k=='jgbhh'):
                    filterstr = filterstr+" and ORG0_CODE = ? "
                    vlist.append(v)
                if(k=='ygghh'):
                    filterstr = filterstr+" and SALE_CODE = ? "
                    vlist.append(v)
        for k in filterlist:
            if(k=='month1'):
                qw=int(yearmonthday/100)
                filterstr = filterstr+" and nn = ? "
                vlist.append(qw)
            if(k=='month2'):
                qw=int(lastdate/100)
                filterstr = filterstr+" and nn = ? "
                vlist.append(qw)
            if(k=='month3'):
                qw=int(yearmonthday/100)
                filterstr = filterstr+" and ym = ? "
                vlist.append(qw)
        return filterstr,vlist,yearmonthday/100


    def column_header(self):
        return ["统计月份","机构号","机构名称","员工号","员工姓名","发卡量","不良率","新增贷记卡","新增丰收贷记卡逾期本金"]

    @property
    def page_size(self):    
        return 15
