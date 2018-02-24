
# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
存款客户账户详情
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CUST_NO','ORG']
        filterstr,vlist = self.make_eq_filterstr() 
        sql ="""
                select d.BUSI_TYPE,d.OPEN_TIME from f_contract_status f
                join d_cust_contract d on d.id=f.CONTRACT_ID
                join CUST_HOOK c on c.CUST_IN_NO=d.CST_NO
                where f.status='正常' %s
	        """%(filterstr)
        print sql
        print vlist
        row = self.engine.execute(sql,vlist).fetchall()
        return row
    
    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'DATE':
                    filterstr = filterstr + " and f.date_id = ? " 
                    vlist.append(v)
                if k == 'SALE_CODE':
                    filterstr = filterstr + " and manager_no = ? "
                    vlist.append(v)
                if k == 'CUST_NO':
                    filterstr = filterstr + " and c.cust_no = ? "
                    vlist.append(v)
                if k == 'ORG':
                    filterstr = filterstr + " and c.org_no = ? "
                    vlist.append(v)
        return filterstr,vlist


    def column_header(self):
        return ["电子银行子类型","开户日期"]

    @property
    def page_size(self):
        return 10

















