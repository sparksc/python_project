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
        self.kaishi=''
        self.jiesu=''
        filterstr,filterstr1, filterstr2, vlist = self.make_eq_filterstr()
        sql ="""
        SELECT %s,%s,f.ORG_CODE,f.ORG_NAME, f.SALE_CODE, f.SALE_NAME, 
        nvl(f1.PUB_BAL, 0.0) / 100.00,                    --期初对公存款余额
        nvl(f.PUB_BAL, 0.0)/ 100.00 ,                    --期末对公存款余额
        f2.AVG_PUB_BAL / 100.00/ (days(to_date(%s,'yyyymmdd'))-days(to_date(%s,'yyyymmdd')) +1),      --对公存款日均
        nvl(f1.PRI_BAL, 0.0) / 100.00,                    --期初对私存款余额
        nvl(f.PRI_BAL, 0.0) / 100.00,                     --期末对私存款余额
        f2.AVG_PRI_BAL / 100.00 / (days(to_date(%s,'yyyymmdd'))-days(to_date(%s,'yyyymmdd')) +1),       --对私存款日均
        nvl(f1.FIN_BAL, 0.0) / 100.00,                    --期初理财余额
        nvl(f.FIN_BAL, 0.0) / 100.00,                     --期末理财余额
        f2.AVG_FIN_BAL / 100.00 / (days(to_date(%s,'yyyymmdd'))-days(to_date(%s,'yyyymmdd')) +1),       --理财日均
        nvl(f1.PUB_BAL, 0.0) / 100.00 + nvl(f1.PRI_BAL, 0.0) / 100.00 + nvl(f1.FIN_BAL, 0.0) / 100.00, --期初余额合计值 
        nvl(f.PUB_BAL, 0.0)/ 100.00 + nvl(f.PRI_BAL, 0.0) / 100.00 + nvl(f.FIN_BAL, 0.0) / 100.00,  --期初余额合计值
        f2.AVG_PUB_BAL / 100.00/ (days(to_date(%s,'yyyymmdd'))-days(to_date(%s,'yyyymmdd')) +1) + f2.AVG_PRI_BAL / 100.00 / (days(to_date(%s,'yyyymmdd'))-days(to_date(%s,'yyyymmdd')) +1) + f2.AVG_FIN_BAL / 100.00 / (days(to_date(%s,'yyyymmdd'))-days(to_date(%s,'yyyymmdd')) +1) --日均合计值


        FROM YDW.REPORT_MANAGER_DEP F
        JOIN V_STAFF_INFO V ON f.SALE_CODE=V.USER_NAME   ----增加非本机构客户经理过滤条件
        JOIN D_ORG DG ON DG.ORG0_CODE=V.ORG AND LEFT(DG.ORG1_CODE,5)=LEFT(f.ORG_CODE,5)  ----增加非本机构客户经理过滤条件
        left join (select * from REPORT_MANAGER_DEP ff where length(ff.SALE_CODE) = 7  %s ) f1 on  f1.ORG_CODE = f.ORG_CODE and f1.SALE_CODE = f.SALE_CODE
        left join (select fff.ORG_CODE, fff.SALE_CODE, sum(PUB_BAL) as AVG_PUB_BAL, sum(PRI_BAL) as AVG_PRI_BAL, sum(FIN_BAL) as AVG_FIN_BAL from REPORT_MANAGER_DEP fff where length(fff.SALE_CODE) = 7  %s  group by fff.ORG_CODE, fff.SALE_CODE)
        f2 on  f2.ORG_CODE = f.ORG_CODE and f2.SALE_CODE = f.SALE_CODE
        WHERE length(f.SALE_CODE) = 7  %s
        """%(self.kaishi,self.jiesu,self.jiesu,self.kaishi,self.jiesu,self.kaishi,self.jiesu,self.kaishi,self.jiesu,self.kaishi,self.jiesu,self.kaishi,self.jiesu,self.kaishi,filterstr1, filterstr2, filterstr)
        print sql
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
        return ["开始时间","结束时间","机构编号","机构名称", "员工编号","员工姓名","期初对公存款余额","期末对公存款余额","对公存款日均", "期初对私存款余额", "期末对私存款余额", "对私存款日均", "期初理财余额", "期末理财余额", "理财日均","期初余额合计值", "期末余额合计值", "日均合计值"]

    @property
    def page_size(self):
        return 15
