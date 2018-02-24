# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from .. import Report as sqsreport
"""
客户经理贷款绩效得分报表
"""

class Query(ObjectQuery):
 
    def prepare_object(self):
        self.filterlist = ['BRANCH_CODE','SALE_CODE','S_DATE']
        sqs = sqsreport('man_dep_sco',self.args,self.conf)
        deprr = sqs.get_list_data()
        print '####################loan start################'
        sqs = sqsreport('man_loan_sco',self.args,self.conf)
        loanrr = sqs.get_list_data()
        print '####################ebk start################'
        sqs = sqsreport('man_ebank_sco',self.args,self.conf)
        ebkrr = sqs.get_list_data()
        print '####################ebk ok!##################'
        sqs = sqsreport('man_sco_input',self.args,self.conf)
        addrr = sqs.get_list_data()
        rr=[]
        while len(deprr)+len(loanrr):
            jgh=''
            ygh=''
            rt = []
            rs=[]
            jgh,ygh,rt=self.find_same1(jgh,ygh,deprr,rt)
            jgh,ygh,rt=self.find_same1(jgh,ygh,loanrr,rt)
            jgh,ygh,rt=self.find_same1(jgh,ygh,ebkrr,rt)
            jgh,ygh,rt=self.find_same1(jgh,ygh,addrr,rt)
            rt.append(round(rt[6]+rt[7]+rt[8]+rt[9],2))
            rr.append(rt) 
        needtrans ={}
        return self.translate(rr,needtrans)
    def find_same1(self,jgh,ygh,rowlist,rt):
        for x in rowlist:
            if jgh=='' and ygh=='':
                jgh=x[2]
                ygh=x[4]
                rt.insert(0,x[5])
                rt.insert(0,x[4])
                rt.insert(0,x[3])
                rt.insert(0,x[2])
                rt.insert(0,x[1])
                rt.insert(0,x[0])
            if jgh==x[2] and ygh==x[4]:
                rt.append(x[-1])
                rowlist.pop(rowlist.index(x))
                return jgh,ygh,rt
        rt.append(0)        
        return jgh,ygh,rt        

    def make_eq_filterstr(self):
        filterstr = ""
        filterstr1 = ""
        filterstr2 = ""
        vlist = []
        for k,v in self.args.items():
            if v and k in self.filterlist:
                if k=='SALE_CODE':
                    filterstr = filterstr+" and %s = ? "%'sm.SALE_CODE'
                    filterstr1 = filterstr1+" and %s = ? "%'MANAGER_CODE'
                    filterstr2 = filterstr2+" and %s = ? "%v
                    vlist.append(v)
                if k=='BRANCH_CODE':
                    filterstr = filterstr+" and %s = ? "%'sm.THIRD_BRANCH_CODE'
                    filterstr1 = filterstr1+" and %s = ? "%'THIRD_ORG_CODE'
                    filterstr2 = filterstr2+" and %s = ? "%'l.STAT_BRANCH_CODE'
                    vlist.append(v)
                if k=='S_DATE':
                    self.s_date=int(v)
                    self.ly_date=(int(v[0:4])-1)*10000+1231
                    self.tm_date=(int(v[0:6]))*100+01
        return filterstr,filterstr1,filterstr2,vlist

    def column_header(self):
        return ["统计年份","统计月份","机构号","机构名称","员工号","员工名称","存款业务得分","贷款业务得分","电子银行业务得分","附加分","绩效总得分"]

    @property
    def page_size(self):
        return 15
