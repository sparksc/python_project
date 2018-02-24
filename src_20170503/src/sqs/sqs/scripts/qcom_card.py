# -*- coding:utf-8 -*-

import sys
import datetime
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
客户经理信用卡业务绩效佣金报表
"""

class Query(ObjectQuery):
  
    def prepare_object(self):
        filterlist1 = ['month1','jgbhh','ygghh']
        filterlist2 = ['month2','jgbhh','ygghh']
        global nyt
        filterstr,vlist,nyt = self.make_eq_filterstr(filterlist1)
        filterstr2,vlist2,ny2 = self.make_eq_filterstr(filterlist2)
        sql1="""
        SELECT ORG0_CODE, ORG0_NAME, SALE_CODE, SALE_NAME, fakaliang
        FROM YDW.M_COM_CARD
        where 1=1 %s
        """%(filterstr)
        row = self.engine.execute(sql1,vlist).fetchall()
        print(">>>>>>>>>>>>>>>>>>") 
        sql2="""
        SELECT ORG0_CODE, ORG0_NAME, SALE_CODE, SALE_NAME, fakaliang
        FROM YDW.M_COM_CARD
        where 1=1 %s
        """%(filterstr2)
        row2 = self.engine.execute(sql2,vlist2).fetchall()
        print(">>>>>>>>>>>>>>>>>")
        """参数查询"""
        sql7=u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_key='xzyh'
        """
        row7 = self.engine.execute(sql7.encode('utf-8')).fetchall()
        cs1=30.000
        for qm in row7:
            if qm[0]==u'每增加一户30':
                cs1=float(qm[1])
        needtrans ={}
        i=0
        resultrow=[]
        if(len(row)>0):
            while True:
                r1=nyt
                r2=row[i][0]
                r3=row[i][1]
                r4=row[i][2]
                """r4员工号"""
                r5=row[i][3]
                q1=row[i][4]
                q2=0
                for mm in row2:
                    if(r4==mm[2] and r2==mm[0]):
                        q2=int(mm[4])
                        break
                p6=int(q1)-int(q2)
                r6=round(float(p6)*cs1,2)
                resultrow.append((r1,r2,r3,r4,r5,r6))
                    
                i=i+1
                if i>=len(row):
                    break
        return self.translate(resultrow,needtrans)
        
    def make_eq_filterstr(self,filterlist):
        filterstr =""
        vlist = []
        global yearmonthdayy
        for k,v in self.args.items():
            if(k=='tdate'):
                if(len(v)!=8):
                    v='10000101'
                yearmonthdayy=int(v)
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
                qw=int(yearmonthdayy/100)
                filterstr = filterstr+" and nn = ? "
                vlist.append(qw)
            if(k=='month2'):
                qw=int(lastdate/100)
                filterstr = filterstr+" and nn = ? "
                vlist.append(qw)
        return filterstr,vlist,yearmonthdayy/100


    def column_header(self):
        return ["统计月份","机构号","机构名称","员工号","员工姓名","发卡量效酬"]

    @property
    def page_size(self):    
        return 15
