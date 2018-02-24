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
    def group_by(self):
        return [0],(7,8),{0:[1]}

    def prepare_object(self):
        self.filterlist = ['IS_OPEN_NEW_WH','DATE_ID','org','SALE_CODE','count','CORPNAME','CUST_IN_NO','org_flag']
        self.mon_date=''
        self.count=""
        filterstr,vlist = self.make_eq_filterstr()
        sql_ebills="""
        select 
        ORG_CODE,
        ORG_NAME,
        MONTH,           --0
        CUST_IN_NO,
        CORPNAME,
        SALE_CODE,
        SALE_NAME,
        round(sum(nvl(TOTAL_SET,0)/1000000.00),2),         -- 国际结算量7
        round(sum(nvl(TOTAL_CROSS,0)/1000000.00),2),      --结售汇8
        IS_OPEN_NEW_WH
        from 
        ebills_hook_org
        where 1=1 %s 
        group by MONTH,ORG_CODE,ORG_NAME,CUST_IN_NO,CORPNAME,SALE_CODE,SALE_NAME,IS_OPEN_NEW_WH
        order by month,ORG_CODE

        """%(filterstr)
        print sql_ebills
        row_ori = self.engine.execute(sql_ebills.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        rowlist=[]
        for i in row_ori:
            t=list(i[0:7])
            for j in i[7:len(i)-1]:
                if j is None:j=0
                j=self.amount_trans_dec(j)
                t.append(j)
            t.append(i[len(i)-1])
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
                elif k=="IS_OPEN_NEW_WH":
                    if v=="是":
                        filterstr=filterstr+" and IS_OPEN_NEW_WH = '%s' "%(v)
                    elif v=="否":
                        filterstr=filterstr+" and IS_OPEN_NEW_WH != '是' "
                    else:
                        pass
                elif k=="org_flag":
                    filterstr=filterstr+" and org_flag = '%s' "%(v)
                else: 
                    pass
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],"SALE_CODE",'ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return [
        [{"name": u"机构编号",'h':2},{"name": u"机构名称",'h':2}, {"name": u"统计月份",'h':2},{"name": u"客户内码",'h':2},{"name": u"客户名称",'h':2},{"name":u"员工号",'h':2},{"name":u"员工姓名",'h':2},{"name":u"结算量合计",'h':2},{"name":u"结售汇量合计",'h':2},{"name":u"是否新开有效外汇账户",'h':2}
        ]]

    @property
    def page_size(self):
        return 15
