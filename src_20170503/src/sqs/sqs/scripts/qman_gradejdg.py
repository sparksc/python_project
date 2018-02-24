# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from objectquery import ObjectQuery
from utils import config

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['org_no', 'kyear', 'user_name']
        filterstr,vlist = self.make_eq_filterstr()
        sql = u"""
        select bf.kyear, bf.org_no,b.branch_name , bf.user_name, fu.name, bf.loan_exp, bf.illegal_score, bf.remarks, bf.id
        from man_grade bf,Branch b,f_user fu  where 1=1 and b.branch_code=bf.org_no and fu.user_name = bf.user_name %s order by kyear desc,id
        """%(filterstr)

        print sql
        row = self.engine.execute(sql, vlist).fetchall()
        needtrans = {}
        return self.translate(row, needtrans)

    def make_eq_filterstr(self):
        filterstr = ""
        vlist = []
        for k, v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org_no':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr + "and bf.org_no in(%s) "%(vvv)
                elif k == 'user_name':
                    filterstr = filterstr + "and bf.user_name in(%s) "%v
                else:
                    filterstr = filterstr + "and %s=?"%k
                    vlist.append(v)
        
        filterstr = "%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'bf.user_name','bf.org_no',None))
       
        return filterstr, vlist
    def column_header(self):
        return ["所属年份","机构号","机构名称","员工号","员工名称","信贷工作经验（年）","违规积分","备注","操作"]

    @property
    def page_size(self):
        return 10

