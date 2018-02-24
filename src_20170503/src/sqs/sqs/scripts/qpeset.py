# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
合约查看
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['pei_freq','object_type']
        filterstr,vlist,c_id = self.make_eq_filterstr() 
        sql ="""
				SELECT * FROM (SELECT NAME,PEI_FREQ,TYPE,OBJECT_TYPE,DESC,DATA_SRC,PEI_ID
				FROM PE_PEI_DEF DEF WHERE NOT EXISTS (SELECT PEI_ID FROM PE_CONTRACT_DETAIL DET WHERE DET.PE_PEI_ID=DEF.PEI_ID AND DET.CONTRACT_ID=%s)) A
				WHERE 1=1 %s 
				ORDER BY PEI_ID DESC 
	    """%(c_id,filterstr)
        
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)
    
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k == 'contract_id':
                c_id=v;
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ?"%k
                vlist.append(v)
        return filterstr,vlist,c_id


    def column_header(self):
		return ["指标名称", "指标周期","指标性质","对象类型","指标描述","数据来源","操作"]

    @property
    def page_size(self):
        return 15
