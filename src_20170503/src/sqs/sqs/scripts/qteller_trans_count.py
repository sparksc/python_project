# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
柜员业务量考核
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['FROM_DATE_ID','END_DATE_ID', 'org']
        self.date_id="" #月末
        filterstr,vlist = self.make_eq_filterstr()
        sql_date='select MONTHEND_ID from d_date where id=%s'%(self.date_id)
        row_date = self.engine.execute(sql_date.encode('utf-8'),vlist).fetchone()
        if int(self.date_id) != int(row_date[0]):
            return (u"未到月末,不能查看")
        sql_begdate="select MONTHBEG_ID,L_YEAREND_ID from D_DATE where id=%s"%(self.date_id)
        month_beg = self.engine.execute(sql_begdate.encode('utf-8'),vlist).fetchone()
        self.month_beg=month_beg[0]#月初
        self.lastyear_mon=month_beg[1]#上年月末
        sql_begdate="select MONTHBEG_ID from D_DATE where id=%s"%(month_beg[1])
        last_month_beg = self.engine.execute(sql_begdate.encode('utf-8'),vlist).fetchone()
        self.lastyear_beg=last_month_beg[0]#上年12月月初
        print(self.date_id,self.month_beg,self.lastyear_mon,self.lastyear_beg)
        sql = """
        select 
        aa.YM,---月
        aa.ORG_no,--机构号
        (nvl(benhang.atm_ben,0)+nvl(tadaiben.atm_ta,0)+aa.wanyin+aa.mobile+aa.zizhu)/((nvl(benhang.atm_ben,0)+nvl(tadaiben.atm_ta,0)+aa.wanyin+aa.mobile+aa.zizhu+aa.guimian)*1.0)*100 as dianzilv,---电子渠道交易率
        (nvl(benhang.atm_ben,0)+nvl(tadaiben.atm_ta,0)+aa.wanyin+aa.mobile+aa.zizhu) as dian_num,--电子渠道笔数
        nvl(benhang.atm_ben,0),--ATM本行
        nvl(tadaiben.atm_ta,0),--ATM她行
        aa.wanyin,--网银
        aa.mobile,--手机银行笔数
        aa.zizhu,--自助
        aa.guimian,--柜面
        nvl(tidai.tidailv,0)*100,--电子银行替代率
        aa.total_num,--总业务
        aa.computer_num,--电脑平台笔数
        aa.hexin,--核心
        aa.xiaoer,--小额
        aa.daishou,--代收
        aa.duiwai--对外
        from
        (select YM,ORG_no,sum(mobile) as mobile, sum(wanyin) as wanyin , sum(zizhu) as  zizhu, sum(guimian) as guimian,sum(hexin_num)-sum(xiaoer)-sum(daishoufu)+((sum(xianjincun)-sum(neibuxianjin))/30000.0) as total_num,
        (sum(hexin_num)-sum(xiaoer)) as computer_num,sum(hexin_num) as hexin,sum(xiaoer) as xiaoer,sum(daishoufu) as daishou,((sum(xianjincun)-sum(neibuxianjin))/30000.0) as duiwai
        from
        (SELECT
        d.id,
        d.ym,
        F.TRAN_BRANCH_CODE as org_no,
        count( (case when   DT.ANALYSIS_CHANNEL IN ('手机银行', 'ME') then  f.teller_jno end) ) as mobile, ---手机
        count( (case when   DT.ANALYSIS_CHANNEL IN ('网银', 'IE') then  f.teller_jno end) ) as wanyin ,---网银
        count( (case when   DT.ANALYSIS_CHANNEL IN ('自助终端', 'AT') then  f.teller_jno end) ) as zizhu ,---自助终端
        count( (case when   DT.ANALYSIS_CHANNEL IN ('柜面', 'TE')  and DT.FIN_FLAG  Like '会计流水%%' AND DT.REV_FLAG ='未抹账' then  f.teller_jno end) ) as guimian, ---柜面
        sum(nvl(t.discount,0)) as hexin_num,---折算后的笔数
        count( (case when  F.TEL_TRAN_CODE IN ('413091','005231', '005232', '005212')  then  f.teller_jno end) ) AS daishoufu, ---代收代付
        count( (case when  F.TEL_TRAN_CODE IN ('001103','001105','001113','001114','004601','004602','004605','004606') AND (F.AMOUNT/100.00)<=10000 then  f.teller_jno end) ) AS xiaoer, ---小额业务笔数
        sum( nvl((case when  F.TEL_TRAN_CODE IN ('001103','001113','004601','004605') then  f.AMOUNT end),0) )/100.00 as xianjincun ,--现金存
        sum( nvl((case when  F.TEL_TRAN_CODE IN ('006213','006218','006253') then  f.AMOUNT end),0) )/100.00 as neibuxianjin --内部现金调整
        FROM
        (select row_number() over(partition by date_id,TELLER_JNO order by AMOUNT desc ) as aa,a.*from F_JRN_TRANSACTION  a where date_id>=%s and date_id<=%s) F
        INNER JOIN D_JRN_TRANSACTION_TYPE DT
        ON F.JRN_TRAN_TYPE_ID=DT.ID
        left join TRANSACTION_CODE t --交易代码的折算率 d
        on F.TEL_TRAN_CODE=t.tranid 
        INNER JOIN D_DATE D
        ON D.ID = F.DATE_ID
        WHERE
        D.ID>=%s and d.id<=%s
        and
        F.TRAN_BRANCH_CODE LIKE '966%%'
        and F.aa=1
        GROUP BY
        D.ID,
        d.ym ,                                                                                  
        F.TRAN_BRANCH_CODE )
        group by  YM,org_no) as aa
        
        left join
        
        (select YM,ORG_no,sum(teller_jno) as atm_ben from 
        (SELECT
        d.id,
        d.ym,
        a.ORG_NO,
        count(distinct f.teller_jno) as teller_jno ---通过交易柜员号去统计每天的数据
        FROM
        F_JRN_TRANSACTION F
        INNER JOIN D_ATM A
        ON F.TERMINAL_CODE=A.ATM_NO
        INNER JOIN D_JRN_TRANSACTION_TYPE DT
        ON F.JRN_TRAN_TYPE_ID=DT.ID
        INNER JOIN D_DATE D
        ON D.ID = F.DATE_ID
        WHERE
        d.ID>=%s and d.id<=%s and
        F.SALE_ROLE='存款对账登记簿' and
        F.TRAN_BRANCH_CODE LIKE '966%%' AND
        F.ACCT_OPEN_BRANCH_CODE LIKE '966%%' AND--通过账户表里的开户机构来查
        DT.ANALYSIS_CHANNEL IN ('CA', 'ATM','NA','农信银ATM', 'UA','银联ATM') 
        GROUP BY
        D.ID,                                                                                   
        a.ORG_no,
        d.ym )                                  
        group by  YM,org_no )benhang on aa.YM=benhang.YM and aa.org_no=benhang.org_no
        left join
        
        (select YM,ORG_no, sum(teller_jno)as atm_ta from
        (SELECT
        d.id,
        d.ym,
        F.ACCT_OPEN_BRANCH_CODE as org_no,
        count(distinct F.teller_jno) as teller_jno ---通过交易柜员号去统计每天的数据
        FROM
        F_JRN_TRANSACTION F
        INNER JOIN D_JRN_TRANSACTION_TYPE DT
        ON F.JRN_TRAN_TYPE_ID=DT.ID
        INNER JOIN D_DATE D
        ON D.ID = F.DATE_ID
        WHERE
        D.ID>=%s and d.id<=%s AND
        --F.ACCT_OPEN_BRANCH_CODE = '966010' and
        F.SALE_ROLE='存款对账登记簿' and
        F.ACCT_OPEN_BRANCH_CODE LIKE '966%' AND
        F.TRAN_BRANCH_CODE not LIKE '966%' AND
        DT.ANALYSIS_CHANNEL IN ('CA', 'ATM','NA','农信银ATM', 'UA','银联ATM') AND
        DT.ATM_FLAG = '非本行ATM'  
        AND F.TERMINAL_CODE not in (select atm_no from  d_atm where TYP in ('取', '存取') AND SUB_TYP = '附')
        GROUP BY
        D.ID,
        d.ym ,                                                                                  
        F.ACCT_OPEN_BRANCH_CODE )
        group by  YM, org_no)
        tadaiben on aa.YM=tadaiben.YM and aa.org_no=tadaiben.org_no
        
        left join
        (select a.org_no,a.ym,a.tidaisum/(b.zongshu*1.0) as tidailv
        from 
        (select YM,ORG_no,atm_Flag,sum(teller_jno) as tidaisum from
        (SELECT
        d.id,
        d.ym,
        '电子替代' as atm_Flag,
        F.TRAN_BRANCH_CODE as org_no,
        count(distinct f.teller_jno) as teller_jno ---通过交易柜员号去统计每天的数据
        FROM
        F_JRN_TRANSACTION F
        INNER JOIN D_JRN_TRANSACTION_TYPE DT
        ON F.JRN_TRAN_TYPE_ID=DT.ID
        INNER JOIN D_DATE D
        ON D.ID = F.DATE_ID
        WHERE
        D.ID>=%s and d.id<=%s
        and
        F.TRAN_BRANCH_CODE LIKE '966%%' AND
        DT.ANALYSIS_CHANNEL IN (
        'CP',   '电话POS','IP', 'POS','NP', '农信银POS','UP',   '银联POS','9134','移动POS','CA', 'ATM','NA','农信银ATM', 'UA','银联ATM','CC',   '电话银行%%','短讯服务','IB',   '支付宝','FC',  '浙金中心电子支付','ND',   '互联网支付系统','PT',  '网上支付','手机银行', 'ME','自助终端', 'AT','网银', 'IE') 
        GROUP BY
        D.ID,
        d.ym ,                                                                                  
        F.TRAN_BRANCH_CODE )
        group by  YM,org_no,atm_Flag) a
        join
        (select YM,ORG_no,atm_Flag,sum(teller_jno) as zongshu from
        (SELECT
        d.id,
        d.ym,
        '电子替代' as atm_Flag,
        F.TRAN_BRANCH_CODE as org_no,
        count(distinct f.teller_jno) as teller_jno ---通过交易柜员号去统计每天的数据
        FROM
        F_JRN_TRANSACTION F
        INNER JOIN D_JRN_TRANSACTION_TYPE DT
        ON F.JRN_TRAN_TYPE_ID=DT.ID
        INNER JOIN D_DATE D
        ON D.ID = F.DATE_ID
        WHERE
        D.ID>=%s and d.id<=%s
        and
        F.TRAN_BRANCH_CODE LIKE '966%%' AND
        DT.ANALYSIS_CHANNEL IN (
        'CP',   '电话POS','IP', 'POS','NP', '农信银POS','UP',   '银联POS','9134','移动POS','CA', 'ATM','NA','农信银ATM', 'UA','银联ATM','CC',   '电话银行%%','短讯服务','IB',   '支付宝','FC',  '浙金中心电子支付','ND',   '互联网支付系统','PT',  '网上支付','手机银行', 'ME','自助终端', 'AT','网银', 'IE','柜面', 'TE') 
        GROUP BY
        D.ID,
        d.ym ,                                                                                  
        F.TRAN_BRANCH_CODE )
        group by  YM,org_no,atm_Flag)b
        on a.ym=b.ym and a.org_no=b.org_no)tidai 
        on aa.ym=tidai.ym and aa.org_no=tidai.org_no
        where 1=1 %s order by aa.org_no
              """%(self.month_beg,self.date_id,self.month_beg,self.date_id,self.month_beg,self.date_id,self.month_beg,self.date_id,self.month_beg,self.date_id,self.month_beg,self.date_id,filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()

        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i)
            sql_org_name="select branch_name from branch where BRANCH_CODE ='%s' "%(t[1])
            row_org_name = self.engine.execute(sql_org_name.encode('utf-8'),vlist).fetchone()
            row_org_name=row_org_name[0]#插第二位置--机构名
            sql_self_org="select is_config_selfhelp from report_manager_workquality_hander where left(date_id,6)= %s and org_code='%s'"%(int(str(self.date_id)[:6]),t[1])
            sql_self_org = self.engine.execute(sql_self_org.encode('utf-8'),vlist).fetchone()
            if sql_self_org is None:
                sql_self_org=u'未配置'
            else:
                sql_self_org=sql_self_org[0] #插第三个配置
            if sql_self_org=u'已配置':
                guimian_lv=t[2]*0.7+t[10]*0.3
            else:
                guimian_lv=t[2]*100% #插第5个位置
            t.insert(2,row_org_name)
            t.insert(3,sql_self_org)
            t.insert(4,0)#上年基数先留着
            t.insert(5,guimian_lv)
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)

#    def get_atm_counts_by_org_no(self, org_no):
#        sql = """ select count(*) from D_ATM M  where M.ORG_NO = ? and M.TYP in ('取', '存取') AND M.SUB_TYP = '附' """
#        atm_count = self.engine.execute(sql, [org_no]).fetchall()[0]
#        return int(atm_count[0])

    def make_eq_filterstr(self):
        filterstr = ""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and aa.ORG_NO in ( %s ) and "%(vvv)
                elif k == 'FROM_DATE_ID':
                    self.date_id= int(v)
                else: 
                    pass
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],"",'aa.ORG_NO', None))
        return filterstr, vlist

    def column_header(self):
        return ["统计月份", "机构编号","机构名称","是否配置自助设备","柜面业务离柜率基数","当月柜面业务离柜率","电子渠道交易率","电子渠道交易笔数","ATM本行交易笔数", "ATM他代本交易笔数","网上银行交易笔数", "手机银行交易笔数", "自助终端交易笔数", "柜面渠道交易笔数", "电子银行替代率", "总业务量", "电脑平台总笔数", "核心系统取数换算后的笔数", "小额业务笔数","代收代付笔数", "对外现金收入量"]

    @property
    def page_size(self):
        return 15
