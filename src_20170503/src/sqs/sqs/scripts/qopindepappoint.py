# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
存款预约新增查看
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['yyrq','khmc','yybljg']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
		    select yyrq,jgbh,jgmc,yggh,ygxm,khmc,khh,zh,dxxh,c.branch_name,yyblrq,yyckje,rqsc,BZ,open_date,para_id
		    from t_zjc_gsgx_ck_yy a 
		    inner join t_cs_yyyxrq b on b.YYYXRQ=a.YYYXRQ
            inner join branch c on c.branch_code = a.yybljg 
		    where a.bz in ('4') and
                NOT EXISTS (SELECT '1' FROM T_ZJC_GSGX_CK C  WHERE a.ZH=C.DXBH AND a.DXXH=C.DXXH) %s 
		    order by yyrq desc
	    """%(filterstr)
        
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={13:'BZZT'}
        return self.translate(row,needtrans)
    
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                filterstr = filterstr+" and %s = ?" % k
                vlist.append(v)
        return filterstr,vlist


    def column_header(self):
        return ["预约日期","机构编号", "机构名称", "员工工号","员工姓名","客户名称","客户号","账户","账户序号","预约办理机构","预约办理日期","预约存款金额","预约有效日期","状态"]

    @property
    def page_size(self):
        return 15
