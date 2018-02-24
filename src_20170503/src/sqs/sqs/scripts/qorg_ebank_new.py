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
机构电子银行指标
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org']
        self.date_id=''
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
        select b.date_id,b.org_code,b.org_name,
        (nvl(b.mb_this_num,0)-nvl(a.mb_this_num,0)),
        (nvl(b.cb_this_num,0)-nvl(a.cb_this_num,0)),
        (nvl(b.pb_this_num,0))-nvl(a.pb_this_num,0),
        (nvl(b.ADD_HIGH_POS_NUM,0)-nvl(a.ADD_HIGH_POS_NUM,0)),
        (nvl(b.ADD_LOW_POS_NUM,0)-nvl(a.ADD_LOW_POS_NUM,0)),
        (nvl(b.epay_this_num,0)-nvl(a.epay_this_num,0)),
        (nvl(b.last_third_depo_num,0)),
        (nvl(b.third_depo_add_num,0)-nvl(a.third_depo_add_num,0)),
        (nvl(b.this_add_etc_num,0)-nvl(a.this_add_etc_num,0)),
        nvl(b.FARM_SERV_HIGH_NUM,0),
        nvl(b.FARM_SERVICE_LOW_NUM,0)
        from
        (select date_id, ORG_CODE,org_name,
        sum(nvl(mb_this_num,0)) as mb_this_num ,
        sum(nvl(cb_this_num,0)) as cb_this_num,
        sum(nvl(PB_THIS_NUM,0)) as pb_this_num,
        sum(nvl(ADD_HIGH_POS_NUM,0))as ADD_HIGH_POS_NUM,
        sum(nvl(ADD_LOW_POS_NUM,0))as ADD_LOW_POS_NUM,
        sum(nvl(epay_this_num,0))as epay_this_num,
        sum(nvl(LAST_THIRD_DEPO_NUM,0)) as last_third_depo_num,
        sum(nvl(THIRD_DEPO_ADD_NUM,0)) as third_depo_add_num, 
        sum(nvl(ETC_THIS_NUM,0))as this_add_etc_num ,
        sum(nvl(FARM_SERV_HIGH_NUM,0))as FARM_SERV_HIGH_NUM,
        sum(nvl(FARM_SERVICE_LOW_NUM,0)) as FARM_SERVICE_LOW_NUM 
        from REPORT_MANAGER_OTHER where 1=1 %s
        group by date_id,org_code ,org_name)b
        left join 
        (select date_id, ORG_CODE,org_name,
        sum(nvl(mb_this_num,0)) as mb_this_num ,
        sum(nvl(cb_this_num,0)) as cb_this_num,
        sum(nvl(PB_THIS_NUM,0)) as pb_this_num,
        sum(nvl(ADD_HIGH_POS_NUM,0))as ADD_HIGH_POS_NUM,
        sum(nvl(ADD_LOW_POS_NUM,0))as ADD_LOW_POS_NUM,
        sum(nvl(epay_this_num,0))as epay_this_num,
        sum(nvl(THIRD_DEPO_ADD_NUM,0)) as third_depo_add_num,
        sum(nvl(ETC_THIS_NUM,0))as this_add_etc_num
        from REPORT_MANAGER_OTHER where date_id =(select L_monthend_ID from d_date where %s)
        group by date_id,org_code,org_name)a
        on b.org_code=a.org_code and a.org_name=b.org_name order by org_code 

            """%(filterstr,self.date_id)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print sql
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i[0:3])
            for j in i[3:]:
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
            #if k == 'login_branch_no':
            #    bb = self.deal_branch_query_auth(v)
            #    if bb != False :
            #        filterstr = filterstr+" and ORG_CODE in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                elif k=='DATE_ID':
                    filterstr = filterstr +" and DATE_ID=  %s  "%(v)
                    self.date_id="ID=%s"%(v)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return ["统计日期","机构编号","机构名称","新增手机银行有效户数","新增企业网银有效户数","新增个人网银有效户数","新增POS机(高扣率)","新增POS机(抵扣率)","新增有效丰收e支付","第三方存量户数","第三方增量户数","新增ETC户数","助农服务点(达到活点率)","助农服务点(未达到活点率)"]

    @property
    def page_size(self):
        return 15
