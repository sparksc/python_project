# -*- coding:utf-8 -*-

from decimal import Decimal
import datetime
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery

"""
机构其他业务指标报表
"""

class Query(ObjectQuery):
 
    def prepare_object(self):
        self.filterlist = ['date','org']
        filterstr3,filterstr2,filterstr1,vlist6,vlist5,vlist4,vlist3,vlist2,vlist1 = self.make_eq_filterstr()
        sql =u"""
                select branch_code,branch_name,nvl(amt,0) from(
                select org_code,count(1) amt,month_days from v_ebank 
                where busi_type='手机银行' %s %s
                group by org_code,month_days) a
                right join branch b on b.branch_code=a.org_code
                where 1=1 %s
                order by branch_code
                """%(filterstr1,filterstr2,self.org)
        row = self.engine.execute(sql.encode('utf-8'),vlist1+vlist3).fetchall()
        row1 = self.engine.execute(sql.encode('utf-8'),vlist2+vlist4).fetchall()
        print 'sj ok'
        sql2 =u"""
                select branch_code,branch_name,nvl(amt,0) from(
                select org_code,count(1) amt,month_days from v_ebank 
                where busi_type='企业网上银行' %s %s
                group by org_code,month_days) a
                right join branch b on b.branch_code=a.org_code
                where 1=1 %s
                order by branch_code
              """%(filterstr1,filterstr2,self.org)
        row2 = self.engine.execute(sql2.encode('utf-8'),vlist1+vlist3).fetchall()
        row3 = self.engine.execute(sql2.encode('utf-8'),vlist2+vlist4).fetchall()
        print 'wy ok'
        sql4 =u"""
                select branch_code,branch_name,nvl(amt,0) from(
                select org_code,count(1) amt,month_days from v_ebank 
                where busi_type='丰收e支付' %s
                group by org_code,month_days) a
                right join branch b on b.branch_code=a.org_code
                where 1=1 %s
                order by branch_code
              """%(filterstr1,self.org)
        row4 = self.engine.execute(sql4.encode('utf-8'),vlist1).fetchall()
        row5 = self.engine.execute(sql4.encode('utf-8'),vlist2).fetchall()
        print 'epay ok'
        sql5 =u"""
                select branch_code,branch_name,nvl(amt,0) from 
                (select open_branch_no,count(1) amt
                from d_cust_contract c 
                where c.busi_type = '第三方存管' %s %s
                group by open_branch_no) a
                right join branch b on b.branch_code=a.open_branch_no 
                where 1=1 %s
                order by branch_code
                """%(filterstr3,self.branch,self.org)
        print sql5
        row6 = self.engine.execute(sql5.encode('utf-8'),vlist5).fetchall()
        row7 = self.engine.execute(sql5.encode('utf-8'),vlist6).fetchall()
        print 'third'
        sql6 =u"""
                select branch_code,branch_name,nvl(amt,0) from(
                select org_code,count(1) amt,month_days from v_ebank 
                where  busi_type='ETC' %s %s
                group by org_code,month_days) a
                right join branch b on b.branch_code=a.org_code
                where 1=1 %s
                order by branch_code
                """%(filterstr1,filterstr2,self.org)
        row8 = self.engine.execute(sql6.encode('utf-8'),vlist1+vlist3).fetchall()
        row9 = self.engine.execute(sql6.encode('utf-8'),vlist2+vlist4).fetchall()
        print 'etc ok'
        i=-1
        rr=[]
        while True:
            i+=1
            if i>=len(row):
                break
            sj = int(row[i][2])-int(row1[i][2])
            wy = int(row2[i][2])-int(row3[i][2])
            epay = int(row4[i][2])-int(row5[i][2])
            third = int(row6[i][2])-int(row7[i][2])
            etc = int(row8[i][2])-int(row9[i][2])
            c1 = self.trans_dec(sj)
            c2 = self.trans_dec(wy)
            c3 = '0'#self.trans_dec()
            c4 = '0'#self.trans_dec()
            c5 = self.trans_dec(epay)
            c6 = self.trans_dec(row7[i][2])
            c7 = self.trans_dec(third)
            c8 = self.trans_dec(etc)
            c9 = '0'#self.trans_dec()
            rr.append((self.ym,row[i][0],row[i][1],c1,c2,c3,c4,c5,c6,c7,c8,c9))
        needtrans ={}
        return self.translate(rr,needtrans)

    def make_eq_filterstr(self):
        filterstr1=filterstr2=filterstr3 = " "
        vlist1,vlist2,vlist3,vlist4,vlist5,vlist6 = [],[],[],[],[],[]
        self.org=""
        self.branch=""
        sql_num=u"""
                select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
                join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
                join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
                where HEADER_NAME='电子银行有效户数天数参数（天）'
                """
        row_num = self.engine.execute(sql_num.encode('utf-8')).fetchall()
        day_on=int(row_num[0][1])
        
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'date':
                    #获得当前日期[date],上月末日期[date_l],有效户判定日期[date_t][date_lt]
                    self.yy = int(v[0:4])
                    self.ym = int(v[0:6])
                    self.dd = int(v[6:8])
                    date = datetime.datetime.strptime(v,'%Y%m%d')
                    date_l = date - datetime.timedelta(days=self.dd)
                    date_t = date - datetime.timedelta(days=day_on)
                    date_lt = date_l - datetime.timedelta(days=day_on)
                    date_t = date_t.strftime('%Y%m%d')
                    date_l = date_l.strftime('%Y%m%d')
                    date_lt = date_lt.strftime('%Y%m%d')
                    
                    filterstr1 = filterstr1 + " and date= ? "
                    vlist1.append(v)
                    vlist2.append(date_l)
                    filterstr1 = filterstr1 + " and l_date>= ? "
                    vlist1.append(date_t)
                    vlist2.append(date_lt)
                    filterstr2 = filterstr2 + " and t_date>= ? "
                    vlist3.append(date_t)
                    vlist4.append(date_lt)
                    
                    filterstr3 = filterstr3 + " and open_date <= ? "
                    vlist5.append(v)
                    vlist6.append(date_l)
                if k == 'org':
                    #获取机构号
                    vv = self.dealfilterlist(v)
                    self.org=vv
                    self.branch=vv
                    filterstr1 = filterstr1 + " and org_code in (%s) "%(vv)
        if self.org<>"":
            self.org = " and branch_code in (%s)"%(self.org)
            self.branch = " and open_branch_no in (%s)"%(self.branch)
        return filterstr3,filterstr2,filterstr1,vlist6,vlist5,vlist4,vlist3,vlist2,vlist1

    def column_header(self):
        return ["统计月份","机构号","机构名称","新增手机银行有效户数","新增企业网银有效户数","新拓展POS机1","新拓展POS机2","新增有效丰收e支付","第三方存管存量户数","第三方存管增量户数","新增ETC","助农服务点月平均活点率"]
    def trans_dec(self,num):
        tmp = Decimal(num)
        tmp = '{:,}'.format(tmp)
        return tmp
    @property
    def page_size(self):
        return 15
