# -*- coding:utf-8 -*-

import re
import decimal
import unittest
import xlrd
from ..model.report import *
from ..model.customer import *


class TestReport(unittest.TestCase):

    def setUp(self):
        self.session=simple_session()
        Base.metadata.drop_all(self.session.bind)
        Base.metadata.create_all(self.session.bind)

        init_report_data(self.session)

        self.init_company_data()


    def iterater_data(self,data_list):
        for item in data_list:
            logging.debug(item)
        

    def query_data(self):
        re_datas = self.session.query(ReportRecord,ReportItems,ReportData)  \
            .outerjoin(ReportItems,ReportRecord.report_id==ReportItems.report_id)  \
            .outerjoin(ReportData,ReportData.item_id==ReportItems.item_id)  \
            .filter(ReportRecord.id==1).order_by(ReportItems.item_id).all()

        data_list = []
        for item in re_datas:
            logging.debug(item)
            r_record = item[0]
            r_item = item[1]
            r_data = item[2] if item[2] else ReportData()
            data_list.append([r_record.id, r_record.report_id, r_item.item_id, r_item.item_name, r_data.value1, r_data.value2])
        return data_list
    
            #logging.debug("%s %s %s %s %s %s"% (r_record.id, r_record.report_id, r_item.item_id, r_item.item_name, r_data.value1, r_data.value2))
            #logging.debug("%s %s %s %s %s %s"% (r_record.id, r_record.report_id, r_item.item_id, r_item.item_name, r_data.value1, r_data.value2))


    def test_import_data(self):
        """

        """
        xl_list = self.read('1.xls')
        logging.debug(xl_list)

        company = self.session.query(Company).filter(Company.no=='500000077').one()

        record = ReportRecord(report_id=1, company=company)
        logging.debug(record.__dict__)

        report_items = self.session.query(ReportItems).all()
        logging.debug(report_items)
        for item in report_items:
            #
            if item.report.report_id == 1:
                
                for xl_item in xl_list:
                    logging.debug("%s %s = %s" % (item.item_name,xl_item[0], item.item_name == xl_item[0]))
                    if item.item_name == xl_item[0]:
                        value1 = 0
                        value2 = 0
                        try:
                            value1 = int(decimal.Decimal(xl_item[1]))
                            value2 = int(decimal.Decimal(xl_item[2]))
                        except Exception,e:
                            logging.warn(e)
                            continue

                        # web context please use param **kwargs
                        report_data = ReportData(report_id=item.report.report_id, record=record, item_id=item.item_id, value1=value1*100,value2=value2*100)
                        self.session.add(report_data)

        self.session.commit()
        self.session.close()
        data_list = self.query_data()
        self.iterater_data(data_list)


    def read(self, filename):
        # TODO: path search please replace flask app open_resource
        wb = xlrd.open_workbook("../static/reports/"+filename)
        s = wb.sheet_by_index(0)
        rows = s.nrows; cols = s.ncols


        xl_list = []

        for r in range(rows):
            col = s.cell(r,0).value.replace(' ','')
            col_val_1 = s.cell(r,1).value
            col_val_2 = s.cell(r,2).value


            col2 = s.cell(r,3).value.replace(' ','')
            col2_val_1 = s.cell(r,4).value
            col2_val_2 = s.cell(r,5).value


            xl_list.append([col,col_val_1, col_val_2])
            xl_list.append([col2,col2_val_1, col2_val_2])
            #logging.debug("cel1: %s , %s , %s" % (col,col_val_1, col_val_2))
            #logging.debug("cel2: %s , %s , %s" % (col2,col2_val_1, col2_val_2))
        return xl_list


    def print_report_data(self):
        reports = self.session.query(Report).all()

        table = "\n"
        for report in reports:
            items = report.report_items

            i = 5
            for item in items:
                table += "%s_%s \t" % (item.item_id,item.item_name)
                i -= 1
                if i < 0:
                    table += "\n"
                    i = 5


            table += "\n\n"

        logging.debug(table)



    def tearDown(self):
        #Base.metadata.drop_all(self.session.bind)
        #Base.metadata.drop_all(self.session.bind)
        logging.debug("finish!!!")

    def init_company_data(self):
        company=Company(no='500000077',name=u'乌海市三金煤制品有限责任公司',company_cn_name=u'乌海市三金煤制品有限责任公司',org_id='X2728906-X')
        customer = Customer(party=company, cust_type="company")
        self.session.add(customer)
        self.session.commit()




