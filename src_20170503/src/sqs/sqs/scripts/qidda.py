# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
参数类型查看
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['instition_number','business_type','nowstate']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select INSTITION_NUMBER,BUSINESS_TYPE,NOW_STATE, ADJUST_TIME_TYPE, ADJUST_TIME,ADJUST_VALUE,ID
            from ALIANGNEW
            where 1=1 %s   
	    """%(filterstr)
        
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ? "%k 
                vlist.append(v) 
        return filterstr,vlist
    

    def column_header(self):
        return ["机构号","业务类型", "状态","调整周期类型", "调整周期","调整值"]

    @property
    def page_size(self):
        return 15
