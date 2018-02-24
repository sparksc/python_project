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
客户经理存款
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID', 'org','SALE_CODE']
        filterstr,filterstr1, filterstr2, vlist = self.make_eq_filterstr()
        sql ="""
        SELECT F.date_id,f.ORG_CODE,f.ORG_NAME, f.SALE_CODE, f.SALE_NAME, 
        nvl(f1.pri_add_num, 0),                                           --对私增户扩面户数 第1天
        nvl(f2.pri_add_num, 0),                                           --对私增户扩面户数 第2天
        nvl(f.pri_add_num, 0),                                            --对私增户扩面户数 第3天
        round(( nvl(f1.pri_add_num, 0) +  nvl(f2.pri_add_num, 0) +  nvl(f.pri_add_num, 0)) / 3, 0),   --对私平均
        nvl(f1.pub_add_num, 0),                                           --对公增户扩面户数 第1天
        nvl(f2.pub_add_num, 0),                                           --对公增户扩面户数 第2天
        nvl(f.pub_add_num, 0),                                            --对公增户扩面户数 第3天
        round(( nvl(f1.pub_add_num, 0) +  nvl(f2.pub_add_num, 0) + nvl(f.pub_add_num, 0)) / 3, 0)   --对公平均
        FROM YDW.REPORT_MANAGER_LOAN F                                                
        left join (select * from REPORT_MANAGER_LOAN ff where length(ff.SALE_CODE) = 7  %s) f1 on  f1.ORG_CODE = f.ORG_CODE and f1.SALE_CODE = f.SALE_CODE
        left join (select * from REPORT_MANAGER_LOAN fff where length(fff.SALE_CODE) = 7  %s) f2 on  f2.ORG_CODE = f.ORG_CODE and f2.SALE_CODE = f.SALE_CODE    
        WHERE length(f.SALE_CODE) = 7 and 
        (round(( nvl(f1.pri_add_num, 0) +  nvl(f2.pri_add_num, 0) +  nvl(f.pri_add_num, 0)) / 3.0, 0) > 0 or round(( nvl(f1.pub_add_num, 0) +  nvl(f2.pub_add_num, 0) + nvl(f.pub_add_num, 0)) / 3.0, 0) > 0) %s
        """%(filterstr1, filterstr2, filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print "0000000000000000000000000", sql
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i[0:5])
            for j in i[5:]:
                if j is None:j=0
                j=self.amount_trans_dec(j)
                t.append(j)
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)    

    def make_eq_filterstr(self):
        filterstr1 =""
        filterstr2 =""
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and f.ORG_CODE in ( %s ) "%(vvv)
                elif k == 'DATE_ID':
                    print v
                    day_sql="""
                        select d.DETAIL_VALUE from T_PARA_TYPE t
                        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
                        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
                        where t.TYPE_NAME='管贷旬均天数选择' and h.HEADER_NAME in ('管贷旬均指标参数1(日)','管贷旬均指标参数2(日)','管贷旬均指标参数3(日)') order by int(d.DETAIL_VALUE)
                        """
                    day_row = self.engine.execute(day_sql).fetchall()
                    if len(day_row)==3:
                        day_row1=str(day_row[0][0]).zfill(2)
                        day_row2=str(day_row[1][0]).zfill(2)
                        day_row3=str(day_row[2][0]).zfill(2)
                    else:
                        raise Exception(u"旬均天数不对,请检查")
                    yearmonth = v[0:6]
                    day1 = yearmonth + day_row1 
                    day2 = yearmonth + day_row2
                    day3 = yearmonth + day_row3
                    print day1, day2, day3
                    filterstr1 = filterstr2 +" and ff.date_id = %s "%day1
                    filterstr2 = filterstr2 +" and fff.date_id = %s "%day2
                    filterstr = filterstr +" and f.date_id = %s "%day3
                elif k == 'SALE_CODE':
                    filterstr = filterstr +" and f.SALE_CODE = '%s' "%v
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'f.SALE_CODE','f.ORG_CODE', None))
        return filterstr,filterstr1, filterstr2,vlist

    def column_header(self):
        return ["日期","机构编号","机构名称", "员工编号","员工姓名", "对私增户扩面户数1", "对私增户扩面户数2", "对私增户扩面户数3", "对私增户扩面户数旬均", "对公增户扩面户数1", "对公增户扩面户数2", "对公增户扩面户数3", "对公增户扩面户数旬均"]

    @property
    def page_size(self):
        return 15
