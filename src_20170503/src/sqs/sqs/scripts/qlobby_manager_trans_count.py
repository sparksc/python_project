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
大堂经理考核
"""
"""
"""
class Query(ObjectQuery):
    def exp_str(self):
        return {"start_row":5,"start_col":1,"cols":17}
    def prepare_object(self):
        self.filterlist = ['DATE_ID','END_DATE_ID', 'org']
        self.date_id="" #月末 20161130
        filterstr,vlist = self.make_eq_filterstr()
        self.lastyear=str(int(self.date_id[:4])-1)+str(self.date_id[4:])#上年
        self.date_id=int(self.date_id)
        sql_lastdate="""select MONTHBEG_ID,MONTHEND_ID from d_date where id=%d """%(int(self.lastyear))
        month_beg=self.engine.execute(sql_lastdate).fetchone()
        self.lastend=int(month_beg[1])#上年月末
        print 'lf.lastend',self.lastend
        print 'self.date_id',self.date_id
        sql = """
        select
            nvl(month1,ym),
            nvl(BRANCH_CODE,TRAN_BRANCH_CODE),
            BRANCH_NAME,
            ---person_num,--考核人数还是空的
            nvl(ATMBH,0),
            nvl(ATMTDB,0),
            nvl(EBANK_TOTAL,0),
            nvl(CELLPHONE_BANK,0),
            nvl(AUTO_BANK,0),
            nvl(lobby_total,0),
            nvl(mid_cnt,0),--中间业务
            nvl(elec_cnt,0),--电子银行
            nvl(mid_total,0),--mid_total
            nvl(MIN_LIMIT_CNT_this,0),
            nvl(TOTAL_LIMIT_CNT_this,0),
            nvl(rate_this,0),
            nvl(rate_last,0),
            nvl(level1,'无')
        from
        (
         select 
         a.month1,
         nvl(a.BRANCH_CODE,b.ORG_CODE) BRANCH_CODE,
         a.BRANCH_NAME,
         ATMBH,
         ATMTDB,
         EBANK_TOTAL,
         CELLPHONE_BANK,
         AUTO_BANK,
         lobby_total,---电子渠道交易笔数总和
         mid_cnt,---中间业务
         elec_cnt, --电子银行
         (mid_cnt+elec_cnt) as mid_total 
         from
         (select 
          left(date,6) month1,
          a.BRANCH_CODE,
          b.BRANCH_NAME,
          --0 as person_num,
          sum(nvl(ATMBH,0)) ATMBH,
          sum(nvl(ATMTDB,0)) ATMTDB,
          sum(nvl(EBANK_TOTAL,0)) EBANK_TOTAL, --网银
          sum(nvl(CELLPHONE_BANK,0)) CELLPHONE_BANK, --手机银行
          sum(nvl(AUTO_BANK,0)) AUTO_BANK,  --自助终端
          sum(nvl(ATMBH,0))+
          sum(nvl(ATMTDB,0)) +
          sum(nvl(EBANK_TOTAL,0))+ 
          sum(nvl(CELLPHONE_BANK,0)) + 
          sum(nvl(AUTO_BANK,0)) lobby_total
          from
          ebank_replace_num a
          left join 
          (select b.*,row_number()over(partition by branch_code order by role_id) rn from BRANCH b) b
          on a.BRANCH_CODE =b.BRANCH_CODE 
          where left(date,6)=%s and b.rn=1 ---本月
        group by
        left(date,6),
        a.BRANCH_CODE,b.BRANCH_NAME) a
        full join
        (
            select
            month1,
            ORG_CODE,
            
            shuiffei+caishui+dingqi+yancao+duanxin+
            dianfei+ranqi+etc+jiaxiao+katong+kuaijie
             mid_cnt,
            
             shouji+qiye+geyin+weixin elec_cnt
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
              from MID_BUSINESS f where left(sign_date,6)=%s and left(date_id,6)=%s
             ) ---本月
group by ORG_CODE,left(sign_date,6)

             )
        ) b
          on a.month1=b.month1 and a.BRANCH_CODE=b.ORG_CODE
        ) a
        full join
            (
            select 
                b.ym,
                nvl(b.TRAN_BRANCH_CODE,c.TRAN_BRANCH_CODE) TRAN_BRANCH_CODE ,
                nvl(MIN_LIMIT_CNT_this,0) MIN_LIMIT_CNT_this,
                nvl(TOTAL_LIMIT_CNT_this,0) TOTAL_LIMIT_CNT_this,
                nvl(rate_this,0) rate_this,
                nvl(rate_last,0) rate_last,
                (case when nvl(rate_this,0)>nvl(rate_last,0) then '上升' when nvl(rate_this,0)<nvl(rate_last,0) then '下降' else '持平' end) level1
             from 
                (select  
                 ym,
                 TRAN_BRANCH_CODE,
                 sum(nvl(MIN_LIMIT_CNT,0)) MIN_LIMIT_CNT_this,---小额业务现金
                 sum(nvl(TOTAL_LIMIT_CNT,0)) TOTAL_LIMIT_CNT_this, ---柜面存取款
                 round(sum(nvl(MIN_LIMIT_CNT,0))*1.000 / ( sum(nvl(TOTAL_LIMIT_CNT,0))),2) rate_this
                  from M_CASH_TRAN_AMOUNT
                  where ym=%s and TOTAL_LIMIT_CNT<>0 --本月
                  group by YM,TRAN_BRANCH_CODE
                ) b 
                full join
                (
                    select  
                    TRAN_BRANCH_CODE,
                    round(sum(nvl(MIN_LIMIT_CNT,0))*1.000 / ( sum(nvl(TOTAL_LIMIT_CNT,0))),2) rate_last
                    from M_CASH_TRAN_AMOUNT
                    where ym=%s and TOTAL_LIMIT_CNT<>0  ---去年月份
                    group by YM,TRAN_BRANCH_CODE
                 ) c
                    on b.TRAN_BRANCH_CODE=c.TRAN_BRANCH_CODE
              ) b
        on b.ym=a.month1 and b.TRAN_BRANCH_CODE=a.BRANCH_CODE
        where 1=1 %s

        """%(str(self.date_id)[:6],str(self.date_id)[:6],str(self.date_id)[:6],str(self.date_id)[:6],str(self.lastend)[:6],filterstr)
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
                    filterstr = filterstr +" and BRANCH_CODE in ( %s ) "%(vvv)
                elif k == 'DATE_ID':
                    self.date_id= v
                else: 
                    pass
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'BRANCH_CODE', None))
        return filterstr, vlist

    def column_header(self):
        #return ["统计月份", "机构编号","机构名称","ATM本行交易笔数", "ATM他代本交易笔数","网上银行交易笔数", "手机银行交易笔数", "自助终端交易笔数","电子渠道交易笔数", "中间业务户数","电子银行户数","中间业务丶电子银行合计","柜面可分离业务笔数", "柜面存取款交易笔数","柜面小额可分离占比","基期柜面小额可分离业务占比","柜面可分离占比变化情况"]
        return[
        [{"name":"统计月份",'h':2},{"name":"机构号",'h':2},{"name":"机构名称",'h':2},{"name":"电子渠道交易笔数",'w':6},{"name":"中间业务丶电子银行户数",'w':3},{"name":"1万元以下现金占比",'w':5}],
        [{"name": u"ATM本行交易笔数",'h':1},{"name": u"ATM他代本交易笔数",'h':1},{"name": u"网上银行交易笔数",'h':1},{"name": u"手机银行交易笔数",'h':1},{"name": u"自助终端交易笔数",'h':1},{"name": u"合计",'h':1},{"name": u"中间业务户数",'h':1},{"name": u"电子银行户数",'h':1},{"name": u"合计",'h':1},{"name": u"柜面可分离业务笔数",'h':1},{"name": u"柜面存取款交易笔数",'h':1},{"name": u"柜面小额可分离占比",'h':1},{"name": u"基期柜面小额可分离业务占比",'h':1},{"name": u"柜面可分离占比变化情况",'h':1}]
        ]

    @property
    def page_size(self):
        return 15
