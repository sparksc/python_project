# -*- coding:utf-8 -*-
import sys
import datetime
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
客户经理电子银行绩效佣金报表
"""

class Query(ObjectQuery):
  
    def prepare_object(self):
        filterlist1 = ['opendate1','jgbhh','ygghh']
        filterlist2 = ['lastdate1','jgbhh','ygghh']
        filterlist6 = []
        filterstr,vlist,ny = self.make_eq_filterstr(filterlist1)
        filterstr2,vlist2,ny2 = self.make_eq_filterstr(filterlist2)
        filterstr6,vlist6,ny3 = self.make_eq_filterstr(filterlist6)
        sql="""
        select sm.MANAGE_CODE,sm.MANAGE_NAME,sm.open_branch_no,o.ORG0_NAME,count(1) as mobile 
        from F_CONTRACT_STATUS f
        inner join D_CUST_CONTRACT sm on sm.id = f.CONTRACT_ID and busi_type='手机银行'
        inner join D_ORG o  on o.ORG0_CODE=sm.OPEN_BRANCH_NO
        where f.status = '正常' %s
        group by sm.MANAGE_CODE,sm.MANAGE_NAME,sm.open_branch_no,o.ORG0_NAME
        """%(filterstr)
        row = self.engine.execute(sql,vlist).fetchall()
        sql2="""
        select sm.MANAGE_CODE,sm.MANAGE_NAME,sm.open_branch_no,o.ORG0_NAME,count(1) as mobile 
        from F_CONTRACT_STATUS f
        inner join D_CUST_CONTRACT sm on sm.id = f.CONTRACT_ID and busi_type='手机银行'
        inner join D_ORG o  on o.ORG0_CODE=sm.OPEN_BRANCH_NO
        where f.status = '正常' %s
        group by sm.MANAGE_CODE,sm.MANAGE_NAME,sm.open_branch_no,o.ORG0_NAME
        """%(filterstr2)
        row2 = self.engine.execute(sql2,vlist2).fetchall()
        sql3="""
        select sm.MANAGE_CODE,sm.MANAGE_NAME,sm.open_branch_no,o.ORG0_NAME,count(1) as mobile 
        from F_CONTRACT_STATUS f
        inner join D_CUST_CONTRACT sm on sm.id = f.CONTRACT_ID and busi_type='企业网上银行' 
        inner join D_ORG o  on o.ORG0_CODE=sm.OPEN_BRANCH_NO
        where f.status = '正常' %s
        group by sm.MANAGE_CODE,sm.MANAGE_NAME,sm.open_branch_no,o.ORG0_NAME
        """%(filterstr)
        row3 = self.engine.execute(sql3,vlist).fetchall()
        sql4="""
        select sm.MANAGE_CODE,sm.MANAGE_NAME,sm.open_branch_no,o.ORG0_NAME,count(1) as mobile 
        from F_CONTRACT_STATUS f
        inner join D_CUST_CONTRACT sm on sm.id = f.CONTRACT_ID and busi_type='企业网上银行' 
        inner join D_ORG o  on o.ORG0_CODE=sm.OPEN_BRANCH_NO
        where f.status = '正常' %s
        group by sm.MANAGE_CODE,sm.MANAGE_NAME,sm.open_branch_no,o.ORG0_NAME
        """%(filterstr2)
        row4 = self.engine.execute(sql4,vlist2).fetchall()
        """参数查询"""
        sql7=u"""
        select h.HEADER_NAME,d.DETAIL_VALUE
        from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where TYPE_key='XZSJYH' or TYPE_key='XZQYWY' or TYPE_KEY='XZDJK' 
            or type_key='XTZPOS' 
        """
        row7 = self.engine.execute(sql7.encode('utf-8')).fetchall()
        for qm in row7:
            if qm[0]==u'新增手机银行有效户数计价参数':
                cs1=int(qm[1])
            if qm[0]==u'新增企业网银有效户数计价参数':
                cs2=int(qm[1])
        needtrans ={}
        i=0
        resultrow=[]
        if(len(row)>0):
            while True:
                r1=ny
                r2=row[i][0]
                """r2员工号"""
                r3=row[i][1]
                r4=row[i][2]
                r5=row[i][3]
                r6=r7=r8=r9=r10=r11=r12=r13=0
                r71=r72=0
                for mm in row2:
                    if(r2==mm[0]):
                        r6=round((int(row[i][4])-int(mm[4]))*cs1,2)
                        break
                for mm in row3:
                    if(r2==mm[0]):
                        r71=int(mm[4])
                        break
                for mm in row4:
                    if(r2==mm[0]):
                        r72=int(mm[4])
                        break
                r7=(r71-r72)*cs2
                r13=round(r6+r7+r8+r9+r10+r11+r12,2) 
                
                resultrow.append((r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13))
                i=i+1
                if i>=len(row):
                    break
        return self.translate(resultrow,needtrans)


    def make_eq_filterstr(self,filterlist):
        filterstr =""
        vlist = []
        global yearmonthday
        global last_logon1
        global last_logon2
        sql_num=u"""
        select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where HEADER_NAME='电子银行有效户数天数参数（天）'
        """
        row_num = self.engine.execute(sql_num.encode('utf-8')).fetchall()
        day_on=int(row_num[0][1])
        global lastdate
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
                date_on = date - datetime.timedelta(days=day_on)
                #date_on 是day_on/180天以前的日期
                last_logon1=int(date_on.strftime('%Y%m%d'))
                dm=last_logon1%100
                date_on2=date_on-datetime.timedelta(days=dm)
                last_logon2=int(date_on2.strftime('%Y%m%d'))
            if v and k in filterlist:
                if(k=='jgbhh'):
                    filterstr = filterstr+" and sm.open_branch_no = ? "
                    vlist.append(v)
                if(k=='ygghh'):
                    filterstr = filterstr+" and sm.MANAGE_CODE = ? "
                    vlist.append(v)
        
        for k in filterlist:
            if (k=='opendate1'):
                v=yearmonthday
                filterstr = filterstr+" and f.date_id = ? "
                vlist.append(v)
                v=last_logon1
                filterstr = filterstr+" and f.last_logon_date >= ? "
                vlist.append(v)

            if (k=='lastdate1'):
                v=lastdate
                filterstr = filterstr+" and f.date_id = ? "
                vlist.append(v)
                v=last_logon2
                filterstr = filterstr+" and f.last_logon_date >= ? "
                vlist.append(v)
        return filterstr,vlist,yearmonthday/100
    

    def column_header(self):
        return ["统计月份","员工号","员工名称","机构号","机构名称","新增手机银行有效户数效酬","新增企业网银有效户数效酬","新增贷记卡效酬","新拓展pos机1效酬","新拓展pos机2效酬","新增有效丰收e支付效酬","助农服务点月活点指标效酬","电子银行总效酬"]

    @property
    def page_size(self):    
        return 15
