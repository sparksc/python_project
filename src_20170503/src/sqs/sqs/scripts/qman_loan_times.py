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
        self.filterlist = ['FROM_DATE_ID', 'END_DATE_ID', 'org','SALE_CODE']
        self.jiesu=''
        self.kaishi=''
        filterstr,filterstr1, filterstr2, vlist = self.make_eq_filterstr()
        sql ="""
        SELECT %s,%s,f.ORG_CODE,f.ORG_NAME, f.SALE_CODE, f.SALE_NAME,
        nvl(f1.PUB_BAL, 0) / 100.00,                                            --期初对公管贷余额
        nvl(f.PUB_BAL, 0) / 100.00,                                               --期末对公管贷余额
        nvl(f2.AVG_PUB_BAL, 0) / 100.00/ (days(to_date(f.date_id,'yyyymmdd'))-days(to_date(f1.DATE_ID,'yyyymmdd')) +1),     --对公管贷日均
        nvl(f1.PRI_BAL, 0) / 100.00,                                              --期初对私管贷余额           
        nvl(f.PRI_BAL, 0) / 100.00,                                             --期末对私管贷余额                   
        nvl(f2.AVG_PRI_BAL, 0) / 100.00 /(days(to_date(f.date_id,'yyyymmdd'))-days(to_date(f1.DATE_ID,'yyyymmdd')) +1),      --对私管贷日均 
        nvl(f1.pub_num, 0),                                             --期初对公管贷户数                                      
        nvl(f1.PUB_THIS_STANDARD_NUM, 0) ,                                --期初对公管贷户数5000
        nvl(f.pub_num, 0),                                               --期末对公管贷户数
        nvl(f.PUB_THIS_STANDARD_NUM, 0) ,                               --期末对公管贷户数5000
        nvl(f1.pri_num, 0),                                              --期初对私管贷户数         
        nvl(f1.PRI_THIS_STANDARD_NUM, 0),                               --期初对私管贷户数5000                 
        nvl(f.pri_num, 0),                                              --期末对私管贷户数                               
        nvl(f.PRI_THIS_STANDARD_NUM, 0)                                 --期末对私管贷户数5000                      
        FROM YDW.REPORT_MANAGER_LOAN F                                                                                                
        left join (select * from REPORT_MANAGER_LOAN ff where length(ff.SALE_CODE) = 7  %s) f1 on  f1.ORG_CODE = f.ORG_CODE and f1.SALE_CODE = f.SALE_CODE 
        left join (select fff.ORG_CODE, fff.SALE_CODE, sum(PUB_BAL) as AVG_PUB_BAL, sum(PRI_BAL) as AVG_PRI_BAL  from REPORT_MANAGER_LOAN fff where length(fff.SALE_CODE) = 7   %s  group by fff.ORG_CODE, fff.SALE_CODE)
        f2 on  f2.ORG_CODE = f.ORG_CODE and f2.SALE_CODE = f.SALE_CODE    
        WHERE length(f.SALE_CODE) = 7 and (nvl(f1.pub_num, 0) > 0 or nvl(f.pub_num, 0) > 0 or nvl(f1.pri_num, 0) > 0 or nvl(f.pri_num, 0) > 0) %s
        """%(self.kaishi,self.jiesu,filterstr1, filterstr2, filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print "0000000000000000000000000", sql
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i[0:6])
            for j in i[6:]:
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
                elif k == 'FROM_DATE_ID':
                    filterstr1 = filterstr1 +" and ff.date_id = %s "%v
                    filterstr2 = filterstr2 +" and fff.date_id >= %s "%v
                    self.kaishi=int(v)
                elif k == 'END_DATE_ID':
                    filterstr = filterstr +" and f.date_id = %s "%v
                    filterstr2 = filterstr2 +" and fff.date_id <= %s "%v
                    self.jiesu=int(v)
                elif k == 'SALE_CODE':
                    filterstr = filterstr +" and f.SALE_CODE = '%s' "%v
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'f.SALE_CODE','f.ORG_CODE', None))
        return filterstr,filterstr1, filterstr2,vlist

    def column_header(self):
        return ["开始时间","结束时间","机构编号","机构名称", "员工编号","员工姓名","期初对公管贷余额","期末对公管贷余额","对公管贷日均", "期初对私管贷余额", "期末对私管贷余额", "对私管贷日均", "期初对公管贷户数", "期初对公管贷户数(大于5000)", "期末对公管贷户数", "期末对公管贷户数(大于5000)", "期初对私管贷户数", "期初对私管贷户数(大于5000)", "期末对私管贷户数", "期末对私管贷户数(大于5000)"]

    @property
    def page_size(self):
        return 15
