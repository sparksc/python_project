#!/usr/bin/python
#-*- coding:utf-8 -*-
import socket
import urllib2
import urllib
import datetime
import time
from xml.etree import ElementTree
import xmlutil
import os
from .settings import DevConfig
from decimal import Decimal
def make_message(fieldList,head):

    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S');

    xw = xmlutil.xmlwrite('./fabs/static/'+'PMC010004_{0}_{1}.XML'.format(head['owner']['value'],now))
    root = xw.write_node_root()
    '''
    u'柜面渠道','TERM',\
                        u'一般贷款放款','120101',\
                        '120101',\
                        'true',\
                        account_owner['account_owner_name'],str(account_owner['account_owner_no'])
    '''
    xw.write_node_head(root,\
                        head['Channel']['name'],head['Channel']['value'],
                        head['Service']['name'],head['Service']['value'],
                        head['ServiceName'],
                        head['Tran'],
                        head['Final'],
                        head['owner']['name'],head['owner']['value']
                        )
    body = xw.write_node(root,'RequestBodyData', {'type':'Group'})
    #
    #print fieldList
    i = 1
    for item in fieldList:
        i = i + 1
        xw.write_node_field(body,item['name'],item['value'],item['type'],item['CDATA'])
    xw.save_xml()
    return root

def send(msg):
    #暂时写死,需要配置
    host = DevConfig.COREHOST#'192.168.10.141'
    port = DevConfig.COREPORT
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print host,port
    try:
        s.connect((host,port))
    except Exception as e:
        raise Exception('核心服务连接失败!')
    l = '%08d'%(len(msg),)
    s.send(l)
    print 'send:',msg
    s.send(msg)
    rl = s.recv(8)
    rl = int(rl)
    data=''
    while(rl):
        item =  s.recv(rl)
        rl = rl - len(item)
        data = data+item
    print len(data),':',data
    # 这里只是暂时的删除后面多余的12位,还需要测试错误情况
    return data[0:-12]
    #eof = chr(255)
    #print s.send(eof)


'''
放款
'''
def trans120000(cust,trans,app,lend,user_info,extra):
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},\
            'Service':{'name':u'一般贷款授信','value':'120000'},\
            'ServiceName':'CBS_CREDIT_OPEN',\
            'Tran':'120000',\
            'Final':'true',\
            'owner':{'name':user_info.name,'value':user_info.user_name}}
    fieldList=[]    
    fieldList.append({'name':u'交易码','value':'120000','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':user_info.user_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'客户编号','value':cust.get('no'),'type':1,'CDATA':True})
    fieldList.append({'name':u'合同编号','value':lend.get('no'),'type':1,'CDATA':True})
    fieldList.append({'name':u'币种','value':u'人民币','type':1,'CDATA':True})
    fieldList.append({'name':u'放款日期','value':lend.get('from_date'),'type':1,'CDATA':True})
    fieldList.append({'name':u'到期日期','value':lend.get('thur_date'),'type':1,'CDATA':True})
    fieldList.append({'name':u'合同金额','value':str(Decimal(trans.get('amount')).quantize(Decimal('0.00'))),'type':1,'CDATA':True})
    fieldList.append({'name':u'贷款产品','value':extra['product_name'],'type':1,'CDATA':True})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))
    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}
    lst = root.getiterator('Field')
    for item in lst:
        fieldDict.update({item.attrib['name']:item.text})
    return fieldDict

