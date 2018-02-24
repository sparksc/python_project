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
柜员业务量调整值
"""

class Query(ObjectQuery):


    def prepare_object(self):
        self.filterlist = ['DATE_ID','ORG_CODE','SALE_CODE','START_DATE','FINISH_DATE']
        self.start_date_id=""
        self.date_id=""
        filterstr,vlist = self.make_eq_filterstr()
        sql1 ="""
        SELECT DATE_ID, CHILD_ORG_CODE, CHILD_ORG_NAME, TRAN_TELLER_CODE, SALE_NAME, ADJ_VALUES, PST_SEASON ,id
        FROM YDW.TELLER_VOLUME_ADJUST where 1=1 %s
        """%(filterstr)
        print sql1
        row1 = self.engine.execute(sql1.encode('utf-8'),vlist).fetchall()

        needtrans ={}
        row = []
        for i in row1:
            t=list(i)
            row.append(t)    
        return self.translate(row,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():

            if v and k in self.filterlist:
                if k == 'ORG_CODE':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and  CHILD_ORG_CODE in ( %s ) "%(vvv)
                elif k=='DATE_ID':
                    filterstr = filterstr +" and left(DATE_ID,6) = %s  "%(int(str(v)[:6]))
                elif k=='SALE_CODE':
                    filterstr = filterstr+" and TRAN_TELLER_CODE ='%s' "%(v)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        return filterstr,vlist

    def column_header(self):
        return["日期","机构号","机构名","柜员号","柜员名","调整值","调整原因","操作"]                                                                            
    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        xxx = '{:,}'.format(tmp)
        return xxx

    @property
    def page_size(self):
        return 15
