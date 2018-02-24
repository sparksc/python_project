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
客户经理不良贷款业务佣金报表
"""

class Query(ObjectQuery):
  
    def prepare_object(self):
        filterlist1 = ['DONE_DATE_ID1','org']
        filterlist2 = ['DONE_DATE_ID2','org']
        filterlist3 = ['DONE_DATE_ID3','org']
        filterlist4 = ['DONE_DATE_ID4','org']
        filterlist6 = []
        global ny1
        filterstr1,vlist1,ny1 = self.make_eq_filterstr(filterlist1)
        filterstr2,vlist2,ny2 = self.make_eq_filterstr(filterlist2)
        filterstr3,vlist3,ny3 = self.make_eq_filterstr(filterlist3)
        filterstr4,vlist4,ny4 = self.make_eq_filterstr(filterlist4)
        filterstr6,vlist6,ny3 = self.make_eq_filterstr(filterlist6)
        sql="""     
        SELECT AFAABRNO,ORG0_NAME,sum(RES1),sum(RES2),sum(RES3)
        FROM OLD_BAD_LOANS
        WHERE 1=1 %s
        group by AFAABRNO,ORG0_NAME
        """%(filterstr1)
        print sql
        row1 = self.engine.execute(sql,vlist1).fetchall()
        sql2="""
        SELECT AFAABRNO,ORG0_NAME,sum(RES1),sum(RES2),sum(RES3)
        FROM OLD_BAD_LOANS
        WHERE 1=1 %s
        group by AFAABRNO,ORG0_NAME
        """%(filterstr2)
        row2 = self.engine.execute(sql2,vlist2).fetchall()
        sql3="""
        SELECT AFAABRNO,ORG0_NAME,sum(RES1),sum(RES2),sum(RES3)
        FROM OLD_BAD_LOANS
        WHERE 1=1 %s
        group by AFAABRNO,ORG0_NAME
        """%(filterstr3)
        row3 = self.engine.execute(sql3,vlist3).fetchall()
        sql4="""
        SELECT AFAABRNO,ORG0_NAME,sum(RES1),sum(RES2),sum(RES3)
        FROM OLD_BAD_LOANS
        WHERE 1=1 %s
        group by AFAABRNO,ORG0_NAME
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
        result=[]
        print row4
        for i in row4:
            print i
            r1=str(ny4)
            r2=str(i[0])
            r3=i[1]
            p41=float(i[2])*cs81
            p51=float(i[3])*cs82
            p61=float(i[4])*cs82
            r4=(p41+p51+p61)/100.0
            result.append((r1,r2,r3,r4))
        for i in row3:
            r1=str(ny3)
            r2=str(i[0])
            r3=i[1]
            p41=float(i[2])*cs71
            p51=float(i[3])*cs72
            p61=float(i[4])*cs72
            r4=(p41+p51+p61)/100.0
            result.append((r1,r2,r3,r4))
        for i in row2:
            r1=str(ny2)
            r2=str(i[0])
            r3=i[1]
            p41=float(i[2])*cs61
            p51=float(i[3])*cs62
            p61=float(i[4])*cs62
            r4=(p41+p51+p61)/100.0
            result.append((r1,r2,r3,r4))
        for i in row1:
            r1=str(ny1)
            r2=str(i[0])
            r3=i[1]
            p41=float(i[2])*cs51
            p51=float(i[3])*cs52
            p61=float(i[4])*cs52
            r4=(p41+p51+p61)/100.0
            result.append((r1,r2,r3,r4))
        print result
        f={}
        for i in result:
            i=list(i)
            if i[0]+i[1] in f:
                f[i[0]+i[1]][3]=f[i[0]+i[1]][3]+i[3]
            else:
                f[i[0]+i[1]]=i
        result=f.values()
        resultrowlist=[]
        for i in result:
            t=list(i[0:3])
            for j in i[3:]:
                if j is None:j=0
                j=self.amount_trans_dec(j)
                t.append(j)
            resultrowlist.append(t)
        return self.translate(resultrowlist,needtrans)
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
            print k,v
            if(k=='DATE_ID'):
                yearmonthday=int(v)/100
                f=int(str(v)[:4]+'01') 
                filterstr = filterstr+" and LCAJDATE >=%s  and LCAJDATE <= %s "%(f,yearmonthday)
            if v and k in filterlist:
                if(k=='org'):
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr+" and AFAABRNO in (%s) "%(vvv)
        for k in filterlist:
            if (k=='DONE_DATE_ID1'):
                qp=cs1
                filterstr = filterstr+" and DONE_DATE_ID <= ? "
                vlist.append(qp)
            if (k=='DONE_DATE_ID2'):
                qp=cs1
                filterstr = filterstr+" and DONE_DATE_ID > ? "
                vlist.append(qp)
                qp=cs2
                filterstr = filterstr+" and DONE_DATE_ID <= ? "
                vlist.append(qp)
            if (k=='DONE_DATE_ID3'):
                qp=cs2
                filterstr = filterstr+" and DONE_DATE_ID > ? "
                vlist.append(qp)
                qp=cs3
                filterstr = filterstr+" and DONE_DATE_ID <= ? "
                vlist.append(qp)
            if (k=='DONE_DATE_ID4'):
                qp=cs3
                filterstr = filterstr+" and DONE_DATE_ID > ? "
                vlist.append(qp)
                qp=cs4
                filterstr = filterstr+" and DONE_DATE_ID <= ? "
                vlist.append(qp)
        print(filterstr,vlist,yearmonthday)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'AFAABRNO', None))
        return filterstr,vlist,yearmonthday
            
        
    def column_header(self):
        return ["统计月份","机构号","机构名称","旧欠不良贷款清收"] 
    @property
    def page_size(self):
        return 15
