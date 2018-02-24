# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
POS待认定
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CUST_NO','CUST_NAME','TYPE','ORG_NO','NOTE','hide']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""SELECT c.START_DATE, c.ORG_NO, d.ORG0_NAME, c.CUST_NO, k.POS_NO,k.MERCHANT_NAME AS CUST_NAME ,k.TYP AS SUB_TYP, NOTE, c.ID 
                 FROM YDW.CUST_HOOK c
                 LEFT JOIN D_ORG d on d.org0_code=c.org_no 
                 LEFT JOIN D_POS k on c.cust_no=k.merchant_no and c.cust_in_no=k.POS_NO  
                 WHERE c.typ='POS' and c.status='待手工' %s ORDER BY c.ID DESC"""%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False :
                    filterstr = filterstr+" and c.org_no in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'ORG_NO':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and c.org_no in( %s ) "%(vvv)
                elif k == 'CUST_NO':
                    filterstr = filterstr + " and c.cust_no =?"
                    vlist.append(v)
                elif k == 'CUST_NAME':
                    filterstr = filterstr + " and k.MERCHANT_NAME like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                elif k == 'NOTE':
                    filterstr = filterstr + " and note like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                elif k == 'TYPE':
                    filterstr = filterstr + " and c.sub_typ = ? " 
                    vlist.append(v)
                elif k == 'hide':
                    filterstr = filterstr + " and c.hide = ? "
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["日期","机构号","机构名","商户号","终端号","商户名","类型","地址信息","操作"]

    @property
    def page_size(self):
        return 10