def lend_trans(cust,trans,app,lend,user_info,extra):
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},\
            'Service':{'name':u'一般贷款放款','value':'120101'},\
            'ServiceName':'CBS_TRAN_INPUT',\
            'Tran':'120101',\
            'Final':'true',\
            'owner':{'name':user_info.name,'value':user_info.user_name}}
    fieldList=[]
    fieldList.append({'name':u'交易码','value':'120101','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':user_info.user_name,'type':1,'CDATA':True})

    #客户信息
    fieldList.append({'name':u'客户编号','value':cust.get('no'),'type':1,'CDATA':True})
    fieldList.append({'name':u'户名','value':cust.get('name'),'type':1,'CDATA':True})
    #合同信息
    fieldList.append({'name':u'合同序号','value':'1','type':1,'CDATA':True})
    fieldList.append({'name':u'合同编号','value':lend.get('no'),'type':1,'CDATA':True})
    fieldList.append({'name':u'合同金额','value':str(Decimal(trans.get('amount')).quantize(Decimal('0.00'))),'type':1,'CDATA':True})
    fieldList.append({'name':u'放款金额','value':str(Decimal(trans.get('amount')).quantize(Decimal('0.00'))),'type':1,'CDATA':True})
    fieldList.append({'name':u'币种','value':u'人民币','type':1,'CDATA':True})
    #日期相关
    fieldList.append({'name':u'放款日期','value':lend.get('from_date'),'type':1,'CDATA':True})
    fieldList.append({'name':u'到期日期','value':lend.get('thur_date'),'type':1,'CDATA':True})
    #还款
    if lend.get('repayment_times') == u'按月还款':
       repayment_times = 'MONTH'
    elif lend.get('repayment_times') == u'按季还款':
       repayment_times = 'QUARTER'
    else:
       repayment_times = 'YEAR'

    fieldList.append({'name':u'还款方式','value':lend.get('repayment_method'),'type':1,'CDATA':True})
    fieldList.append({'name':u'还款周期','value':repayment_times,'type':1,'CDATA':True})
    fieldList.append({'name':u'还款周期频率','value':str(lend.get('repayment_times')),'type':1,'CDATA':True})
    fieldList.append({'name':u'首期还款日期','value':lend.get('first_rep_date'),'type':1,'CDATA':True})
    #利率
    fieldList.append({'name':u'产品利率','value':str(Decimal(lend.get('product_rate')).quantize(Decimal('0.000000'))),'type':1,'CDATA':True})
    fieldList.append({'name':u'合规利率','value':str(Decimal(lend.get('compliance_rate')).quantize(Decimal('0.0000000'))),'type':1,'CDATA':True})
    fieldList.append({'name':u'利率浮动方式','value':lend.get('product_float_type'),'type':1,'CDATA':True})
    fieldList.append({'name':u'浮动值','value':str(Decimal(lend.get('product_rate_float')).quantize(Decimal('0.00'))),'type':1,'CDATA':True})
    fieldList.append({'name':u'执行利率','value':str(Decimal(lend.get('execute_rate')).quantize(Decimal('0.000000'))),'type':1,'CDATA':True})
    fieldList.append({'name':u'逾期利率上浮比例','value':str(Decimal(lend.get('overdue_rate_more')).quantize(Decimal('0.00'))),'type':1,'CDATA':True})
    fieldList.append({'name':u'逾期利率','value':str(Decimal(lend.get('overdue_rate')).quantize(Decimal('0.000000'))),'type':1,'CDATA':True})
    fieldList.append({'name':u'用途违规罚息上浮比例','value':str(Decimal(lend.get('shift_fine_rate')).quantize(Decimal('0.00'))),'type':1,'CDATA':True})
    fieldList.append({'name':u'用途违规罚息率','value':str(Decimal(lend.get('shift_rate')).quantize(Decimal('0.000000'))),'type':1,'CDATA':True})
    fieldList.append({'name':u'欠息复利上浮比例','value':str(Decimal(lend.get('debt_interest')).quantize(Decimal('0.00'))),'type':1,'CDATA':True})
    fieldList.append({'name':u'欠息复利利率','value':str(Decimal(lend.get('debt_interest_and')).quantize(Decimal('0.000000'))),'type':1,'CDATA':True})
    #利息
    if lend.get('interest_period') == '按月结息':
       interest_period = 'MONTH' 
    else:
       interest_period = 'QUARTER'
    fieldList.append({'name':u'结息方式','value':lend.get('grace_pay_interest'),'type':1,'CDATA':True})
    fieldList.append({'name':u'结息周期','value':interest_period,'type':1,'CDATA':True})
    fieldList.append({'name':u'结息周期频率','value':lend.get('int_per_fre'),'type':1,'CDATA':True})
    fieldList.append({'name':u'首次结息日期','value':lend.get('first_int_date'),'type':1,'CDATA':True})
    fieldList.append({'name':u'起息日期','value':lend.get('from_date'),'type':1,'CDATA':True})
    #其他信息
    fieldList.append({'name':u'主担保方式','value':lend.get('main_gua_type'),'type':1,'CDATA':True})
    fieldList.append({'name':u'贷款产品','value':extra['product_name'],'type':1,'CDATA':True})
    fieldList.append({'name':u'贷款用途','value':lend.get('purpose_type'),'type':1,'CDATA':True})
    fieldList.append({'name':u'结算账号/卡号','value':lend.get('repayment_account_no'),'type':1,'CDATA':True})
    fieldList.append({'name':u'扣款账号','value':lend.get('repayment_account_no'),'type':1,'CDATA':True})
    fieldList.append({'name':u'行业类别','value':app.get('industry_4'),'type':1,'CDATA':True})
    fieldList.append({'name':u'行业类别代码','value':app.get('industry_4'),'type':1,'CDATA':True})
    fieldList.append({'name':u'抵押担保资料号','value':lend.get('gua_doc_no'),'type':1,'CDATA':True})
    fieldList.append({'name':u'理财产品签约号','value':lend.get('money_pru_no'),'type':1,'CDATA':True})
    fieldList.append({'name':u'原授信合同号','value':lend.get('credit_con_no'),'type':1,'CDATA':True})

    print fieldList
    #fieldList.append({'name':})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))
    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}
    lst = root.getiterator('Field')
    for item in lst:
        fieldDict.update({item.attrib['name']:item.text})
    return fieldDict


