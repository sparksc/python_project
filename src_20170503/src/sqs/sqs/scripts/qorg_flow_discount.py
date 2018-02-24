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
柜员业务量
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org','SALE_CODE','START_DATE','FINISH_DATE']
        self.start_date_id=""
        self.date_id=""
        filterstr,vlist = self.make_eq_filterstr()
        """
        交易业务量
        """
        sql1 ="""
        select * from ORG_FLOW_DISCOUNT where 1=1 %s
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
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and ORG_CODE in ( %s ) "%(vvv)
                elif k=='START_DATE':
                    filterstr = filterstr +" and START_DATE >= %s  "%(int(v))
                elif k=='FINISH_DATE':
                    filterstr = filterstr +" and START_DATE >= %s  "%(int(v))
                elif k=='PST_NAME':
                    filterstr = filterstr+" and PST_NAME like '%s' "%(v)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return[u"机构号",u"机构名",u"岗位名称",u"折算系数",u"生效年月",u"终止年月"]                                                                            
    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        xxx = '{:,}'.format(tmp)
        return xxx

    @property
    def page_size(self):
        return 15