def init_report_data(session):
    logging.debug("init report data !")
    rt1 = ReportType(name="2003版资产负债表",cotes=2)
    rt2 = ReportType(name="2003版损益表",cotes=1)
    rt3 = ReportType(name="2003版现金流量",cotes=1)
    rt4 = ReportType(name="财务指标",cotes=1)
    rt5 = ReportType(name="2007版资产负债",cotes=2)
    rt6 = ReportType(name="2007版损益",cotes=1)
    rt7 = ReportType(name="2007版现金流量",cotes=1)
    rt8 = ReportType(name="事业单位资产负债",cotes=2)
    rt9 = ReportType(name="事业单位现金流量",cotes=1)

    session.add_all([rt1,rt2,rt3,rt4,rt5,rt6,rt7,rt8,rt9])

    r1 = Report(report_id=1,report_name="资产负债表",report_type=rt1)
    r2 = Report(report_id=2,report_name="损益表",report_type=rt2)
    r3 = Report(report_id=3,report_name="现金流量表",report_type=rt3)
    r4 = Report(report_id=4,report_name="财务指标值表",report_type=rt4)
    r5 = Report(report_id=5,report_name="财务指标值表",report_type=rt4)
    r6 = Report(report_id=6,report_name="资产负债表（新）",report_type=rt5)
    r7 = Report(report_id=7,report_name="损益表（新）",report_type=rt6)
    r8 = Report(report_id=8,report_name="现金流量表（新）",report_type=rt7)
    r9 = Report(report_id=9,report_name="资产负债表（事业单位）",report_type=rt8)
    r10 = Report(report_id=10,report_name="收入支出表（事业单位）",report_type=rt9)

    session.add_all([r1,r2,r3,r4,r5,r6,r7,r8,r9,r10])



    """
        SELECT     'ReportItems(item_id='||substr(item_id,3)||', item_name=u"'|| item_name ||'", report_type='||
        case
        when r.rpt_type='01' then 'r1'
        when r.rpt_type='02' then 'r2'
        when r.rpt_type='03' then 'r3'
        when r.rpt_type='04' then 'r4'
        when r.rpt_type='04' then 'r5'
        when r.rpt_type='07' then 'r6'
        when r.rpt_type='08' then 'r7'
        when r.rpt_type='09' then 'r8'
        when r.rpt_type='10' then 'r9'
        when r.rpt_type='11' then 'r10'
        end
        ||') ,'
        ,r.* from rpt_items r order by rpt_type, item_id;

    """
    session.add_all([
            ReportItems(item_id=1010000, item_name=u"资产类", report=r1) ,
            ReportItems(item_id=1020000, item_name=u"流动资产", report=r1) ,
            ReportItems(item_id=1020100, item_name=u"货币资金", report=r1) ,
            ReportItems(item_id=1020200, item_name=u"短期投资", report=r1) ,
            ReportItems(item_id=1020210, item_name=u"资产跌价准备", report=r1) ,
            ReportItems(item_id=1020300, item_name=u"短期投资净额", report=r1 , item_formula="rl[dc[1020200]][4]-rl[dc[1020210]][4]", item_formula1="rl[dc[1020200]][5]-rl[dc[1020210]][5]") ,
            ReportItems(item_id=1020400, item_name=u"应收票据", report=r1) ,
            ReportItems(item_id=1020500, item_name=u"应收股利", report=r1) ,
            ReportItems(item_id=1020600, item_name=u"应收利息", report=r1) ,
            ReportItems(item_id=1020700, item_name=u"应收账款", report=r1) ,
            ReportItems(item_id=1020710, item_name=u"坏帐准备", report=r1) ,
            ReportItems(item_id=1020800, item_name=u"应收账款净额", report=r1, item_formula="rl[dc[1020700]][4]-rl[dc[1020710]][4]", item_formula1="rl[dc[1020700]][5]-rl[dc[1020710]][5]") ,
            ReportItems(item_id=1020900, item_name=u"预付账款", report=r1,re_name=u"预付款项") ,
            ReportItems(item_id=1021000, item_name=u"期货保证金", report=r1) ,
            ReportItems(item_id=1021100, item_name=u"应收补贴款", report=r1) ,
            ReportItems(item_id=1021200, item_name=u"应收出口退税", report=r1) ,
            ReportItems(item_id=1021300, item_name=u"其他应收款", report=r1) ,
            ReportItems(item_id=1021400, item_name=u"存货", report=r1) ,
            ReportItems(item_id=1021410, item_name=u"存货原材料", report=r1) ,
            ReportItems(item_id=1021420, item_name=u"存货产成品", report=r1) ,
            ReportItems(item_id=1021430, item_name=u"存货跌价准备", report=r1) ,
            ReportItems(item_id=1021500, item_name=u"存货净值", report=r1, item_formula="rl[dc[1021400]][4]-rl[dc[1021430]][4]", item_formula1="rl[dc[1021400]][5]-rl[dc[1021430]][5]") ,
            ReportItems(item_id=1021600, item_name=u"待摊费用", report=r1) ,
            ReportItems(item_id=1021700, item_name=u"待处理流动资产净损失", report=r1) ,
            ReportItems(item_id=1021800, item_name=u"一年期长期债券投资", report=r1,re_name=u"一年内到期的长期债权投资") ,
            ReportItems(item_id=1021900, item_name=u"其他流动资产", report=r1) ,
            ReportItems(item_id=1022000, item_name=u"流动资产合计", report=r1,item_formula="rl[dc[1021400]][4]-rl[dc[1021430]][4]+rl[dc[1020700]][4]*1-rl[dc[1020710]][4]+rl[dc[1020200]][4]*1-rl[dc[1020210]][4]+rl[dc[1020100]][4]*1+rl[dc[1020400]][4]*1+rl[dc[1020500]][4]*1+rl[dc[1020600]][4]*1+rl[dc[1020900]][4]*1+rl[dc[1021000]][4]*1+rl[dc[1021100]][4]*1+rl[dc[1021200]][4]*1+rl[dc[1021300]][4]*1+rl[dc[1021600]][4]*1+rl[dc[1021700]][4]*1+rl[dc[1021800]][4]*1+rl[dc[1021900]][5]*1", item_formula1="rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]*1-rl[dc[1020710]][5]+rl[dc[1020200]][5]*1-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1") ,

            ReportItems(item_id=1030000, item_name=u"长期投资", report=r1) ,
            ReportItems(item_id=1030100, item_name=u"长期投资", report=r1) ,
            ReportItems(item_id=1030110, item_name=u"长期股权投资", report=r1) ,
            ReportItems(item_id=1030120, item_name=u"长期债券投资", report=r1) ,
            ReportItems(item_id=1030130, item_name=u"长期应收款", report=r1) ,
            ReportItems(item_id=1030140, item_name=u"长期待摊费用", report=r1) ,
            ReportItems(item_id=1030150, item_name=u"持有至到期投资", report=r1) ,
            
            ReportItems(item_id=1030200, item_name=u"合并价差", report=r1) ,
            ReportItems(item_id=1030300, item_name=u"长期投资合计", report=r1, item_formula="rl[dc[1030100]][4]*1+rl[dc[1030200]][4]*1", item_formula1="rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1") ,
            ReportItems(item_id=1040000, item_name=u"固定资产", report=r1) ,
            ReportItems(item_id=1040100, item_name=u"固定资产原价", report=r1) ,
            ReportItems(item_id=1040110, item_name=u"累计折旧", report=r1,re_name=u"减：累计折价") ,
            ReportItems(item_id=1040200, item_name=u"固定资产净值", report=r1, item_formula="rl[dc[1040100]][4]-rl[dc[1040110]][4]", item_formula1="rl[dc[1040100]][5]-rl[dc[1040110]][5]") ,
            ReportItems(item_id=1040210, item_name=u"固定资产值减值准备", report=r1,re_name=u"减：固定资产减值准备 ") ,
            ReportItems(item_id=1040300, item_name=u"固定资产净额", report=r1, item_formula="rl[dc[1040100]][4]-rl[dc[1040110]][4]-rl[dc[1040210]][4]", item_formula1="rl[dc[1040100]][5]-rl[dc[1040110]][5]-rl[dc[1040210]][5]") ,
            ReportItems(item_id=1040400, item_name=u"工程物资", report=r1) ,
            ReportItems(item_id=1040500, item_name=u"在建工程", report=r1) ,
            ReportItems(item_id=1040600, item_name=u"固定资产清理", report=r1) ,
            ReportItems(item_id=1040700, item_name=u"待处理固定资产净损失", report=r1) ,
            ReportItems(item_id=1040800, item_name=u"固定资产合计", report=r1, item_formula="rl[dc[1040100]][4]-rl[dc[1040110]][4]-rl[dc[1040210]][4]+rl[dc[1040400]][4]*1+rl[dc[1040500]][4]*1+rl[dc[1040600]][4]*1+rl[dc[1040700]][4]*1", item_formula1="rl[dc[1040100]][5]-rl[dc[1040110]][5]-rl[dc[1040210]][5]+rl[dc[1040400]][5]*1+rl[dc[1040500]][5]*1+rl[dc[1040600]][5]*1+rl[dc[1040700]][5]*1") ,

            ReportItems(item_id=1050000, item_name=u"无形资产及其他资产", report=r1) ,
            ReportItems(item_id=1050100, item_name=u"无形资产", report=r1) ,
            ReportItems(item_id=1050110, item_name=u"无形资产土地使用权", report=r1) ,
            ReportItems(item_id=1050200, item_name=u"递延资产", report=r1) ,
            ReportItems(item_id=1050210, item_name=u"递延资产固定资产修理", report=r1) ,
            ReportItems(item_id=1050220, item_name=u"递延资产固定资产改良支出", report=r1) ,
            ReportItems(item_id=1050300, item_name=u"其他长期资产", report=r1) ,
            ReportItems(item_id=1050310, item_name=u"其他长期资产特准储备物资", report=r1) ,
            ReportItems(item_id=1050400, item_name=u"非流动资产合计", report=r1,re_name=u"无形资产及其他资产合计", item_formula="rl[dc[1050100]][4]*1+rl[dc[1050200]][4]*1+rl[dc[1050300]][4]*1", item_formula1="rl[dc[1050100]][5]*1+rl[dc[1050200]][5]*1+rl[dc[1050300]][5]*1") ,
            ReportItems(item_id=1060000, item_name=u"递延税项", report=r1) ,
            ReportItems(item_id=1060100, item_name=u"递延税项借项", report=r1) ,
            ReportItems(item_id=1100000, item_name=u"资产总计", report=r1,item_formula="rl[dc[1021400]][4]-rl[dc[1021430]][4]+rl[dc[1020700]][4]*1-rl[dc[1020710]][4]+rl[dc[1020200]][4]*1-rl[dc[1020210]][4]+rl[dc[1020100]][4]*1+rl[dc[1020400]][4]*1+rl[dc[1020500]][4]*1+rl[dc[1020600]][4]*1+rl[dc[1020900]][4]*1+rl[dc[1021000]][4]*1+rl[dc[1021100]][4]*1+rl[dc[1021200]][4]*1+rl[dc[1021300]][4]*1+rl[dc[1021600]][4]*1+rl[dc[1021700]][4]*1+rl[dc[1021800]][4]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][4]*1+rl[dc[1030200]][4]*1+  rl[dc[1040100]][4]-rl[dc[1040110]][4]     -rl[dc[1040210]][4]+rl[dc[1040400]][4]*1+rl[dc[1040500]][4]*1+rl[dc[1040600]][4]*1+rl[dc[1040700]][4]*1+rl[dc[1050100]][4]*1+rl[dc[1050200]][4]*1+rl[dc[1050300]][4]*1+rl[dc[1060100]][4]*1", \
			item_formula1="rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]*1-rl[dc[1020710]][5]+rl[dc[1020200]][5]*1-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1+rl[dc[1040100]][5]-rl[dc[1040110]][5]-rl[dc[1040210]][5]+rl[dc[1040400]][5]*1+rl[dc[1040500]][5]*1+rl[dc[1040600]][5]*1+rl[dc[1040700]][5]*1+rl[dc[1050100]][5]*1+rl[dc[1050200]][5]*1+rl[dc[1050300]][5]*1+rl[dc[1060100]][5]*1") ,

    # 负债及所有者权益

            ReportItems(item_id=2010000, item_name=u"负债及所有者权益", report=r1) ,
            ReportItems(item_id=2020000, item_name=u"流动负债", report=r1) ,
            ReportItems(item_id=2020100, item_name=u"短期借款", report=r1) ,
            ReportItems(item_id=2020200, item_name=u"应付票据", report=r1) ,
            ReportItems(item_id=2020300, item_name=u"应付账款", report=r1) ,
            ReportItems(item_id=2020400, item_name=u"预收账款", report=r1,re_name=u"预收款项") ,
            ReportItems(item_id=2020500, item_name=u"应付工资", report=r1) ,
            ReportItems(item_id=2020600, item_name=u"应付福利费", report=r1) ,
            ReportItems(item_id=2020700, item_name=u"应付股利", report=r1) ,
            ReportItems(item_id=2020800, item_name=u"应付职工薪酬", report=r1) ,
            ReportItems(item_id=2020900, item_name=u"应交税金", report=r1,re_name=u"应交税费") ,
            
            ReportItems(item_id=2021000, item_name=u"其他应交款", report=r1) ,
            ReportItems(item_id=2021100, item_name=u"其他应付款", report=r1) ,
            ReportItems(item_id=2021200, item_name=u"预提费用", report=r1) ,
            ReportItems(item_id=2021300, item_name=u"预计负债", report=r1) ,
            ReportItems(item_id=2021400, item_name=u"一年内到期的长期负债", report=r1) ,
            ReportItems(item_id=2021500, item_name=u"其他流动负债", report=r1) ,
            ReportItems(item_id=2131000, item_name=u"流动负债合计", report=r1, item_formula="rl[dc[2020100]][4]*1+rl[dc[2020200]][4]*1+rl[dc[2020300]][4]*1+rl[dc[2020400]][4]*1+rl[dc[2020500]][4]*1+rl[dc[2020600]][4]*1+rl[dc[2020700]][4]*1+rl[dc[2020900]][4]*1+rl[dc[2021000]][4]*1+rl[dc[2021100]][4]*1+rl[dc[2021200]][4]*1+rl[dc[2021300]][4]*1+rl[dc[2021400]][4]*1+rl[dc[2021500]][4]*1", item_formula1="rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1") ,
            ReportItems(item_id=2140000, item_name=u"非流动负债", report=r1) ,
            ReportItems(item_id=2150000, item_name=u"长期负债", report=r1) ,
            ReportItems(item_id=2150100, item_name=u"长期借款", report=r1) ,
            ReportItems(item_id=2150200, item_name=u"应付债券", report=r1) ,
            ReportItems(item_id=2150300, item_name=u"长期应付款", report=r1) ,
            ReportItems(item_id=2150400, item_name=u"专项应付款", report=r1) ,
            ReportItems(item_id=2150500, item_name=u"其他长期负债", report=r1) ,
            ReportItems(item_id=2150510, item_name=u"特准储备基金", report=r1) ,
            ReportItems(item_id=2200000, item_name=u"长期负债合计", report=r1, item_formula="rl[dc[2150100]][4]*1+rl[dc[2150200]][4]*1+rl[dc[2150300]][4]*1+rl[dc[2150400]][4]*1+rl[dc[2150500]][4]*1", item_formula1="rl[dc[2150100]][5]*1+rl[dc[2150200]][5]*1+rl[dc[2150300]][5]*1+rl[dc[2150400]][5]*1+rl[dc[2150500]][5]*1") ,
            
            ReportItems(item_id=2300000, item_name=u"非流动负债合计", report=r1) ,
            ReportItems(item_id=2350000, item_name=u"递延税项", report=r1) ,
            ReportItems(item_id=2350100, item_name=u"递延税项贷项", report=r1) ,
            ReportItems(item_id=2400000, item_name=u"负债合计", report=r1, item_formula="rl[dc[2020100]][4]*1+rl[dc[2020200]][4]*1+rl[dc[2020300]][4]*1+rl[dc[2020400]][4]*1+rl[dc[2020500]][4]*1+rl[dc[2020600]][4]*1+rl[dc[2020700]][4]*1+rl[dc[2020900]][4]*1+rl[dc[2021000]][4]*1+rl[dc[2021100]][4]*1+rl[dc[2021200]][4]*1+rl[dc[2021300]][4]*1+rl[dc[2021400]][4]*1+rl[dc[2021500]][4]*1+rl[dc[2150100]][4]*1+rl[dc[2150200]][4]*1+rl[dc[2150300]][4]*1+rl[dc[2150400]][4]*1+rl[dc[2150500]][4]*1", item_formula1="rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1+rl[dc[2150100]][5]*1+rl[dc[2150200]][5]*1+rl[dc[2150300]][5]*1+rl[dc[2150400]][5]*1+rl[dc[2150500]][5]*1") ,

            ReportItems(item_id=3010000, item_name=u"少数股东权益", report=r1) ,
            ReportItems(item_id=3100000, item_name=u"少数股东权益", report=r1) ,
            ReportItems(item_id=4010000, item_name=u"所有者权益", report=r1) ,
            ReportItems(item_id=4020100, item_name=u"实收资本", report=r1,re_name=u"实收资本（或股本）", item_formula="rl[dc[4020110]][4]*1+rl[dc[4020120]][4]*1+rl[dc[4020130]][4]*1+rl[dc[4020140]][4]*1+rl[dc[4020150]][4]*1", item_formula1="rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1") ,
            ReportItems(item_id=4020110, item_name=u"国家资本", report=r1) ,
            ReportItems(item_id=4020120, item_name=u"集体资本", report=r1) ,
            ReportItems(item_id=4020130, item_name=u"法人资本", report=r1) ,
            ReportItems(item_id=4020131, item_name=u"国有法人资本", report=r1) ,
            ReportItems(item_id=4020132, item_name=u"集体法人资本", report=r1) ,
            ReportItems(item_id=4020140, item_name=u"个人资本", report=r1) ,
            ReportItems(item_id=4020150, item_name=u"外商资本", report=r1) ,
            ReportItems(item_id=4020200, item_name=u"资本公积", report=r1) ,
            ReportItems(item_id=4020300, item_name=u"减:库存股", report=r1) ,
            ReportItems(item_id=4020400, item_name=u"盈余公积", report=r1, item_formula="rl[dc[4020410]][4]*1+rl[dc[4020420]][4]*1+rl[dc[4020430]][4]*1", item_formula1="rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1") ,
            ReportItems(item_id=4020410, item_name=u"法定盈余公积", report=r1) ,
            ReportItems(item_id=4020420, item_name=u"公益金", report=r1) ,
            ReportItems(item_id=4020430, item_name=u"补充流动资本", report=r1) ,
            ReportItems(item_id=4020500, item_name=u"未确认的投资损失", report=r1) ,
            ReportItems(item_id=4020600, item_name=u"未分配利润", report=r1) ,
            ReportItems(item_id=4020700, item_name=u"外币报表折算差额", report=r1) ,
            ReportItems(item_id=4100000, item_name=u"所有者权益合计", report=r1,re_name=u"所有者权益（或股东权益）合计", item_formula="rl[dc[4020410]][4]*1+rl[dc[4020420]][4]*1+rl[dc[4020430]][4]*1+rl[dc[4020110]][4]*1+rl[dc[4020120]][4]*1+rl[dc[4020130]][4]*1+rl[dc[4020140]][4]*1+rl[dc[4020150]][4]*1+rl[dc[4020200]][4]*1+rl[dc[4020500]][4]*1+rl[dc[4020600]][4]*1+rl[dc[4020700]][4]*1", item_formula1="rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1+rl[dc[4020200]][5]*1+rl[dc[4020500]][5]*1+rl[dc[4020600]][5]*1+rl[dc[4020700]][5]*1") ,
            ReportItems(item_id=5100000, item_name=u"负债和所有者权益总计", report=r1,re_name=u"负债和所有者权益",  item_formula="rl[dc[4020410]][4]*1+rl[dc[4020420]][4]*1+rl[dc[4020430]][4]*1+rl[dc[4020110]][4]*1+rl[dc[4020120]][4]*1+rl[dc[4020130]][4]*1+rl[dc[4020140]][4]*1+rl[dc[4020150]][4]*1+rl[dc[4020200]][4]*1+rl[dc[4020500]][4]*1+rl[dc[4020600]][4]*1+rl[dc[4020700]][4]*1+rl[dc[2020100]][4]*1+rl[dc[2020200]][4]*1+rl[dc[2020300]][4]*1+rl[dc[2020400]][4]*1+rl[dc[2020500]][4]*1+rl[dc[2020600]][4]*1+rl[dc[2020700]][4]*1+rl[dc[2020900]][4]*1+rl[dc[2021000]][4]*1+rl[dc[2021100]][4]*1+rl[dc[2021200]][4]*1+rl[dc[2021300]][4]*1+rl[dc[2021400]][4]*1+rl[dc[2021500]][4]*1+rl[dc[2150100]][4]*1+rl[dc[2150200]][4]*1+rl[dc[2150300]][4]*1+rl[dc[2150400]][4]*1+rl[dc[2150500]][4]*1+rl[dc[3100000]][4]*1", \
			item_formula1="rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1+rl[dc[4020200]][5]*1+rl[dc[4020500]][5]*1+rl[dc[4020600]][5]*1+rl[dc[4020700]][5]*1+rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1+rl[dc[2150100]][5]*1+rl[dc[2150200]][5]*1+rl[dc[2150300]][5]*1+rl[dc[2150400]][5]*1+rl[dc[2150500]][5]*1+rl[dc[3100000]][5]*1") ,
            ReportItems(item_id=6100000, item_name=u"未结清对外担保余额", report=r1) ,






            ReportItems(item_id=10100000, item_name=u"一、主营业务收入", report=r2) ,
            ReportItems(item_id=11110100, item_name=u"出口产品销售收入", report=r2) ,
            ReportItems(item_id=11110200, item_name=u"进口产品销售收入", report=r2) ,
            ReportItems(item_id=11120300, item_name=u"折扣与折让", report=r2) ,
            ReportItems(item_id=12100000, item_name=u"二、主营业务收入净额", report=r2, item_formula="rl[dc[11010000]][4]-rl[dc[11120300]][4]", item_formula1="rl[dc[11010000]][5]-rl[dc[11120300]][5]") ,
            ReportItems(item_id=12110100, item_name=u"减：主营业务成本", report=r2) ,
            ReportItems(item_id=12110111, item_name=u"出口产品销售成本", report=r2) ,
            ReportItems(item_id=12110120, item_name=u"主营业务税金及附加", report=r2) ,
            ReportItems(item_id=12110130, item_name=u"经营费用", report=r2) ,
            ReportItems(item_id=12110140, item_name=u"其他费用", report=r2) ,
            ReportItems(item_id=12120100, item_name=u"递延收益", report=r2) ,
            ReportItems(item_id=12120110, item_name=u"代购代销收入", report=r2) ,
            ReportItems(item_id=12120120, item_name=u"其他收入", report=r2) ,
            ReportItems(item_id=13100000, item_name=u"三、主营业务利润", report=r2 ,re_name=u"二、主营业务利润（亏损以“-”号填列）", item_formula="rl[dc[11010000]][4]-rl[dc[11120300]][4]-rl[dc[12110100]][4]-rl[dc[12110100]][4]-rl[dc[12110120]][4]-rl[dc[12110130]][4]-rl[dc[12110140]][4]-rl[dc[12120100]][4]+rl[dc[12120110]][4]*1+rl[dc[12120120]][4]*1", item_formula1="rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1") ,
            ReportItems(item_id=13110100, item_name=u"加：其他业务利润", report=r2 ,re_name=u"加：其他业务利润（亏损以“-”号填列）") ,
            ReportItems(item_id=13110200, item_name=u"减：营业费用", report=r2) ,
            ReportItems(item_id=13110310, item_name=u"管理费用", report=r2) ,
            ReportItems(item_id=13110410, item_name=u"财务费用", report=r2) ,
            ReportItems(item_id=13110510, item_name=u"其他费用", report=r2) ,
            ReportItems(item_id=14100000, item_name=u"四、营业利润", report=r2 ,re_name=u"三、营业利润（亏损以“-”号填列）", item_formula="rl[dc[11010000]][4]-rl[dc[11120300]][4]-rl[dc[12110100]][4]-rl[dc[12110100]][4]-rl[dc[12110120]][4]-rl[dc[12110130]][4]-rl[dc[12110140]][4]-rl[dc[12120100]][4]+rl[dc[12120110]][4]*1+rl[dc[12120120]][4]*1+rl[dc[13110100]][4]*1-rl[dc[13110200]][4]-rl[dc[13110310]][4]-rl[dc[13110410]][4]-rl[dc[13110510]][4]", item_formula1="rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]") ,
            ReportItems(item_id=14110100, item_name=u"加:投资收益", report=r2 , re_name=u"加：投资收益（损失以“-”号填列）") ,
            ReportItems(item_id=14110210, item_name=u"期货收益", report=r2) ,
            ReportItems(item_id=14110310, item_name=u"补贴收入", report=r2) ,
            ReportItems(item_id=14110311, item_name=u"补贴前亏损的企业补贴收入", report=r2) ,
            ReportItems(item_id=14110410, item_name=u"营业外收入", report=r2) ,
            ReportItems(item_id=14110510, item_name=u"期中:处置固定资产净收益", report=r2) ,
            ReportItems(item_id=14110611, item_name=u"非货币性交易收益", report=r2) ,
            ReportItems(item_id=14110612, item_name=u"出售无形资产收益", report=r2) ,
            ReportItems(item_id=14110613, item_name=u"罚款净收入", report=r2) ,
            ReportItems(item_id=14110710, item_name=u"其他收入", report=r2) ,
            ReportItems(item_id=14110711, item_name=u"用以前年度含量工资节余弥补利润", report=r2) ,
            ReportItems(item_id=14110800, item_name=u"营业外支出", report=r2 ,re_name=u"减：营业外支出") ,
            ReportItems(item_id=14110810, item_name=u"期中:处置固定资产净损失", report=r2) ,
            ReportItems(item_id=14110821, item_name=u"债务重组损失", report=r2) ,
            ReportItems(item_id=14110831, item_name=u"罚款支出", report=r2) ,
            ReportItems(item_id=14110841, item_name=u"捐赠支出", report=r2) ,
            ReportItems(item_id=14110910, item_name=u"其他支出", report=r2) ,
            ReportItems(item_id=14111011, item_name=u"结转的含量工资包干节余", report=r2) ,
            ReportItems(item_id=14111100, item_name=u"以前年度损益调整", report=r2) ,

            ReportItems(item_id=15100000, item_name=u"五、利润总额", report=r2 ,re_name=u"四、利润总额（亏损总额以“-”号填列）", item_formula="rl[dc[11010000]][4]-rl[dc[11120300]][4]-rl[dc[12110100]][4]-rl[dc[12110100]][4]-rl[dc[12110120]][4]-rl[dc[12110130]][4]-rl[dc[12110140]][4]-rl[dc[12120100]][4]+rl[dc[12120110]][4]*1+rl[dc[12120120]][4]*1+rl[dc[13110100]][4]*1-rl[dc[13110200]][4]-rl[dc[13110310]][4]-rl[dc[13110410]][4]-rl[dc[13110510]][4]+rl[dc[14110100]][4]*1+rl[dc[14110210]][4]*1+rl[dc[14110310]][4]*1+rl[dc[14110410]][4]*1+rl[dc[14110710]][4]*1-rl[dc[14110800]][4]-rl[dc[14110910]][4]", item_formula1="(rl[dc[11010000]][5]-rl[dc[11120300]][5])-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5]"),
            ReportItems(item_id=15110100, item_name=u"减:所得税", report=r2) ,
            ReportItems(item_id=15110110, item_name=u"少数股东损益", report=r2) ,
            ReportItems(item_id=15110200, item_name=u"加:未确认的投资损失", report=r2) ,
            ReportItems(item_id=16100000, item_name=u"六:净利润", report=r2 , re_name=u"五、净利润（净亏损以“-”号填列）", item_formula="rl[dc[11010000]][4]-rl[dc[11120300]][4]-rl[dc[12110100]][4]-rl[dc[12110100]][4]-rl[dc[12110120]][4]-rl[dc[12110130]][4]-rl[dc[12110140]][4]-rl[dc[12120100]][4]+rl[dc[12120110]][4]*1+rl[dc[12120120]][4]*1+rl[dc[13110100]][4]*1-rl[dc[13110200]][4]-rl[dc[13110310]][4]-rl[dc[13110410]][4]-rl[dc[13110510]][4]+rl[dc[14110100]][4]*1+rl[dc[14110210]][4]*1+rl[dc[14110310]][4]*1+rl[dc[14110410]][4]*1+rl[dc[14110710]][4]*1-rl[dc[14110800]][4]-rl[dc[14110910]][4]-rl[dc[15110100]][4]-rl[dc[15110110]][4]+rl[dc[15110200]][4]*1", item_formula1="rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5]-rl[dc[15110100]][5]-rl[dc[15110110]][5]+rl[dc[15110200]][5]*1"),
            ReportItems(item_id=16110100, item_name=u"加:年初未分配利润", report=r2) ,
            ReportItems(item_id=16110110, item_name=u"盈余公积补亏", report=r2) ,
            ReportItems(item_id=16110120, item_name=u"其他调整因素", report=r2) ,
            ReportItems(item_id=17100000, item_name=u"七:可供分配的利润", report=r2, item_formula="rl[dc[11010000]][4]-rl[dc[11120300]][4]-rl[dc[12110100]][4]-rl[dc[12110100]][4]-rl[dc[12110120]][4]-rl[dc[12110130]][4]-rl[dc[12110140]][4]-rl[dc[12120100]][4]+rl[dc[12120110]][4]*1+rl[dc[12120120]][4]*1+rl[dc[13110100]][4]*1-rl[dc[13110200]][4]-rl[dc[13110310]][4]-rl[dc[13110410]][4]-rl[dc[13110510]][4]+rl[dc[14110100]][4]*1+rl[dc[14110210]][4]*1+rl[dc[14110310]][4]*1+rl[dc[14110410]][4]*1+rl[dc[14110710]][4]*1-rl[dc[14110800]][4]-rl[dc[14110910]][4]-rl[dc[15110100]][4]-rl[dc[15110110]][4]+rl[dc[15110200]][4]*1+rl[dc[16110100]][4]*1-rl[dc[16110110]][4]*1+rl[dc[16110120]][4]*1", item_formula1="rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5]-rl[dc[15110100]][5]-rl[dc[15110110]][5]+rl[dc[15110200]][5]*1+rl[dc[16110100]][5]*1-rl[dc[16110110]][5]*1+rl[dc[16110120]][5]*1"),
            ReportItems(item_id=17110100, item_name=u"减:单项留用的利润", report=r2) ,
            ReportItems(item_id=17110110, item_name=u"补充流动资本", report=r2) ,
            ReportItems(item_id=17110120, item_name=u"提取法定盈余公积", report=r2) ,
            ReportItems(item_id=17110130, item_name=u"提取法定公益金", report=r2) ,
            ReportItems(item_id=17110140, item_name=u"提取职工奖励及福利基金", report=r2) ,
            ReportItems(item_id=17110150, item_name=u"提取储备基金", report=r2) ,
            ReportItems(item_id=17110160, item_name=u"提取企业发展基金", report=r2) ,
            ReportItems(item_id=17110170, item_name=u"利润归还投资", report=r2) ,
            ReportItems(item_id=17110180, item_name=u"其他", report=r2) ,
            ReportItems(item_id=18100000, item_name=u"可供投资者分配的利润", report=r2, item_formula="rl[dc[11010000]][4]-rl[dc[11120300]][4]-rl[dc[12110100]][4]-rl[dc[12110100]][4]-rl[dc[12110120]][4]-rl[dc[12110130]][4]-rl[dc[12110140]][4]-rl[dc[12120100]][4]+rl[dc[12120110]][4]*1+rl[dc[12120120]][4]*1+rl[dc[13110100]][4]*1-rl[dc[13110200]][4]-rl[dc[13110310]][4]-rl[dc[13110410]][4]-rl[dc[13110510]][4]+rl[dc[14110100]][4]*1+rl[dc[14110210]][4]*1+rl[dc[14110310]][4]*1+rl[dc[14110410]][4]*1+rl[dc[14110710]][4]*1-rl[dc[14110800]][4]-rl[dc[14110910]][4]-rl[dc[15110100]][4]-rl[dc[15110110]][4]+rl[dc[15110200]][4]*1-rl[dc[17110100]][4]-rl[dc[17110110]][4]-rl[dc[17110120]][4]-rl[dc[17110130]][4]-rl[dc[17110140]][4]-rl[dc[17110150]][4]-rl[dc[17110160]][4]-rl[dc[17110170]][4]-rl[dc[17110180]][4]", item_formula1="rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5]-rl[dc[15110100]][5]-rl[dc[15110110]][5]+rl[dc[15110200]][5]*1-rl[dc[17110100]][5]-rl[dc[17110110]][5]-rl[dc[17110120]][5]-rl[dc[17110130]][5]-rl[dc[17110140]][5]-rl[dc[17110150]][5]-rl[dc[17110160]][5]-rl[dc[17110170]][5]-rl[dc[17110180]][5]"),
            ReportItems(item_id=18110100, item_name=u"减:应付优先股股利", report=r2) ,
            ReportItems(item_id=18110110, item_name=u"提取任意盈余公积", report=r2) ,
            ReportItems(item_id=18110120, item_name=u"应付普通股股利", report=r2) ,
            ReportItems(item_id=18110130, item_name=u"转作资本的普通股股利", report=r2) ,
            ReportItems(item_id=18110140, item_name=u"其他", report=r2) ,
            ReportItems(item_id=19000000, item_name=u"未分配利润", report=r2, item_formula="rl[dc[11010000]][4]-rl[dc[11120300]][4]-rl[dc[12110100]][4]-rl[dc[12110100]][4]-rl[dc[12110120]][4]-rl[dc[12110130]][4]-rl[dc[12110140]][4]-rl[dc[12120100]][4]+rl[dc[12120110]][4]*1+rl[dc[12120120]][4]*1+rl[dc[13110100]][4]*1-rl[dc[13110200]][4]-rl[dc[13110310]][4]-rl[dc[13110410]][4]-rl[dc[13110510]][4]+rl[dc[14110100]][4]*1+rl[dc[14110210]][4]*1+rl[dc[14110310]][4]*1+rl[dc[14110410]][4]*1+rl[dc[14110710]][4]*1-rl[dc[14110800]][4]-rl[dc[14110910]][4]-rl[dc[15110100]][4]-rl[dc[15110110]][4]+rl[dc[15110200]][4]*1-rl[dc[17110100]][4]-rl[dc[17110110]][4]-rl[dc[17110120]][4]-rl[dc[17110130]][4]-rl[dc[17110140]][4]-rl[dc[17110150]][4]-rl[dc[17110160]][4]-rl[dc[17110170]][4]-rl[dc[17110180]][4]-rl[dc[18110100]][4]-rl[dc[18110110]][4]-rl[dc[18110120]][4]-rl[dc[18110130]][4]-rl[dc[18110140]][4]", item_formula1="rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5]-rl[dc[15110100]][5]-rl[dc[15110110]][5]+rl[dc[15110200]][5]*1-rl[dc[17110100]][5]-rl[dc[17110110]][5]-rl[dc[17110120]][5]-rl[dc[17110130]][5]-rl[dc[17110140]][5]-rl[dc[17110150]][5]-rl[dc[17110160]][5]-rl[dc[17110170]][5]-rl[dc[17110180]][5]-rl[dc[18110100]][5]-rl[dc[18110110]][5]-rl[dc[18110120]][5]-rl[dc[18110130]][5]-rl[dc[18110140]][5]"),
            ReportItems(item_id=19010100, item_name=u"应由以后年度税前利润弥补的亏损", report=r2) ,


            #旧现金流量表
            ReportItems(item_id=21100000, item_name=u"一、经营活动产生的现金流量", report=r3),
            ReportItems(item_id=21110100, item_name=u"销售商品、提供劳务收到的现金", report=r3, item_formula="rl[dc[10100000]][5]*1+rl[dc[2020400]][5]*1-rl[dc[1020900]][4]-(rl[dc[1020700]][5]-rl[dc[1020700]][4]+rl[dc[1020400]][5]*1-rl[dc[1020400]][4]+rl[dc[1021300]][5]*1-rl[dc[1021300]][4]+rl[dc[1021100]][5]*1-rl[dc[1021100]][4])") ,
            ReportItems(item_id=21110200, item_name=u"收到的税费返还", report=r3, item_formula="rl[dc[10100000]][5]*0.17"),
            ReportItems(item_id=21110300, item_name=u"收到的其他与经营活动有关的现金", report=r3, item_formula="rl[dc[13110100]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110310]][5]*1-rl[dc[14110800]][5]"),
            ReportItems(item_id=21110311, item_name=u"经营活动现金流入小计", report=r3, item_formula="rl[dc[10100000]][5]*1+rl[dc[2020400]][5]*1-rl[dc[1020900]][4]-(rl[dc[1020700]][5]-rl[dc[1020700]][4]+rl[dc[1020400]][5]*1-rl[dc[1020400]][4]+rl[dc[1021300]][5]*1-rl[dc[1021300]][4]+rl[dc[1021100]][5]*1-rl[dc[1021100]][4])+rl[dc[10100000]][5]*0.17+rl[dc[13110100]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110310]][5]*1-rl[dc[14110800]][5]"),
            ReportItems(item_id=21110400, item_name=u"购买商品、接受劳务支付的现金", report=r3, item_formula="rl[dc[12110100]][5]*1+rl[dc[1021400]][5]*1-rl[dc[1021400]][4]+rl[dc[1021900]][5]*1-rl[dc[1021900]][4]+rl[dc[1021700]][5]*1-rl[dc[1021700]][4]+rl[dc[1020900]][5]*1-rl[dc[1020900]][4]+rl[dc[2020300]][5]*1-rl[dc[2020300]][4]+rl[dc[2020200]][5]*1-rl[dc[2020200]][4]+rl[dc[2021000]][5]*1-rl[dc[2021000]][4]+rl[dc[2150300]][5]*1-rl[dc[2150300]][4]"),
            ReportItems(item_id=21110500, item_name=u"支付给职工以及为职工支付的现金", report=r3, item_formula="(rl[dc[2020900]][4]*1+rl[dc[2020900]][5]*1)/2/0.14*1.02"),
            ReportItems(item_id=21110600, item_name=u"支付的各项税费", report=r3, item_formula="rl[dc[12110120]][5]*1+rl[dc[15110100]][5]*1-(rl[dc[2020900]][5]-rl[dc[2020900]][4])"),
            ReportItems(item_id=21110700, item_name=u"支付的其他与经营活动有关的现金", report=r3, item_formula="rl[dc[13110200]][5]*1+rl[dc[1021600]][5]*1-rl[dc[1021600]][4]+(rl[dc[1040110]][5]*1-rl[dc[1040110]][4]+rl[dc[2021200]][5]*1-rl[dc[2021200]][4]+rl[dc[2020500]][5]*1-rl[dc[2020500]][4]+rl[dc[2020600]][5]*1-rl[dc[2020600]][4]+rl[dc[2021000]][5]*1-rl[dc[2021000]][4])+rl[dc[13110310]][5]*1"),
            ReportItems(item_id=21110711, item_name=u"经营活动现金流出小计", report=r3, item_formula="rl[dc[12110100]][5]*1+rl[dc[1021400]][5]*1-rl[dc[1021400]][4]+rl[dc[1021900]][5]*1-rl[dc[1021900]][4]+rl[dc[1021700]][5]*1-rl[dc[1021700]][4]+rl[dc[1020900]][5]*1-rl[dc[1020900]][4]+rl[dc[2020300]][5]*1-rl[dc[2020300]][4]+rl[dc[2020200]][5]*1-rl[dc[2020200]][4]+rl[dc[2021000]][5]*1-rl[dc[2021000]][4]+rl[dc[2150300]][5]*1-rl[dc[2150300]][4]+(rl[dc[2020900]][4]*1+rl[dc[2020900]][5]*1)/2/0.14*1.02+rl[dc[12110120]][5]*1+rl[dc[15110100]][5]*1-(rl[dc[2020900]][5]-rl[dc[2020900]][4])+rl[dc[13110200]][5]*1+rl[dc[1021600]][5]*1-rl[dc[1021600]][4]+(rl[dc[1040110]][5]*1-rl[dc[1040110]][4]+rl[dc[2021200]][5]*1-rl[dc[2021200]][4]+rl[dc[2020500]][5]*1-rl[dc[2020500]][4]+rl[dc[2020600]][5]*1-rl[dc[2020600]][4]+rl[dc[2021000]][5]*1-rl[dc[2021000]][4])+rl[dc[13110310]][5]*1"),
            ReportItems(item_id=21110800, item_name=u"经营活动产生的现金流量净额", report=r3, item_formula="(rl[dc[10100000]][5]*1+rl[dc[2020400]][5]*1-rl[dc[1020900]][4]-(rl[dc[1020700]][5]-rl[dc[1020700]][4]+rl[dc[1020400]][5]*1-rl[dc[1020400]][4]+rl[dc[1021300]][5]*1-rl[dc[1021300]][4]+rl[dc[1021100]][5]*1-rl[dc[1021100]][4])+rl[dc[10100000]][5]*0.17+rl[dc[13110100]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110310]][5]*1-rl[dc[14110800]][5])-(rl[dc[12110100]][5]*1+rl[dc[1021400]][5]*1-rl[dc[1021400]][4]+rl[dc[1021900]][5]*1-rl[dc[1021900]][4]+rl[dc[1021700]][5]*1-rl[dc[1021700]][4]+rl[dc[1020900]][5]*1-rl[dc[1020900]][4]+rl[dc[2020300]][5]*1-rl[dc[2020300]][4]+rl[dc[2020200]][5]*1-rl[dc[2020200]][4]+rl[dc[2021000]][5]*1-rl[dc[2021000]][4]+rl[dc[2150300]][5]*1-rl[dc[2150300]][4]+(rl[dc[2020900]][4]*1+rl[dc[2020900]][5]*1)/2/0.14*1.02+rl[dc[12110120]][5]*1+rl[dc[15110100]][5]*1-(rl[dc[2020900]][5]-rl[dc[2020900]][4])+rl[dc[13110200]][5]*1+rl[dc[1021600]][5]*1-rl[dc[1021600]][4]+(rl[dc[1040110]][5]*1-rl[dc[1040110]][4]+rl[dc[2021200]][5]*1-rl[dc[2021200]][4]+rl[dc[2020500]][5]*1-rl[dc[2020500]][4]+rl[dc[2020600]][5]*1-rl[dc[2020600]][4]+rl[dc[2021000]][5]*1-rl[dc[2021000]][4])+rl[dc[13110310]][5]*1)"),
            ReportItems(item_id=22010000, item_name=u"投资活动产生的现金流量", report=r3) ,
            ReportItems(item_id=22110100, item_name=u"收回投资所收到的现金", report=r3, item_formula="rl[dc[14110100]][5]"),
            ReportItems(item_id=22110200, item_name=u"取得投资收益所收到的现金", report=r3) ,
            ReportItems(item_id=22110300, item_name=u"处置固定、无形和其他长期资产所收回的现金净额", report=r3) ,
            ReportItems(item_id=22110400, item_name=u"收到的其他与投资活动有关的现金", report=r3) ,
            ReportItems(item_id=22110411, item_name=u"投资活动现金流入小计", report=r3, item_formula="(rl[dc[14110100]][5])+rl[dc[22110200]][4]*1+rl[dc[22110300]][4]*1+rl[dc[22110400]][4]*1"),
            ReportItems(item_id=22110500, item_name=u"投资所支付的现金", report=r3) ,
            ReportItems(item_id=22110600, item_name=u"购建固定资产、无形资产和其他长期资产所支付的现金", report=r3) ,
            ReportItems(item_id=22110700, item_name=u"支付的其他与投资活动有关的现金", report=r3) ,
            ReportItems(item_id=22110711, item_name=u"投资活动现金流出小计", report=r3, item_formula="rl[dc[22110600]][4]*1+rl[dc[22110500]][4]*1+rl[dc[22110700]][4]*1"),
            ReportItems(item_id=22110800, item_name=u"投资活动产生的现金流量净额", report=r3, item_formula="((rl[dc[14110100]][5])+rl[dc[22110200]][4]*1+rl[dc[22110300]][4]*1+rl[dc[22110400]][4]*1)-(rl[dc[22110600]][4]*1+rl[dc[22110500]][4]*1+rl[dc[22110700]][4]*1)"),

            ReportItems(item_id=23010000, item_name=u"筹资活动产生的现金流量", report=r3) ,
            ReportItems(item_id=23110100, item_name=u"吸收投资所收到的现金", report=r3, item_formula="(rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1)-(rl[dc[4020110]][4]*1+rl[dc[4020120]][4]*1+rl[dc[4020130]][4]*1+rl[dc[4020140]][4]*1+rl[dc[4020150]][4]*1)"),
            ReportItems(item_id=23110200, item_name=u"借款所收到的现金", report=r3) ,
            ReportItems(item_id=23110300, item_name=u"收到的其他与筹资活动有关的现金", report=r3, item_formula="rl[dc[4020200]][5]-rl[dc[4020200]][4]"),
            ReportItems(item_id=23110311, item_name=u"筹资活动现金流入小计", report=r3,  item_formula="(rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1)-(rl[dc[4020110]][4]*1+rl[dc[4020120]][4]*1+rl[dc[4020130]][4]*1+rl[dc[4020140]][4]*1+rl[dc[4020150]][4]*1)+rl[dc[23110200]][4]*1+rl[dc[4020200]][5]*1-rl[dc[4020200]][4]"),
            ReportItems(item_id=23110400, item_name=u"偿还债务所支付的现金", report=r3) ,
            ReportItems(item_id=23110500, item_name=u"分配股利、利润或偿付利息所支付的现金", report=r3, item_formula="rl[dc[13110410]][5]*1+(rl[dc[11010000]][5]-rl[dc[11120300]][5])-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5]-rl[dc[15110100]][5]-rl[dc[15110110]][5]+rl[dc[15110200]][5]*1-(rl[dc[4020600]][5]-rl[dc[4020600]][4])+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1-(rl[dc[4020410]][4]*1+rl[dc[4020420]][4]*1+rl[dc[4020430]][4]*1)+rl[dc[2020700]][5]*1-rl[dc[2020700]][4]"),
            ReportItems(item_id=23110600, item_name=u"支付的其他与筹资活动有关的现金", report=r3) ,
            ReportItems(item_id=23110611, item_name=u"筹资活动现金流出小计", report=r3, item_formula="rl[dc[23110400]][4]*1+rl[dc[13110410]][5]*1+(rl[dc[11010000]][5]-rl[dc[11120300]][5])-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5]-rl[dc[15110100]][5]-rl[dc[15110110]][5]+rl[dc[15110200]][5]*1-(rl[dc[4020600]][5]-rl[dc[4020600]][4])+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1-(rl[dc[4020410]][4]*1+rl[dc[4020420]][4]*1+rl[dc[4020430]][4]*1)+rl[dc[2020700]][5]*1-rl[dc[2020700]][4]+rl[dc[23110600]][4]*1"),
            ReportItems(item_id=23110700, item_name=u"筹资活动产生的现金流量净额", report=r3, item_formula="((rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1)-(rl[dc[4020110]][4]*1+rl[dc[4020120]][4]*1+rl[dc[4020130]][4]*1+rl[dc[4020140]][4]*1+rl[dc[4020150]][4]*1)+rl[dc[23110200]][4]*1+rl[dc[4020200]][5]*1-rl[dc[4020200]][4])-(rl[dc[23110400]][4]*1+rl[dc[13110410]][5]*1+(rl[dc[11010000]][5]-rl[dc[11120300]][5])-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5]-rl[dc[15110100]][5]-rl[dc[15110110]][5]+rl[dc[15110200]][5]*1-(rl[dc[4020600]][5]-rl[dc[4020600]][4])+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1-(rl[dc[4020410]][4]*1+rl[dc[4020420]][4]*1+rl[dc[4020430]][4]*1)+rl[dc[2020700]][5]*1-rl[dc[2020700]][4]+rl[dc[23110600]][4]*1)"),
            ReportItems(item_id=24000000, item_name=u"汇率变动对现金的影响", report=r3) ,
            ReportItems(item_id=25000000, item_name=u"现金及现金等价物净增加额", report=r3, item_formula="(rl[dc[10100000]][5]*1+rl[dc[2020400]][5]*1-rl[dc[1020900]][4]-(rl[dc[1020700]][5]-rl[dc[1020700]][4]+rl[dc[1020400]][5]*1-rl[dc[1020400]][4]+rl[dc[1021300]][5]*1-rl[dc[1021300]][4]+rl[dc[1021100]][5]*1-rl[dc[1021100]][4])+rl[dc[10100000]][5]*0.17+rl[dc[13110100]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110310]][5]*1-rl[dc[14110800]][5])-(rl[dc[12110100]][5]*1+rl[dc[1021400]][5]*1-rl[dc[1021400]][4]+rl[dc[1021900]][5]*1-rl[dc[1021900]][4]+rl[dc[1021700]][5]*1-rl[dc[1021700]][4]+rl[dc[1020900]][5]*1-rl[dc[1020900]][4]+rl[dc[2020300]][5]*1-rl[dc[2020300]][4]+rl[dc[2020200]][5]*1-rl[dc[2020200]][4]+rl[dc[2021000]][5]*1-rl[dc[2021000]][4]+rl[dc[2150300]][5]*1-rl[dc[2150300]][4]+(rl[dc[2020900]][4]*1+rl[dc[2020900]][5]*1)/2/0.14*1.02+rl[dc[12110120]][5]*1+rl[dc[15110100]][5]*1-(rl[dc[2020900]][5]-rl[dc[2020900]][4])+rl[dc[13110200]][5]*1+rl[dc[1021600]][5]*1-rl[dc[1021600]][4]+(rl[dc[1040110]][5]*1-rl[dc[1040110]][4]+rl[dc[2021200]][5]*1-rl[dc[2021200]][4]+rl[dc[2020500]][5]*1-rl[dc[2020500]][4]+rl[dc[2020600]][5]*1-rl[dc[2020600]][4]+rl[dc[2021000]][5]*1-rl[dc[2021000]][4])+rl[dc[13110310]][5]*1)+((rl[dc[14110100]][5])+rl[dc[22110200]][4]*1+rl[dc[22110300]][4]*1+rl[dc[22110400]][4]*1)-(rl[dc[22110600]][4]*1+rl[dc[22110500]][4]*1+rl[dc[22110700]][4]*1)+((rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1)-(rl[dc[4020110]][4]*1+rl[dc[4020120]][4]*1+rl[dc[4020130]][4]*1+rl[dc[4020140]][4]*1+rl[dc[4020150]][4]*1)+rl[dc[23110200]][4]*1+rl[dc[4020200]][5]*1-rl[dc[4020200]][4])-(rl[dc[23110400]][4]*1+rl[dc[13110410]][5]*1+(rl[dc[11010000]][5]-rl[dc[11120300]][5])-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5]-rl[dc[15110100]][5]-rl[dc[15110110]][5]+rl[dc[15110200]][5]*1-(rl[dc[4020600]][5]-rl[dc[4020600]][4])+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1-(rl[dc[4020410]][4]*1+rl[dc[4020420]][4]*1+rl[dc[4020430]][4]*1)+rl[dc[2020700]][5]*1-rl[dc[2020700]][4]+rl[dc[23110600]][4]*1)"),
     # 旧系统没有的
            ReportItems(item_id=25010000, item_name=u"将净利润调节为经营活动现金流量：", report=r3) ,
            ReportItems(item_id=25010100, item_name=u"净利润", report=r3) ,
            ReportItems(item_id=25010101, item_name=u"计提的资产减值准备", report=r3) ,
            ReportItems(item_id=25010102, item_name=u"固定资产折旧", report=r3) ,
            ReportItems(item_id=25010103, item_name=u"无形资产摊销", report=r3) ,
            ReportItems(item_id=25010104, item_name=u"长期待摊费用摊销", report=r3) ,
            ReportItems(item_id=25010105, item_name=u"待摊费用减少", report=r3) ,
            ReportItems(item_id=25010106, item_name=u"预提费用增加", report=r3) ,
            ReportItems(item_id=25010107, item_name=u"处置固定资产、无形资产和其他长期资产的损失", report=r3) ,
            ReportItems(item_id=25010108, item_name=u"固定资产报废损失", report=r3) ,
            ReportItems(item_id=25010110, item_name=u"财务费用", report=r3) ,
            ReportItems(item_id=25010111, item_name=u"投资损失", report=r3) ,
            ReportItems(item_id=25010112, item_name=u"递延税款贷项", report=r3) ,
            ReportItems(item_id=25010113, item_name=u"存货的减少", report=r3) ,
            ReportItems(item_id=25010114, item_name=u"经营性应收项目的减少", report=r3) ,
            ReportItems(item_id=25010115, item_name=u"经营性应付项目的增加", report=r3) ,
            ReportItems(item_id=25010116, item_name=u"其他", report=r3) ,
            ReportItems(item_id=25010117, item_name=u"经营活动产生的现金流量净额", report=r3) ,
            ReportItems(item_id=25020000, item_name=u"不涉及现金收支的投资和筹资活动：", report=r3) ,
            ReportItems(item_id=25020100, item_name=u"债务转为资本", report=r3) ,
            ReportItems(item_id=25020200, item_name=u"一年内到期的可转换公司债券", report=r3) ,
            ReportItems(item_id=25020300, item_name=u"融资租入固定资产", report=r3) ,
            ReportItems(item_id=25020400, item_name=u"其他", report=r3) ,
            ReportItems(item_id=25030000, item_name=u"现金及现金等价物净增加情况：", report=r3) ,
            ReportItems(item_id=25030100, item_name=u"现金的期末余额", report=r3) ,
            ReportItems(item_id=25030200, item_name=u"现金的期初余额", report=r3) ,
            ReportItems(item_id=25030300, item_name=u"现金等价物的期末余额", report=r3) ,
            ReportItems(item_id=25030400, item_name=u"现金等价物的期初余额", report=r3) ,
            ReportItems(item_id=25030500, item_name=u"现金及现金等价物净增加额", report=r3) ,
     # -------
            ReportItems(item_id=31010000, item_name=u"盈利能力分析指标", report=r4) ,
            ReportItems(item_id=31110100, item_name=u"销售利润率", report=r4, item_formula="(rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1)/(rl[dc[10100000]][5])*100"),
            ReportItems(item_id=31110200, item_name=u"营业利润率", report=r4, item_formula="(rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5])/rl[dc[10100000]][5]*100"),
            ReportItems(item_id=31110300, item_name=u"税前利润率", report=r4, item_formula="(rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5])/rl[dc[10100000]][5]*100"),
            ReportItems(item_id=31110400, item_name=u"销售净利润率", report=r4, item_formula="(rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5]-rl[dc[15110100]][5]-rl[dc[15110110]][5]+rl[dc[15110200]][5]*1)/rl[dc[10100000]][5]*100"),
            ReportItems(item_id=31110500, item_name=u"成本费用利润率", report=r4, item_formula="(rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5])/(rl[dc[12110100]][5]+rl[dc[12110130]][5]*1+rl[dc[13110200]][5]*1+rl[dc[13110310]][5]*1+rl[dc[13110410]][5]*1)*100"),
            ReportItems(item_id=31110600, item_name=u"资产收益率", report=r4, item_formula="(rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5])/(rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1+rl[dc[1040100]][5]-rl[dc[1040110]][5]-rl[dc[1040210]][5]+rl[dc[1040400]][5]*1+rl[dc[1040500]][5]*1+rl[dc[1040600]][5]*1+rl[dc[1040700]][5]*1+rl[dc[1050100]][5]*1+rl[dc[1050200]][5]*1+rl[dc[1050300]][5]*1+rl[dc[1060100]][5]*1)*100"),
            ReportItems(item_id=31110700, item_name=u"净资产收益率", report=r4, item_formula="(rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5]-rl[dc[15110100]][5]-rl[dc[15110110]][5]+rl[dc[15110200]][5]*1)*2/((rl[dc[4020410]][4]*1+rl[dc[4020420]][4]*1+rl[dc[4020430]][4]*1+rl[dc[4020110]][4]*1+rl[dc[4020120]][4]*1+rl[dc[4020130]][4]*1+rl[dc[4020140]][4]*1+rl[dc[4020150]][4]*1+rl[dc[4020200]][4]*1+rl[dc[4020500]][4]*1+rl[dc[4020600]][4]*1+rl[dc[4020700]][4]*1)+(rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1+rl[dc[4020200]][5]*1+rl[dc[4020500]][5]*1+rl[dc[4020600]][5]*1+rl[dc[4020700]][5]*1))*100"),
			ReportItems(item_id=31110800, item_name=u"总资产报酬率", report=r4, item_formula="(rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5]+rl[dc[13110410]][5]*1)/(rl[dc[1021400]][4]-rl[dc[1021430]][4]+rl[dc[1020700]][4]-rl[dc[1020710]][4]+rl[dc[1020200]][4]-rl[dc[1020210]][4]+rl[dc[1020100]][4]*1+rl[dc[1020400]][4]*1+rl[dc[1020500]][4]*1+rl[dc[1020600]][4]*1+rl[dc[1020900]][4]*1+rl[dc[1021000]][4]*1+rl[dc[1021100]][4]*1+rl[dc[1021200]][4]*1+rl[dc[1021300]][4]*1+rl[dc[1021600]][4]*1+rl[dc[1021700]][4]*1+rl[dc[1021800]][4]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][4]*1+rl[dc[1030200]][4]*1+rl[dc[1040100]][4]-rl[dc[1040110]][4]-rl[dc[1040210]][4]+rl[dc[1040400]][4]*1+rl[dc[1040500]][4]*1+rl[dc[1040600]][4]*1+rl[dc[1040700]][4]*1+rl[dc[1050100]][4]*1+rl[dc[1050200]][4]*1+rl[dc[1050300]][4]*1+rl[dc[1060100]][4]*1+rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1+rl[dc[1040100]][5]-rl[dc[1040110]][5]-rl[dc[1040210]][5]+rl[dc[1040400]][5]*1+rl[dc[1040500]][5]*1+rl[dc[1040600]][5]*1+rl[dc[1040700]][5]*1+rl[dc[1050100]][5]*1+rl[dc[1050200]][5]*1+rl[dc[1050300]][5]*1+rl[dc[1060100]][5]*1)*2*100"),
            ReportItems(item_id=31110900, item_name=u"投资收益率", report=r4, item_formula="rl[dc[14110100]][5]/(rl[dc[1020200]][5]*1+rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1)*100"),
            ReportItems(item_id=31111000, item_name=u"主营收入现金率", report=r4, item_formula="(rl[dc[10100000]][5]*1+rl[dc[2020400]][5]*1-rl[dc[1020900]][4]-(rl[dc[1020700]][5]-rl[dc[1020700]][4]+rl[dc[1020400]][5]*1-rl[dc[1020400]][4]+rl[dc[1021300]][5]*1-rl[dc[1021300]][4]+rl[dc[1021100]][5]*1-rl[dc[1021100]][4])+rl[dc[10100000]][5]*0.17+rl[dc[13110100]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110310]][5]*1-rl[dc[14110800]][5])/rl[dc[10100000]][5]*100"),
            ReportItems(item_id=31111100, item_name=u"毛利率", report=r4, item_formula="(rl[dc[10100000]][5]-rl[dc[12110100]][5])/rl[dc[10100000]][5]*100"),
            ReportItems(item_id=31111200, item_name=u"投资收益现金率", report=r4, item_formula="rl[dc[22110200]][4]/rl[dc[14110100]][5]*100"),
            ReportItems(item_id=32010000, item_name=u"营运能力分析指标", report=r4),
            ReportItems(item_id=32110100, item_name=u"总资产周转率(次)", report=r4, item_formula="rl[dc[10100000]][5]/(rl[dc[1021400]][4]-rl[dc[1021430]][4]+rl[dc[1020700]][4]-rl[dc[1020710]][4]+rl[dc[1020200]][4]-rl[dc[1020210]][4]+rl[dc[1020100]][4]*1+rl[dc[1020400]][4]*1+rl[dc[1020500]][4]*1+rl[dc[1020600]][4]*1+rl[dc[1020900]][4]*1+rl[dc[1021000]][4]*1+rl[dc[1021100]][4]*1+rl[dc[1021200]][4]*1+rl[dc[1021300]][4]*1+rl[dc[1021600]][4]*1+rl[dc[1021700]][4]*1+rl[dc[1021800]][4]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][4]*1+rl[dc[1030200]][4]*1+  rl[dc[1040100]][4]-rl[dc[1040110]][4]     -rl[dc[1040210]][4]+rl[dc[1040400]][4]*1+rl[dc[1040500]][4]*1+rl[dc[1040600]][4]*1+rl[dc[1040700]][4]*1+rl[dc[1050100]][4]*1+rl[dc[1050200]][4]*1+rl[dc[1050300]][4]*1+rl[dc[1060100]][4]*1+rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1+rl[dc[1040100]][5]-rl[dc[1040110]][5]-rl[dc[1040210]][5]+rl[dc[1040400]][5]*1+rl[dc[1040500]][5]*1+rl[dc[1040600]][5]*1+rl[dc[1040700]][5]*1+rl[dc[1050100]][5]*1+rl[dc[1050200]][5]*1+rl[dc[1050300]][5]*1+rl[dc[1060100]][5]*1)*2*100"),
            ReportItems(item_id=32110200, item_name=u"固定资产周转率(次)", report=r4, item_formula="rl[dc[10100000]][5]/(rl[dc[1040100]][4]-rl[dc[1040110]][4]+rl[dc[1040100]][5]-rl[dc[1040110]][5])*2*100"),
            ReportItems(item_id=32110300, item_name=u"流动资产周转率(次)", report=r4, item_formula="rl[dc[10100000]][5]/(rl[dc[1021400]][4]-rl[dc[1021430]][4]+rl[dc[1020700]][4]-rl[dc[1020710]][4]+rl[dc[1020200]][4]-rl[dc[1020210]][4]+rl[dc[1020100]][4]*1+rl[dc[1020400]][4]*1+rl[dc[1020500]][4]*1+rl[dc[1020600]][4]*1+rl[dc[1020900]][4]*1+rl[dc[1021000]][4]*1+rl[dc[1021100]][4]*1+rl[dc[1021200]][4]*1+rl[dc[1021300]][4]*1+rl[dc[1021600]][4]*1+rl[dc[1021700]][4]*1+rl[dc[1021800]][4]*1+rl[dc[1021900]][5]*1+rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1)*2*100"),
            ReportItems(item_id=32110400, item_name=u"应收帐款周转率(次)", report=r4, item_formula="rl[dc[10100000]][5]/(rl[dc[1020700]][4]*1+rl[dc[1020700]][5]*1)*2"),
            ReportItems(item_id=32110500, item_name=u"存货周转率(次)", report=r4, item_formula="rl[dc[10100000]][5]/(rl[dc[1021400]][4]*1+rl[dc[1021400]][5]*1)*2"),
            ReportItems(item_id=32110600, item_name=u"权益报酬率", report=r4, item_formula="(rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5])/((rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1+rl[dc[4020200]][5]*1+rl[dc[4020500]][5]*1+rl[dc[4020600]][5]*1+rl[dc[4020700]][5]*1)-rl[dc[1050100]][5])*100"),
            ReportItems(item_id=32110700, item_name=u"商品销售率", report=r4, item_formula="(rl[dc[1021400]][4]*1+(rl[dc[12110100]][5]*1+rl[dc[1021400]][5]*1-rl[dc[1021400]][4]+rl[dc[1021900]][5]*1-rl[dc[1021900]][4]+rl[dc[1021700]][5]*1-rl[dc[1021700]][4]+rl[dc[1020900]][5]*1-rl[dc[1020900]][4]+rl[dc[2020300]][5]*1-rl[dc[2020300]][4]+rl[dc[2020200]][5]*1-rl[dc[2020200]][4]+rl[dc[2021000]][5]*1-rl[dc[2021000]][4]+rl[dc[2150300]][5]*1-rl[dc[2150300]][4])-rl[dc[1021400]][5])/(rl[dc[1021400]][4]*1+(rl[dc[12110100]][5]*1+rl[dc[1021400]][5]*1-rl[dc[1021400]][4]+rl[dc[1021900]][5]*1-rl[dc[1021900]][4]+rl[dc[1021700]][5]*1-rl[dc[1021700]][4]+rl[dc[1020900]][5]*1-rl[dc[1020900]][4]+rl[dc[2020300]][5]*1-rl[dc[2020300]][4]+rl[dc[2020200]][5]*1-rl[dc[2020200]][4]+rl[dc[2021000]][5]*1-rl[dc[2021000]][4]+rl[dc[2150300]][5]*1-rl[dc[2150300]][4]))*100"),

            ReportItems(item_id=33010000, item_name=u"长期偿债能力分析指标", report=r4),
            ReportItems(item_id=33110100, item_name=u"资产负债比率", report=r4, item_formula="(rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1+rl[dc[2150100]][5]*1+rl[dc[2150200]][5]*1+rl[dc[2150300]][5]*1+rl[dc[2150400]][5]*1+rl[dc[2150500]][5]*1)/(rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1+rl[dc[1040100]][5]-rl[dc[1040110]][5]-rl[dc[1040210]][5]+rl[dc[1040400]][5]*1+rl[dc[1040500]][5]*1+rl[dc[1040600]][5]*1+rl[dc[1040700]][5]*1+rl[dc[1050100]][5]*1+rl[dc[1050200]][5]*1+rl[dc[1050300]][5]*1+rl[dc[1060100]][5]*1)*100"),
            ReportItems(item_id=33110200, item_name=u"负债与所有者权益比率", report=r4, item_formula="(rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1+rl[dc[2150100]][5]*1+rl[dc[2150200]][5]*1+rl[dc[2150300]][5]*1+rl[dc[2150400]][5]*1+rl[dc[2150500]][5]*1)/(rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1+rl[dc[4020200]][5]*1+rl[dc[4020500]][5]*1+rl[dc[4020600]][5]*1+rl[dc[4020700]][5]*1)*100"),
            ReportItems(item_id=33110300, item_name=u"负债与有形净资产比率", report=r4, item_formula="(rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1+rl[dc[2150100]][5]*1+rl[dc[2150200]][5]*1+rl[dc[2150300]][5]*1+rl[dc[2150400]][5]*1+rl[dc[2150500]][5]*1)/((rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1+rl[dc[4020200]][5]*1+rl[dc[4020500]][5]*1+rl[dc[4020600]][5]*1+rl[dc[4020700]][5]*1))*100"),
            ReportItems(item_id=33110400, item_name=u"利息保障倍数", report=r4, item_formula="(rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5]+rl[dc[25010110]][5]*1)/rl[dc[25010110]][5]"),
            
			ReportItems(item_id=33110500, item_name=u"长期投资占净资产比率", report=r4, item_formula="(rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1)/(rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1+rl[dc[4020200]][5]*1+rl[dc[4020500]][5]*1+rl[dc[4020600]][5]*1+rl[dc[4020700]][5]*1)*100"),
            ReportItems(item_id=33110600, item_name=u"长期债务与营运资金比率", report=r4, item_formula="(rl[dc[2150100]][5]*1+rl[dc[2150200]][5]*1+rl[dc[2150300]][5]*1+rl[dc[2150400]][5]*1+rl[dc[2150500]][5]*1)/(rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1+(rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1))*100"),
            ReportItems(item_id=33110700, item_name=u"净资产与期末贷款余额比率", report=r4, item_formula="(rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1+rl[dc[4020200]][5]*1+rl[dc[4020500]][5]*1+rl[dc[4020600]][5]*1+rl[dc[4020700]][5]*1)/(rl[dc[2020100]][5]*1+rl[dc[2150100]][5]*1)*100"),
            ReportItems(item_id=33110800, item_name=u"资本固定化比率", report=r4, item_formula="((rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1+rl[dc[1040100]][5]-rl[dc[1040110]][5]-rl[dc[1040210]][5]+rl[dc[1040400]][5]*1+rl[dc[1040500]][5]*1+rl[dc[1040600]][5]*1+rl[dc[1040700]][5]*1+rl[dc[1050100]][5]*1+rl[dc[1050200]][5]*1+rl[dc[1050300]][5]*1+rl[dc[1060100]][5]*1)-(rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1))/(rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1+rl[dc[4020200]][5]*1+rl[dc[4020500]][5]*1+rl[dc[4020600]][5]*1+rl[dc[4020700]][5]*1)*100"),
            ReportItems(item_id=33110900, item_name=u"固定资产净值率", report=r4, item_formula="(rl[dc[1040100]][5]-rl[dc[1040110]][5])/rl[dc[1040100]][5]*100"),
            ReportItems(item_id=33111000, item_name=u"长期投资与长期资本比率", report=r4, item_formula="(rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1)/((rl[dc[2150100]][5]*1+rl[dc[2150200]][5]*1+rl[dc[2150300]][5]*1+rl[dc[2150400]][5]*1+rl[dc[2150500]][5]*1)+rl[dc[3100000]][5]*1+(rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1+rl[dc[4020200]][5]*1+rl[dc[4020500]][5]*1+rl[dc[4020600]][5]*1+rl[dc[4020700]][5]*1))*100"),
            ReportItems(item_id=33111100, item_name=u"长期资产适合率", report=r4, item_formula="((rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1+rl[dc[4020200]][5]*1+rl[dc[4020500]][5]*1+rl[dc[4020600]][5]*1+rl[dc[4020700]][5]*1)+(rl[dc[2150100]][5]*1+rl[dc[2150200]][5]*1+rl[dc[2150300]][5]*1+rl[dc[2150400]][5]*1+rl[dc[2150500]][5]*1))/(rl[dc[1040100]][5]-rl[dc[1040110]][5]+rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1)*100"),
            ReportItems(item_id=33111200, item_name=u"总资本化比率", report=r4, item_formula="(rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1+rl[dc[2150100]][5]*1+rl[dc[2150200]][5]*1+rl[dc[2150300]][5]*1+rl[dc[2150400]][5]*1+rl[dc[2150500]][5]*1)/((rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1+rl[dc[2150100]][5]*1+rl[dc[2150200]][5]*1+rl[dc[2150300]][5]*1+rl[dc[2150400]][5]*1+rl[dc[2150500]][5]*1)+(rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1+rl[dc[4020200]][5]*1+rl[dc[4020500]][5]*1+rl[dc[4020600]][5]*1+rl[dc[4020700]][5]*1)+rl[dc[3100000]][5]*1)*100"),

            ReportItems(item_id=34010000, item_name=u"短期偿债能力分析指标", report=r4) ,
            ReportItems(item_id=34110100, item_name=u"流动比率", report=r4, item_formula="(rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1)/(rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1)*100"),
            ReportItems(item_id=34110200, item_name=u"速动比率", report=r4, item_formula="(rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1-rl[dc[1021400]][5]-rl[dc[1021430]][5]-rl[dc[1020900]][5]-rl[dc[1021600]][5])/(rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1)*100"),
			
            ReportItems(item_id=34110300, item_name=u"现金比率", report=r4, item_formula="(rl[dc[1020100]][5]*1+rl[dc[1020200]][5]*1)/(rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1)*100"),
            ReportItems(item_id=34110400, item_name=u"营运资金", report=r4, item_formula="(rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1)-rl[dc[2300000]][5]"),
            ReportItems(item_id=34110500, item_name=u"现金流动负债比率", report=r4, item_formula="rl[dc[25010117]][4]/(rl[dc[2300000]][4]*1+rl[dc[2300000]][5]*1)*2*100"),
            ReportItems(item_id=34110600, item_name=u"投资性现金流动负债比率", report=r4, item_formula="(((rl[dc[14110100]][5])+rl[dc[22110200]][4]*1+rl[dc[22110300]][4]*1+rl[dc[22110400]][4]*1)-(rl[dc[22110600]][4]*1+rl[dc[22110500]][4]*1+rl[dc[22110700]][4]*1))/((rl[dc[2020100]][4]*1+rl[dc[2020200]][4]*1+rl[dc[2020300]][4]*1+rl[dc[2020400]][4]*1+rl[dc[2020500]][4]*1+rl[dc[2020600]][4]*1+rl[dc[2020700]][4]*1+rl[dc[2020900]][4]*1+rl[dc[2021000]][4]*1+rl[dc[2021100]][4]*1+rl[dc[2021200]][4]*1+rl[dc[2021300]][4]*1+rl[dc[2021400]][4]*1+rl[dc[2021500]][4]*1)+(rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1))*2*100"),
            ReportItems(item_id=34110700, item_name=u"担保比率", report=r4, item_formula="rl[dc[1040100]][5]-rl[dc[1040110]][5]+(rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1+rl[dc[1040100]][5]-rl[dc[1040110]][5]-rl[dc[1040210]][5]+rl[dc[1040400]][5]*1+rl[dc[1040500]][5]*1+rl[dc[1040600]][5]*1+rl[dc[1040700]][5]*1+rl[dc[1050100]][5]*1+rl[dc[1050200]][5]*1+rl[dc[1050300]][5]*1+rl[dc[1060100]][5]*1)+(rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1+rl[dc[1040100]][5]-rl[dc[1040110]][5]-rl[dc[1040210]][5]+rl[dc[1040400]][5]*1+rl[dc[1040500]][5]*1+rl[dc[1040600]][5]*1+rl[dc[1040700]][5]*1+rl[dc[1050100]][5]*1+rl[dc[1050200]][5]*1+rl[dc[1050300]][5]*1+rl[dc[1060100]][5]*1)"),

            ReportItems(item_id=35010000, item_name=u"增长比率", report=r4) ,
            ReportItems(item_id=35110100, item_name=u"净利润增长率", report=r4, item_formula="(rl[dc[11010000]][4]-rl[dc[11120300]][4]-rl[dc[12110100]][4]-rl[dc[12110100]][4]-rl[dc[12110120]][4]-rl[dc[12110130]][4]-rl[dc[12110140]][4]-rl[dc[12120100]][4]+rl[dc[12120110]][4]*1+rl[dc[12120120]][4]*1+rl[dc[13110100]][4]*1-rl[dc[13110200]][4]-rl[dc[13110310]][4]-rl[dc[13110410]][4]-rl[dc[13110510]][4]+rl[dc[14110100]][4]*1+rl[dc[14110210]][4]*1+rl[dc[14110310]][4]*1+rl[dc[14110410]][4]*1+rl[dc[14110710]][4]*1-rl[dc[14110800]][4]-rl[dc[14110910]][4]-rl[dc[15110100]][4]-rl[dc[15110110]][4]+rl[dc[15110200]][4]*1)/((rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5]-rl[dc[15110100]][5]-rl[dc[15110110]][5]+rl[dc[15110200]][5]*1)-(rl[dc[11010000]][4]-rl[dc[11120300]][4]-rl[dc[12110100]][4]-rl[dc[12110100]][4]-rl[dc[12110120]][4]-rl[dc[12110130]][4]-rl[dc[12110140]][4]-rl[dc[12120100]][4]+rl[dc[12120110]][4]*1+rl[dc[12120120]][4]*1+rl[dc[13110100]][4]*1-rl[dc[13110200]][4]-rl[dc[13110310]][4]-rl[dc[13110410]][4]-rl[dc[13110510]][4]+rl[dc[14110100]][4]*1+rl[dc[14110210]][4]*1+rl[dc[14110310]][4]*1+rl[dc[14110410]][4]*1+rl[dc[14110710]][4]*1-rl[dc[14110800]][4]-rl[dc[14110910]][4]-rl[dc[15110100]][4]-rl[dc[15110110]][4]+rl[dc[15110200]][4]*1))*100"),
            ReportItems(item_id=35110200, item_name=u"总资产增长率", report=r4, item_formula="((rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1+rl[dc[1040100]][5]-rl[dc[1040110]][5]-rl[dc[1040210]][5]+rl[dc[1040400]][5]*1+rl[dc[1040500]][5]*1+rl[dc[1040600]][5]*1+rl[dc[1040700]][5]*1+rl[dc[1050100]][5]*1+rl[dc[1050200]][5]*1+rl[dc[1050300]][5]*1+rl[dc[1060100]][5]*1)-(rl[dc[1021400]][4]-rl[dc[1021430]][4]+rl[dc[1020700]][4]-rl[dc[1020710]][4]+rl[dc[1020200]][4]-rl[dc[1020210]][4]+rl[dc[1020100]][4]*1+rl[dc[1020400]][4]*1+rl[dc[1020500]][4]*1+rl[dc[1020600]][4]*1+rl[dc[1020900]][4]*1+rl[dc[1021000]][4]*1+rl[dc[1021100]][4]*1+rl[dc[1021200]][4]*1+rl[dc[1021300]][4]*1+rl[dc[1021600]][4]*1+rl[dc[1021700]][4]*1+rl[dc[1021800]][4]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][4]*1+rl[dc[1030200]][4]*1+  rl[dc[1040100]][4]-rl[dc[1040110]][4]     -rl[dc[1040210]][4]+rl[dc[1040400]][4]*1+rl[dc[1040500]][4]*1+rl[dc[1040600]][4]*1+rl[dc[1040700]][4]*1+rl[dc[1050100]][4]*1+rl[dc[1050200]][4]*1+rl[dc[1050300]][4]*1+rl[dc[1060100]][4]*1))/(rl[dc[1021400]][4]-rl[dc[1021430]][4]+rl[dc[1020700]][4]-rl[dc[1020710]][4]+rl[dc[1020200]][4]-rl[dc[1020210]][4]+rl[dc[1020100]][4]*1+rl[dc[1020400]][4]*1+rl[dc[1020500]][4]*1+rl[dc[1020600]][4]*1+rl[dc[1020900]][4]*1+rl[dc[1021000]][4]*1+rl[dc[1021100]][4]*1+rl[dc[1021200]][4]*1+rl[dc[1021300]][4]*1+rl[dc[1021600]][4]*1+rl[dc[1021700]][4]*1+rl[dc[1021800]][4]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][4]*1+rl[dc[1030200]][4]*1+  rl[dc[1040100]][4]-rl[dc[1040110]][4]     -rl[dc[1040210]][4]+rl[dc[1040400]][4]*1+rl[dc[1040500]][4]*1+rl[dc[1040600]][4]*1+rl[dc[1040700]][4]*1+rl[dc[1050100]][4]*1+rl[dc[1050200]][4]*1+rl[dc[1050300]][4]*1+rl[dc[1060100]][4]*1)*100"),
            ReportItems(item_id=35110300, item_name=u"总负债增长率", report=r4, item_formula="((rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1+rl[dc[2150100]][5]*1+rl[dc[2150200]][5]*1+rl[dc[2150300]][5]*1+rl[dc[2150400]][5]*1+rl[dc[2150500]][5]*1)-(rl[dc[2020100]][4]*1+rl[dc[2020200]][4]*1+rl[dc[2020300]][4]*1+rl[dc[2020400]][4]*1+rl[dc[2020500]][4]*1+rl[dc[2020600]][4]*1+rl[dc[2020700]][4]*1+rl[dc[2020900]][4]*1+rl[dc[2021000]][4]*1+rl[dc[2021100]][4]*1+rl[dc[2021200]][4]*1+rl[dc[2021300]][4]*1+rl[dc[2021400]][4]*1+rl[dc[2021500]][4]*1+rl[dc[2150100]][4]*1+rl[dc[2150200]][4]*1+rl[dc[2150300]][4]*1+rl[dc[2150400]][4]*1+rl[dc[2150500]][4]*1))/(rl[dc[2020100]][4]*1+rl[dc[2020200]][4]*1+rl[dc[2020300]][4]*1+rl[dc[2020400]][4]*1+rl[dc[2020500]][4]*1+rl[dc[2020600]][4]*1+rl[dc[2020700]][4]*1+rl[dc[2020900]][4]*1+rl[dc[2021000]][4]*1+rl[dc[2021100]][4]*1+rl[dc[2021200]][4]*1+rl[dc[2021300]][4]*1+rl[dc[2021400]][4]*1+rl[dc[2021500]][4]*1+rl[dc[2150100]][4]*1+rl[dc[2150200]][4]*1+rl[dc[2150300]][4]*1+rl[dc[2150400]][4]*1+rl[dc[2150500]][4]*1)*100"),
            ReportItems(item_id=35110400, item_name=u"资产净值增长率", report=r4, item_formula="((rl[dc[4020110]][5]*1+rl[dc[4020120]][5]*1+rl[dc[4020130]][5]*1+rl[dc[4020140]][5]*1+rl[dc[4020150]][5]*1+rl[dc[4020410]][5]*1+rl[dc[4020420]][5]*1+rl[dc[4020430]][5]*1+rl[dc[4020200]][5]*1+rl[dc[4020500]][5]*1+rl[dc[4020600]][5]*1+rl[dc[4020700]][5]*1)-(rl[dc[4020410]][4]*1+rl[dc[4020420]][4]*1+rl[dc[4020430]][4]*1+rl[dc[4020110]][4]*1+rl[dc[4020120]][4]*1+rl[dc[4020130]][4]*1+rl[dc[4020140]][4]*1+rl[dc[4020150]][4]*1+rl[dc[4020200]][4]*1+rl[dc[4020500]][4]*1+rl[dc[4020600]][4]*1+rl[dc[4020700]][4]*1))/(rl[dc[4020410]][4]*1+rl[dc[4020420]][4]*1+rl[dc[4020430]][4]*1+rl[dc[4020110]][4]*1+rl[dc[4020120]][4]*1+rl[dc[4020130]][4]*1+rl[dc[4020140]][4]*1+rl[dc[4020150]][4]*1+rl[dc[4020200]][4]*1+rl[dc[4020500]][4]*1+rl[dc[4020600]][4]*1+rl[dc[4020700]][4]*1)*100"),
            ReportItems(item_id=35110500, item_name=u"营业收入增长率", report=r4, item_formula="rl[dc[10100000]][4]/(rl[dc[10100000]][5])/rl[dc[10100000]][4]*100"),
            ReportItems(item_id=35110600, item_name=u"利润增长率", report=r4, item_formula="(rl[dc[11010000]][5]-rl[dc[11120300]][5]-rl[dc[12110100]][4]-rl[dc[12110100]][4]-rl[dc[12110120]][4]-rl[dc[12110130]][4]-rl[dc[12110140]][4]-rl[dc[12120100]][4]+rl[dc[12120110]][4]*1+rl[dc[12120120]][4]*1+rl[dc[13110100]][4]*1-rl[dc[13110200]][4]-rl[dc[13110310]][4]-rl[dc[13110410]][4]-rl[dc[13110510]][4]+rl[dc[14110100]][4]*1+rl[dc[14110210]][4]*1+rl[dc[14110310]][4]*1+rl[dc[14110410]][4]*1+rl[dc[14110710]][4]*1-rl[dc[14110800]][4]-rl[dc[14110910]][4])/(((rl[dc[11010000]][5]-rl[dc[11120300]][5])-rl[dc[12110100]][5]-rl[dc[12110100]][5]-rl[dc[12110120]][5]-rl[dc[12110130]][5]-rl[dc[12110140]][5]-rl[dc[12120100]][5]+rl[dc[12120110]][5]*1+rl[dc[12120120]][5]*1+rl[dc[13110100]][5]*1-rl[dc[13110200]][5]-rl[dc[13110310]][5]-rl[dc[13110410]][5]-rl[dc[13110510]][5]+rl[dc[14110100]][5]*1+rl[dc[14110210]][5]*1+rl[dc[14110310]][5]*1+rl[dc[14110410]][5]*1+rl[dc[14110710]][5]*1-rl[dc[14110800]][5]-rl[dc[14110910]][5])-((rl[dc[11010000]][5]-rl[dc[11120300]][5])-rl[dc[12110100]][4]-rl[dc[12110100]][4]-rl[dc[12110120]][4]-rl[dc[12110130]][4]-rl[dc[12110140]][4]-rl[dc[12120100]][4]+rl[dc[12120110]][4]*1+rl[dc[12120120]][4]*1+rl[dc[13110100]][4]*1-rl[dc[13110200]][4]-rl[dc[13110310]][4]-rl[dc[13110410]][4]-rl[dc[13110510]][4]+rl[dc[14110100]][4]*1+rl[dc[14110210]][4]*1+rl[dc[14110310]][4]*1+rl[dc[14110410]][4]*1+rl[dc[14110710]][4]*1-rl[dc[14110800]][4]-rl[dc[14110910]][4]))*100"),
            ReportItems(item_id=37010000, item_name=u"经济实力", report=r4) ,
            ReportItems(item_id=37020100, item_name=u"实有净资产", report=r4, item_formula="(rl[dc[1021400]][5]-rl[dc[1021430]][5]+rl[dc[1020700]][5]-rl[dc[1020710]][5]+rl[dc[1020200]][5]-rl[dc[1020210]][5]+rl[dc[1020100]][5]*1+rl[dc[1020400]][5]*1+rl[dc[1020500]][5]*1+rl[dc[1020600]][5]*1+rl[dc[1020900]][5]*1+rl[dc[1021000]][5]*1+rl[dc[1021100]][5]*1+rl[dc[1021200]][5]*1+rl[dc[1021300]][5]*1+rl[dc[1021600]][5]*1+rl[dc[1021700]][5]*1+rl[dc[1021800]][5]*1+rl[dc[1021900]][5]*1+rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1+rl[dc[1040100]][5]-rl[dc[1040110]][5]-rl[dc[1040210]][5]+rl[dc[1040400]][5]*1+rl[dc[1040500]][5]*1+rl[dc[1040600]][5]*1+rl[dc[1040700]][5]*1+rl[dc[1050100]][5]*1+rl[dc[1050200]][5]*1+rl[dc[1050300]][5]*1+rl[dc[1060100]][5]*1)-(rl[dc[2020100]][5]*1+rl[dc[2020200]][5]*1+rl[dc[2020300]][5]*1+rl[dc[2020400]][5]*1+rl[dc[2020500]][5]*1+rl[dc[2020600]][5]*1+rl[dc[2020700]][5]*1+rl[dc[2020900]][5]*1+rl[dc[2021000]][5]*1+rl[dc[2021100]][5]*1+rl[dc[2021200]][5]*1+rl[dc[2021300]][5]*1+rl[dc[2021400]][5]*1+rl[dc[2021500]][5]*1+rl[dc[2150100]][5]*1+rl[dc[2150200]][5]*1+rl[dc[2150300]][5]*1+rl[dc[2150400]][5]*1+rl[dc[2150500]][5]*1)-rl[dc[1040700]][5]-rl[dc[1021700]][5]"),
            ReportItems(item_id=37020200, item_name=u"有形长期资产", report=r4, item_formula="(rl[dc[1040100]][5]-rl[dc[1040110]][5]+rl[dc[1040500]][5])*1+rl[dc[1030100]][5]*1+rl[dc[1030200]][5]*1"),



        # 资产（新）

            ReportItems(item_id=41010000, item_name=u"资产", report=r6) ,
            ReportItems(item_id=41020000, item_name=u"流动资产", report=r6) ,
            ReportItems(item_id=41020100, item_name=u"货币资金", report=r6) ,
            ReportItems(item_id=41020200, item_name=u"交易性金融资产", report=r6) ,
            ReportItems(item_id=41020300, item_name=u"应收票据", report=r6) ,
            ReportItems(item_id=41020400, item_name=u"应收账款", report=r6) ,
            ReportItems(item_id=41020500, item_name=u"预付账款", report=r6) ,
            ReportItems(item_id=41020600, item_name=u"应收利息", report=r6) ,
            ReportItems(item_id=41020700, item_name=u"应收股利", report=r6) ,
            ReportItems(item_id=41020800, item_name=u"其他应收款", report=r6) ,
            ReportItems(item_id=41020900, item_name=u"存货", report=r6) ,
            ReportItems(item_id=41021000, item_name=u"一年内到期的非流动资产", report=r6) ,
            ReportItems(item_id=41021100, item_name=u"其他流动资产", report=r6) ,
            ReportItems(item_id=41100000, item_name=u"流动资产合计", report=r6, item_formula="rl[dc[41020100]][4]*1+rl[dc[41020200]][4]*1+rl[dc[41020300]][4]*1+rl[dc[41020400]][4]*1+rl[dc[41020500]][4]*1+rl[dc[41020600]][4]*1+rl[dc[41020700]][4]*1+rl[dc[41020800]][4]*1+rl[dc[41020900]][4]*1+rl[dc[41021000]][4]*1+rl[dc[41021100]][4]*1", item_formula1="rl[dc[41020100]][5]*1+rl[dc[41020200]][5]*1+rl[dc[41020300]][5]*1+rl[dc[41020400]][5]*1+rl[dc[41020500]][5]*1+rl[dc[41020600]][5]*1+rl[dc[41020700]][5]*1+rl[dc[41020800]][5]*1+rl[dc[41020900]][5]*1+rl[dc[41021000]][5]*1+rl[dc[41021100]][5]*1"),

            ReportItems(item_id=41120000, item_name=u"非流动资产", report=r6) ,
            ReportItems(item_id=41120100, item_name=u"可供出售的金融资产", report=r6) ,
            ReportItems(item_id=41120200, item_name=u"持有至到期投资", report=r6) ,
            ReportItems(item_id=41120300, item_name=u"长期股权投资", report=r6) ,
            ReportItems(item_id=41120400, item_name=u"长期应收款", report=r6) ,
            ReportItems(item_id=41120500, item_name=u"投资性房地产", report=r6) ,
            ReportItems(item_id=41120600, item_name=u"固定资产", report=r6) ,
            ReportItems(item_id=41120700, item_name=u"在建工程", report=r6) ,
            ReportItems(item_id=41120800, item_name=u"工程物资", report=r6) ,
            ReportItems(item_id=41120900, item_name=u"固定资产清理", report=r6) ,
            ReportItems(item_id=41121000, item_name=u"生产性生物资产", report=r6) ,
            ReportItems(item_id=41121100, item_name=u"油气资产", report=r6) ,
            ReportItems(item_id=41121200, item_name=u"无形资产", report=r6) ,
            ReportItems(item_id=41121300, item_name=u"开发支出", report=r6) ,
            ReportItems(item_id=41121400, item_name=u"商誉", report=r6) ,
            ReportItems(item_id=41121500, item_name=u"长期待摊费用", report=r6) ,
            ReportItems(item_id=41121600, item_name=u"递延所得税资产", report=r6) ,
            ReportItems(item_id=41121700, item_name=u"其他非流动资产", report=r6) ,
            ReportItems(item_id=41200000, item_name=u"非流动资产合计", report=r6, item_formula="rl[dc[41120100]][4]*1+rl[dc[41120200]][4]*1+rl[dc[41120300]][4]*1+rl[dc[41120400]][4]*1+rl[dc[41120500]][4]*1+rl[dc[41120600]][4]*1+rl[dc[41120700]][4]*1+rl[dc[41120800]][4]*1+rl[dc[41120900]][4]*1+rl[dc[41121000]][4]*1+rl[dc[41121100]][4]*1+rl[dc[41121200]][4]*1+rl[dc[41121300]][4]*1+rl[dc[41121400]][4]*1+rl[dc[41121500]][4]*1+rl[dc[41121600]][4]*1+rl[dc[41121700]][4]*1", item_formula1="rl[dc[41120100]][5]*1+rl[dc[41120200]][5]*1+rl[dc[41120300]][5]*1+rl[dc[41120400]][5]*1+rl[dc[41120500]][5]*1+rl[dc[41120600]][5]*1+rl[dc[41120700]][5]*1+rl[dc[41120800]][5]*1+rl[dc[41120900]][5]*1+rl[dc[41121000]][5]*1+rl[dc[41121100]][5]*1+rl[dc[41121200]][5]*1+rl[dc[41121300]][5]*1+rl[dc[41121400]][5]*1+rl[dc[41121500]][5]*1+rl[dc[41121600]][5]*1+rl[dc[41121700]][5]*1"),
            ReportItems(item_id=41300000, item_name=u"资产总计", report=r6, item_formula="rl[dc[41120100]][4]*1+rl[dc[41120200]][4]*1+rl[dc[41120300]][4]*1+rl[dc[41120400]][4]*1+rl[dc[41120500]][4]*1+rl[dc[41120600]][4]*1+rl[dc[41120700]][4]*1+rl[dc[41120800]][4]*1+rl[dc[41120900]][4]*1+rl[dc[41121000]][4]*1+rl[dc[41121100]][4]*1+rl[dc[41121200]][4]*1+rl[dc[41121300]][4]*1+rl[dc[41121400]][4]*1+rl[dc[41121500]][4]*1+rl[dc[41121600]][4]*1+rl[dc[41121700]][4]*1+rl[dc[41020100]][4]*1+rl[dc[41020200]][4]*1+rl[dc[41020300]][4]*1+rl[dc[41020400]][4]*1+rl[dc[41020500]][4]*1+rl[dc[41020600]][4]*1+rl[dc[41020700]][4]*1+rl[dc[41020800]][4]*1+rl[dc[41020900]][4]*1+rl[dc[41021000]][4]*1+rl[dc[41021100]][4]*1", \
			item_formula1="rl[dc[41020100]][5]*1+rl[dc[41020200]][5]*1+rl[dc[41020300]][5]*1+rl[dc[41020400]][5]*1+rl[dc[41020500]][5]*1+rl[dc[41020600]][5]*1+rl[dc[41020700]][5]*1+rl[dc[41020800]][5]*1+rl[dc[41020900]][5]*1+rl[dc[41021000]][5]*1+rl[dc[41021100]][5]*1+rl[dc[41120100]][5]*1+rl[dc[41120200]][5]*1+rl[dc[41120300]][5]*1+rl[dc[41120400]][5]*1+rl[dc[41120500]][5]*1+rl[dc[41120600]][5]*1+rl[dc[41120700]][5]*1+rl[dc[41120800]][5]*1+rl[dc[41120900]][5]*1+rl[dc[41121000]][5]*1+rl[dc[41121100]][5]*1+rl[dc[41121200]][5]*1+rl[dc[41121300]][5]*1+rl[dc[41121400]][5]*1+rl[dc[41121500]][5]*1+rl[dc[41121600]][5]*1+rl[dc[41121700]][5]*1"),

# 负债（新）

            ReportItems(item_id=42010000, item_name=u"负债", report=r6) ,
            ReportItems(item_id=42020000, item_name=u"流动负债", report=r6) ,
            ReportItems(item_id=42020100, item_name=u"短期借款", report=r6) ,
            ReportItems(item_id=42020200, item_name=u"交易性金融负债", report=r6) ,
            ReportItems(item_id=42020300, item_name=u"应付票据", report=r6) ,
            ReportItems(item_id=42020400, item_name=u"应付账款", report=r6) ,
            ReportItems(item_id=42020500, item_name=u"预收账款", report=r6) ,
            ReportItems(item_id=42020600, item_name=u"应付利息", report=r6) ,
            ReportItems(item_id=42020700, item_name=u"应付职工薪酬", report=r6) ,
            ReportItems(item_id=42020800, item_name=u"应交税费", report=r6) ,
            ReportItems(item_id=42020900, item_name=u"应付股利", report=r6) ,
            ReportItems(item_id=42021000, item_name=u"其他应付款", report=r6) ,
            ReportItems(item_id=42021100, item_name=u"一年内到期的非流动负债", report=r6) ,
            ReportItems(item_id=42021200, item_name=u"其他流动负债", report=r6) ,
            ReportItems(item_id=42100000, item_name=u"流动负债合计", report=r6, item_formula="rl[dc[42020100]][4]*1+rl[dc[42020200]][4]*1+rl[dc[42020300]][4]*1+rl[dc[42020400]][4]*1+rl[dc[42020500]][4]*1+rl[dc[42020600]][4]*1+rl[dc[42020700]][4]*1+rl[dc[42020800]][4]*1+rl[dc[42020900]][4]*1+rl[dc[42021000]][4]*1+rl[dc[42021100]][4]*1+rl[dc[42021200]][4]*1", item_formula1="rl[dc[42020100]][5]*1+rl[dc[42020200]][5]*1+rl[dc[42020300]][5]*1+rl[dc[42020400]][5]*1+rl[dc[42020500]][5]*1+rl[dc[42020600]][5]*1+rl[dc[42020700]][5]*1+rl[dc[42020800]][5]*1+rl[dc[42020900]][5]*1+rl[dc[42021000]][5]*1+rl[dc[42021100]][5]*1+rl[dc[42021200]][5]*1") ,

            ReportItems(item_id=42120000, item_name=u"非流动负债", report=r6) ,
            ReportItems(item_id=42120100, item_name=u"长期借款", report=r6) ,
            ReportItems(item_id=42120200, item_name=u"应付债券", report=r6) ,
            ReportItems(item_id=42120300, item_name=u"长期应付款", report=r6) ,
            ReportItems(item_id=42120400, item_name=u"专项应付款", report=r6) ,
            ReportItems(item_id=42120500, item_name=u"预计负债", report=r6) ,
            ReportItems(item_id=42120600, item_name=u"递延所得税负债", report=r6) ,
            ReportItems(item_id=42120700, item_name=u"其他非流动负债", report=r6) ,
            ReportItems(item_id=42200000, item_name=u"非流动负债合计", report=r6, item_formula="rl[dc[42120100]][4]*1+rl[dc[42120200]][4]*1+rl[dc[42120300]][4]*1+rl[dc[42120400]][4]*1+rl[dc[42120500]][4]*1+rl[dc[42120600]][4]*1+rl[dc[42120700]][4]*1", item_formula1="rl[dc[42120100]][5]*1+rl[dc[42120200]][5]*1+rl[dc[42120300]][5]*1+rl[dc[42120400]][5]*1+rl[dc[42120500]][5]*1+rl[dc[42120600]][5]*1+rl[dc[42120700]][5]*1") ,
            ReportItems(item_id=42300000, item_name=u"负债总计", report=r6, item_formula="rl[dc[42120100]][4]*1+rl[dc[42120200]][4]*1+rl[dc[42120300]][4]*1+rl[dc[42120400]][4]*1+rl[dc[42120500]][4]*1+rl[dc[42120600]][4]*1+rl[dc[42120700]][4]*1+rl[dc[42020100]][4]*1+rl[dc[42020200]][4]*1+rl[dc[42020300]][4]*1+rl[dc[42020400]][4]*1+rl[dc[42020500]][4]*1+rl[dc[42020600]][4]*1+rl[dc[42020700]][4]*1+rl[dc[42020800]][4]*1+rl[dc[42020900]][4]*1+rl[dc[42021000]][4]*1+rl[dc[42021100]][4]*1+rl[dc[42021200]][4]*1", item_formula1="rl[dc[42020100]][5]*1+rl[dc[42020200]][5]*1+rl[dc[42020300]][5]*1+rl[dc[42020400]][5]*1+rl[dc[42020500]][5]*1+rl[dc[42020600]][5]*1+rl[dc[42020700]][5]*1+rl[dc[42020800]][5]*1+rl[dc[42020900]][5]*1+rl[dc[42021000]][5]*1+rl[dc[42021100]][5]*1+rl[dc[42021200]][5]*1+rl[dc[42120100]][5]*1+rl[dc[42120200]][5]*1+rl[dc[42120300]][5]*1+rl[dc[42120400]][5]*1+rl[dc[42120500]][5]*1+rl[dc[42120600]][5]*1+rl[dc[42120700]][5]*1") ,
            ReportItems(item_id=43010100, item_name=u"实收资本（或股本）", report=r6) ,
            ReportItems(item_id=43010200, item_name=u"资本公积", report=r6) ,
            ReportItems(item_id=43010300, item_name=u"减：库存股", report=r6) ,
            ReportItems(item_id=43010400, item_name=u"盈余公积", report=r6) ,
            ReportItems(item_id=43010500, item_name=u"未分配利润", report=r6) ,
            ReportItems(item_id=43100000, item_name=u"所有者权益合计", report=r6, item_formula="rl[dc[43010100]][4]*1+rl[dc[43010200]][4]*1-rl[dc[43010300]][4]+rl[dc[43010400]][4]*1+rl[dc[43010500]][4]*1", item_formula1="rl[dc[43010100]][5]*1+rl[dc[43010200]][5]*1-rl[dc[43010300]][5]+rl[dc[43010400]][5]*1+rl[dc[43010500]][5]*1") ,
            ReportItems(item_id=43200000, item_name=u"负债和所有者权益合计", report=r6,item_formula="rl[dc[43010100]][4]*1+rl[dc[43010200]][4]*1-rl[dc[43010300]][4]+rl[dc[43010400]][4]*1+rl[dc[43010500]][4]*1+rl[dc[42120100]][4]*1+rl[dc[42120200]][4]*1+rl[dc[42120300]][4]*1+rl[dc[42120400]][4]*1+rl[dc[42120500]][4]*1+rl[dc[42120600]][4]*1+rl[dc[42120700]][4]*1+rl[dc[42020100]][4]*1+rl[dc[42020200]][4]*1+rl[dc[42020300]][4]*1+rl[dc[42020400]][4]*1+rl[dc[42020500]][4]*1+rl[dc[42020600]][4]*1+rl[dc[42020700]][4]*1+rl[dc[42020800]][4]*1+rl[dc[42020900]][4]*1+rl[dc[42021000]][4]*1+rl[dc[42021100]][4]*1+rl[dc[42021200]][4]*1", item_formula1="rl[dc[42020100]][5]*1+rl[dc[42020200]][5]*1+rl[dc[42020300]][5]*1+rl[dc[42020400]][5]*1+rl[dc[42020500]][5]*1+rl[dc[42020600]][5]*1+rl[dc[42020700]][5]*1+rl[dc[42020800]][5]*1+rl[dc[42020900]][5]*1+rl[dc[42021000]][5]*1+rl[dc[42021100]][5]*1+rl[dc[42021200]][5]*1+rl[dc[42120100]][5]*1+rl[dc[42120200]][5]*1+rl[dc[42120300]][5]*1+rl[dc[42120400]][5]*1+rl[dc[42120500]][5]*1+rl[dc[42120600]][5]*1+rl[dc[42120700]][5]*1+rl[dc[43010100]][5]*1+rl[dc[43010200]][5]*1-rl[dc[43010300]][5]+rl[dc[43010400]][5]*1+rl[dc[43010500]][5]*1") ,








            # 损益表（新）

            ReportItems(item_id=51000000, item_name=u"一、营业收入", report=r7) ,
            ReportItems(item_id=51010100, item_name=u"减：营业成本", report=r7) ,
            ReportItems(item_id=51010200, item_name=u"营业税金及附加", report=r7) ,
            ReportItems(item_id=51010300, item_name=u"销售费用", report=r7) ,
            ReportItems(item_id=51010400, item_name=u"管理费用", report=r7) ,
            ReportItems(item_id=51010500, item_name=u"财务费用", report=r7) ,
            ReportItems(item_id=51010600, item_name=u"资产减值损失", report=r7) ,
            ReportItems(item_id=51010700, item_name=u"加：公允价值变动收益（损失以“-”号填列）", report=r7) ,
            ReportItems(item_id=51010800, item_name=u"投资收益（损失以“－”号填列）", report=r7) ,
            ReportItems(item_id=51010900, item_name=u"其中：对联营企业和合营企业的投资收益", report=r7) ,
            ReportItems(item_id=52000000, item_name=u"二、营业利润（亏损以“－”号填列）", report=r7, item_formula="rl[dc[51000000]][4]-rl[dc[51010100]][4]-rl[dc[51010200]][4]-rl[dc[51010300]][4]-rl[dc[51010400]][4]-rl[dc[51010500]][4]-rl[dc[51010600]][4]-rl[dc[51010700]][4]-rl[dc[51010800]][4]", item_formula1="rl[dc[51000000]][5]-rl[dc[51010100]][5]-rl[dc[51010200]][5]-rl[dc[51010300]][5]-rl[dc[51010400]][5]-rl[dc[51010500]][5]-rl[dc[51010600]][5]-rl[dc[51010700]][5]-rl[dc[51010800]][5]"),
            ReportItems(item_id=52010100, item_name=u"加：营业外收入", report=r7) ,
            ReportItems(item_id=52010200, item_name=u"减：营业外支出", report=r7) ,
            ReportItems(item_id=52010300, item_name=u"其中：非流动资产处置损失", report=r7) ,
            ReportItems(item_id=53000000, item_name=u"三、利润总额（亏损总额以“－”号填列）", report=r7, item_formula="rl[dc[51000000]][4]-rl[dc[51010100]][4]-rl[dc[51010200]][4]-rl[dc[51010300]][4]-rl[dc[51010400]][4]-rl[dc[51010500]][4]-rl[dc[51010600]][4]-rl[dc[51010700]][4]-rl[dc[51010800]][4]+rl[dc[52010100]][4]*1-rl[dc[52010200]][4]", item_formula1="rl[dc[51000000]][5]-rl[dc[51010100]][5]-rl[dc[51010200]][5]-rl[dc[51010300]][5]-rl[dc[51010400]][5]-rl[dc[51010500]][5]-rl[dc[51010600]][5]-rl[dc[51010700]][5]-rl[dc[51010800]][5]+rl[dc[52010100]][5]*1-rl[dc[52010200]][5]"),
            ReportItems(item_id=53010100, item_name=u"减：所得税费用", report=r7) ,
            ReportItems(item_id=54000000, item_name=u"四、净利润（净亏损以“－”号填列）", report=r7, item_formula="(rl[dc[51000000]][4]-rl[dc[51010100]][4]-rl[dc[51010200]][4]-rl[dc[51010300]][4]-rl[dc[51010400]][4]-rl[dc[51010500]][4]-rl[dc[51010600]][4]-rl[dc[51010700]][4]-rl[dc[51010800]][4]+rl[dc[52010100]][4]*1-rl[dc[52010200]][4])-rl[dc[53010100]][4]", item_formula1="(rl[dc[51000000]][5]-rl[dc[51010100]][5]-rl[dc[51010200]][5]-rl[dc[51010300]][5]-rl[dc[51010400]][5]-rl[dc[51010500]][5]-rl[dc[51010600]][5]-rl[dc[51010700]][5]-rl[dc[51010800]][5]+rl[dc[52010100]][5]*1-rl[dc[52010200]][5])-rl[dc[53010100]][5]"),
            ReportItems(item_id=55000000, item_name=u"五、每股收益：", report=r7) ,
            ReportItems(item_id=55010200, item_name=u"（一）基本每股收益", report=r7) ,
            ReportItems(item_id=55010300, item_name=u"（二）稀释每股收益", report=r7) ,
# 现金流量表（新）
            ReportItems(item_id=61010000, item_name=u"一、经营活动产生的现金流量：", report=r8) ,
            ReportItems(item_id=61110100, item_name=u"销售商品、提供劳务收到的现金", report=r8) ,
            ReportItems(item_id=61110200, item_name=u"收到的税费返还", report=r8) ,
            ReportItems(item_id=61110300, item_name=u"收到其他与经营活动有关的现金", report=r8) ,
            ReportItems(item_id=61110400, item_name=u"经营活动现金流入小计", report=r8, item_formula="rl[dc[61110100]][4]*1+rl[dc[61110200]][4]*1+rl[dc[61110300]][4]*1"),
            ReportItems(item_id=61110500, item_name=u"购买商品、接受劳务支付的现金", report=r8) ,
            ReportItems(item_id=61110600, item_name=u"支付给职工以及为职工支付的现金", report=r8) ,
            ReportItems(item_id=61110700, item_name=u"支付的各项税费", report=r8) ,
            ReportItems(item_id=61110800, item_name=u"支付其他与经营活动有关的现金", report=r8) ,
            ReportItems(item_id=61110900, item_name=u"经营活动现金流出小计", report=r8, item_formula="rl[dc[61110500]][4]*1+rl[dc[61110600]][4]*1+rl[dc[61110700]][4]*1+rl[dc[61110800]][4]*1"),
            ReportItems(item_id=61111000, item_name=u"经营活动产生的现金流量净额", report=r8, item_formula="rl[dc[61110100]][4]*1+rl[dc[61110200]][4]*1+rl[dc[61110300]][4]*1+rl[dc[61110500]][4]*1+rl[dc[61110600]][4]*1+rl[dc[61110700]][4]*1+rl[dc[61110800]][4]*1"),

            ReportItems(item_id=62010000, item_name=u"二、投资活动产生的现金流量：", report=r8) ,
            ReportItems(item_id=62110100, item_name=u"收回投资收到的现金", report=r8) ,
            ReportItems(item_id=62110200, item_name=u"取得投资收益收到的现金", report=r8) ,
            ReportItems(item_id=62110300, item_name=u"处置固定资产、无形资产和其他长期资产收回的现金净额", report=r8) ,
            ReportItems(item_id=62110400, item_name=u"处置子公司及其他营业单位收到的现金净额", report=r8) ,
            ReportItems(item_id=62110500, item_name=u"收到其他与投资活动有关的现金", report=r8) ,
            ReportItems(item_id=62110600, item_name=u"投资活动现金流入小计", report=r8, item_formula="rl[dc[62110100]][4]*1+rl[dc[62110200]][4]*1+rl[dc[62110300]][4]*1+rl[dc[62110400]][4]*1+rl[dc[62110500]][4]*1"),
            ReportItems(item_id=62110700, item_name=u"购建固定资产、无形资产和其他长期资产支付的现金", report=r8) ,
            ReportItems(item_id=62110800, item_name=u"投资所支付的现金", report=r8) ,
            ReportItems(item_id=62110900, item_name=u"取得子公司及其他营业单位支付的现金净额", report=r8) ,
            ReportItems(item_id=62111000, item_name=u"支付其他与投资活动有关的现金", report=r8) ,
            ReportItems(item_id=62111100, item_name=u"投资活动现金流出小计", report=r8, item_formula="rl[dc[62110700]][4]*1+rl[dc[62110800]][4]*1+rl[dc[62110900]][4]*1+rl[dc[62111000]][4]*1"),
            ReportItems(item_id=62111200, item_name=u"投资活动产生的现金流量净额", report=r8, item_formula="(rl[dc[62110100]][4]*1+rl[dc[62110200]][4]*1+rl[dc[62110300]][4]*1+rl[dc[62110400]][4]*1+rl[dc[62110500]][4]*1)-(rl[dc[62110700]][4]*1+rl[dc[62110800]][4]*1+rl[dc[62110900]][4]*1+rl[dc[62111000]][4]*1)"),

            ReportItems(item_id=63010000, item_name=u"三、筹资活动产生的现金流量：", report=r8) ,
            ReportItems(item_id=63110100, item_name=u"吸收投资收到的现金", report=r8) ,
            ReportItems(item_id=63110200, item_name=u"取得借款收到的现金", report=r8) ,
            ReportItems(item_id=63110300, item_name=u"收到其他与筹资活动有关的现金", report=r8) ,
            ReportItems(item_id=63110400, item_name=u"筹资活动现金流入小计", report=r8, item_formula="rl[dc[63110100]][4]*1+rl[dc[63110200]][4]*1+rl[dc[63110300]][4]*1"),
            ReportItems(item_id=63110500, item_name=u"偿还债务支付的现金", report=r8) ,
            ReportItems(item_id=63110600, item_name=u"分配股利、利润或偿付利息支付的现金", report=r8) ,
            ReportItems(item_id=63110700, item_name=u"支付其他与筹资活动有关的现金", report=r8) ,
            ReportItems(item_id=63110800, item_name=u"筹资活动现金流出小计", report=r8, item_formula="rl[dc[63110500]][4]*1+rl[dc[63110600]][4]*1+rl[dc[63110700]][4]*1"),
            ReportItems(item_id=63110900, item_name=u"筹资活动产生的现金流量净额", report=r8, item_formula="(rl[dc[63110100]][4]*1+rl[dc[63110200]][4]*1+rl[dc[63110300]][4]*1)-(rl[dc[63110500]][4]*1+rl[dc[63110600]][4]*1+rl[dc[63110700]][4]*1)"),

            ReportItems(item_id=64000000, item_name=u"四、汇率变动对现金及现金等价物的影响", report=r8) ,
            ReportItems(item_id=65000000, item_name=u"五、现金及现金等价物净增加额", report=r8, item_formula="(rl[dc[63110100]][4]*1+rl[dc[63110200]][4]*1+rl[dc[63110300]][4]*1)-(rl[dc[63110500]][4]*1+rl[dc[63110600]][4]*1+rl[dc[63110700]][4]*1)+(rl[dc[62110100]][4]*1+rl[dc[62110200]][4]*1+rl[dc[62110300]][4]*1+rl[dc[62110400]][4]*1+rl[dc[62110500]][4]*1)-(rl[dc[62110700]][4]*1+rl[dc[62110800]][4]*1+rl[dc[62110900]][4]*1+rl[dc[62111000]][4]*1)+rl[dc[61110100]][4]*1+rl[dc[61110200]][4]*1+rl[dc[61110300]][4]*1+rl[dc[61110500]][4]*1+rl[dc[61110600]][4]*1+rl[dc[61110700]][4]*1+rl[dc[61110800]][4]*1+rl[dc[64000000]][4]*1"),
            ReportItems(item_id=65010100, item_name=u"加：期初现金及现金等价物余额", report=r8) ,
            ReportItems(item_id=66000000, item_name=u"六、 期末现金及现金等价物余额", report=r8, item_formula="(rl[dc[63110100]][4]*1+rl[dc[63110200]][4]*1+rl[dc[63110300]][4]*1)-(rl[dc[63110500]][4]*1+rl[dc[63110600]][4]*1+rl[dc[63110700]][4]*1)+(rl[dc[62110100]][4]*1+rl[dc[62110200]][4]*1+rl[dc[62110300]][4]*1+rl[dc[62110400]][4]*1+rl[dc[62110500]][4]*1)-(rl[dc[62110700]][4]*1+rl[dc[62110800]][4]*1+rl[dc[62110900]][4]*1+rl[dc[62111000]][4]*1)+rl[dc[61110100]][4]*1+rl[dc[61110200]][4]*1+rl[dc[61110300]][4]*1+rl[dc[61110500]][4]*1+rl[dc[61110600]][4]*1+rl[dc[61110700]][4]*1+rl[dc[61110800]][4]*1+rl[dc[64000000]][4]*1+rl[dc[65010100]][4]*1"),
            ReportItems(item_id=66010000, item_name=u"现金流量表补充资料如下：", report=r8) ,
            ReportItems(item_id=66020000, item_name=u"1.将净利润调节为经营活动现金流量：", report=r8) ,
            ReportItems(item_id=66020100, item_name=u"净利润", report=r8) ,
            ReportItems(item_id=66020200, item_name=u"加：资产减值准备", report=r8) ,
            ReportItems(item_id=66020210, item_name=u"　　固定资产折旧、油气资产折耗、生产性生物资产折旧", report=r8) ,
            ReportItems(item_id=66020220, item_name=u"　　无形资产摊销", report=r8) ,
            ReportItems(item_id=66020230, item_name=u"　　长期待摊费用摊销", report=r8) ,
            ReportItems(item_id=66020240, item_name=u"　　待摊费用减少（减：增加）", report=r8) ,
            ReportItems(item_id=66020250, item_name=u"　　预提费用增加（减：减少）", report=r8) ,
            ReportItems(item_id=66020260, item_name=u"　　处置固定资产、无形资产和其他长期资产的损失（收益以“-”号填列）", report=r8) ,
            ReportItems(item_id=66020270, item_name=u"　　固定资产报废损失（收益以“-”号填列）", report=r8) ,
            ReportItems(item_id=66020280, item_name=u"　　公允价值变动损失（收益以“-”号填列）", report=r8) ,
            ReportItems(item_id=66020290, item_name=u"　　财务费用（收益以“-”号填列）", report=r8) ,
            ReportItems(item_id=66020310, item_name=u"　　投资损失（收益以“-”号填列）", report=r8) ,
            ReportItems(item_id=66020320, item_name=u"　　递延所得税资产减少（增加以“-”号填列）", report=r8) ,
            ReportItems(item_id=66020400, item_name=u"递延所得税负债增加（减少以“-”号填列）", report=r8) ,
            ReportItems(item_id=66020410, item_name=u"　　存货的减少（增加以“-”号填列）", report=r8) ,
            ReportItems(item_id=66020420, item_name=u"　　经营性应收项目的减少（增加以“-”号填列）", report=r8) ,
            ReportItems(item_id=66020430, item_name=u"　　经营性应付项目的增加（减少以“-”号填列）", report=r8) ,
            ReportItems(item_id=66020500, item_name=u"其他", report=r8) ,
            ReportItems(item_id=66020600, item_name=u"经营活动产生的现金流量净额", report=r8, item_formula="rl[dc[66020100]][4]*1+rl[dc[66020200]][4]*1+rl[dc[66020210]][4]*1+rl[dc[66020220]][4]*1+rl[dc[66020230]][4]*1+rl[dc[66020240]][4]*1+rl[dc[66020250]][4]*1+rl[dc[66020260]][4]*1+rl[dc[66020270]][4]*1+rl[dc[66020280]][4]*1+rl[dc[66020290]][4]*1+rl[dc[66020310]][4]*1+rl[dc[66020320]][4]*1+rl[dc[66020400]][4]*1+rl[dc[66020410]][4]*1+rl[dc[66020420]][4]*1+rl[dc[66020430]][4]*1+rl[dc[66020500]][4]*1"),
            ReportItems(item_id=66030000, item_name=u"2.不涉及现金收支的重大投资和筹资活动：", report=r8) ,
            ReportItems(item_id=66030100, item_name=u"债务转为资本", report=r8) ,
            ReportItems(item_id=66030200, item_name=u"一年内到期的可转换公司债券", report=r8) ,
            ReportItems(item_id=66030300, item_name=u"融资租入固定资产", report=r8) ,
            ReportItems(item_id=66030400, item_name=u"其他", report=r8) ,
            ReportItems(item_id=66040000, item_name=u"3.现金及现金等价物净变动情况：", report=r8) ,
            ReportItems(item_id=66040200, item_name=u"现金的期末余额", report=r8) ,
            ReportItems(item_id=66040300, item_name=u"减：现金的期初余额", report=r8) ,
            ReportItems(item_id=66040400, item_name=u"加：现金等价物的期末余额", report=r8) ,
            ReportItems(item_id=66040500, item_name=u"减：现金等价物的期初余额", report=r8) ,
            ReportItems(item_id=66040600, item_name=u"现金及现金等价物净增加额", report=r8, item_formula="rl[dc[66040200]][4]-rl[dc[66040300]][4]*1+rl[dc[66040400]][4]*1-rl[dc[66040500]][4]"),
            # 资产负债表（事业单位）
            ReportItems(item_id=71010000, item_name=u"一、资产类", report=r9) ,
            ReportItems(item_id=71110100, item_name=u"现金", report=r9) ,
            ReportItems(item_id=71110200, item_name=u"银行存款", report=r9) ,
            ReportItems(item_id=71110300, item_name=u"应收票据", report=r9) ,
            ReportItems(item_id=71110400, item_name=u"应收账款", report=r9) ,
            ReportItems(item_id=71110500, item_name=u"预付账款", report=r9) ,
            ReportItems(item_id=71110600, item_name=u"其他应收款", report=r9) ,
            ReportItems(item_id=71110700, item_name=u"材料", report=r9) ,
            ReportItems(item_id=71110800, item_name=u"产成品", report=r9) ,
            ReportItems(item_id=71110900, item_name=u"对外投资", report=r9) ,
            ReportItems(item_id=71111000, item_name=u"固定资产", report=r9) ,
            ReportItems(item_id=71111100, item_name=u"无形资产", report=r9) ,
            ReportItems(item_id=71200000, item_name=u"资产合计：", report=r9, item_formula="rl[dc[71110100]][4]*1+rl[dc[71110200]][4]*1+rl[dc[71110300]][4]*1+rl[dc[71110400]][4]*1+rl[dc[71110500]][4]*1+rl[dc[71110600]][4]*1+rl[dc[71110700]][4]*1+rl[dc[71110800]][4]*1+rl[dc[71110900]][4]*1+rl[dc[71111000]][4]*1+rl[dc[71111100]][4]*1",item_formula1="rl[dc[71110100]][5]*1+rl[dc[71110200]][5]*1+rl[dc[71110300]][5]*1+rl[dc[71110400]][5]*1+rl[dc[71110500]][5]*1+rl[dc[71110600]][5]*1+rl[dc[71110700]][5]*1+rl[dc[71110800]][5]*1+rl[dc[71110900]][5]*1+rl[dc[71111000]][5]*1+rl[dc[71111100]][5]*1"),

            ReportItems(item_id=72010000, item_name=u"五、支出类", report=r9) ,
            ReportItems(item_id=72110100, item_name=u"拨出经费", report=r9) ,
            ReportItems(item_id=72110200, item_name=u"拨出专款", report=r9) ,
            ReportItems(item_id=72110300, item_name=u"专款支出", report=r9) ,
            ReportItems(item_id=72110400, item_name=u"事业支出", report=r9) ,
            ReportItems(item_id=72110500, item_name=u"经营支出", report=r9) ,
            ReportItems(item_id=72110600, item_name=u"成本费用", report=r9) ,
            ReportItems(item_id=72110700, item_name=u"销售税金", report=r9) ,
            ReportItems(item_id=72110800, item_name=u"上缴上级支出", report=r9) ,
            ReportItems(item_id=72110900, item_name=u"对附属单位补助", report=r9) ,
            ReportItems(item_id=72111000, item_name=u"结转自筹基建", report=r9) ,
            ReportItems(item_id=72200000, item_name=u"支出合计：", report=r9, item_formula="rl[dc[72110100]][4]*1+rl[dc[72110200]][4]*1+rl[dc[72110300]][4]*1+rl[dc[72110400]][4]*1+rl[dc[72110500]][4]*1+rl[dc[72110600]][4]*1+rl[dc[72110700]][4]*1+rl[dc[72110800]][4]*1+rl[dc[72110900]][4]*1+rl[dc[72111000]][4]*1",item_formula1="rl[dc[72110100]][5]*1+rl[dc[72110200]][5]*1+rl[dc[72110300]][5]*1+rl[dc[72110400]][5]*1+rl[dc[72110500]][5]*1+rl[dc[72110600]][5]*1+rl[dc[72110700]][5]*1+rl[dc[72110800]][5]*1+rl[dc[72110900]][5]*1+rl[dc[72111000]][5]*1"),
            ReportItems(item_id=72300000, item_name=u"资产部类总计：", report=r9,  item_formula="rl[dc[72110100]][4]*1+rl[dc[72110200]][4]*1+rl[dc[72110300]][4]*1+rl[dc[72110400]][4]*1+rl[dc[72110500]][4]*1+rl[dc[72110600]][4]*1+rl[dc[72110700]][4]*1+rl[dc[72110800]][4]*1+rl[dc[72110900]][4]*1+rl[dc[72111000]][4]*1+rl[dc[71110100]][4]*1+rl[dc[71110200]][4]*1+rl[dc[71110300]][4]*1+rl[dc[71110400]][4]*1+rl[dc[71110500]][4]*1+rl[dc[71110600]][4]*1+rl[dc[71110700]][4]*1+rl[dc[71110800]][4]*1+rl[dc[71110900]][4]*1+rl[dc[71111000]][4]*1+rl[dc[71111100]][4]*1",item_formula1="rl[dc[72110100]][5]*1+rl[dc[72110200]][5]*1+rl[dc[72110300]][5]*1+rl[dc[72110400]][5]*1+rl[dc[72110500]][5]*1+rl[dc[72110600]][5]*1+rl[dc[72110700]][5]*1+rl[dc[72110800]][5]*1+rl[dc[72110900]][5]*1+rl[dc[72111000]][5]*1+rl[dc[71110100]][5]*1+rl[dc[71110200]][5]*1+rl[dc[71110300]][5]*1+rl[dc[71110400]][5]*1+rl[dc[71110500]][5]*1+rl[dc[71110600]][5]*1+rl[dc[71110700]][5]*1+rl[dc[71110800]][5]*1+rl[dc[71110900]][5]*1+rl[dc[71111000]][5]*1+rl[dc[71111100]][5]*1"),

            ReportItems(item_id=73010000, item_name=u"二、负债类", report=r9) ,
            ReportItems(item_id=73110100, item_name=u"借记款项", report=r9) ,
            ReportItems(item_id=73110200, item_name=u"应付票据", report=r9) ,
            ReportItems(item_id=73110300, item_name=u"应付账款", report=r9) ,
            ReportItems(item_id=73110400, item_name=u"预收账款", report=r9) ,
            ReportItems(item_id=73110500, item_name=u"其他应付款", report=r9) ,
            ReportItems(item_id=73110600, item_name=u"应缴预算款", report=r9) ,
            ReportItems(item_id=73110700, item_name=u"应缴财政专户款", report=r9) ,
            ReportItems(item_id=73110800, item_name=u"应交税金", report=r9) ,
            ReportItems(item_id=73200000, item_name=u"负债合计：", report=r9, item_formula="rl[dc[73110100]][4]*1+rl[dc[73110200]][4]*1+rl[dc[73110300]][4]*1+rl[dc[73110400]][4]*1+rl[dc[73110500]][4]*1+rl[dc[73110600]][4]*1+rl[dc[73110700]][4]*1+rl[dc[73110800]][4]*1",item_formula1="rl[dc[73110100]][5]*1+rl[dc[73110200]][5]*1+rl[dc[73110300]][5]*1+rl[dc[73110400]][5]*1+rl[dc[73110500]][5]*1+rl[dc[73110600]][5]*1+rl[dc[73110700]][5]*1+rl[dc[71110800]][5]*1"),
            ReportItems(item_id=74010000, item_name=u"三、净资产类", report=r9) ,
            ReportItems(item_id=74110100, item_name=u"事业基金", report=r9) ,
            ReportItems(item_id=74110200, item_name=u"其中：一般基金", report=r9) ,
            ReportItems(item_id=74110300, item_name=u"投资基金", report=r9) ,
            ReportItems(item_id=74110400, item_name=u"固定基金", report=r9) ,
            ReportItems(item_id=74110500, item_name=u"专用基金", report=r9) ,
            ReportItems(item_id=74110600, item_name=u"事业结余", report=r9) ,
            ReportItems(item_id=74110700, item_name=u"经营结余", report=r9) ,
            ReportItems(item_id=74200000, item_name=u"净资产合计：", report=r9, item_formula="rl[dc[74110100]][4]*1+rl[dc[74110200]][4]*1+rl[dc[74110300]][4]*1+rl[dc[74110400]][4]*1+rl[dc[74110500]][4]*1+rl[dc[74110600]][4]*1+rl[dc[74110700]][4]*1",item_formula1="rl[dc[74110100]][5]*1+rl[dc[74110200]][5]*1+rl[dc[74110300]][5]*1+rl[dc[74110400]][5]*1+rl[dc[74110500]][5]*1+rl[dc[74110600]][5]*1+rl[dc[74110700]][5]*1"),
            ReportItems(item_id=75010000, item_name=u"四、收入类", report=r9) ,
            ReportItems(item_id=75110100, item_name=u"财政补助收入", report=r9) ,
            ReportItems(item_id=75110200, item_name=u"上级补助收入", report=r9) ,
            ReportItems(item_id=75110300, item_name=u"拨入专款", report=r9) ,
            ReportItems(item_id=75110400, item_name=u"事业收入", report=r9) ,
            ReportItems(item_id=75110500, item_name=u"经营收入", report=r9) ,
            ReportItems(item_id=75110600, item_name=u"附属单位缴款", report=r9) ,
            ReportItems(item_id=75110700, item_name=u"其他收入", report=r9) ,
            ReportItems(item_id=75200000, item_name=u"收入合计：", report=r9, item_formula="rl[dc[75110100]][4]*1+rl[dc[75110200]][4]*1+rl[dc[75110300]][4]*1+rl[dc[75110400]][4]*1+rl[dc[75110500]][4]*1",item_formula1="rl[dc[75110100]][5]*1+rl[dc[75110200]][5]*1+rl[dc[75110300]][5]*1+rl[dc[75110400]][5]*1+rl[dc[75110500]][5]*1"),
            ReportItems(item_id=75300000, item_name=u"负债部类总计：", report=r9, item_formula="rl[dc[75110100]][4]*1+rl[dc[75110200]][4]*1+rl[dc[75110300]][4]*1+rl[dc[75110400]][4]*1+rl[dc[75110500]][4]*1+rl[dc[74110100]][4]*1+rl[dc[74110200]][4]*1+rl[dc[74110300]][4]*1+rl[dc[74110400]][4]*1+rl[dc[74110500]][4]*1+rl[dc[74110600]][4]*1+rl[dc[74110700]][4]*1+rl[dc[73110100]][4]*1+rl[dc[73110200]][4]*1+rl[dc[73110300]][4]*1+rl[dc[73110400]][4]*1+rl[dc[73110500]][4]*1+rl[dc[73110600]][4]*1+rl[dc[73110700]][4]*1+rl[dc[73110800]][4]*1",item_formula1="rl[dc[75110100]][5]*1+rl[dc[75110200]][5]*1+rl[dc[75110300]][5]*1+rl[dc[75110400]][5]*1+rl[dc[75110500]][5]*1+rl[dc[74110100]][5]*1+rl[dc[74110200]][5]*1+rl[dc[74110300]][5]*1+rl[dc[74110400]][5]*1+rl[dc[74110500]][5]*1+rl[dc[74110600]][5]*1+rl[dc[74110700]][5]*1+rl[dc[73110100]][5]*1+rl[dc[73110200]][5]*1+rl[dc[73110300]][5]*1+rl[dc[73110400]][5]*1+rl[dc[73110500]][5]*1+rl[dc[73110600]][5]*1+rl[dc[73110700]][5]*1+rl[dc[71110800]][5]*1"),
            # 收入支出表（事业单位）
            ReportItems(item_id=81010100, item_name=u"财政补助收入", report=r10) ,
            ReportItems(item_id=81010200, item_name=u"上级补助收入", report=r10) ,
            ReportItems(item_id=81010300, item_name=u"附属单位缴款", report=r10) ,
            ReportItems(item_id=81010400, item_name=u"事业收入", report=r10) ,
            ReportItems(item_id=81010500, item_name=u"其中：预算外资金收入", report=r10) ,
            ReportItems(item_id=81010600, item_name=u"其他收入", report=r10) ,
            ReportItems(item_id=81010700, item_name=u"小计", report=r10) ,
            ReportItems(item_id=81010800, item_name=u"经营收入", report=r10) ,
            ReportItems(item_id=81010900, item_name=u"小计", report=r10) ,
            ReportItems(item_id=81011000, item_name=u"拨入专款", report=r10) ,
            ReportItems(item_id=81011100, item_name=u"小计", report=r10) ,
            ReportItems(item_id=81011200, item_name=u"总计", report=r10) ,
            ReportItems(item_id=81011300, item_name=u"拨出经费", report=r10) ,
            ReportItems(item_id=81011400, item_name=u"上缴上级支出", report=r10) ,
            ReportItems(item_id=81011500, item_name=u"对附属单位补助", report=r10) ,
            ReportItems(item_id=81011600, item_name=u"事业支出", report=r10) ,
            ReportItems(item_id=81011700, item_name=u"其中：财政补助支出", report=r10) ,
            ReportItems(item_id=81011800, item_name=u"预算外资金支出", report=r10) ,
            ReportItems(item_id=81011900, item_name=u"销售税金", report=r10) ,
            ReportItems(item_id=81012000, item_name=u"结转自筹基建", report=r10) ,
            ReportItems(item_id=81012100, item_name=u"小计", report=r10) ,
            ReportItems(item_id=81012200, item_name=u"经营支出", report=r10) ,
            ReportItems(item_id=81012300, item_name=u"销售税金", report=r10) ,
            ReportItems(item_id=81012400, item_name=u"小计", report=r10) ,
            ReportItems(item_id=81012500, item_name=u"拨出专款", report=r10) ,
            ReportItems(item_id=81012600, item_name=u"专款支出", report=r10) ,
            ReportItems(item_id=81012700, item_name=u"小计", report=r10) ,
            ReportItems(item_id=81012800, item_name=u"总计", report=r10) ,
            ReportItems(item_id=81020000, item_name=u"事业结余", report=r10) ,
            ReportItems(item_id=81020100, item_name=u"1.正常收入结余", report=r10) ,
            ReportItems(item_id=81020200, item_name=u"2.收回以前年度事业支出", report=r10) ,
            ReportItems(item_id=81030000, item_name=u"经营结余", report=r10) ,
            ReportItems(item_id=81030100, item_name=u"以前年度经营亏损（一）", report=r10) ,
            ReportItems(item_id=81030200, item_name=u"结余分配", report=r10) ,
            ReportItems(item_id=81030300, item_name=u"1.应交所得税", report=r10) ,
            ReportItems(item_id=81030400, item_name=u"2.提取专用基金", report=r10) ,
            ReportItems(item_id=81030500, item_name=u"3.转入事业基金", report=r10) ,
            ReportItems(item_id=81030600, item_name=u"4.其他", report=r10)
        ])

    session.commit()
