# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from objectquery import ObjectQuery
"""
理财预约查看
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['yyrq','khmc','yybljg']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
		    select yyrq,jgbh,jgmc,yggh,ygxm,khmc,c.branch_name,yyblrq,yyckje,para_id 
		    from t_zjc_gsgx_ck_yy a 
            inner join branch c on c.branch_code = a.yybljg 
		    where 1=1 and typ='理财' %s 
		    order by yyrq desc
	    """%(filterstr)
        
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={10:'BZZT'}
        return self.translate(row,needtrans)
    
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ?"%k
                vlist.append(v)
        return filterstr,vlist


    def column_header(self):
        return ["预约日期","机构编号", "机构名称", "员工工号","员工姓名","客户名称","预约办理机构","预约办理日期","预约理财金额"]

    @property
    def page_size(self):
        return 15
