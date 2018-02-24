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
客户经理存款
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['FROM_DATE_ID', 'END_DATE_ID', 'org']
        filterstr,filterstr1, filterstr2, vlist = self.make_eq_filterstr()
        sql ="""
        select  f.org_code,org.BRANCH_NAME,
        qcye / 100.00,          --期初余额
        qmye/ 100.00,           --期末余额
        sum(case when substr(f.subj_no, 1,6 ) in ('132102','132101','132109', '132121','132199','132103','132122') then -1 else 1 end * f.credit_bal)/ 100.00 / (days(to_date(f2.date_id,'yyyymmdd'))-days(to_date(f1.DATE_ID,'yyyymmdd')) +1) --日均
        from F_BALANCE_SUMMARY f
        join d_date d on d.id = f.date_id   
        left join (select  date_id, org_code, sum(case when substr(ff.subj_no, 1,6 ) in ('132102','132101','132109', '132121','132199','132103','132122') then -1 else 1 end * credit_bal) as qcye from F_BALANCE_SUMMARY ff  where ( left(ff.subj_no,4) in ('2001','2002','2006','2011','2014','2012','2013','2003','2004') or left(ff.subj_no,6) in ('200501','200502','231402','132102''231401','231409','132101','132109','231421','132121','231499','132199','231403','132103','231422','132122','201712','201713','201714','201702','201703','201704') or ff.subj_no in ('20070101','20070201','20070301','20170198','20171198') )  %s group by ff.date_id, ff.org_code) f1 on f1.org_code = f.org_code
        left join (select date_id, org_code, sum(case when substr(ff.subj_no, 1,6 ) in ('132102','132101','132109', '132121','132199','132103','132122') then -1 else 1 end * credit_bal) as qmye from F_BALANCE_SUMMARY ff  where ( left(ff.subj_no,4) in ('2001','2002','2006','2011','2014','2012','2013','2003','2004') or left(ff.subj_no,6) in ('200501','200502','231402','132102''231401','231409','132101','132109','231421','132121','231499','132199','231403','132103','231422','132122','201712','201713','201714','201702','201703','201704') or ff.subj_no in ('20070101','20070201','20070301','20170198','20171198') )  %s group by ff.date_id, ff.org_code) f2 on f2.org_code = f.org_code
        join BRANCH org on org.BRANCH_CODE = f.ORG_CODE
        where ( left(f.subj_no,4) in ('2001','2002','2006','2011','2014','2012','2013','2003','2004') or left(f.subj_no,6) in ('200501','200502','231402','132102''231401','231409','132101','132109','231421','132121','231499','132199','231403','132103','231422','132122','201712','201713','201714','201702','201703','201704') or f.subj_no in ('20070101','20070201','20070301','20170198','20171198') ) %s
        group by  f.org_code, org.BRANCH_NAME, qcye, qmye, f1.date_id, f2.date_id
        """%(filterstr1, filterstr2, filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print "0000000000000000000000000", sql
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i[0:2])
            for j in i[2:]:
                if j is None:j=0
                j=self.amount_trans_dec(j)
                t.append(j)
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)    

    def make_eq_filterstr(self):
        filterstr1 =""
        filterstr2 =""
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and f.ORG_CODE in ( %s ) "%(vvv)
                elif k == 'FROM_DATE_ID':
                    filterstr1 = filterstr1 +" and ff.date_id = %s "%v
                    filterstr = filterstr +" and f.date_id >= %s "%v
                elif k == 'END_DATE_ID':
                    filterstr2 = filterstr2 +" and ff.date_id = %s "%v
                    filterstr = filterstr +" and f.date_id <= %s "%v
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'f.ORG_CODE', None))
        return filterstr,filterstr1, filterstr2,vlist

    def column_header(self):
        return ["机构编号","机构名称", "期初存款余额","期末存款余额","存款日均"]

    @property
    def page_size(self):
        return 15
