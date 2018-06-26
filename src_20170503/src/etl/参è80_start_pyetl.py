# -*- coding:utf-8 -*-
#!/bin/python  
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

def start_pyetl1(etldate):
	etldate = int(etldate)
	info("start python etl")
	#measure_clacs(etldate)#预约处理程序
	info("finish measure ")
	large_loss(etldate)#大额变动处理程序
	info("finish largeloss")
	#phone_move_account_rate(etldate)#手机动户率
	#info('finish phone_move_account_rate')
	info("finish python etl")


def start_pyetl(etldate):
	etldate = int(etldate)
	info("refresh MQT table")
	"""添加刷新物化视图的语句"""
	print "刷新物化视图"
	call_refresh_produce()
	info("finish MQT table")
	info("start python etl")
	info("start datainstitutions")	
	print "机构数据汇总"
	Datainstitutions(etldate).run()#机构数据汇总
	info("finish datainstitutions")
	info('start  staffbasicsalary')
	print "员工基本薪酬"
	Staffbasicsalary(etldate).run()#员工基本薪酬	
	info('finish staffbasicsalary')
	info('start loanexecutive')
	print "贷款管户（增户管户 历史增户管户）"
	Loanexecutive(etldate).run()#贷款管户（增户管户 历史增户管户）	
	info('finish loanexecutive')
	info("start managerdepost")
	print "客户经理日均存款与计价"
	Managerdeposit(etldate).run()#客户经理日均存款与计价
	info('finish managerdeposit')
	info('start loanindexes')
	print "贷款指标计价"
	Loanindexes(etldate).run()#贷款指标计价
	info('finish loanindexes')
	info('start nonmarketstaff')
	print "非营销人员"
	Nonmarketstaff(etldate).run()#非营销人员绩效薪酬
	info('finish nonmarketstaff')
	info('start networkdeposit')
	print "网点存款绩效薪酬"
	Networkdeposit(etldate).run()#网点存款绩效薪酬
	info('finish networkdeposit')	
	info('start stafftrade')
	print "柜员业务量（复核柜员，操作柜员）"
	Stafftrade(etldate).run()#柜员业务量（复核柜员，操作柜员）
	info('finish stafftrade')
	info('start stafftradeperormance')
	print "柜员业务量绩效"
	Stafftradeperormance(etldate).run()#柜员业务量绩效
	info('finish stafftradeperpormance')
	info('start performancesummary')
	print "薪酬汇总"
	Performancesummary(etldate).run()#薪酬汇总
	info('finish performancesummary')	

	info('start phone_move_account_rate')
	#print "手机动户率"
	#phone_move_account_rate(etldate)#手机动户率
	info('finish phone_move_account_rate')
	info('start organizationindexes')
	print "机构指标"
	Organizationindexes(etldate).run()#机构指标
	info('finish organizationindexes')	
	info('start measure')	
	print "预约处理程序"
	measure_clacs(etldate)#预约处理程序
	info("finish measure ")
	info("start largeloss")
	print "大额变动处理程序"
	large_loss(etldate)#大额变动处理程序
	info("finish largeloss")
	info("finish python etl")
def start_jgzb(etldate):
	#phone_move_account_rate(etldate)#手机动户率
	info('finish phone_move_account_rate')
	


if __name__=='__main__':	
	arglen=len(sys.argv)
	if arglen  == 2:
		start_pyetl(sys.argv[1])
	else :
		print "please input python %s  YYYYMMDD"%(sys.argv[0])
