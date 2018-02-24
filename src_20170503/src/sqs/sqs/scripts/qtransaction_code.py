# -*- coding:utf-8 -*-
import sys
import datetime
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
"""
交易码折算率
"""
class Query(ObjectQuery):
  
    def prepare_object(self):
        self.filterlist = ['DATE_ID','ORG_CODE','TRANNAME','TRANID']
        filterstr,vlist = self.make_eq_filterstr()
        print filterstr,vlist
        sql=u"""
        SELECT TRANID,TRANNAME,BEGIN_DT,END_DT,DISCOUNT,ID FROM TRANSACTION_CODE  WHERE 1=1 %s
        ORDER BY ID 
        """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print sql 
        needtrans ={}
        i=0
        rowlist=[]
       
        for i in row:
            t = list(i[0:2])
            for j in i[2:]:
                if j is None: j=0
                j = str(j)
                t.append(j)
            rowlist.append(t)
        return self.translate(rowlist,needtrans)
        
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                print k,v
                if k == 'TRANID' :
                    filterstr = filterstr+" and TRANID =  '%s' "%(v)
                elif k == 'TRANNAME':
                    filterstr = filterstr+" and TRANNAME  like '%%%s%%' "%(v)
                else:
                    return filterstr,vlist
        return filterstr,vlist


    def column_header(self):
        return ["交易码","交易名称","开始时间","结束时间","折算率","操作"]
    
    @property
    def page_size(self):    
        return 15
