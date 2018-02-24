# -*- coding:utf-8 -*-

import datetime
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery

"""
客户经理第三方佣金
"""

class Query(ObjectQuery):
 
    def prepare_object(self):
        self.filterlist = ['S_DATE','BRANCH_CODE','SALE_CODE']
        filterstr2,filterstr1,vlist2,vlist1,ym = self.make_eq_filterstr()
        sql =u"""
                select user_name,name,nvl(amt,0),branch_code,branch_name from
                (select manage_code,count(1) amt from d_cust_contract
                where busi_type='第三方存管' and manage_code<>'无' %s
                group by manage_code) a
                right join teller d on d.user_name=a.manage_code
                where 1=1 %s
                order by branch_code,user_name
                """%(filterstr1,filterstr2)
        row = self.engine.execute(sql.encode('utf-8'),vlist1).fetchall()
        row1 = self.engine.execute(sql.encode('utf-8'),vlist2).fetchall()
        
        sql1 =u"""
                select user_name,name,nvl(amt,0),branch_code,branch_name from
                (select manage_code,count(1) amt from d_cust_contract
                where busi_type='ETC' and manage_code<>'无' %s
                group by manage_code) a
                right join teller d on d.user_name=a.manage_code
                where 1=1 %s
                order by branch_code,user_name
                """%(filterstr1,filterstr2)
        row2 = self.engine.execute(sql1.encode('utf-8'),vlist1).fetchall()
        row3 = self.engine.execute(sql1.encode('utf-8'),vlist2).fetchall()
        print sql1
        sql0 =u"""
                select d.detail_value from t_para_type t
                join t_para_header h on h.para_type_id = t.id
                join t_para_detail d on d.para_header_id = h.id
                where type_name='股票第三方存管计价参数' and h.header_name = '单价（元/户）'
               """
        row0 = self.engine.execute(sql0.encode('utf-8')).fetchall()
        
        sqla =u"""
                select d.detail_value from t_para_type t
                join t_para_header h on h.para_type_id = t.id
                join t_para_detail d on d.para_header_id = h.id
                where type_name='新增ETC计价参数' and h.header_name = '单价（元/户）'
               """
        rowa = self.engine.execute(sqla.encode('utf-8')).fetchall()
        i=0
        rr=[]
        while True:
            inc = int(row[i][2]) - int(row1[i][2])
            inc1 = int(row2[i][2])-int(row3[i][2])
            com = inc*int(row0[0][0])
            com1 = inc1*int(rowa[0][0])
            rr.append((ym,row[i][3],row[i][4],row[i][0],row[i][1],com,com1,com+com1))
            i+=1
            if i>=len(row):
               break
        needtrans ={}
        return self.translate(rr,needtrans)
    #参数处理方法
    def make_eq_filterstr(self):
        filterstr1 = " "
        filterstr2 = " "
        vlist1 = []
        vlist2 = []
        ym = ""
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'S_DATE':#获得当前日期date和上月末日期date_l
                    yy = int(v[0:4])
                    ym = v[0:6]
                    dd = int(v[6:8])
                    date = datetime.datetime.strptime(v,'%Y%m%d')
                    date_l = date - datetime.timedelta(days=dd)
                    filterstr1 = filterstr1 + " and open_date <= ? "
                    vlist1.append(int(v))
                    vlist2.append(int(date_l.strftime('%Y%m%d')))
                if k == 'BRANCH_CODE':#机构号
                    filterstr2 =filterstr2 + " and branch_code = ? "
                    vlist1.append(v)
                    vlist2.append(v)
                if k == 'SALE_CODE':#柜员号
                    filterstr2 = filterstr2 + " and user_name = ? "
                    vlist1.append(v)
                    vlist2.append(v)
        return filterstr2,filterstr1,vlist2,vlist1,ym
    def column_header(self):
        return ["统计月份","机构编号","机构名称","客户经理编号","客户经理名称","股票第三方存管效酬","新增ETC效酬","客户经理中间业务总效酬"]
    @property
    def page_size(self):
        return 15