#查询理财产品签约号
def trans120192(cert_no,cust_name):
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},\
            'Service':{'name':u'查询理财产品签约号','value':'120192'},\
            'ServiceName':'CBS_CREDIT_FINANCIAL_CONTRACT_QUERY',\
            'Tran':'120192',\
            'Final':'true',\
            'owner':{'name':u'郭强','value':'00779'}
         }
    fieldList=[]
    fieldList.append({'name':u'交易码','value':'120192','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':'00779','type':1,'CDATA':True})
    fieldList.append({'name':u'理财产品签约号','value':'1','type':1,'CDATA':True})
    fieldList.append({'name':u'扣款账号','value':cert_no,'type':1,'CDATA':True})
    fieldList.append({'name':u'户名','value':cust_name,'type':1,'CDATA':True})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))
    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}
    lst = root.getiterator('Field')
    for item in lst:
        fieldDict.update({item.attrib['name']:item.text})
    return fieldDict

#个人客户信息查询
def trans120199(cert_no,cust_name):
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},
            'Service':{'name':u'个人客户信息查询','value':'120199'},
            'ServiceName':'CBS_CREDIT_PERSON_QUERY2',
            'Tran':'120199',
            'Final':'true',
            'owner':{'name':u'郭强','value':'00779'}
         }
    fieldList=[]
    fieldList.append({'name':u'交易码','value':'120199','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':'00779','type':1,'CDATA':True})
    fieldList.append({'name':u'证件类型','value':'1','type':1,'CDATA':True})
    fieldList.append({'name':u'证件号码','value':cert_no,'type':1,'CDATA':True})
    fieldList.append({'name':u'姓名','value':cust_name,'type':1,'CDATA':True})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))

    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}
    lst = root.getiterator('Field')
    for item in lst:
        fieldDict.update({item.attrib['name']:item.text})
    return fieldDict

