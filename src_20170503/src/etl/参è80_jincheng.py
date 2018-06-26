# -*- coding:utf-8 -*-
#!/bin/python  
import multiprocessing

from etl.star.logger import *
from etl.star.util import call_refresh_produce
from etl.performance.measure import *
from etl.performance.largeloss import *
from etl.performance.phonemoveaccount import *
from etl.performance.datainstitutions import Datainstitutions
from etl.performance.staffbasicsalary import Staffbasicsalary
from etl.performance.loanexecutive import Loanexecutive
from etl.performance.loanindexes import Loanindexes
from etl.performance.nonmarketstaff import Nonmarketstaff
from etl.performance.networkdeposit import Networkdeposit
from etl.performance.stafftrade import Stafftrade
from etl.performance.stafftradeperormance import Stafftradeperormance
from etl.performance.managerdeposit import Managerdeposit
from etl.performance.performancesummary import Performancesummary
from etl.performance.organizationindexes import Organizationindexes



def writer_proc(q,etldate):      
    try:         
	#call_refresh_produce()
        print "机构数据汇总"
        Datainstitutions(etldate).run()#机构数据汇总
        print "员工基本薪酬"
        Staffbasicsalary(etldate).run()#员工基本薪酬    
        print "贷款管户（增户管户 历史增户管户）"
        Loanexecutive(etldate).run()#贷款管户（增户管户 历史增户管户）  
        print "客户经理日均存款与计价"
        Managerdeposit(etldate).run()#客户经理日均存款与计价
        print "贷款指标计价"
        Loanindexes(etldate).run()#贷款指标计价
        q.put((1)) 
    except:         
	q.put((2))
	print "error"
        pass   

def reader_proc(q,etldate):      
    try:         
       	a=q.get(True)
	if a==1 :
		print a
	else:
		raise Exception("有问题")
	print "非营销人员绩效薪酬"
	Nonmarketstaff(etldate).run()#非营销人员绩效薪酬
        print "网点存款绩效薪酬"
        Networkdeposit(etldate).run()#网点存款绩效薪酬
        print "柜员业务量（复核柜员，操作柜员）"
        Stafftrade(etldate).run()#柜员业务量（复核柜员，操作柜员）
    except:         
	print "reader error"
        pass

if __name__ == "__main__":
	arglen=len(sys.argv)
        if arglen  == 2:
		q = multiprocessing.Queue()
		writer = multiprocessing.Process(target=writer_proc, args=(q,sys.argv[1]))  
		writer.start()   
		reader = multiprocessing.Process(target=reader_proc, args=(q,sys.argv[1]))
		reader.start()  

		reader.join()  
		writer.join()
        else :
                print "please input python %s  YYYYMMDD"%(sys.argv[0])
