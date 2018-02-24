# -*- coding: utf-8 -*-

def singleton(cls, *args, **kw):  
	instances = {}
	#print args,kw
	def _singleton():  
		if cls not in instances:
			instances[cls] = cls(*args, **kw)
		return instances[cls]
	return _singleton
	
@singleton
class MyClass(object):
	a = 1
	def __init__(self):
		self.x = 1
	
	def tt(self):
		print "tt"
one = MyClass()  
two = MyClass()   