# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery

"""
机具待认定
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CUST_NO','MANAGER_NO','TYP','SRC','ORG_NO','STATUS','NOTE','SUB_TYP','hide']
        filterstr,vlist = self.make_eq_filterstr()
        print"filterstr----%s\n"%filterstr
        print"vlist----------%s\n"%vlist
        sql =u"""SELECT c.ETL_DATE,c.sub_typ, c.ORG_NO, d.ORG0_NAME, c.CUST_NO, i.CUST_NAME, c.NOTE,q.sub_typ ,c.ID 
                 FROM YDW.CUST_HOOK c
                 LEFT JOIN D_ORG d on d.org0_code=c.org_no 
                 LEFT JOIN D_CUST_INFO i on i.cust_no=c.cust_no
                 LEFT JOIN D_ATM q on c.cust_no=q.atm_no
                 WHERE c.typ='机具' and c.status='待手工' %s ORDER BY c.ID DESC"""%(filterstr)
        print "sql========%s====\n"%sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        print("args.items---------%s\n"%self.args)
        print("self.filterlist===%s"%self.filterlist)
        for k,v in self.args.items():
            if k == 'login_branch_no':
                bb = self.deal_branch_query_auth(v)
                if bb != False :
                    filterstr = filterstr+" and c.org_no in ( %s )"%bb
            if v and k in self.filterlist:
                print "k====%s"%k
                print "v====%s"%v
                if k == 'ORG_NO':
                    vvv = self.dealfilterlist(v)
                    print "vvv---%s"%vvv
                    filterstr = filterstr +" and c.org_no in( %s ) "%(vvv)
                elif k=='TYP':
                    filterstr = filterstr+" and c.SUB_TYP in('%s')"%(v)
                elif k=='SUB_TYP':
                    filterstr = filterstr+"and q.SUB_TYP in('%s')"%v
                elif k == 'CUST_NO':
                    filterstr = filterstr + " and c.cust_no =? "
                    vlist.append(v)
                elif k == 'NOTE':
                    filterstr = filterstr + " and note like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                elif k == 'hide':
                    filterstr = filterstr + " and c.hide = ? "
                    vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["日期","机具类型","机构号","机构名","机具编号","客户名","地址信息","附离类型","操作"]

    @property
    def page_size(self):
        return 10
