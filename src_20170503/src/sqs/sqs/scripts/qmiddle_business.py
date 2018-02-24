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
中间业务考核
"""
"""
"""
class Query(ObjectQuery):
    def exp_str(self):
        return {"start_row":5,"start_col":1,"cols":20}
    def prepare_object(self):
        self.filterlist = ['DATE_ID','END_DATE_ID', 'org']
        self.date_id="" #月末 20161130
        filterstr,vlist = self.make_eq_filterstr()
        sql = """
        select
        month1,
        ORG_CODE,
        branch_name,
        shuiffei,
        caishui,
        dingqi,
        yancao,
        duanxin,
        dianfei,
        ranqi,
        etc,
        jiaxiao,
        shouji,
        qiye,
        geyin,
        qiye+geyin,
        katong,
        kuaijie,
        katong+kuaijie,
        weixin
        from
        (
         select
         left(sign_date,6) month1,
         ORG_CODE,
         sum(case when mid_type in ('水费') and STATE='1'  and rn=1 and action in ('A','I')  then 1 else 0 end) shuiffei,
         sum(case when mid_type in ('财库税银') and STATE='1'  and rn=1 and action in ('A','I')  then 1 else 0 end) caishui,
         sum(case when mid_type in ('定期借记') and STATE='0'  and rn=1 and action in ('A','I')  and (MID_KEY1 like '%%-0001-ding' or MID_KEY1 like '%%-0002-ding') then 1 else 0 end) dingqi,
         sum(case when mid_type in ('烟草') and STATE='1'  and rn=1 and action in ('A','I')     then 1 else 0 end) yancao,
         sum(case when mid_type in ('短信') and STATE='1'  and rn=1  and action in ('A','I')    then 1 else 0 end) duanxin,
         sum(case when mid_type in ('电费') and STATE='1'  and rn=1  and action in ('A','I')    then 1 else 0 end) dianfei,
         sum(case when mid_type in ('燃气') and STATE='1'  and rn=1 and action in ('A','I')      then 1 else 0 end) ranqi,
         sum(case when mid_type in ('ETC') and STATE='1'  and rn=1 and action in ('A','I')      then 1 else 0 end)  etc,
         sum(case when mid_type in ('驾校') and STATE='1'and action in ('A','I')   then 1 else 0 end) jiaxiao,

         sum(case when mid_type in ('手机银行') and STATE='1' and action in ('A','I')  then 1 else 0 end) shouji,
         sum(case when mid_type in ('企业网上银行') and STATE='1' and action in ('A','I')  then 1 else 0 end) qiye,
         sum(case when mid_type in ('个人网上银行') and STATE='1' and action in ('A','I')   then 1 else 0 end) geyin,
         sum(case when mid_type in ('支付宝卡通') and STATE='1'  and action in ('A','I')  then 1 else 0 end) katong,
         sum(case when mid_type in ('支付宝快捷支付') and STATE='1' and action in ('A','I')  then 1 else 0 end) kuaijie,
         sum(case when mid_type in ('微信银行') and STATE='0'and action in ('A','I')   and rn=1 then 1 else 0 end) weixin
         from 
        (select
         row_number() over(partition by MID_KEY1,MID_KEY2 order by date_id desc ,SIGN_DATE desc ,ACTION desc,state desc) rn ,f.*
         from MID_BUSINESS f where left(sign_date,6)=%s and left(date_id,6)=%s %s
        ) 
        group by ORG_CODE,left(sign_date,6)
        ) a
        left join branch b
        on a.org_code=b.branch_code
        """%(str(self.date_id)[:6],str(self.date_id)[:6],filterstr)
        row = self.engine.execute(sql,vlist).fetchall()

        needtrans ={}
        rowlist=[]
        for i in row:
           t=list(i) 
           for j in range(3,len(t)-3): 
                t[j] =t[j] or 0
                t[j]=self.amount_trans_dec(t[j])
           rowlist.append(t)    
        return self.translate(rowlist,needtrans)


    def make_eq_filterstr(self):
        filterstr = ""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                elif k == 'DATE_ID':
                    self.date_id= v
                else: 
                    pass
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'ORG_CODE', None))
        return filterstr, vlist

    def column_header(self):
        return[
        [{"name":"统计月份",'h':2},{"name":"机构号",'h':2},{"name":"",'h':2},{"name":"水费",'h':2},{"name":"财库税银",'h':2},{"name":"定期借记",'h':2},{"name":"烟草",'h':2},{"name":"短信",'h':2},{"name":"电费",'h':2},{"name":"燃气",'h':2},{"name":"ETC",'h':2},{"name":"驾校",'h':2},{"name":"手机银行",'h':2},{"name":"网上银行",'w':3},{"name":"支付宝",'w':3},{"name":"微信银行",'h':2}],
        [{"name":"企业网上银行",'h':1},{"name":"个人网上银行",'h':1},{"name":"合计",'h':1},{"name":"支付宝卡通",'h':1},{"name":"支付宝快捷支付",'h':1},{"name":"合计",'h':1}]
        ]

    @property
    def page_size(self):
        return 15
