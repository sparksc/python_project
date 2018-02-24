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
客户经理管理核销贷款明细查询
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['CUST_NO','MANAGER_NO','ORG_NO','ACCOUNT_NO']
        filterstr,vlist = self.make_eq_filterstr()
        sql =u"""
        SELECT C.ORG_NO,O.ORG0_NAME,C.MANAGER_NO,M.SALE_NAME ,A.AFAACONO,D.ACCOUNT_NO,F.CST_NO,D.CST_ID,D.CST_NAME,C.NOTE,NVL(I.TEL_CORE,''),A.AFBJDATE,F.OUT_BALANCE/100.00 OUT_BALANCE
         FROM F_BALANCE F JOIN D_LOAN_ACCOUNT D ON F.ACCOUNT_ID=D.ID AND F.DATE_ID=(SELECT MAX(DATE_ID) FROM F_BALANCE_CHECK)
         JOIN D_SALE_MANAGE_RELA M ON F.MANAGE_ID=M.MANAGE_ID
         JOIN D_ORG O ON F.ORG_ID=O.ID
         JOIN D_CUST_INFO I ON I.CUST_NO=F.CST_NO
         JOIN CUST_HOOK C ON F.CST_NO=C.CUST_IN_NO AND C.TYP='贷款' AND C.ORG_NO=O.ORG0_CODE
         LEFT JOIN (SELECT DISTINCT AFAACONO,AFAAAC15,AFBJDATE FROM  F_CORE_BLFMCNAF) A ON A.AFAAAC15=D.ACCOUNT_NO
         WHERE  F.OUT_BALANCE>0 AND F.ACCT_TYPE='4'  %s 
         ORDER BY C.ORG_NO,C.MANAGER_NO,F.OUT_BALANCE
         WITH UR
        """%(filterstr)
        print sql
        print vlist
        row = self.engine.execute(sql,vlist).fetchall()
        row = list(row)
        for i in range(0,len(row)):
            row[i] = list(row[i])
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'ORG_NO':
                    vvv = self.dealfilterlist(v)
                    if self.top_branch_no not in vvv:
                        filterstr = filterstr +" and c.org_no in( %s ) "%(vvv)
                elif k == 'CUST_NO':
                    filterstr = filterstr + " and D.CST_ID = ?"
                    vlist.append(v)
                elif k == 'ACCOUNT_NO':
                    filterstr = filterstr + " and D.ACCOUNT_NO = ?"
                    vlist.append(v)
                elif k == 'MANAGER_NO':
                    filterstr = filterstr + " and c.manager_no = ? "
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],'c.manager_no','c.org_no', None))
        return filterstr,vlist
    def column_header(self):
        return ["机构号","机构名","员工号","员工名","贷款合同号",'贷款账号','客户内码','客户号',"客户名","地址信息","联系方式","核销日期",'核销余额']

    def trans_dec(self,num):
        tmp = Decimal(num).quantize(Decimal("0.00"))
        xxx = '{:,}'.format(tmp)
        return xxx
    @property
    def page_size(self):
        return 15