#个人客户信息修改
def trans120198(cert_no,cust_name):
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},
            'Service':{'name':u'个人客户信息修改','value':'120198'},\
            'ServiceName':'CBS_CREDIT_PERSON_MODIFY',\
            'Tran':'120198',\
            'Final':'true',\
            'owner':{'name':u'郭强','value':'00779'}
         }
    fieldList=[]
    fieldList.append({'name':u'交易码','value':'120198','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':'00779','type':1,'CDATA':True})
    fieldList.append({'name':u'证件类型','value':'1','type':1,'CDATA':True})
    fieldList.append({'name':u'证件号码','value':cert_no,'type':1,'CDATA':True})
    fieldList.append({'name':u'姓名','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'性别','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'客户编号','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'证件类型','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'证件号码','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'民族','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'出生日期','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'证件到期日期','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'地址','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'籍贯','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'婚姻状况','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'工作单位','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'主要收入来源','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'家庭年收入','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'供养人数','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'手机号码','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'电话号码','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'当前职位','value':cust_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'联系地址','value':cust_name,'type':1,'CDATA':True})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))

    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}
    lst = root.getiterator('Field')
    for item in lst:
        fieldDict.update({item.attrib['name']:item.text})
    return fieldDict

#对公客户信息查询
def trans120197(com_no,com_name):
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},\
            'Service':{'name':u'对公客户信息查询','value':'120197'},\
            'ServiceName':'CBS_CREDIT_ORGANIZATION_QUERY2',\
            'Tran':'120197',\
            'Final':'true',\
            'owner':{'name':u'郭强','value':'00779'}
        }
    fieldList=[]
    fieldList.append({'name':u'交易码','value':'120197','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':'00779','type':1,'CDATA':True})
    fieldList.append({'name':u'机构代码','value':com_no,'type':1,'CDATA':True})
    fieldList.append({'name':u'客户名称','value':com_name,'type':1,'CDATA':True})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))

    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}

    lst = root.getiterator('Field')
    for item in lst:
        fieldDict.update({item.attrib['name']:item.text})
    return fieldDict

#利率查询
def trans120191(loan_name, date):
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},\
            'Service':{'name':u'贷款利率查询','value':'120191'},\
            'ServiceName':'CBS_RATE_QUERY2',\
            'Tran':'120191',\
            'Final':'true',\
            'owner':{'name':u'郭强','value':'00779'}
    }
    fieldList=[]
    fieldList.append({'name':u'交易码','value':'120191','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':'00779','type':1,'CDATA':True})
    fieldList.append({'name':u'贷款产品','value':loan_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'期限','value':date,'type':1,'CDATA':True})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))

    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}
    lst = root.getiterator('Field')
    print lst
    for item in lst:
       fieldDict.update({item.attrib['name']:item.text})
    return fieldDict

#存款账户余额查询接口
def trans120201(account_no):
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},\
            'Service':{'name':u'存款账户余额查询','value':'120201'},\
            'ServiceName':'CBS_CREDIT_BALANCE_QUERY',\
            'Tran':'120201',\
            'Final':'true',\
            'owner':{'name':u'郭强','value':'00779'}
    }
    fieldList=[]
    fieldList.append({'name':u'交易码','value':'120201','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':'00779','type':1,'CDATA':True})
    fieldList.append({'name':u'账号','value':account_no,'type':1,'CDATA':True})
    fieldList.append({'name':u'户名','value':"",'type':1,'CDATA':True})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))
    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}
    lst = root.getiterator('Field')
    print lst
    for item in lst:
       fieldDict.update({item.attrib['name']:item.text})
    return fieldDict

#存款账户明细查询接口
def trans120202(loan_name, date):
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},\
            'Service':{'name':u'贷款利率查询','value':'120202'},\
            'ServiceName':'CBS_CREDIT_ACCOUNT_DETAIL_QUERY',\
            'Tran':'120202',\
            'Final':'true',\
            'owner':{'name':u'郭强','value':'00779'}
    }
    fieldList=[]
    fieldList.append({'name':u'交易码','value':'120202','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':'00779','type':1,'CDATA':True})
    fieldList.append({'name':u'账号','value':loan_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'户名','value':date,'type':1,'CDATA':True})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))
    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}
    lst = root.getiterator('Field')
    print lst
    for item in lst:
       fieldDict.update({item.attrib['name']:item.text})
    return fieldDict

