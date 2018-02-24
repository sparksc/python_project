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
				SELECT NAME,OBJECT_TYPE,DATA_SRC,WEIGHT,TARGET,DESC,FACT,SCORE,PEI_ID FROM PE_PEI_DEF A
				INNER JOIN PE_CONTRACT_DETAIL B ON B.PE_PEI_ID=A.PEI_ID
				WHERE B.CONTRACT_ID=%s %s 
				ORDER BY NAME 
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
		return ["指标名称","指标性质","数据来源","权重","目标值","指标描述","实际完成值","指标得分"]

    @property
    def page_size(self):
        return 15
