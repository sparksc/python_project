# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
"""
存款业务计划数参数
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['BE_YEAR','org','SALE_CODE']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT YEAR,THIRD_ORG_CODE,THIRD_ORG_NAME,ORG_CODE,ORG_NAME,MANAGER_CODE,MANAGER_NAME,TAR_SJ,TAR_WY,TAR_POS,TAR_ETC,TAR_EPAY,TAR_ZN,ID FROM P_EBANK_NUM 
        WHERE 1=1 %s
        ORDER BY YEAR,THIRD_ORG_CODE,ORG_CODE,MANAGER_CODE,THIRD_ORG_NAME,ORG_NAME,MANAGER_NAME 
        """%(filterstr)

        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            print k,v
            if k == 'login_teller_no':
                if self.deal_teller_query_auth(v) == True:
                    filterstr = filterstr+" and MANAGER_CODE = '%s'"%v
            elif k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False:
                    filterstr = filterstr+" and THIRD_ORG_CODE in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr+" and THIRD_ORG_CODE in ( %s) "%(vvv)
                elif k=='BE_YEAR':
                    if v != '':
                        filterstr = filterstr+" and YEAR = '%s'"%v
                elif k=='SALE_CODE':
                    if v !='':
                        filterstr = filterstr+" and MANAGER_CODE = '%s'"%v
 
        print filterstr,vlist
        return filterstr,vlist
    def column_header(self):
        return ["所属年份","网点编号","网点名称","客户经理编号","客户经理名称","新增手机银行有效户数(户)","新增企业网银有效户数(户)","新拓展POS机(户)","新增ETC户数(户)","新增有效丰收e支付户数(户)","助农服务点数量(个)","操作"]

    @property
    def page_size(self):
        return 15
