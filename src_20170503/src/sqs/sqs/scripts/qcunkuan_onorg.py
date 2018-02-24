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
国际业务机构
"""
class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['IS_OPEN_NEW_WH','DATE_ID','org','SALE_CODE','count','CORPNAME','CUST_IN_NO']
        self.mon_date=''
        self.count=""
        filterstr,vlist,month = self.make_eq_filterstr()
        sql_ebills="""
        select 
        MONTH,           --0
        ORG_CODE,           --1
        ORG_NAME,     --2
        round(sum(nvl(BALANCE,0)/1000000.00),2) BALANCE, ---外币存款折人民币余额30 
        round(sum(nvl(MONTHAMT,0)/1000000.00),2) monthamt,--外币存款折人民币月日均28
        round(sum(nvl(DAYAMT,0)/1000000.00),2) DAYAMT --外币存款折人民币年日均29
        from 
        EBILLS_HOOK_CUNKUAN
        where 1=1 %s 
        group by ORG_CODE,ORG_NAME,month
        order by month,ORG_CODE
        """%(filterstr)
        print sql_ebills
        row_ori = self.engine.execute(sql_ebills.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row_ori:
            t=list(i[0:3])
            for j in i[3:len(i)]:
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
                    month=int(str(v)[:6])
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
                elif k=="IS_OPEN_NEW_WH":
                    if v=="是":
                        filterstr=filterstr+" and IS_OPEN_NEW_WH = '%s' "%(v)
                    elif v=="否":
                        filterstr=filterstr+" and IS_OPEN_NEW_WH != '是' "
                    else:
                        pass
                else: 
                    pass
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],"SALE_CODE",'ORG_CODE', None))
        return filterstr,vlist,month

    def column_header(self):
        return [
        [{"name": u"统计月份",'h':2},{"name": u"机构编号",'h':2},{"name": u"机构名称",'h':2},{"name":u"外币存款余额--国业部分摊(万元)",'h':2},{"name":u"外币存款月日均--国业部分摊(万元)",'h':2},{"name":u"外币存款年日均--国业部分摊(万元)",'h':2}
        ]]

    @property
    def page_size(self):
        return 15
