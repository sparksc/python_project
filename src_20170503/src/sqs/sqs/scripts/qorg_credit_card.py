# -*- coding:utf-8 -*-

import sys
import datetime
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
机构信用卡业务报表
"""

class Query(ObjectQuery):
  
    def prepare_object(self):
        filterlist1 = ['month1','jgbhh']
        filterlist2 = ['month2','jgbhh']
        filterlist3 = ['month3','jgbhh']
        global ny 
        filterstr,vlist,ny = self.make_eq_filterstr(filterlist1)
        filterstr2,vlist2,ny2 = self.make_eq_filterstr(filterlist2)
        filterstr3,vlist3,ny3 = self.make_eq_filterstr(filterlist3)
        sql1="""
        SELECT ORG0_CODE, ORG0_NAME, sum(fakaliang)
        FROM YDW.M_COM_CARD
        where  1=1  %s
        group by ORG0_CODE, ORG0_NAME
        """%(filterstr)
        row = self.engine.execute(sql1,vlist).fetchall()
        
        sql2="""
        SELECT ORG0_CODE, ORG0_NAME, sum(fakaliang)
        FROM YDW.M_COM_CARD
        where  1=1  %s
        group by ORG0_CODE, ORG0_NAME
        """%(filterstr2)
        row2 = self.engine.execute(sql2,vlist2).fetchall()
        sql3="""
        select org0_code,org0_name,sum(buliangl1) as x, sum(buliangl2) as x2
        from m_com_card2
        where 1=1 %s
        group by org0_code,org0_name
        """%(filterstr3)
        row3 = self.engine.execute(sql3,vlist3).fetchall()
        needtrans ={}
        i=0
        resultrow=[]
        if(len(row)>0):
            while True:
                r1=ny
                r2=row[i][0]
                r3=row[i][1]
                q1=row[i][2]
                q2=r5=0
                q4=0.00
                q5=1.00
                for mm in row2:
                    if(r2==mm[0]):
                        q2=int(mm[2])
                        break
                for mm in row3:
                    if(r2==mm[0]):
                        q4=float(mm[2])
                        q5=float(mm[3])
                        break
                r4=int(q1)-int(q2)
                if q5>0:
                    r5=q4/q5
                resultrow.append((r1,r2,r3,r4,round(r5,2),0,0))
                    
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
                    vv = self.dealfilterlist(v)
                    filterstr = filterstr+" and ORG0_CODE in (%s) "%(vv)
        for k in filterlist:
            if(k=='month1'):
                qw=int(yearmonthday/100)
                filterstr = filterstr+" and nn = ? "
                vlist.append(qw)
            if(k=='month2'):
                qw=int(lastdate/100)
                filterstr = filterstr+" and nn = ? "
                vlist.append(qw)
        return filterstr,vlist,int(yearmonthday/100)


    def column_header(self):
        return ["统计月份","机构号","机构名称","发卡量","不良率","新增贷记卡","新增贷记卡逾期本金"]

    @property
    def page_size(self):    
        return 15
