# -*- coding:utf-8 -*-
from ..server.javax import java


def test_toHashMap():
	adict={"name":"jasonchiu",
        "age":"26",
        "contact":{"fa":"ktchiu",
                        "othen":{
                                "age":"56",
                                "m":{
                                        "hi":"A"
                                },
                                "wei":[{
                                        'x':1,
                                        'w':2
                                },{'c':3}],
                        }},
        "ma":{"name":"yzchao"}}
        print java.toHashMap(adict)

def test_load_class():
        print java.load_class("java.util.HashMap")
        print java.load_class("java.util.ArrayList")
        print java.load_class("java.util.ArrayList")

def test_load_extjar_class():
        print java.load_class("com.yinsho.ExcelUtils")
        
def test_create_map():
        dmap= java.HashMap()
        # no matching overloads found for this line:
        dmap.put('name','Linux')
        dmap.put('age','22')

        dep1= java.HashMap()
        dep1.put('name',u'张三')
        dep1.put('age',22)
        dep2= java.HashMap()
        dep2.put('name','john')
        dep2.put('age',12)
        dep3= java.HashMap()
        dep3.put('name','maky')
        dep3.put('age',32)

        jlist= java.ArrayList()
        jlist.add(dep1)
        jlist.add(dep2)
        jlist.add(dep3)

        beanParams= java.HashMap()
        beanParams.put('departments',jlist)
        beanParams.put('department',dmap)
	return beanParams

def test_dict2HashMap():
	mdict = {"department":{"age":22, "name":"Linux"}, "departments":[{"age":22, "name":u"pick"}, {"age":12, "name":"john"}, {"age":32, "name":"maky"}]}
        datamap = java.toHashMap(mdict)
	print datamap.toString()
	print mdict
	return datamap

def test_transformat():
        srcFilePath = "../../resource/xlst/sample.xls"
        destFilePath = "/tmp/sample_out.xls"
	beanParams = test_dict2HashMap()
	print beanParams
	java.ExcelUtils().transformat(srcFilePath, beanParams, destFilePath)

"""
if __name__=='__main__':
	test_load_class()
        test_load_extjar_class()
	test_create_map()
	test_dict2HashMap()
	test_transformat()
"""









 
