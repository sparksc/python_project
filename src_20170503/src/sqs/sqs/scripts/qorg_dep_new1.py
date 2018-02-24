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
机构存款指标

对私存款：科目号前4位为('2003','2004')+科目号前6位为'200502'+('231402'-'132102')
对公存款：科目号前4位为('2001','2002','2006','2011','2014','2012','2013')+'20070101'+'20070201'+'20070301'+'20170198'+'20171198'+科目号前6位为'200501'+('231401'+'231409'-'132101'-'132109'+'231421'-'132121'+'231499'-'132199'
+'231403'-'132103'+'231422'-'132122')+'201712'+'201713'+'201714'+'201702'+'201703'+'201704'
"""

class Query(ObjectQuery):

    def prepare_object(self):
        self.filterlist = ['DATE_ID','org']
        filterstr,date_id, vlist = self.make_eq_filterstr()
        sql ="""
        select a.date_id, a.org_code, a.branch_name, nvl(a.clye, 0.0) / 100.00, nvl(a.xlye, 0.0) / 100.00, nvl(a.yjye1, 0.0) / 100.00, nvl(b.clye, 0.0) / 100.00, nvl(b.xlye, 0.0) / 100.00, nvl(b.yjye1, 0.0) / 100.00, nvl(c.clye, 0.0) / 100.00, nvl(c.xlye, 0.0) / 100.00, nvl(c.yjye1, 0.0) / 100.00 from
        (
         --对私
         select f.date_id, f.org_code,org.BRANCH_NAME, clye, sum(case when substr(f.subj_no, 1,6 ) ='132102' then -1 else 1 end * CREDIT_BAL) as xlye, (yjye / d.beg_month_days) as yjye1
         from F_BALANCE_SUMMARY f
         join d_date d on d.id = f.date_id
         left join (select ff.date_id, dd.id as tj_date_id, org_code, sum( case when substr(ff.subj_no, 1,6 ) ='132102' then -1 else 1 end * credit_bal) as clye from F_BALANCE_SUMMARY ff 
                 join d_date dd  on ff.date_id = dd.l_yearend_id where (( left(ff.subj_no,4) in ('2003','2004') or left(ff.subj_no,6) in ('200502', '231402', '132102')) and ff.subj_no != '20040108' ) and dd.id = '%s' group by ff.date_id, dd.id, ff.org_code) f1 on f1.org_code = f.org_code and f1.tj_date_id = f.date_id
         left join (select org_code, sum( case when substr(ff.subj_no, 1,6 ) ='132102' then -1 else 1 end * credit_bal) as yjye from F_BALANCE_SUMMARY ff where (( left(ff.subj_no,4) in ('2003','2004')
                                 or left(ff.subj_no,6) in ('200502', '231402', '132102')) and ff.subj_no != '20040108' ) and ff.date_id >= (select dd.MONTHBEG_ID from d_date dd where dd.id = '%s') and ff.date_id <= '%s' group by  ff.org_code) f2 on f2.org_code = f.org_code
         join BRANCH org on org.BRANCH_CODE = f.ORG_CODE
         where (( left(f.subj_no,4) in ('2003','2004') or left(f.subj_no,6) in ('200502', '231402', '132102')) and f.subj_no != '20040108' ) 
         group by f.date_id, f.org_code, org.BRANCH_NAME, clye, yjye,d.beg_month_days       
        ) a
        left join
        (
         --对公存款
         select f.date_id, f.org_code,org.BRANCH_NAME, clye, sum(case when substr(f.subj_no, 1,6 ) in ('132101','132109', '132121','132199','132103','132122') then -1 else 1 end * CREDIT_BAL) as xlye, yjye / d.beg_month_days as yjye1
         from F_BALANCE_SUMMARY f                                                
         join d_date d on d.id = f.date_id                                       
         left join (select date_id, dd.id as tj_date_id, org_code, sum(case when substr(ff.subj_no, 1,6 ) in ('132101','132109', '132121','132199','132103','132122') then -1 else 1 end * credit_bal) as clye from F_BALANCE_SUMMARY ff 
                 join d_date dd on ff.date_id = dd.l_yearend_id where ( ff.subj_no != '20020104' and ( left(ff.subj_no,4) in ('2001','2002','2006','2011','2014','2012','2013') or left(ff.subj_no,6) in ('200501','231401','231409','132101','132109','231421','132121','231499','132199','231403','132103','231422','132122','201712','201713','201714','201702','201703','201704') or ff.subj_no in ('20070101','20070201','20070301','20170198','20171198') )) and dd.id = '%s' group by ff.date_id, dd.id, ff.org_code) f1 on f1.org_code = f.org_code and f1.tj_date_id = f.date_id
         left join (select org_code, sum(case when substr(ff.subj_no, 1,6 ) in ('132101','132109', '132121','132199','132103','132122') then -1 else 1 end * credit_bal) as yjye from F_BALANCE_SUMMARY ff where ( ff.subj_no != '20020104' and ( left(ff.subj_no,4) in ('2001','2002','2006','2011','2014','2012','2013')
                                 or left(ff.subj_no,6) in ('200501','231401','231409','132101','132109','231421','132121','231499','132199','231403','132103','231422','132122','201712','201713','201714','201702','201703','201704') or ff.subj_no in ('20070101','20070201','20070301','20170198','20171198') )) and ff.date_id >= (select dd.MONTHBEG_ID from d_date dd where dd.id = '%s') and ff.date_id <= '%s' group by ff.org_code) f2 on f2.org_code = f.org_code
         join BRANCH org on org.BRANCH_CODE = f.ORG_CODE

         where (( left(f.subj_no,4) in ('2001','2002','2006','2011','2014','2012','2013')
                         or left(f.subj_no,6) in ('200501','231401','231409','132101','132109','231421','132121','231499','132199','231403','132103','231422','132122','201712','201713','201714','201702','201703','201704') or f.subj_no in ('20070101','20070201','20070301','20170198','20171198') ))
         group by f.date_id, f.org_code, org.BRANCH_NAME, clye, yjye,d.beg_month_days                                                                               
        )b on a.date_id = b.date_id and a.org_code = b.org_code and a.branch_name = b.branch_name
        left join
        (
         --理财 
         select f.date_id, f.org_code,org.BRANCH_NAME, clye, sum(CREDIT_BAL) as xlye, yjye / d.beg_month_days as yjye1                                              
         from F_BALANCE_SUMMARY f
         join d_date d on d.id = f.date_id
         left join (select date_id, dd.id as tj_date_id, org_code, sum(credit_bal) as clye from F_BALANCE_SUMMARY ff 
                 join d_date dd on ff.date_id = dd.l_yearend_id where ff.subj_no in ('20020104','20040108') and dd.id = '%s' group by ff.date_id, dd.id, ff.org_code) f1 on f1.org_code = f.org_code and f1.tj_date_id = f.date_id
         left join (select org_code, sum(credit_bal) as yjye from F_BALANCE_SUMMARY ff where ff.subj_no in ('20020104','20040108') and ff.date_id >= (select dd.MONTHBEG_ID from d_date dd where dd.id = '%s') and ff.date_id <= '%s' group by ff.org_code) f2 on f2.org_code = f.org_code
         join BRANCH org on org.BRANCH_CODE = f.ORG_CODE                                                                                                 

         where f.subj_no in ('20020104','20040108')         
         group by f.date_id, f.org_code, org.BRANCH_NAME, clye, yjye,d.beg_month_days
        )c on b.date_id = c.date_id and b.org_code = c.org_code and b.branch_name = c.branch_name
        where 1=1 %s
            """%(date_id, date_id, date_id, date_id, date_id, date_id, date_id, date_id, date_id, filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print sql
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i[0:3])
            for j in i[3:]:
                if j is None:j=0
                j=self.amount_trans_dec(j)
                t.append(j)
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        date_id = ""
        vlist = []
        for k,v in self.args.items():
            print k,v
            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and a.ORG_CODE in ( %s ) "%(vvv)
                elif k == 'DATE_ID':
                    filterstr = filterstr +" and a.date_id = %s "%v
                    date_id = v
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'a.ORG_CODE', None))
        return filterstr,date_id, vlist

    def column_header(self):
        return ["统计日期","机构编号","机构名称","对私存量存款", "对私现量存款", "对私月日均", "对公存量存款", "对公现量存款", "对公月日均", "理财存量", "理财现量", "理财月日均"]

    @property
    def page_size(self):
        return 15
