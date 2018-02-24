# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
机构存贷款数据调整
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['institution','timestype','businessType','adjustState']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
            select times,c2.dict_value,b.BRANCH_NAME,c1.dict_value, adjustNum, adjustState,ID
            from T_CQK_TYPE
            inner join BRANCH b on BRANCH_CODE = INSTITUTION
            inner join DICT_DATA  c1 on c1.DICT_KEY = BUSINESSTYPE and c1.DICT_TYPE = 'ywlx'
            inner join DICT_DATA  c2 on c2.DICT_KEY = TIMESTYPE and c2.DICT_TYPE = 'tzzxlx'
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
        return ["调整周期","调整周期类型","机构号","业务类型", "调整值", "状态","操作"]

    @property
    def page_size(self):
        return 10
