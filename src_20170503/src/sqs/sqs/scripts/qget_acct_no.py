# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
存款帐号详情
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CST_NO','DATE','ORG']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
            select d.account_no
            from f_balance f
            join d_account d on d.id=f.ACCOUNT_ID
            join d_org o on o.ID=f.ORG_ID
            where f.DATE_ID=20150103 and f.acct_type=1 %s
	    """%(filterstr)
        print sql
        print vlist
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans = {}
        return self.translate(row,needtrans)
    
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                #if k == 'DATE':
                #    filterstr = filterstr + " and f.date_id = ? " 
                #    vlist.append(v)
                if k == 'CST_NO':
                    filterstr = filterstr + " and f.cst_no = ? "
                    vlist.append(v)
                if k == 'ORG':
                    filterstr = filterstr + " and o.org0_code = ? "
                    vlist.append(v)
        return filterstr,vlist


    def column_header(self):
        return ["账户","占比", "机构号","机构名","员工号","员工名","余额","状态","管理开始日期", "管理结束日期"]

    @property
    def page_size(self):
        return 20
