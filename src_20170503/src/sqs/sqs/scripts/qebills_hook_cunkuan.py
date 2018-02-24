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
国际业务归属
"""
class Query(ObjectQuery):
    
    def group_by(self):
            return [0],(5,6,7),{0:[1]}
    def cancal_merge(self):
        return True
    
    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE','count','CORPNAME','CUST_IN_NO']
        self.mon_date=''
        self.count=""
        filterstr,vlist = self.make_eq_filterstr()
        sql_ebills="""

        select * from 
        (
        select 
        ORG_CODE,           
        ORG_NAME,     
        MONTH,           --0
        CUST_IN_NO,
        CORPNAME,
        round(sum(nvl(BALANCE,0)/1000000.00),2) BALANCE, ---外币存款折人民币余额30 
        round(sum(nvl(MONTHAMT,0)/1000000.00),2) monthamt,--外币存款折人民币月日均28
        round(sum(nvl(DAYAMT,0)/1000000.00),2) DAYAMT --外币存款折人民币年日均29
        from 
        ebills_hook
        where 1=1 %s 
        group by ORG_CODE,ORG_NAME,month,CUST_IN_NO,CORPNAME)
        where monthamt!=0 or DAYAMT !=0 or BALANCE!=0
        order by month,ORG_CODE 

        """%(filterstr)
        print sql_ebills
        row_ori = self.engine.execute(sql_ebills.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row_ori:
            t=list(i[0:5])
            for j in i[5:len(i)]:
                if j is None:j=0
                j=self.amount_trans_dec(j)
                t.append(j)
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            print k,v
            if v and k in self.filterlist:
                if k == 'DATE_ID':
                    filterstr = filterstr +" and  MONTH = %s "%(int(str(v)[:6]))
                elif k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                elif k == 'SALE_CODE':
                    filterstr = filterstr +" and SALE_CODE = '%s' "%v
                elif k=='count':
                    self.count='%s'%v
                elif k=='CORPNAME':
                    filterstr= filterstr +" and CORPNAME like '%%%s%%' "%v
                elif k=='CUST_IN_NO':
                    filterstr=filterstr+" and CUST_IN_NO = '%s' "%v
                else: 
                    pass
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],"SALE_CODE",'ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return [
        [{"name": u"机构编号",'h':2},{"name": u"机构名称",'h':2},{"name": u"统计月份",'h':2},{"name": u"客户内码",'h':2},{"name": u"客户名称",'h':2},{"name":u"外币存款折人民币(万元)",'w':3}],
        [{"name":u"余额",'h':1},{"name":u"月日均",'h':1},{"name":u"年日均",'h':1}]
        ]


    @property
    def page_size(self):
        return 15
