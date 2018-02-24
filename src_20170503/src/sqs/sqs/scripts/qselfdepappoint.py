# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
存款预约新增查看
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['yyrq','yggh','khmc']
        filterstr,vlist = self.make_eq_filterstr() 
	    #todo
	    #用于没有数据先使用ydw下的两个表显
        sql ="""
		    select yyrq,jgbh,jgmc,yggh,ygxm,khmc,c.branch_name,yyblrq,yyckje,rqsc,BZ,para_id 
		    from t_zjc_gsgx_ck_yy a 
		    inner join t_cs_yyyxrq b on b.YYYXRQ=a.YYYXRQ
            inner join branch c on c.branch_code = a.yybljg 
		    where a.bz not in ('1') %s 
		    order by yyrq desc
	    """%(filterstr)
        
        print filterstr,vlist
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
        return ["预约日期","机构编号", "机构名称", "员工工号","员工姓名","客户名称","预约办理机构","预约办理日期","预约存款金额","预约有效日期","状态"]

    @property
    def page_size(self):
        return 15
