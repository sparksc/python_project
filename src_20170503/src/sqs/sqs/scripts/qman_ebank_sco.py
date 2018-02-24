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
客户经理其他业务得分指标报表
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['BRANCH_CODE','SALE_CODE','S_DATE']
        filterstr3,filterstr2,filterstr1,vlist6,vlist5,vlist4,vlist3,vlist2,vlist1 = self.make_eq_filterstr()
        sql1 =u"""
                select branch_code,branch_name,user_name,name,nvl(amt,0) from(
                select org_code,sale_code,count(1) amt from v_ebank 
                where busi_type='手机银行' %s %s
                group by org_code,sale_code) a
                right join teller t on t.user_name=a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(filterstr1,filterstr2,self.org)
        print sql1
        row = self.engine.execute(sql1.encode('utf-8'),vlist1+vlist3).fetchall()
        row1 = self.engine.execute(sql1.encode('utf-8'),vlist2+vlist4).fetchall()
        sql2 =u"""
                select branch_code,branch_name,user_name,name,nvl(amt,0) from(
                select org_code,sale_code,count(1) amt from v_ebank 
                where busi_type='企业网上银行' %s %s
                group by org_code,sale_code) a
                right join teller t on t.user_name=a.sale_code
                where 1=1 %s
                order by branch_code,user_name
              """%(filterstr1,filterstr2,self.org)
        print sql2
        row2 = self.engine.execute(sql2.encode('utf-8'),vlist1+vlist3).fetchall()
        row3 = self.engine.execute(sql2.encode('utf-8'),vlist2+vlist4).fetchall()
        sql3 =u"""
                select branch_code,branch_name,user_name,name,nvl(amt,0) from(
                select org_code,sale_code,count(1) amt from v_ebank 
                where busi_type='丰收e支付' %s
                group by org_code,sale_code) a
                right join teller t on t.user_name=a.sale_code
                where 1=1 %s
                order by branch_code,user_name
              """%(filterstr1,self.org)
        print sql3
        row4 = self.engine.execute(sql3.encode('utf-8'),vlist1).fetchall()
        row5 = self.engine.execute(sql3.encode('utf-8'),vlist2).fetchall()
        sql4 =u"""
                select branch_code,branch_name,user_name,name,nvl(amt,0) from(
                select org_code,sale_code,count(1) amt from v_ebank 
                where  busi_type='ETC' %s %s
                group by org_code,sale_code)  a
                right join teller t on t.user_name=a.sale_code
                where 1=1 %s
                order by branch_code,user_name
                """%(filterstr1,filterstr2,self.org)
        print sql4
        row6 = self.engine.execute(sql4.encode('utf-8'),vlist1+vlist3).fetchall()
        row7 = self.engine.execute(sql4.encode('utf-8'),vlist2+vlist4).fetchall()
        sql_sj =u"""
                select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
                join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
                join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
                where TYPE_NAME='新增手机银行有效户数得分参数'
                order by h.HEADER_NAME
                """
        row_sj = self.engine.execute(sql_sj.encode('utf-8')).fetchall()

        sql_wy =u"""
                select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
                join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
                join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
                where TYPE_NAME='新增企业网银有效户数得分参数'
                order by h.HEADER_NAME
                """
        row_wy = self.engine.execute(sql_wy.encode('utf-8')).fetchall()

        sql_pos =u"""
                select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
                join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
                join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
                where TYPE_NAME='新拓展pos机得分参数'
                order by h.HEADER_NAME
                """
        row_pos = self.engine.execute(sql_pos.encode('utf-8')).fetchall()
        
        sql_epay =u"""
                select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
                join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
                join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
                where TYPE_NAME='新增有效丰收e支付得分参数'
                order by h.HEADER_NAME
                """
        row_epay = self.engine.execute(sql_epay.encode('utf-8')).fetchall()
        
        sql_etc =u"""
                select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
                join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
                join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
                where TYPE_NAME='新增ETC得分参数'
                order by h.HEADER_NAME
                """
        row_etc = self.engine.execute(sql_etc.encode('utf-8')).fetchall()
        sql_zn =u"""
                select h.HEADER_NAME,d.DETAIL_VALUE from T_PARA_TYPE t
                join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
                join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
                where TYPE_NAME='助农服务点月活点指标限制参数'
                order by h.HEADER_NAME
                """
        row_zn = self.engine.execute(sql_zn.encode('utf-8')).fetchall()
        sql_tar =u"""
                select * from p_ebank_num
                """
        row_tar = self.engine.execute(sql_tar.encode('utf-8')).fetchall()
        rr=[]
        std,max,min,score={},{},{},{}
        for i in row_sj:
            if i[0]==u'标准分（分）':
                std['sj']=float(i[1])
            elif i[0]==u'最高分（分）':
                max['sj']=float(i[1])
            elif i[0]==u'最低分（分）':
                min['sj']=float(i[1])
        for i in row_wy:
            if i[0]==u'标准分':
                std['wy']=float(i[1])
            elif i[0]==u'最高分':
                max['wy']=float(i[1])
            elif i[0]==u'最低分':
                min['wy']=float(i[1])
        for i in row_pos:
            if i[0]==u'标准分':
                std['pos']=float(i[1])
            elif i[0]==u'最高分':
                max['pos']=float(i[1])
            elif i[0]==u'最低分':
                min['pos']=float(i[1])
        for i in row_epay:
            if i[0]==u'标准分':
                std['epay']=float(i[1])
            elif i[0]== u'最高分':
                max['epay']=float(i[1])
            elif i[0]==u'最低分':
                min['epay']=float(i[1])
        for i in row_etc:
            if i[0]==u'标准分':
                std['etc']=float(i[1])
            elif i[0]==u'最高分':
                max['etc']=float(i[1])
            elif i[0]==u'最低分':
                min['etc']=float(i[1])
        i=-1
        while True:
            i+=1
            if i>=len(row):
                break
            #sj sco
            amt=int(row[i][2])-int(row1[i][2])
            tar=int(row_tar[0][5])
            score['sj']=(amt/tar)*std['sj']
            if score['sj']>max['sj']: 
                score['sj']=max['sj']
            elif score['sj']<min['sj']:
                score['sj']=min['sj']

            #wy sco
            amt=int(row2[i][2])-int(row3[i][2])
            tar=int(row_tar[0][6])
            score['wy']=(amt/tar)*std['wy']
            if score['wy']>max['wy']: 
                score['wy']=max['wy']
            elif score['wy']<min['wy']:
                score['wy']=min['wy']

            #pos sco
            '''
            amt=int(row4[i][2]-row5[i][2])
            tar=int(row_tar[0][7])
            score_etc=(amt/tar)*stdc_etc
            if score_etc>maxc_etc: 
                score_etc=maxc_etc
            elif score_etc<minc_etc:
                score_etc=minc_etc
            '''

            #epay sco 
            amt=int(row4[i][2])-int(row5[i][2])
            tar=int(row_tar[0][9])
            score['epay']=(amt/tar)*std['epay']
            if score['epay']>max['epay']: 
                score['epay']=max['epay']
            elif score['epay']<min['epay']:
                score['epay']=min['epay']

            #etc sco
            amt=int(row2[i][2])-int(row3[i][2])
            tar=int(row_tar[0][8])
            score['etc']=(amt/tar)*std['etc']
            if score['etc']>max['etc']: 
                score['etc']=max['etc']
            elif score['etc']<min['etc']:
                score['etc']=min['etc']

            #zn sco

            c1 = score['sj']
            c2 = score['wy']
            c3 = '0'#score['pos']
            c4 = score['epay']
            c5 = score['etc']
            c6 = '0'#score['zn']
            rr.append((self.ym,row[i][0],row[i][1],row[i][3],row[i][4],c1,c2,c3,c4,c5,c6))
        needtrans ={}
        return self.translate(rr,needtrans)

    def make_eq_filterstr(self):
        filterstr1=filterstr2=filterstr3 = " "
        vlist1,vlist2,vlist3,vlist4,vlist5,vlist6 = [],[],[],[],[],[]
        self.org,self.branch,self.id,self.manage="","","",""
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
                if k == 'S_DATE':
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
                if k == 'BRANCH_CODE':
                    #获取机构号
                    self.org=v
                    self.branch=v
                    filterstr1 = filterstr1 + " and org_code = ? "
                    vlist1.append(v)
                    vlist2.append(v)
                if k == 'SALE_CODE':
                    #获取客户经理号
                    self.id=v
                    self.manage=v
                    filterstr1 = filterstr1 + " and sale_code=? "
                    vlist1.append(v)
                    vlist2.append(v)
        if self.org<>"":
            self.org = " and branch_code="+self.org+" "
            self.branch = " and open_branch_no="+self.branch+" "
        if self.manage<>"":
            self.org = " and user_name="+self.id+" "
            self.branch = " and manage_coed="+self.manage+" "
        return filterstr3,filterstr2,filterstr1,vlist6,vlist5,vlist4,vlist3,vlist2,vlist1

    def column_header(self):
        return ["统计月份","机构号","机构名称","客户经理编号","客户经理名称","新增手机银行得分","新增企业网银得分","POS得分","新增有效丰收e支付得分","新增ETC得分","助农服务点月平均活点率得分"]
    def trans_dec(self,num):
        tmp = Decimal(num)
        tmp = '{:,}'.format(tmp)
        return tmp
    @property
    def page_size(self):
        return 15
