# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from utils import config
"""
客户层面转移
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ["note","ORG_NO", "manager_no", "cust_no","typ","status"]
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
                select a.id,branch_code,branch_name,user_name,name,a.cust_no,d.cust_name,percentage,a.note
                from cust_hook a  
                join branch o on o.branch_code=a.org_no
                join f_user s on s.user_name=a.manager_no
                left join D_CUST_INFO d on d.cust_no=a.cust_in_no
                where 1=1 %s
                order by id desc
            """%(filterstr)
        print sql
        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():

            if v and k in self.filterlist:
                if k == 'ORG_NO':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and o.branch_code in ( %s ) "%(vvv)
                elif k == 'note':
                    print v
                    filterstr = filterstr + " and a.note like " + " '%'||"+"?"+"||'%' "
                    vlist.append(v)
                elif k == 'cust_no':
                    filterstr = filterstr + " and a.cust_no = ? " 
                    vlist.append(v)
                elif k == 'manager_no':
                    filterstr = filterstr +" and a.manager_no = ? "
                    vlist.append(v)
                else:
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['transfer'],'a.manager_no','a.org_no', None))
        return filterstr,vlist
    def column_header(self):
        for k,v in self.args.items():
            if k=='typ' and v=='机具':
                return ["序号","机构号","机构名","员工号","员工名","机具编号","客户名","占比(%)","地址信息","操作"]
            elif k=='typ' and v=='POS':    
                return ["序号","机构号","机构名","员工号","员工名","商户号","客户名","占比(%)","地址信息","操作"]
        return ["序号","机构号","机构名","员工号","员工名","客户号","客户名","占比(%)","地址信息","操作"]

    @property
    def page_size(self):
        return 15
