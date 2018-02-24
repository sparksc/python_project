# -*- coding:utf-8 -*-
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from utils import config
"""
客户经理不良贷款业务佣金报表
"""

class Query(ObjectQuery):
  
    def prepare_object(self):
        filterlist1 = ['LCAJDATE1','jgbhh']
        filterlist2 = ['LCAJDATE2','jgbhh']
        filterlist3 = ['LCAJDATE3','jgbhh']
        filterlist4 = ['LCAJDATE4','jgbhh']
        filterlist6 = []
        global ny1
        filterstr1,vlist1,ny1 = self.make_eq_filterstr(filterlist1)
        filterstr2,vlist2,ny2 = self.make_eq_filterstr(filterlist2)
        filterstr3,vlist3,ny3 = self.make_eq_filterstr(filterlist3)
        filterstr4,vlist4,ny4 = self.make_eq_filterstr(filterlist4)
        filterstr6,vlist6,ny3 = self.make_eq_filterstr(filterlist6)
        sql="""     
        SELECT LCAABRNO,ORG0_NAME,sum(RES1),sum(RES2),sum(RES3)
        FROM M_COM_BAD
        WHERE 1=1 %s
        group by LCAABRNO,ORG0_NAME
        """%(filterstr1)
        row1 = self.engine.execute(sql,vlist1).fetchall()
        sql2="""
        SELECT LCAABRNO,ORG0_NAME,sum(RES1),sum(RES2),sum(RES3)
        FROM M_COM_BAD
        WHERE 1=1 %s
        group by LCAABRNO,ORG0_NAME
        """%(filterstr2)
        row2 = self.engine.execute(sql2,vlist2).fetchall()
        sql3="""
        SELECT LCAABRNO,ORG0_NAME,sum(RES1),sum(RES2),sum(RES3)
        FROM M_COM_BAD
        WHERE 1=1 %s
        group by LCAABRNO,ORG0_NAME
        """%(filterstr3)
        row3 = self.engine.execute(sql3,vlist3).fetchall()
        sql4="""
        SELECT LCAABRNO,ORG0_NAME,sum(RES1),sum(RES2),sum(RES3)
        FROM M_COM_BAD
        WHERE 1=1 %s
        group by LCAABRNO,ORG0_NAME
        """%(filterstr4)
        row4 = self.engine.execute(sql4,vlist4).fetchall()
        """参数查询"""
        sql5=u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_key='BLDKQS'
        """
        row5 = self.engine.execute(sql5.encode('utf-8')).fetchall()
        for qm in row5:
            if qm[0]==u'本金计酬比例1':
                cs51=float(qm[1])
            if qm[0]==u'本金计酬比例2':
                cs61=float(qm[1])
            if qm[0]==u'本金计酬比例3':
                cs71=float(qm[1])
            if qm[0]==u'本金计酬比例4':
                cs81=float(qm[1])
            if qm[0]==u'利息计酬比例1':
                cs52=float(qm[1])
            if qm[0]==u'利息计酬比例2':
                cs62=float(qm[1])
            if qm[0]==u'利息计酬比例3':
                cs72=float(qm[1])
            if qm[0]==u'利息计酬比例4':
                cs82=float(qm[1])
        needtrans ={}
        i=0
        resultrow=[]
        if(len(row4)>0):
            while True:
                r1=ny1
                r2=row4[i][0]
                r3=row4[i][1]
                p41=float(row4[i][2])*cs81
                p51=float(row4[i][3])*cs82
                p61=float(row4[i][4])*cs82
                p42=p52=p62=p43=p53=p63=p44=p54=p64=0.00
                for mm in row3:
                    if(r2==mm[0]):
                        p42=float(mm[2])*cs71
                        p52=float(mm[3])*cs72
                        p62=float(mm[4])*cs72
                for mm in row2:
                    if(r2==mm[0]):
                        p43=float(mm[2])*cs61
                        p53=float(mm[3])*cs62
                        p63=float(mm[4])*cs62
                for mm in row1:
                    if(r2==mm[0]):
                        p44=float(mm[2])*cs51
                        p54=float(mm[3])*cs52
                        p64=float(mm[4])*cs52
                r4=round((p41+p42+p43+p44+p51+p52+p53+p54+p61+p62+p63+p64)/100,2)
                resultrow.append((r1,r2,r3,r4))
                i=i+1
                if i>=len(row4):
                    break
        return self.translate(resultrow,needtrans)
    def make_eq_filterstr(self,filterlist):
        filterstr =""
        vlist = []
        global yearmonthday
        """参数查询"""
        sql7=u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_key='BLDKQS'
        """
        row7 = self.engine.execute(sql7.encode('utf-8')).fetchall()
        for qm in row7:
            if qm[0]==u'产生时间1':
                cs1=int(qm[1])#20041231
            if qm[0]==u'产生时间2':
                cs2=int(qm[1])#20101231
            if qm[0]==u'产生时间3':
                cs3=int(qm[1])#20131231
            if qm[0]==u'产生时间4':
                cs4=int(qm[1])#20151231
        for k,v in self.args.items():
            if(k=='tdate'):
                yearmonthday=int(v)
            if v and k in filterlist:
                if(k=='jgbhh'):
                    filterstr = filterstr+" and LCAABRNO = ? "
                    vlist.append(v)
        for k in filterlist:
            if (k=='LCAJDATE1'):
                qp=str(cs1/10000)+'-'+str(cs1/100%100)+'-'+str(cs1%100)
                filterstr = filterstr+" and LCAJDATE <= ? "
                vlist.append(qp)
            if (k=='LCAJDATE2'):
                qp=str(cs1/10000)+'-'+str(cs1/100%100)+'-'+str(cs1%100)
                filterstr = filterstr+" and LCAJDATE > ? "
                vlist.append(qp)
                qp=str(cs2/10000)+'-'+str(cs2/100%100)+'-'+str(cs2%100)
                filterstr = filterstr+" and LCAJDATE <= ? "
                vlist.append(qp)
            if (k=='LCAJDATE3'):
                qp=str(cs2/10000)+'-'+str(cs2/100%100)+'-'+str(cs2%100)
                filterstr = filterstr+" and LCAJDATE > ? "
                vlist.append(qp)
                qp=str(cs3/10000)+'-'+str(cs3/100%100)+'-'+str(cs3%100)
                filterstr = filterstr+" and LCAJDATE <= ? "
                vlist.append(qp)
            if (k=='LCAJDATE4'):
                qp=str(cs3/10000)+'-'+str(cs3/100%100)+'-'+str(cs3%100)
                filterstr = filterstr+" and LCAJDATE > ? "
                vlist.append(qp)
                qp=str(cs4/10000)+'-'+str(cs4/100%100)+'-'+str(cs4%100)
                filterstr = filterstr+" and LCAJDATE <= ? "
                vlist.append(qp)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'LCAABRNO', None))
        return filterstr,vlist,yearmonthday/100
            
        
    def column_header(self):
        return ["统计月份","机构号","机构名称","旧欠不良贷款清收"] 
    @property
    def page_size(self):
        return 15
