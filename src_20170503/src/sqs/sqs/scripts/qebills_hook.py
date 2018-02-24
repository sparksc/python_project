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
国际业务归属自动认定
"""
class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE','count','CORPNAME','CUST_IN_NO',"IS_OPEN_NEW_WH","check_workno"]
        self.mon_date=''
        self.count=""
        filterstr,vlist = self.make_eq_filterstr()
        sql_ebills="""
        select 
        MONTH,           --0
        ORG_CODE,           --1
        ORG_NAME,     --2
        CORPNAME,          --3中文名称
        SALE_CODE,         --4
        SALE_NAME,             --5
        round(nvl(EXBPAMT,0)/1000000.00,2) ,           -- '出口议付金额' 6
        
        round(nvl(EXAGENTAMT,0)/1000000.00,2),         -- '出口托收金额' 7
        round(nvl(EXCLEANAMT,0)/1000000.00,2),         -- '出口光票托收金额'8
        round(nvl(NTCLEANAMT,0)/1000000.00,2),         -- '非贸易光盘托收金额'9

        round(nvl(EXAGENTAMT,0)/1000000.00,2)+         -- '出口托收金额' 7
        round(nvl(EXCLEANAMT,0)/1000000.00,2)+         -- '出口光票托收金额'8
        round(nvl(NTCLEANAMT,0)/1000000.00,2),         -- '非贸易光盘托收金额'9
        ---round((nvl(EXAGENTAMT,0)+nvl(EXCLEANAMT,0)+nvl(NTCLEANAMT,0))/1000000.00,2),--托收合计10
        
        round(nvl(EXINREMITAMT,0)/1000000.00,2),       -- '出口汇入汇款金额'11
        round(nvl(NTINREMITAMT,0)/1000000.00,2),       -- '非贸易汇入汇款金额'12

        round(nvl(EXINREMITAMT,0)/1000000.00,2)+       -- '出口汇入汇款金额'11
        round(nvl(NTINREMITAMT,0)/1000000.00,2),       -- '非贸易汇入汇款金额'12

       --round((nvl(EXINREMITAMT,0)+nvl(NTINREMITAMT,0))/1000000.00,2),--汇入汇款合计13
        
        round(nvl(imoutremtiamt,0)/1000000.00,2),      -- '进口汇出汇款金额'14
        round(nvl(ntoutremitamt,0)/1000000.00,2),      -- '非贸易汇出汇款金额'15

        round(nvl(IMOUTREMTIAMT,0)/1000000.00,2)+      -- '进口汇出汇款金额'14
        round(nvl(NTOUTREMITAMT,0)/1000000.00,2),      -- '非贸易汇出汇款金额'15


        ---round((nvl(IMOUTREMTIAMT,0)+nvl(NTOUTREMITAMT,0))/1000000.00,2),--汇出汇款合计16
        
        round(nvl(IMLCAMT,0)/1000000.00,2),            -- '进口开证金额'17
        round(nvl(IMICAMT,0)/1000000.00,2),            -- '进口代收金额'18
        round(nvl(FIINREMITAMT,0)/1000000.00,2),       -- '资本项下汇入汇款金额'19
        round(nvl(FIOUTREMITAMT,0)/1000000.00,2),      -- '资本项下汇出汇款金额'20
        round(nvl(LGAMT,0)/1000000.00,2),              -- '保函金额'21
        round(nvl(IMLGAMT,0)/1000000.00 ,2),          -- '进口保函金额'22
        

        round(nvl(EXBPAMT,0)/1000000.00,2) +          -- '出口议付金额' 6
        round(nvl(EXAGENTAMT,0)/1000000.00,2)+         -- '出口托收金额' 7
        round(nvl(EXCLEANAMT,0)/1000000.00,2)+         -- '出口光票托收金额'8
        round(nvl(NTCLEANAMT,0)/1000000.00,2)+         -- '非贸易光盘托收金额'9
        round(nvl(EXINREMITAMT,0)/1000000.00,2)+       -- '出口汇入汇款金额'11
        round(nvl(NTINREMITAMT,0)/1000000.00,2)+       -- '非贸易汇入汇款金额'12
        round(nvl(imoutremtiamt,0)/1000000.00,2)+      -- '进口汇出汇款金额'14
        round(nvl(ntoutremitamt,0)/1000000.00,2)+      -- '非贸易汇出汇款金额'15
        round(nvl(IMLCAMT,0)/1000000.00,2)+            -- '进口开证金额'17
        round(nvl(IMICAMT,0)/1000000.00,2)+            -- '进口代收金额'18
        round(nvl(FIINREMITAMT,0)/1000000.00,2)+       -- '资本项下汇入汇款金额'19
        round(nvl(FIOUTREMITAMT,0)/1000000.00,2)+      -- '资本项下汇出汇款金额'20
        round(nvl(LGAMT,0)/1000000.00,2)+              -- '保函金额'21
        round(nvl(IMLGAMT,0)/1000000.00 ,2),          -- '进口保函金额'22
 

        ---round((nvl(EXBPAMT,0)+nvl(EXAGENTAMT,0)+nvl(EXCLEANAMT,0)+nvl(NTCLEANAMT,0)+nvl(EXINREMITAMT,0)+nvl(NTINREMITAMT,0)+nvl(IMOUTREMTIAMT,0)+nvl(NTOUTREMITAMT,0)+nvl(IMLCAMT,0)+nvl(IMICAMT,0)+nvl(FIINREMITAMT,0)+nvl(FIOUTREMITAMT,0)+nvl(LGAMT,0)+nvl(IMLGAMT,0))*1.0/1000000,2),--国际业务结算量23
        
        round(nvl(USANCEAMT,0)/1000000.00,2),--远期24 
        round(nvl(SIGHTAMT,0)/1000000.00,2),--即期 25
        round(nvl(CROSSBORDERAMT,0)/1000000.00,2),--跨境26

        round(nvl(USANCEAMT,0)/1000000.00,2)+  --远期24 
        round(nvl(SIGHTAMT,0)/1000000.00,2)+   --即期 25
        round(nvl(CROSSBORDERAMT,0)/1000000.00,2),--跨境26


        ---round((nvl(USANCEAMT,0)+nvl(SIGHTAMT,0)+nvl(CROSSBORDERAMT,0))/1000000.00,2),--结售汇合计27

        round(nvl(MONTHAMT,0)/1000000.00,2),--外币存款折人民币月日均28
        round(nvl(DAYAMT,0)/1000000.00,2),--外币存款折人民币年日均29
        round(nvl(BALANCE,0)/1000000.00,2), ---外币存款折人民币余额30 
        IS_OPEN_NEW_WH,--31
        id, --32
        cust_in_no --33 
        from 
        ebills_hook
        where 1=1 %s order by month,org_code
        """%(filterstr)
        print sql_ebills
        row_ori = self.engine.execute(sql_ebills.encode('utf-8'),vlist).fetchall()
        needtrans ={}
        rowlist=[]
        if self.count=='count':
            for i in row_ori:
                i=list(i)
                t=list(i[0:6])
                for j in range(6,len(i)):
                    if i[j] is None:i[j]=0
                    t.append(i[j])
                rowlist.append(t)           
            return self.translate(rowlist,needtrans)
        else:
            for i in row_ori:
                i=list(i)
                t=list(i[0:6])
                for j in range(6,len(i)):
                    if i[j] is None:i[j]=0
                    t.append(i[j])
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
                elif k=="check_workno":
                    if v=="true":
                        filterstr = filterstr +" and (SALE_CODE is null or SALE_CODE='') "
                else: 
                    pass
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],"SALE_CODE",'ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return [
        [{"name": u"统计月份",'h':2},{"name": u"机构编号",'h':2},{"name": u"机构名称",'h':2},{"name": u"客户名称",'h':2},{"name":u"员工号",'h':2},{"name":u"员工姓名",'h':2},{"name":u"出口议付",'w':1},{"name":u"托收",'w':4},{"name": u"汇入汇款",'w':3},{"name": u"汇出汇款",'w':3},{"name":u"进口开证",'w':1},{"name":u"进口代收金额",'w':1},{"name":u"资本项目",'w':2},{"name":u"保函",'w':2},{"name":u"国际业务量合计值",'w':1},{"name":u"结售汇",'w':4},{"name":u"外币存款转人民币",'w':3},{"name":u"是否新开有效外汇账户",'w':1}],
        [{"name":u"出口议付",'h':1},{"name":u"出口托收",'h':1},{"name":u"出口光票托收",'h':1},{"name":u"非贸易光票托收",'h':1},{"name":u"托收合计",'h':1},{"name":u"出口汇入汇款",'h':1},{"name":u"非贸易汇入汇款",'h':1},{"name":u"汇入汇款合计",'h':1},{"name":u"进口汇出汇款",'h':1},{"name":u"非贸易汇出汇款",'h':1},{"name":u"汇出汇款合计",'h':1},{"name":u"进口开证",'h':1},{"name":u"进口代收金额",'h':1},{"name":u"资本项目下汇入汇款",'h':1}, {"name":u"资本项目下汇出汇款",'h':1}, {"name":u"保函",'h':1}, {"name":u"进口保函",'h':1}, {"name":u"国际业务量合计值",'h':1}, {"name":u"远期",'h':1}, {"name":u"即期",'h':1}, {"name":u"跨境",'h':1}, {"name":u"结售汇合计值",'h':1},{"name":u"外币存款折人民币月日均",'h':1}, {"name":u"外币存款折人民币年日均",'h':1},{"name":u"外币存款折人民币余额",'h':1},{"name":u"是否新开有效外汇账户",'h':1}]
    ]

    @property
    def page_size(self):
        return 15
