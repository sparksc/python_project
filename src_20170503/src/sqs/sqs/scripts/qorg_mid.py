# -*- coding:utf-8 -*-

import datetime
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery

"""
机构第三方
"""

class Query(ObjectQuery):
 
    def prepare_object(self):
        self.filterlist = ['date','org']
        filterstr2,filterstr1,vlist2,vlist1,ym = self.make_eq_filterstr()
        print filterstr2,filterstr1,vlist2,vlist1,ym
        sql =u"""
                select org0_code,org0_name,nvl(amt,0) from 
                (select open_branch_no,count(1) amt
                from d_cust_contract c 
                where c.busi_type = '第三方存管' %s
                group by open_branch_no) a
                right join d_org d on d.org0_code = a.open_branch_no 
                where org0_code<>'无' %s
                order by org0_code
                """%(filterstr1,filterstr2)
        row = self.engine.execute(sql.encode('utf-8'),vlist1).fetchall()
        row1 = self.engine.execute(sql.encode('utf-8'),vlist2).fetchall()
        
        i=0
        rr=[]
        while True:
            inc = int(row[i][2]) - int(row1[i][2])
            rr.append((ym,row[i][0],row[i][1],row[i][2],row1[i][2],inc))
            i+=1
            if i>=len(row):
               break
        needtrans ={}
        return self.translate(rr,needtrans)
    def make_eq_filterstr(self):
        filterstr1 = " "
        filterstr2 = " "
        vlist1 = []
        vlist2 = []
        ym=""
        date_on=""
        yy=""
        
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'date':#获得当前日期date和上月末日期date_l
                    yy = int(v[0:4])
                    ym = int(v[0:6])
                    dd = int(v[6:8])
                    date = datetime.datetime.strptime(v,'%Y%m%d')
                    date_l = date - datetime.timedelta(days=dd)
                    filterstr1 = filterstr1 + " and open_date <= ? "
                    vlist1.append(int(v))
                    vlist2.append(int(date_l.strftime('%Y%m%d')))
                if k == 'org':#机构号
                    filterstr2 = filterstr2 + " and org0_code = ? "
                    vlist1.append(int(v))
                    vlist2.append(int(v))
        print date_on
        return filterstr2,filterstr1,vlist2,vlist1,ym
    def column_header(self):
        return ["统计月份","机构号","机构名称","股票第三方存管当前户数","股票第三方存管存量户数","股票第三方当月新增户数"]
    @property
    def page_size(self):
        return 15
