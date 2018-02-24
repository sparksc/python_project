# -*- coding:utf-8 -*-
u"""
报告数据模型测试文件
"""
from sqlalchemy import Integer,Column,Table,ForeignKey,Sequence,String,Date,DateTime,UniqueConstraint, Index
from sqlalchemy.orm import mapper,relationship,backref

import logging, datetime
from .configure import Configure
from ..model import Base
from ..domain.model import *

with Configure() as cfg:
    #database = cfg.get_database('aml_database_for_test')
    database = cfg.get_database('aml_database')

def insert_suspicious_character():
    database.session.add_all([
            SuspiciousCharacter(code='9001', description="可疑交易补充信息"),
            SuspiciousCharacter(code='0001', description="怀疑客户为恐怖组织、恐怖分子以及恐怖活动犯罪募集或者企图募集资金或者其他形式的资产"),
            SuspiciousCharacter(code='0002', description="怀疑客户为恐怖组织、恐怖分子、从事恐怖融资活动的人以及恐怖活动犯罪提供或者企图提供资金或其他形式财产的"),
            SuspiciousCharacter(code='0003', description="怀疑客户为恐怖组织、恐怖分子保存、管理、运作或企图保存、管理、运作资金或者其他形式的资产"),
            SuspiciousCharacter(code='0004', description="怀疑客户或者其交易对手时恐怖组织、恐怖分子以及从事恐怖融资活动人员"),
            SuspiciousCharacter(code='0005', description="怀疑资金或者其他形式财产来源于或者将来源于恐怖组织、恐怖分子、从事恐怖融资活动人员的"),
            SuspiciousCharacter(code='0006', description="怀疑资金或者其他形式财产来源于或者将用于恐怖融资、恐怖活动以及其他恐怖主义目的，或者怀疑资金或者其他形式财产被恐怖组织、恐怖分子、从事恐怖融资活动人员使用的"),
            SuspiciousCharacter(code='0007', description="金融机构及其工作人员有合理理由怀疑资金、其他形式财产、交易、客户与恐怖主义、恐怖活动犯罪、恐怖组织、恐怖分子、从事恐怖融资活动人有关的其他情形"),
            SuspiciousCharacter(code='0008', description="有合理理由怀疑客户或者其交易对手与国务院有关部门、机构发布的恐怖组织、恐怖分子名单相关"),
            SuspiciousCharacter(code='0009', description="有合理理由怀疑客户或者其交易对手与司法机关发布的恐怖组织、恐怖分子名单相关"),
            SuspiciousCharacter(code='0010', description="有合理理由怀疑客户或者其交易对手与联合国安理会决议中所列的恐怖组织、恐怖分子名单相关"),
            SuspiciousCharacter(code='0011', description="有合理理由怀疑客户或者其交易对手与中国人民人行要求关注的其他恐怖组织、恐怖份子名单相关"),
            SuspiciousCharacter(code='0012', description="短期内资金分散转入、集中转出或者集中转入、分散转出，与客户身份、财务状况、经营业务明显不符"),
            SuspiciousCharacter(code='0013', description="短期内相同收付款人之间频繁发生资金收付，且交易金额接近大额交易标准"),
            SuspiciousCharacter(code='0014', description="法人、其他组织和个体工商户短期内频繁收取与其经营业务明显无关的汇款，或者自然人客户短期内频繁收取法人、其他组织的汇款"),
            SuspiciousCharacter(code='0015', description="长期闲置的账户原因不明地突然启用或者平常资金流量小的账户突然有异常资金流入，且短期内出现大量资金收付。"),
            SuspiciousCharacter(code='0016', description="与来自于贩毒、走私、恐怖活动、赌博严重地区或者避税型离岸金融中心的客户之间的资金往来活动在短期内明显增多，或者频繁发生大量资金收付"),
            SuspiciousCharacter(code='0017', description="没有正常原因的多头开户、销户，且销户前发生大量资金收付"),
            SuspiciousCharacter(code='0018', description="提前偿还贷款，与其财务状况明显不符"),
            SuspiciousCharacter(code='0019', description="客户用于境外投资的购汇人民币资金大部分为现金或者从非同名银行账户转入"),
            SuspiciousCharacter(code='0020', description="客户要求进行本外币间的掉期业务，而其资金的来源和用途可疑"),
            SuspiciousCharacter(code='0021', description="客户经常存入境外开立的旅行支票或者外币汇票存款，与其经营状况不符"),
            SuspiciousCharacter(code='0022', description="外商投资企业以外币现金方式进行投资或者在收到投资款后，在短期内将资金迅速转到境外，与其生产经营支付需求不符"),
            SuspiciousCharacter(code='0023', description="外商投资企业外方投入资本金数额超过批准金额或者借入的直接外债，从无关联企业的第三国汇入"),
            SuspiciousCharacter(code='0024', description="证券经营机构指令银行划出与证券交易、清算无关的资金，与其实际经营情况不符"),
            SuspiciousCharacter(code='0025', description="证券经营机构通过银行频繁大量拆借外汇资金"),
            SuspiciousCharacter(code='0026', description="保险机构通过银行频繁大量对同一家投保人发生赔付或者办理退保"),
            SuspiciousCharacter(code='0027', description="自然人银行账户频繁进行现金收付且情形可疑，或者一次性大额存取现金且情形可疑"),
            SuspiciousCharacter(code='0028', description="居民自然人频繁收到境外汇入的外汇后，要求银行开具旅行支票、汇票或者非居民自然人频繁存入外币现钞并要求银行开具旅行支票、汇票带出或者频繁订购、兑现大量旅行支票、汇票"),
            SuspiciousCharacter(code='0029', description="多个境内居民接受一个离岸账户汇款，其资金的划转和结汇均由一人或者少数人操作"),
            SuspiciousCharacter(code='0030', description="其他"),
            SuspiciousCharacter(code='0031', description="客户拒绝提供有效或者其他身份证明文件的"),
            SuspiciousCharacter(code='0032', description="对向境内汇入资金的境外机构提出要求后，仍无法完整获得汇款人姓名或者名称，汇款人账号和汇款人住所及其他相关替代性信息的"),
            SuspiciousCharacter(code='0033', description="客户无正当理由拒绝更新客户基本信息的"),
            SuspiciousCharacter(code='0034', description="采取必要措施后，仍怀疑先前获得的客户身份资料的真实性，有效性，完整行的"),
            SuspiciousCharacter(code='0035', description="录行客户身份识别义务时发现的其他可疑行为")
        ])
    logging.debug("insert data into suspicious_character.....")
    database.session.commit()
    logging.debug("insert success.....")

