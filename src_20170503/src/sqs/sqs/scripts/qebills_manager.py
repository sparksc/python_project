# -*- coding:utf-8 -*-

from decimal import Decimal
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from utils import config
"""
国际业务归属自动认定
"""

class Query(ObjectQuery):
    def prepare_object(self):
        self.filterlist = ['SALE_CODE', 'org']
        self.date_id=""
        filterstr,vlist = self.make_eq_filterstr()
        sql = """
            select b.BRANCH_CODE, b.BRANCH_NAME, u.USER_NAME, u.NAME, em.MANAGER_NO from F_USER u 
            left join USER_BRANCH ub ON u.ROLE_ID = ub.USER_ID
            left join BRANCH b ON b.ROLE_ID = ub.BRANCH_ID
            left join EBILLS_MANAGER em ON em.F_USER_NO = u.USER_NAME
            where  u.WORK_STATUS = '在职' and u.USER_NAME like '966%%' %s order by b.BRANCH_CODE, u.USER_NAME
            """%(filterstr)

        print sql
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()

        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i)
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)

    def make_eq_filterstr(self):
        filterstr = ""
        vlist = []
        for k,v in self.args.items():
            print k,v
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +"and  b.BRANCH_CODE in ( %s )  "%(vvv)
                elif k == 'SALE_CODE':
                    filterstr = filterstr +" and u.USER_NAME = '%s' "%(v)
                else: 
                    pass
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],"u.USER_NAME",'b.BRANCH_CODE', None))
        return filterstr, vlist

    def column_header(self):
        return ["机构编号","机构名称","员工号","员工姓名","国业系统客户经理编号", "操作"]

    @property
    def page_size(self):
        return 15
