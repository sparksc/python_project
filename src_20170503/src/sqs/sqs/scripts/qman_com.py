# -*- coding:utf-8 -*-

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from objectquery import ObjectQuery
from qcom_dep import Query as depQuery
from .. import Report as sqsreport
"""
客户经理绩效佣金报表
"""

class Query(ObjectQuery):
 
    def prepare_object(self):
        self.filterlist = ['BRANCH_CODE','SALE_CODE','S_DATE']
        print self.code, self.args
        #print self.conf
        targs=self.args
        targs['tdate']=0
        if 'S_DATE' in self.args:
            targs['tdate']=self.args['S_DATE'][0:6]
        sqs = sqsreport('com_dep',targs,self.conf)
        deprr = sqs.get_list_data()
        print '*****************'
        print len(deprr)
        if 'S_DATE' in self.args:
            targs['tdate']=self.args['S_DATE']
        sqs = sqsreport('com_loan',targs,self.conf)
        loanrr = sqs.get_list_data()
        print len(loanrr)

        sqs = sqsreport('com_mid',targs,self.conf)
        midrr = sqs.get_list_data()
        print len(midrr)
        print '##########com_mid oooooooooook!#########'

        sqs = sqsreport('com_ebank',targs,self.conf)
        ebankrr = sqs.get_list_data()
        print len(ebankrr)
        sqs = sqsreport('com_int',targs,self.conf)
        intrr = sqs.get_list_data()
        print len(intrr)
        
        sqs = sqsreport('man_per_input',targs,self.conf)
        addrr = sqs.get_list_data()
        print len(addrr)
        rr=[]
        while len(deprr)+len(loanrr)+len(ebankrr):
            jgh=''
            ygh=''
            rt = []
            rs=[]
            jgh,ygh,rt=self.find_same1(jgh,ygh,deprr,rt)
            jgh,ygh,rt=self.find_same1(jgh,ygh,loanrr,rt)
            jgh,ygh,rt=self.find_same1(jgh,ygh,midrr,rt)
            jgh,ygh,rt=self.find_same1(jgh,ygh,ebankrr,rt)
            rt.append(0)
            jgh,ygh,rt=self.find_same1(jgh,ygh,addrr,rt)
            rt.append(round(rt[6],2))
            print rt    
            rr.append(rt) 
        needtrans ={}
        return self.translate(rr,needtrans)
   
    def find_same(self,jgh,ygh,rowlist,rt):
        for x in rowlist:
            if jgh=='' and ygh=='':
                jgh=x[0]
                ygh=x[2]
                rt.insert(0,x[3])
                rt.insert(0,x[2])
                rt.insert(0,x[1])
                rt.insert(0,x[0])
            if jgh==x[0] and ygh==x[2]:
                rt.append(x[4])
                rowlist.pop(rowlist.index(x))
                return jgh,ygh,rt
        rt.append(0)        
        return jgh,ygh,rt        

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
        return ["统计月份","员工号","员工名称","机构号","机构名称","存款业务业绩效酬","贷款业务业绩效酬","中间业务业绩效酬","电子银行业务绩效效酬","国际业务业绩效酬","信用卡业务业绩效酬","附加效酬","总效酬"]

    @property
    def page_size(self):
        return 15
