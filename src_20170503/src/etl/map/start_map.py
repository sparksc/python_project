# -*- coding:utf-8 -*-
#!/bin/python  
from etl.base.logger import *
from etl.base.util import call_refresh_produce

def start_pyetl(etldate):
	etldate = int(etldate)
	info("refresh MQT table")
	"""添加刷新物化视图的语句"""
	print "刷新物化视图"
	call_refresh_produce()
	info("finish MQT table")
	info("start python etl")
	
	info("finish python etl")

if __name__=='__main__':	
	arglen=len(sys.argv)
	if arglen  == 2:
		start_pyetl(sys.argv[1])
	else :
		print "please input python %s  YYYYMMDD"%(sys.argv[0])
