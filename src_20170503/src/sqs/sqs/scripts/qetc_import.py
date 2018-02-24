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
ETC导入数据查询
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID', 'sign_org', 'org','license','owner']
        filterstr, vlist = self.make_eq_filterstr()
        sql ="""
         SELECT DATE_ID, CUST_NET_NO, CUST_NAME, CARD_NO, CARD_NAME, SIGN_ORG_NO, SIGN_TELLER_NO, TELLER_NO,ORG_NO, ID
            FROM YDW.ETC_DATA d
         where 1=1 %s
         order by d.CUST_NET_NO
        """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print "etc_import:", sql
        needtrans ={}
        return self.translate(list(row),needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and d.ORG_NO in ( %s ) "%(vvv)
                elif k == 'DATE_ID':
                    filterstr = filterstr+" and d.DATE_ID = ?"
                    vlist.append(v)
                elif k == 'license':
                    filterstr = filterstr+" and d.CUST_NET_NO= ?"
                    vlist.append(v)
                elif k == 'owner':
                    filterstr = filterstr+" and d.CUST_NAME= ?"
                    vlist.append(v)
                else: 
                    pass
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'d.TELLER_NO','d.ORG_NO', None))
        return filterstr,vlist

    def column_header(self):
        return [ "签约日期", "车牌号", "车主", "卡号" , "卡主", "签约机构", "签约柜员", "归属柜员号", "归属机构号","操作"]

    @property
    def page_size(self):
        return 15