#银行承兑汇票签发
def trans130101(cust,trans,app,lend,user_info,extra):
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},\
            'Service':{'name':u'银行承兑汇票签发','value':'130101'},\
            'ServiceName':'CBS_TRAN_INPUT',\
            'Tran':'130101',\
            'Final':'true',\
            'owner':{'name':u'郭强','value':'00779'}
    }
    fieldList=[]
    fieldList.append({'name':u'交易码','value':'130101','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':user_info.user_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'承兑合同号','value':'0473231412JGHZ00044','type':1,'CDATA':True})
    fieldList.append({'name':u'合同序号','value':'1','type':1,'CDATA':True})
    fieldList.append({'name':u'出票人账号','value':'04732301200000007365','type':1,'CDATA':True})
    fieldList.append({'name':u'质押票号','value':'3130005100000001','type':1,'CDATA':True})
    fieldList.append({'name':u'出票金额','value':'100000.00','type':1,'CDATA':True})
    fieldList.append({'name':u'保证金账号','value':'13130005100000001','type':1,'CDATA':True})
    fieldList.append({'name':u'保证金额','value':'100000.00','type':1,'CDATA':True})
    fieldList.append({'name':u'票据种类','value':'1','type':1,'CDATA':True})
    fieldList.append({'name':u'票据号码','value':'1','type':1,'CDATA':True})
    fieldList.append({'name':u'收款人账号','value':'0','type':1,'CDATA':True})
    fieldList.append({'name':u'收款人名称','value':'0','type':1,'CDATA':True})
    fieldList.append({'name':u'收款行名称','value':'0','type':1,'CDATA':True})
    fieldList.append({'name':u'银承到期日期','value':'2016-05-07','type':1,'CDATA':True})
    fieldList.append({'name':u'计息方式','value':(''),'type':1,'CDATA':True})
    fieldList.append({'name':u'执行利率','value':lend.get('execute_rate'),'type':1,'CDATA':True})
    fieldList.append({'name':u'核心会计日期','value':'2015-12-16','type':1,'CDATA':True})
    fieldList.append({'name':u'出票人户名','type':1,'CDATA':True})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))
    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}
    lst = root.getiterator('Field')
    for item in lst:
        fieldDict.update({item.attrib['name']:item.text})
    return fieldDict