def insert_aml_customer():
    database.session.add_all([
            AMLCustomer(name='浙江北城网络科技有限公司',cust_type='企业客户',nationality='中国',certificate_type='营业执照证件',
                certificate_id='330500000025812',legal_per_name='卢威军',legal_per_certificate_type='身份证',
                legal_per_certificate_id='330501197202242617',legal_per_match_cust_id='51504498'),
            AMLCustomer(name='湖州康山立丰食品有限公司',cust_type='企业客户',nationality='中国',certificate_type='营业执照证件',
                certificate_id='330508000062064',legal_per_name='敖显清',legal_per_certificate_type='身份证',
                legal_per_certificate_id='510225197009098738',legal_per_match_cust_id='40514962'),
            AMLCustomer(name='慎佩辉',cust_type='个人客户',nationality='中国',certificate_type='身份证',
                certificate_id='330511194107028224',legal_per_name='',legal_per_certificate_type='',
                legal_per_certificate_id='',legal_per_match_cust_id=''),
            AMLCustomer(name='顾翼虎',cust_type='个人客户',nationality='中国',certificate_type='身份证',
                certificate_id='330501197404262616',legal_per_name='',legal_per_certificate_type='',
                legal_per_certificate_id='',legal_per_match_cust_id=''),
            AMLCustomer(name='吴月英',cust_type='个人客户',nationality='中国',certificate_type='身份证',
                certificate_id='330501197404262616',legal_per_name='',legal_per_certificate_type='',
                legal_per_certificate_id='',legal_per_match_cust_id=''),
        ])
    logging.debug("insert data into aml_customer.....")
    database.session.commit()
    logging.debug("insert success.....")

def insert_suspicous_model():
    database.session.add_all([
                SuspiciousModel(code='A0000', name='结算型地下钱庄模型'         , description='结算型地下钱庄模型'),
                SuspiciousModel(code='A0001', name='结算型地下钱庄模型-账户类型', description='个体工商户，注册资金少于5万。', parent_code='A0000'),
                SuspiciousModel(code='A0002', name='结算型地下钱庄模型-空壳公司', description='注册地址虚假，或家庭地址，无固定电话，或多家公司相同地址。', parent_code='A0000'),
                SuspiciousModel(code='A0003', name='结算型地下钱庄模型-亲属关系', description='与多个公司具有相同的法人，或者法人为学生或老人，或者法人之间存在亲属关系。', parent_code='A0000'),
                SuspiciousModel(code='A0004', name='结算型地下钱庄模型-集中注册', description='与多个公司在同一时间，同一机构注册。', parent_code='A0000'),
                SuspiciousModel(code='A0005', name='结算型地下钱庄模型-公司网银', description='开户开通网银，不设置转出金额上限，和个人转账不做过多限制。', parent_code='A0000'),
                SuspiciousModel(code='A0006', name='结算型地下钱庄模型-支票'    , description='公司开户后不领取转账支票和现金支票。', parent_code='A0000'),
                SuspiciousModel(code='A0007', name='结算型地下钱庄模型-代理开户', description='与其他公司具有相同的代理人，并且代理人不为湖州人。', parent_code='A0000'),
                SuspiciousModel(code='A0008', name='结算型地下钱庄模型-异地开户', description='异地企业跨省、跨地区开设一般存款账户、专用存款账户。', parent_code='A0000'),
                SuspiciousModel(code='A0009', name='结算型地下钱庄模型-沉睡期'  , description='公司开户至第一次交易沉睡时间。', parent_code='A0000'),
                SuspiciousModel(code='A0010', name='结算型地下钱庄模型-初始交易', description='公司账户开始无业务，或交易量小。', parent_code='A0000'),
                SuspiciousModel(code='A0011', name='结算型地下钱庄模型-测试交易', description='公司账户启用交易小额资金（几十到几百划转），多为（网银、公转私、ATM转账、提现）', parent_code='A0000'),
                SuspiciousModel(code='A0012', name='结算型地下钱庄模型-超规模交易', description='公司账户突然大进大出，每日余额非常少。个人账户大量现金交易，不购汇，快进快出。', parent_code='A0000'),
                SuspiciousModel(code='A0013', name='结算型地下钱庄模型-交易周期', description='资金交易持续时间呈短、中期。'),
                SuspiciousModel(code='B0000', name='汇兑型地下钱庄模型', description='汇兑型地下钱庄模型'),
                SuspiciousModel(code='B0001', name='汇兑型地下钱庄模型-账户数量', description='名下拥有账户数量多，超过50个。', parent_code='B0000')
                ])
    logging.debug("insert data into suspicous_mode.....")
    database.session.commit()
    logging.debug("insert success.....")

