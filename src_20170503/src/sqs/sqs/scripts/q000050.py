# -*- coding:utf-8 -*-

from objectquery import ObjectQuery
"""
存款归属关系新增
"""

class Query(ObjectQuery):

    def prepare_object(self):
	self.args.pop('e_p_OPEN_DATE')
        self.filterlist = ['OPEN_DATE','THIRD_ORG_CODE','ACCOUNT_NO','ACCOUNT_NAME','CARD_NO']
        filterstr,vlist = self.make_eq_filterstr()
        sql ="""
SELECT to_char(to_date(A.OPEN_DATE ,'YYYY-MM-DD'),'YYYY-MM-DD') DRRQ,trim(A.CARD_NO) KH,TRIM(A.ACCOUNT_NO) ZH,A.ACCOUNT_SBSQ ZHXH,A.ACCOUNT_NAME HM,A.THIRD_ORG_CODE JGBH,A.CUST_SEQ KHNM, A.CCY BZ,A.BALANCE*0.01 RQYE FROM M_ACCOUNT A  WHERE A.BALANCE!=0 and not exists (select '1' from t_zjc_gsgx_ck b where a.ACCOUNT_NO=b.dxbh and a.ACCOUNT_SBSQ=b.dxxh ) and substr(subj_code,1,4) in ('2001','2002','2003','2004','2005','2006','2007','2011','2014','2017') %s order by DRRQ desc,ZH
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
        return ["开户日期","卡号","账号","账号序号","客户姓名","机构编号","客户号","币种","日切余额","操作"]

    @property
    def page_size(self):
        return 10
