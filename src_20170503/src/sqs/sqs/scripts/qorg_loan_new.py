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
"""

class Query(ObjectQuery):
    def group_by(self):
        return [0],(4,5,6,7,8,9,10,11,12,15,16,17,18)

    def prepare_object(self):
        self.etldate=""
        self.filterlist = ['DATE_ID','org']
        filterstr,vlist = self.make_eq_filterstr()
        day_sql="""
        select d.DETAIL_VALUE from T_PARA_TYPE t
        join T_PARA_HEADER h on h.PARA_TYPE_ID=t.ID
        join T_PARA_DETAIL d on d.PARA_HEADER_ID=h.ID
        where t.TYPE_NAME='管贷旬均天数选择' and h.HEADER_NAME in ('管贷旬均指标参数1(日)',          '管贷旬均指标参数2(日)','管贷旬均指标参数3(日)') order by int(d.DETAIL_VALUE)
        """
        day_row=self.engine.execute(day_sql).fetchall()
        #day_row=self.engine.fetchall()
        if len(day_row)==3:
            day_row1=str(day_row[0][0]).zfill(2)
            day_row2=str(day_row[1][0]).zfill(2)
            day_row3=str(day_row[2][0]).zfill(2)
            print day_row1,day_row2,day_row3
        else:
            raise Exception(u"旬均天数不对,请检查")

        month_sql='''
        select left(L_monthend_ID,6),left(id,6) from d_date where %s
        '''%(self.etldate)
        month=self.engine.execute(month_sql).fetchall()
        print month_sql
        last_month=month[0][0]
        this_month=month[0][1]
        print last_month,this_month
        sql = """
        (select b.parent_name,r.date_id,r.org_code,r.org_name,
        sum(nvl(PRI_NUM,0)) ,
        sum(nvl(PUB_NUM,0)) ,
        sum(nvl(PRI_LAST_AVG,0))/100.00 as PRI_LAST_AVG ,
        SUM(nvl(PUB_LAST_AVG,0))/100.00  as PUB_LAST_AVG,
        SUM(NVL(pri_add_num,0)) as pri_add_num,
        SUM(NVL(pub_add_num,0)) as pub_add_num,
        sum(nvl(pri_add_bal,0))/100.00 as pri_add_bal,
        sum(nvl(pub_add_bal,0))/100.00 as pub_add_bal,
        sum(nvl(PRI_THIS_MON_AVG,0)-nvl(PRI_LAST_AVG,0))/100.00 as PRI_add_MON_AVG,
        sum(nvl(PUB_THIS_MON_AVG,0)-nvl(PUB_LAST_AVG,0))/100.00 as PUB_add_MON_AVG,
        (sum(nvl(min_crd_num ,0)) / (case when sum(nvl(min_num,0))=0 then 1.00 else (sum(nvl(min_num,0))*1.00) end))*100 as min_crd_num,
        (sum(nvl(min_crd_bal,0)) / (case when sum(nvl(min_bal,0))=0 then 1.00 else (sum(nvl(min_bal,0))*1.00) end ))*100 as min_crd_bal,
        sum(nvl(bad_num,0)) as bad_num,
        sum(nvl(bad_bal,0))/100.00 as bad_bal ,
        sum(nvl(two_thsi_num,0)-nvl(two_last_num,0)) as two_thsi_num
        from report_manager_loan as r
        join (SELECT B.BRANCH_CODE CHILD_CODE,B.BRANCH_NAME,A.BRANCH_CODE PARENT_CODE,A.BRANCH_NAME PARENT_NAME,A.BRANCH_LEVEL FROM BRANCH A
        JOIN BRANCH B ON A.ROLE_ID=B.PARENT_ID WHERE A.BRANCH_LEVEL='支行')B ON R.ORG_CODE=B.CHILD_CODE
        WHERE 1=1 %s 
        group by r.date_id,r.org_code,r.org_name,b.parent_name order by r.org_code)
        """%(filterstr)
        row = self.engine.execute(sql.encode('utf-8'),vlist).fetchall()
        print sql
        needtrans ={}
        rowlist=[]
        for i in row:
            t=list(i[0:4])
            for j in i[4:]:
                if j is None:j=0
                j=self.amount_trans_dec(j)
                t.append(j)
            rowlist.append(t)    
        return self.translate(rowlist,needtrans)    

    def make_eq_filterstr(self):
        filterstr =""
        vlist = []
        for k,v in self.args.items():
            print k,v
            #if k == 'login_branch_no':
            #    bb = self.deal_branch_query_auth(v)
            #    if bb != False :
            #        filterstr = filterstr+" and ORG_CODE in ( %s )"%bb

            if v and k in self.filterlist:
                if k == 'org':
                    vvv = self.dealfilterlist(v)
                    filterstr = filterstr +" and r.ORG_CODE in ( %s ) "%(vvv)
                elif k=='DATE_ID':
                    filterstr = filterstr +" and r.DATE_ID =  %s  "%(v)
                    self.etldate="ID=%s"%(v)
                else: 
                    filterstr = filterstr+" and %s = ?"%k
                    vlist.append(v)
        filterstr ="%s and %s"%(filterstr,self.get_auth_sql(config.DATATYPE['query'],None,'ORG_CODE', None))
        return filterstr,vlist

    def column_header(self):
        return ["支行汇总","统计日期","机构编号","机构名称","对私管贷(现)","对公管贷(现)","对私存量日均管贷余额","对公日均存量管贷余额","对私扩面(户)","对公扩面(户)","对私扩面(余额)","对公扩面(余额)","对私贷款日均增量","对公贷款日均增量","小额信用贷款户数占比(%)","小额信用贷款余额占比(%)","资产不良贷款户数","资产不良贷款余额","丰收两卡合同新增户数"]

    @property
    def page_size(self):
        return 15