def insert_suspicous_report():
    report1 = SuspiciousTranReport(cust_id ='2', rept_date = datetime.datetime.now())
    listA1 = ModelTriggerList(trigger_model_code='A0000')
    listA1.model_trigger_entry.extend([
       ModelTriggerEntry(trigger_entry_code='A0001', trigger_message='注册资金为1万元'),
       ModelTriggerEntry(trigger_entry_code='A0002', trigger_message='注册地址为家庭地址'),
       ModelTriggerEntry(trigger_entry_code='A0004', trigger_message='与5个公司同一时间注册'),
       ModelTriggerEntry(trigger_entry_code='A0006', trigger_message='未领取支票'),
       ModelTriggerEntry(trigger_entry_code='A0008', trigger_message='该公司为跨省异地企业'),
       ModelTriggerEntry(trigger_entry_code='A0009', trigger_message='沉睡期超过6个月'),
    ])
    listA2 =  ModelTriggerList(trigger_model_code ='B0000')
    listA2.model_trigger_entry.extend([
       ModelTriggerEntry(trigger_entry_code='B0001', trigger_message='名下拥有199个账户'),
    ])
    report1.model_trigger_list.extend([listA1, listA2])


    report2 = SuspiciousTranReport(cust_id ='3', rept_date = datetime.datetime.now())
    listB1 =  ModelTriggerList(trigger_model_code ='A0000')
    listB1.model_trigger_entry.extend([
       ModelTriggerEntry(trigger_entry_code='A0006', trigger_message='未领取支票'),
       ModelTriggerEntry(trigger_entry_code='A0008', trigger_message='该公司为跨省异地企业'),
       ModelTriggerEntry(trigger_entry_code='A0009', trigger_message='沉睡期超过6个月'),
    ])
    
    logging.debug("insert data into suspicous_report.....")
    database.session.add_all([report1, report2])
    database.session.commit()
    logging.debug("insert successful.....")

def insert_customer_sort():
    database.session.add_all([AMLCustomerSort(network_id=101,customer_id=1,customer_name='顾长庚',evaluate_date='2015-02-14',system_evaluate='高',person_evaluate='低',status='未调查'),
    AMLCustomerSort(network_id=102,customer_id=2,customer_name='张三',evaluate_date='2015-02-14',system_evaluate='高',person_evaluate='低',status='未调查'),
    AMLCustomerSort(network_id=103,customer_id=3,customer_name='李四',evaluate_date='2015-02-14',system_evaluate='高',person_evaluate='低',status='未调查'),
    AMLCustomerSort(network_id=104,customer_id=4,customer_name='王五',evaluate_date='2015-02-14',system_evaluate='高',person_evaluate='低',status='未调查'),
])
    logging.debug('insert into customer_sort')
    database.session.commit()
    logging.debug('customer_sort success')
    
def insert_report_charcter():
    database.session.add_all([
        ReportCharacter(report_id='2', character_code="0004")
    ])
    logging.debug('insert data into report_charcter')
    database.session.commit()
    logging.debug('customer_sort success')
    
    
def test_ResetDB():
    logging.debug(str(database.session))
    Base.metadata.drop_all(database.engine)
    logging.debug("drop db.....")
    Base.metadata.create_all(database.engine)
    logging.debug("create db.....")
    database.session.commit()
    logging.debug("AML database create successfull.....")
    insert_aml_customer()
    insert_suspicous_model()
    insert_suspicous_report()
    insert_customer_sort()
    insert_suspicious_character()
    insert_report_charcter()

def ResetDB():
    logging.debug(str(database.session))
    Base.metadata.drop_all(database.engine)
    logging.debug("drop db.....")
    database.session.commit()
    Base.metadata.create_all(database.engine)
    logging.debug("create db.....")
    database.session.commit()
    logging.debug("AML database create successfull.....")
    insert_aml_customer()
    insert_suspicous_model()
    insert_suspicous_report()
    insert_customer_sort()
    insert_suspicious_character()
    insert_report_charcter()
    
if __name__=="__main__":
    test_ResetDB()