#贴现接口
def trans130211(cust,trans,app,lend,user_info,extra):
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},\
            'Service':{'name':u'贴现接口','value':'130211'},\
            'ServiceName':'CBS_TRAN_INPUT',\
            'Tran':'130211',\
            'Final':'true',\
            'owner':{'name':u'郭强','value':user_info.user_name}
    }
    print extra
    fieldList=[]
    fieldList.append({'name':u'交易码','value':'130211','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':user_info.user_name,'type':1,'CDATA':True})
    fieldList.append({'name':u'合同编号','value':extra.get('contract_no'),'type':1,'CDATA':True})
    fieldList.append({'name':u'合同序号','value':'1','type':1,'CDATA':True})
    fieldList.append({'name':u'票据种类','value':extra.get('bill_kill'),'type':1,'CDATA':True})
    fieldList.append({'name':u'票据类型','value':extra.get('bill_type'),'type':1,'CDATA':True})
    fieldList.append({'name':u'票据号码','value':extra.get('bill_no'),'type':1,'CDATA':True})
    fieldList.append({'name':u'票面金额','value':str(int(extra.get('bill_amount'))*100),'type':1,'CDATA':True})
    fieldList.append({'name':u'票据出票日','value':str(extra.get('bill_from_date')),'type':1,'CDATA':True})
    fieldList.append({'name':u'票据到期日','value':str(extra.get('bill_due_date')),'type':1,'CDATA':True})
    fieldList.append({'name':u'承兑行类型','value':'商业','type':1,'CDATA':True})
    fieldList.append({'name':u'出票人全称','value':extra.get('bill_person'),'type':1,'CDATA':True})
    fieldList.append({'name':u'承兑行名称','value':extra.get('bill_start_branch'),'type':1,'CDATA':True})
    fieldList.append({'name':u'承兑行行号','value':str(extra.get('bill_pay_branch_no')),'type':1,'CDATA':True})
    fieldList.append({'name':u'收款人全称','value':extra.get('payee'),'type':1,'CDATA':True})
    fieldList.append({'name':u'贴现利率','value':str(extra.get('discount_rate')),'type':1,'CDATA':True})
    fieldList.append({'name':u'贴现到期日','value':str(extra.get('bill_due_date')),'type':1,'CDATA':True})
    fieldList.append({'name':u'贴现人账号','value':lend.get('proposer_acc'),'type':1,'CDATA':True})
    fieldList.append({'name':u'贴现人名称','value':cust.get('name'),'type':1,'CDATA':True})
    fieldList.append({'name':u'在途天数','value':str(extra.get('use_date')),'type':1,'CDATA':True})
    fieldList.append({'name':u'行业类别','value':lend.get('industry_4'),'type':1,'CDATA':True})
    fieldList.append({'name':u'行业类别代码','value':lend.get('industry_4'),'type':1,'CDATA':True})
    fieldList.append({'name':u'营销柜员号','value':'00449','type':1,'CDATA':True})
    fieldList.append({'name':u'营销柜员姓名','value':u'郭强','type':1,'CDATA':True})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))
    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}
    lst = root.getiterator('Field')
    for item in lst:
        fieldDict.update({item.attrib['name']:item.text})
    return fieldDict

#买方付息贴现接口
def trans130221():
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},\
            'Service':{'name':u'贴现接口','value':'130221'},\
            'ServiceName':'CBS_TRAN_INPUT',\
            'Tran':'130221',\
            'Final':'true',\
            'owner':{'name':u'郭强','value':'00779'}
    }
    fieldList=[]
    fieldList.append({'name':u'交易码','value':'130221','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':'00779','type':1,'CDATA':True})
    fieldList.append({'name':u'合同编号','value':'0477021512JTTX05891','type':1,'CDATA':True})
    fieldList.append({'name':u'合同序号','value':'1','type':1,'CDATA':True})
    fieldList.append({'name':u'票据种类','value':'纸票','type':1,'CDATA':True})
    fieldList.append({'name':u'票据类型','value':'3130005100000001','type':1,'CDATA':True})
    fieldList.append({'name':u'票据号码','value':'100000.00','type':1,'CDATA':True})
    fieldList.append({'name':u'票面金额','value':'13130005100000001','type':1,'CDATA':True})
    fieldList.append({'name':u'票据出票日','value':'100000.00','type':1,'CDATA':True})
    fieldList.append({'name':u'票据到期日','value':'1','type':1,'CDATA':True})
    fieldList.append({'name':u'承兑行类型','value':'1','type':1,'CDATA':True})
    fieldList.append({'name':u'出票人全称','value':'0','type':1,'CDATA':True})
    fieldList.append({'name':u'承兑行名称','value':'0','type':1,'CDATA':True})
    fieldList.append({'name':u'承兑行行号','value':'0','type':1,'CDATA':True})
    fieldList.append({'name':u'收款人全称','value':'2016-05-07','type':1,'CDATA':True})
    fieldList.append({'name':u'贴现利率','value':'00','type':1,'CDATA':True})
    fieldList.append({'name':u'贴现到期日','value':'0.000000','type':1,'CDATA':True})
    fieldList.append({'name':u'贴现人账号','value':'2015-12-16','type':1,'CDATA':True})
    fieldList.append({'name':u'贴现人名称','type':1,'CDATA':True})
    fieldList.append({'name':u'在途天数','type':1,'CDATA':True})
    fieldList.append({'name':u'行业类别','value':app.get('industry_4'),'type':1,'CDATA':True})
    fieldList.append({'name':u'行业类别代码','value':app.get('industry_4'),'type':1,'CDATA':True})
    fieldList.append({'name':u'营销柜员号','type':1,'CDATA':True})
    fieldList.append({'name':u'营销柜员姓名','type':1,'CDATA':True})
    fieldList.append({'name':u'上手背书人账号','type':1,'CDATA':True})
    fieldList.append({'name':u'上手背书人户名','type':1,'CDATA':True})
    fieldList.append({'name':u'付息企业名称1','type':1,'CDATA':True})
    fieldList.append({'name':u'付息企业名称2','type':1,'CDATA':True})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))
    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}
    lst = root.getiterator('Field')
    for item in lst:
        fieldDict.update({item.attrib['name']:item.text})
    return fieldDict

