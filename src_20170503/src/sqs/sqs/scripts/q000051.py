# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
贷款归属关系新增
"""

class Query(ObjectQuery):

    def prepare_object(self):
	if( 'e_p_THIRD_ORG_CODE' in self.args):
	    self.args.pop('e_p_THIRD_ORG_CODE')
        self.filterlist = ['THIRD_ORG_CODE','ACCOUNT_NAME','ACCOUNT_NO']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""SELECT A.THIRD_ORG_CODE JGBH,A.ACCOUNT_NAME HM,A.CUST_SEQ KHNM,TRIM(A.ACCOUNT_NO) ZH,TRIM(A.DEBIT_NO) ZHXH,A.CCY BZ,A.BALANCE*0.01 RQYE FROM M_ACCOUNT A  WHERE A.BALANCE!=0 and not exists (select '1' from t_zjc_gsgx_dk b where a.ACCOUNT_NO=b.dxbh and a.DEBIT_NO=b.dxxh ) and substr(subj_code,1,4) in ('1301','1302','1303','1304','1305','1306') %s order by ZH
            """%(filterstr)

        row = self.engine.execute(sql,vlist).fetchall()
        needtrans ={}
        return self.translate(row,needtrans)

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k[4: ] in self.filterlist:
                filterstr = filterstr+" and %s = ?"%k[4: ]
                vlist.append(v)
        return filterstr,vlist
    def column_header(self):
        return ["机构号","户名","客户内码","账号","账号序号","币种","日切余额","操作"]

    @property
    def page_size(self):
        return 10
