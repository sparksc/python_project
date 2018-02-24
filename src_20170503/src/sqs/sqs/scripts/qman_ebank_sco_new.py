# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
客户经理电子银行得分
"""

class Query(ObjectQuery):
 
    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql="""
        SELECT R.DATE_ID,R.ORG_CODE,R.ORG_NAME,R.SALE_CODE,R.SALE_NAME,(NVL(R.MB_THIS_NUM,0)-R1.MB_THIS_NUM),MB_ADD_SCO/ 100.00,(NVL(R.CB_THIS_NUM,0)-R1.CB_THIS_NUM),CB_ADD_SCO/ 100.00,
        (NVL(R.POS_THIS_NUM,0)-R1.POS_THIS_NUM),POS_ADD_SCO/ 100.00, NVL(RMC.BAD_ALL/ 100.0,0),BAD_ADD_SCO/ 100.00,(NVL(R.ETC_THIS_NUM,0)-R1.ETC_THIS_NUM),ETC_ADD_SCO/ 100.00,
        (R.EPAY_THIS_NUM-R1.EPAY_THIS_NUM),EPAY_ADD_SCO/ 100.00, 
        CASE WHEN NVL(R.FARM_SERV_HIGH_NUM,0)!=0 THEN (NVL(R.FARM_SERV_HIGH_NUM,0))*100.00/(NVL(R.FARM_SERVICE_LOW_NUM,0)+NVL(R.FARM_SERV_HIGH_NUM,0)) ELSE 0 END,FRAM_SCO/ 100.00,
        FLOAT(NVL(MB_PERCENT,0)), NVL(MB_PERCENT_SAL,0)/ 100.00,FLOAT(NVL(PUB_PERCENT,0)),NVL(PUB_PERCENT_SAL,0)/100.00,ALL_SCO/ 100.00
        FROM REPORT_MANAGER_OTHER R
        JOIN ( SELECT O.DATE_ID,O.ORG_CODE,O.SALE_CODE,NVL((O.MB_THIS_NUM),0) AS MB_THIS_NUM ,NVL((O.CB_THIS_NUM),0) AS CB_THIS_NUM,NVL((O.EPAY_THIS_NUM),0) AS EPAY_THIS_NUM,NVL((O.ETC_THIS_NUM),0)  AS ETC_THIS_NUM,(NVL(O.POS_THIS_NUM,0)) AS POS_THIS_NUM FROM REPORT_MANAGER_OTHER O WHERE O.DATE_ID =(SELECT L_YEAREND_ID FROM D_DATE WHERE ID=?) ) R1 ON R1.SALE_CODE=R.SALE_CODE
        JOIN REPORT_MANAGER_CREDITCARD RMC ON  RMC.SALE_CODE=R.SALE_CODE AND RMC.DATE_ID=R.DATE_ID
        WHERE 1=1 %s 
        GROUP BY R.DATE_ID,R.ORG_CODE,R.ORG_NAME,R.SALE_CODE,R.SALE_NAME,ALL_SCO,FRAM_SCO,POS_ADD_SCO,CB_ADD_SCO,MB_ADD_SCO,EPAY_ADD_SCO,R.FARM_SERV_HIGH_NUM,R.FARM_SERVICE_LOW_NUM,R.EPAY_THIS_NUM,R1.EPAY_THIS_NUM,ETC_ADD_SCO,R.ETC_THIS_NUM,R1.ETC_THIS_NUM,BAD_ADD_SCO ,RMC.BAD_ALL,R.POS_THIS_NUM,R1.POS_THIS_NUM,R1.CB_THIS_NUM,R.CB_THIS_NUM,R1.MB_THIS_NUM,R.MB_THIS_NUM,R.PUB_PERCENT_SAL,R.MB_PERCENT_SAL,R.MB_PERCENT,R.PUB_PERCENT
        ORDER BY R.DATE_ID,R.ORG_CODE,R.SALE_CODE
        """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print sql 
        needtrans ={}
        i=0
        rowlist=[]
        for i in row:
            t = list(i[0:5])
            for j in i[5:]:
                if j is None:j=0
                j = round(j,2)
                t.append(j)
            rowlist.append(t)
        return self.translate(rowlist,needtrans)


    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        global ymday
        for k,v in self.args.items():
            print k,v
            if k == 'login_teller_no':
                if self.deal_teller_query_auth(v) == True:
                    filterstr = filterstr+" and R.SALE_CODE = '%s'"%v
            elif k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False:
                    filterstr = filterstr+" and R.ORG_CODE in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr+" and R.ORG_CODE in ( %s) "%(vvv)
                elif k== 'DATE_ID':
                    filterstr = filterstr+" and R.DATE_ID = ?"
                    vlist.append(v)
                    vlist.append(v)
                else :
                    filterstr = filterstr+" and R.SALE_CODE = '%s'"%v
            
        return filterstr,vlist

    def column_header(self):
        return ["统计时间","机构号","机构名称","员工号","员工名称","新增手机银行有效户数","新增手机银行有效户数得分","新增企业网银有效户数","新增企业网银有效户数得分","新拓展POS机","新拓展POS机得分","新增丰收贷记卡逾期本金","新增丰收贷记卡逾期本金得分","新增ETC","新增ETC指标得分","新增有效丰收e支付","新增有效丰收e支付得分","助农服务点月平均活点率","助农服务点月平均活点率得分","对私类贷款客户有效手机银行绑定率","对私类贷款客户有效手机银行绑定率得分","公司类贷款客户有效网上银行绑定率","公司类贷款客户有效网上银行绑定率得分","电子银行总得分"]
    @property
    def page_size(self):
        return 15