#一般贷款授信
'''
def trans120000():
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},
            'Service':{'name':u'一般贷款授信','value':'CBS_CREDIT_OPEN'},
            'Tran':'120000',
            'Final':'true',
            'owner':{'name':u'郭强','value':'00779'}
    }
    fieldList=[]
    fieldList.append({'name':u'交易码','value':'120000','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':'00779','type':1,'CDATA':True})
    fieldList.append({'name':u'客户编号','value':'0477021512JTTX05891','type':1,'CDATA':True})
    fieldList.append({'name':u'贷款日期','value':'1','type':1,'CDATA':True})
    fieldList.append({'name':u'币种','value':'纸票','type':1,'CDATA':True})
    fieldList.append({'name':u'合同编号','value':'3130005100000001','type':1,'CDATA':True})
    fieldList.append({'name':u'合同金额','value':'100000.00','type':1,'CDATA':True})
    fieldList.append({'name':u'到期日期','value':'100000.00','type':1,'CDATA':True})
    fieldList.append({'name':u'贷款产品','value':'100000.00','type':1,'CDATA':True})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))
    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}
    lst = root.getiterator('Field')
    for item in lst:
        fieldDict.update({item.attrib['name']:item.text})
    return fieldDict
'''
#对公卡授信
def trans120311():
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},
            'Service':{'name':u'对公卡授信','value':'CBS_TRAN_INPUT'},
            'Tran':'120311',
            'Final':'true',
            'owner':{'name':u'郭强','value':'00779'}
    }
    fieldList=[]
    fieldList.append({'name':u'交易码','value':'120311','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':'00779','type':1,'CDATA':True})
    fieldList.append({'name':u'授信类型','type':1,'CDATA':True})
    fieldList.append({'name':u'授信合同编号','value':'0473031505JHAQ00052','type':1,'CDATA':True})
    fieldList.append({'name':u'新授信合同编号','type':1,'CDATA':True})
    fieldList.append({'name':u'客户编号','value':'600000777','type':1,'CDATA':True})
    fieldList.append({'name':u'客户名称','value':'乌海市隆信祥物流有限公司','type':1,'CDATA':True})
    fieldList.append({'name':u'授信额度','value':'5000000.00','type':1,'CDATA':True})
    fieldList.append({'name':u'授信日期','value':'2015-06-08','type':1,'CDATA':True})
    fieldList.append({'name':u'授信到期日期','value':'2018-04-16','type':1,'CDATA':True})
    fieldList.append({'name':u'借据期限','value':'12','type':1,'CDATA':True})
    fieldList.append({'name':u'主担保方式','value':'抵押','type':1,'CDATA':True})
    fieldList.append({'name':u'贷款产品','value':'商住房抵押及保证经营性50（卡）','type':1,'CDATA':True})
    fieldList.append({'name':u'贷款用途','value':'货款','type':1,'CDATA':True})
    fieldList.append({'name':u'抵押合同号','value':'04730300011081','type':1,'CDATA':True})
    fieldList.append({'name':u'还款方式','value':'一次还本','type':1,'CDATA':True})
    fieldList.append({'name':u'合规利率','value':'4.2500000','type':1,'CDATA':True})
    fieldList.append({'name':u'产品利率','value':'9.600000','type':1,'CDATA':True})
    fieldList.append({'name':u'利率浮动方式','value':'比例浮动','type':1,'CDATA':True})
    fieldList.append({'name':u'浮动值','value':'0.00','type':1,'CDATA':True})
    fieldList.append({'name':u'执行利率','value':'9.600000','type':1,'CDATA':True})
    fieldList.append({'name':u'逾期利率上浮比例','value':'50.00','type':1,'CDATA':True})
    fieldList.append({'name':u'逾期利率','value':'14.400000','type':1,'CDATA':True})
    fieldList.append({'name':u'用途违规罚息上浮比例','value':'100.00','type':1,'CDATA':True})
    fieldList.append({'name':u'用途违规罚息率','value':'19.200000','type':1,'CDATA':True})
    fieldList.append({'name':u'欠息复利上浮比例','value':'50.00','type':1,'CDATA':True})
    fieldList.append({'name':u'欠息复利利率','value':'14.400000','type':1,'CDATA':True})
    fieldList.append({'name':u'结息方式','value':'按周期结息','type':1,'CDATA':True})
    fieldList.append({'name':u'结息周期','value':'QUARTER','type':1,'CDATA':True})
    fieldList.append({'name':u'结息周期频率','value':'QUARTER','type':1,'CDATA':True})
    fieldList.append({'name':u'扣款账号','value':'QUARTER','type':1,'CDATA':True})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))
    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}
    lst = root.getiterator('Field')
    for item in lst:
        fieldDict.update({item.attrib['name']:item.text})
    return fieldDict


#撤销交易
def trans999999():
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},
            'Service':{'name':u'一般贷款授信','value':'CBS_TRAN_DELETE'},
            'Tran':'120104',
            'Final':'true',
            'owner':{'name':u'郭强','value':'00779'}
    }
    fieldList=[]
    fieldList.append({'name':u'交易码','value':'120104','type':1,'CDATA':True})
    fieldList.append({'name':u'机构号','value':'047308','type':1,'CDATA':True})
    fieldList.append({'name':u'柜员号','value':'00779','type':1,'CDATA':True})
    fieldList.append({'name':u'原流水号','value':'120076082','type':1,'CDATA':True})
    msg = make_message(fieldList,head).toxml()
    data = send(str(msg))
    fieldDict = {}
    try:
        root = ElementTree.fromstring(data)
    except Exception as e:
        return {'code':'-1','reason':'报文解析错误'}
    lst = root.getiterator('Field')
    for item in lst:
        fieldDict.update({item.attrib['name']:item.text})
    return fieldDict

def test():
     #组织报文头
    head={'Channel':{'name':u'信贷渠道','value':'CREDIT'},
            'Service':{'name':u'一般贷款放款','value':'120101'},
            'ServiceName':'CBS_TRAN_INPUT', 
            'Tran':'120101',
            'Final':'true',
            'owner':{'name':u'郭强','value':'00779'}
         }
    #获取 报文体
    #fieldList=[]
    #field = {'name':'服务名称','type':1,'value':'CBS_TRAN_INPUT','CDATA':True}
    #fieldList.append(field)
    fieldList=test_read_xml()
    #拼接报文
    msg = make_message(fieldList,head).toxml()
    #发送报文
    send(str(msg))


if __name__ == '__main__':

    #组织报文头
    head={'Channel':{'name':u'柜面渠道','value':'TERM'},
            'Service':{'name':u'一般贷款放款','value':'120101'},
            'ServiceName':'CBS_TRAN_INPUT',
            'Tran':'120101',
            'Final':'true',
            'owner':{'name':u'郭强','value':'00779'}
         }
    #获取 报文体
    #fieldList=[]
    #field = {'name':'服务名称','type':1,'value':'CBS_TRAN_INPUT','CDATA':True}
    #fieldList.append(field)
    fieldList=test_read_xml()
    #拼接报文
    msg = make_message(fieldList,head).toxml()
    #发送报文
    send(str(msg))

