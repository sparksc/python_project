# -*- coding:utf-8 -*-
from nose.tools import eq_, raises, assert_true
from sqlalchemy.orm import aliased
import unittest
import json
import time
import logging
from sys import modules
import datetime
import random
from ..model.customer import *
from ..model.party import *
from ..model.common import *
from ..model.user import *
from ..model.common import *
from ..model.report import *
#from ..database.logger import  log
from db2_utils import DB2
log = logging.getLogger()
#log = logging.getLogger()
#log.basicConfig(level=logging.DEBUG)

class TestLoadInfo():

    def setUp(self):
        log.debug("执行setup")
        self.session=simple_session()
        Base.metadata.create_all(self.session.bind)
    def convert_year_month(self,YM):
        if '-' in YM:
            return None;
        else:
            return YM.strip();
    # def use_call(self,session):
        # self.session= session
        # self.recordinfo()
        # self.datainfo()
    # def recordinfo(self): 
        # period_map = {'1':u'月报','2':u'季报','3':u'半年报','4':u'年报'}
        # db2= DB2()
        # db2.db_conn()
        # log.debug('-------------------------------')
        # db2.exesql("select * from CUS_COM_RPT ","CUS_COM_RPT")
        # while db2.is_end() == False:
            # cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            # if cus_id ==None:
                # db2.get_next()
                # continue;
            # YM = db2.get_byName("RPT_YM")
            # ym = self.convert_year_month(YM)
            # if ym == None:
                # db2.get_next()
                # continue;
            # record = ReportRecord(report_period=period_map[db2.get_byName("RPT_CYCLE_TYPE").strip()],
                            # year_month=ym,
                            # report_date=db2.get_byName("REG_DATE"),
                            # opertor_id=db2.get_byName("REG_OPT_ID").strip(),
                            # company_id=cus_id.id)
            # self.session.add(record)
            # db2.get_next()
            # self.session.commit()
    def test_datainfo(self):  
        item_map = {'Z01000000':u'1010000','Z01010000':u'1020000','Z01010100':u'1020100','Z01010210':u'1020200','Z01010220':u'1020210','Z01010200':u'1020300','Z01010300':u'1020400', \
        'Z01010400':u'1020500','Z01010500':u'1020600','Z01010610':u'1020700','Z01010620':u'1020710','Z01010600':u'1020800','Z01010700':u'1020900','Z01010800':u'1021000','Z01010900':u'1021100', \
        'Z01011000':u'1021200','Z01011100':u'1021300','Z01011210':u'1021400','Z02000000':u'2010000','Z02010000':u'2020000','Z02010100':u'2020100','Z02010200':u'2020200','Z02010300':u'2020300', \
        'Z02010400':u'2020400','Z02010500':u'2020500','Z02010600':u'2020600','Z02010700':u'2020700','Z02010800':u'2020900','Z01011211':u'1021410','Z01011212':u'1021420','Z01011220':u'1021430', \
        'Z01011200':u'1021500','Z01011300':u'1021600','Z01011400':u'1021700','Z01011500':u'1021800','Z01011600':u'1021900','Z01020000':u'1030000','Z01010001':u'1022000','Z01020100':u'1030100', \
        'Z01020110':u'1030110','Z01020120':u'1030120','Z01020200':u'1030200','Z01020001':u'1030300','Z01030000':u'1040000','Z01030111':u'1040100','Z01030112':u'1040110','Z01030110':u'1040200', \
        'Z01030120':u'1040210','Z01030100':u'1040300','Z01030200':u'1040400','Z01030300':u'1040500','Z01030400':u'1040600','Z01030500':u'1040700','Z01030001':u'1040800','Z01040000':u'1050000', \
        'Z01040100':u'1050100','Z01040110':u'1050110','Z01040200':u'1050200','Z01040210':u'1050210','Z01040220':u'1050220','Z01040300':u'1050300','Z01040310':u'1050310','Z01040001':u'1060000', \
        'Z01050001':u'1060100','Z01000001':u'1100000','Z02010900':u'2021000','Z02011000':u'2021100','Z02011100':u'2021200','Z02011200':u'2021200','Z02011300':u'2021300','Z02011400':u'2021400', \
        'Z02010001':u'2021500','Z02020000':u'2131000','Z02020100':u'2150000','Z02020200':u'2150100','Z02020300':u'2150300','Z02020400':u'2150400','Z02020500':u'2150500','Z02020520':u'2150510', \
        'Z02020001':u'2200000','Z02030000':u'2350000','Z02030001':u'2350100','Z02000001':u'2400000','Z03000000':u'3010000','Z03000001':u'3100000','Z04000000':u'4010000','Z04010000':u'4020100', \
        'Z04010100':u'4020110','Z04010200':u'4020120','Z04010300':u'4020130','Z04010310':u'4020131','Z04010320':u'4020132','Z04010400':u'4020140','Z04010500':u'4020150','Z04020000':u'4020200', \
        'Z04030000':u'4020400','Z04030100':u'4020410','Z04030200':u'4020420','Z04030300':u'4020430','L05040000':u'15110200','Z04050000':u'4020600','Z04060000':u'4020700','Z04000001':u'4100000', \
        'Z05000000':u'5100000','L01000000':u'10100000','L01010100':u'11110100','L01010200':u'11110200','L01020000':u'11120300','L02010000':u'12100000','L02020000':u'12110100','L02020100':u'12110111', \
        'X01000000':u'21100000','L02040000':u'12110130','L02050000':u'12110140','L02060000':u'12120100','L02070000':u'12120110','L02080000':u'12120120','L03010000':u'13100000','L03020000':u'13110100', \
        'L03030000':u'13110200','L03040000':u'13110310','L03050000':u'13110410','L03060000':u'14110710','L04050100':u'14110510','L04050200':u'14110611','L04050300':u'14110612','L04050400':u'14110613', \
        'L04060100':u'14110711','L04070000':u'14110800','L04070100':u'14110810','L04070200':u'14110821','L04070300':u'14110831','L04070400':u'14110841','L04080000':u'14110910','L04080100':u'14111011', \
        'L04040100':u'14110311','L04090000':u'14111100','L05010000':u'15100000','L05020000':u'15110100','L05030000':u'15110110','X01010000':u'21110100','L06010000':u'16100000','L06020000':u'16110100', \
        'L06030000':u'16110110','L06040000':u'16110120','L07010000':u'17100000','L07020000':u'17110100','L07030000':u'17110110','L07040000':u'17110120','L07050000':u'17110130','L07060000':u'17110140', \
        'L07070000':u'17110150','L07080000':u'17110160','L07090000':u'17110170','L070a0000':u'17110180','L08010000':u'18100000','L08020000':u'18110100','L08030000':u'18110110','L08040000':u'18110120', \
        'L08050000':u'18110130','L08060000':u'18110140','L09010000':u'19000000','L09010100':u'19010100','L02030000':u'12110120','X01020000':u'21110200','X05010101':u'25010101','X05010102':u'25010102', \
        'X01040000':u'21110311','X01030000':u'21110300','X01050000':u'21110400','X01060000':u'21110500','X01070000':u'21110600','X01080000':u'21110700','X01090000':u'21110711','X01100000':u'21110800', \
        'X02000000':u'22110200','X02010000':u'22110100','X02020000':u'22110200','X02040000':u'22110400','X02050000':u'22110411','X02060000':u'22110600','X02070000':u'22110500','X02080000':u'22110700', \
        'X02090000':u'22110711','X02100000':u'22110800','X03000000':u'23010000','X03010000':u'23110100','X03020000':u'23110200','X03030000':u'23110300','X03040000':u'23110311','X03050000':u'23110400', \
        'X03060000':u'23110500','X03070000':u'23110600','X03080000':u'23110611','X03090000':u'23110700','X04000000':u'24000000','X05000000':u'25000000','X05010000':u'25010000','X05010100':u'25010100', \
        'X05010103':u'25010103','X05010104':u'25010104','X05010105':u'25010105','X05010106':u'25010106','X05010107':u'25010107','X05010108':u'25010108','X05010110':u'25010110','X05010111':u'25010111', \
        'X05010112':u'25010112','X05010113':u'25010113','X05010114':u'25010114','X05010115':u'25010115','X05010116':u'25010116','X05010117':u'25010117','X05020000':u'25020000','X05020100':u'25020100', \
        'X05020200':u'25020200','X05020300':u'25020300','X05020400':u'25020400','X05030000':u'25030000','X05030100':u'25030100','X05030200':u'25030200','X05030300':u'25030300','X05030400':u'25030400', \
        'X05030500':u'25030500','X02030000':u'25010107','Z04040000':u'4020500','C01000000':u'31010000','C01010000':u'31110100','C01020000':u'31110200','C01030000':u'31110300','C01040000':u'31110400', \
        'C01050000':u'31110500','C01060000':u'31110600','C01070000':u'31110700','C01100000':u'31110800','C01110000':u'31110900','C01120000':u'31111000','C01130000':u'31111100','C01140000':u'31111200', \
        'C02000000':u'32010000','C02010000':u'32110100','C02020000':u'32110200','C02030000':u'32110400','C02040000':u'32110500','C02050000':u'32110600','C02060000':u'32110700','C03000000':u'33010000', \
        'C03010000':u'33110100','C03020000':u'33110200','C03030000':u'33110300','C03040000':u'33110400','C03050000':u'33110500','C03060000':u'33110600','C03070000':u'33110700','C03080000':u'33110800', \
        'D01000000':u'41010000','D01010000':u'41020000','D01010100':u'41020100','D01010200':u'41020200','D01010300':u'41020300','D01010400':u'41020400','D01010500':u'41020500','D01010600':u'41020600', \
        'D01010700':u'41020700','D01010800':u'41020800','D01010900':u'41020900','D01011000':u'41021000','D01011100':u'41021100','D01010001':u'41100000','D01010002':u'41120000','D01011200':u'41120100', \
        'D01011300':u'41120200','D01011400':u'41120300','D01011500':u'41120400','D01011600':u'41120500','D01011700':u'41120600','D01011800':u'41120700','D01011900':u'41120800','D01012000':u'41120900', \
        'D01012100':u'41121000','D01012200':u'41121100','D01012300':u'41121200','D01012400':u'41121300','D01012500':u'41121400','D01012600':u'41121500','D01012700':u'41121600','D01012800':u'41121700', \
        'C03090000':u'33110900','C03100000':u'33111000','C04000000':u'34010000','C04010000':u'34110100','C04020000':u'34110200','C04030000':u'34110300','C04040000':u'34110400','C04050000':u'34110500', \
        'C04060000':u'34110700','C05000000':u'35010000','C05010000':u'35110100','C05020000':u'35110200','C05030000':u'35110300','C05040000':u'35110400','C05050000':u'35110500','C05060000':u'35110600', \
        'C06000000':u'37010000','C06010000':u'37020100','C06020000':u'37020200','Z06000100':u'6100000','C02070000':u'32110300','C03110000':u'33111100','C03120000':u'33111200','C04070000':u'34110600', \
        'L04010000':u'14100000','L04050000':u'14110410','L04020000':u'14110100','L04060000':u'14110710','E01000000':u'51000000','L04030000':u'14110210','L04040000':u'14110310','D01010003':u'41200000', \
        'D02000000':u'42010000','D02010000':u'42020000','D02010100':u'42020100','D02010200':u'42020200','D02010300':u'42020300','D02010400':u'42020400','D02010500':u'42020500','D02010600':u'42020600', \
        'D02010700':u'42020700','D02010800':u'42020800','D02010900':u'42020900','D02011000':u'42021000','D02011100':u'42021100','D02011200':u'42021200','D02010001':u'42100000','D02010002':u'42120000', \
        'D02011400':u'42120100','D02011410':u'42120200','D02011500':u'42120300','D02011600':u'42120400','D02011700':u'42120500','D02011800':u'42120600','D02011900':u'42120700','D02010003':u'42200000', \
        'D02000001':u'42300000','D03010100':u'43010100','D03010200':u'43010200','D03010300':u'43010300','D03010400':u'43010400','D03010500':u'43010500','D03000000':u'43100000','D03000001':u'43200000', \
        'F01000000':u'61010000','F01010100':u'61110100','F01010200':u'61110200','F01010300':u'61110300','F01010400':u'61110400','F01010500':u'61110500','F01010600':u'61110600','F01010700':u'61110700', \
        'F01010800':u'61110800','F01010900':u'61110900','F01011000':u'61111000','F02000000':u'62010000','F02010100':u'62110100','F02010200':u'62110200','F02010300':u'62110300','F02010400':u'62110400', \
        'F02010500':u'62110500','F02010600':u'62110600','F02010700':u'62110700','F02010800':u'62110800','F02010900':u'62110900','F02011000':u'62111000','F02011100':u'62111100','F02011200':u'62111200', \
        'F03000000':u'63010000','F03010100':u'63110100','F03010200':u'63110200','F03010300':u'63110300','F03010400':u'63110400','F03010500':u'63110500','F03010600':u'63110600','F03010700':u'63110700', \
        'F03010800':u'63110800','F03010900':u'63110900','F03011000':u'64000000','F03011100':u'65000000','F03011200':u'65010100','F03011300':u'66000000','F04000000':u'66010000','F04010100':u'66020000', \
        'F04010200':u'66020100','F04010300':u'66020200','F04010400':u'66020210','F04010500':u'66020220','F04010600':u'66020230','F04010700':u'66020240','F04010800':u'66020250','F04010900':u'66020260', \
        'F04011000':u'66020270','F04011100':u'66020280','F04011200':u'66020290','F04011300':u'66020310','F04011400':u'66020320','F04011500':u'66020400','F04011600':u'66020410','F04011700':u'66020420', \
        'F04011800':u'66020430','F04011900':u'66020500','F04012000':u'66020600','F04012100':u'66030000','F04012200':u'66030100','F04012300':u'66030200','F04012400':u'66030300','F04012500':u'66030400', \
        'F04012600':u'66040000','F04012700':u'66040200','F04012800':u'66040300','F04012900':u'66040400','F04013000':u'66040500','F04013100':u'66040600','D01000001':u'41300000'}
        db2= DB2()
        db2.db_conn()
        # 月报1月
        db2.exesql("select * from CUS_COM_BS_ITEMS  where ITEM_ID LIKE '%D%' and INIT_AMOUNT1 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"01").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT1"),
                            value2=db2.get_byName("END_AMOUNT1"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报2月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT2 is not NULL ","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"02").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT2"),
                            value2=db2.get_byName("END_AMOUNT2"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报3月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT3 is not NULL ","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"03").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT3"),
                            value2=db2.get_byName("END_AMOUNT3"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报4月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT4 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"04").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT4"),
                            value2=db2.get_byName("END_AMOUNT4"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报5月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT5 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"05").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT5"),
                            value2=db2.get_byName("END_AMOUNT5"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报6月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT6 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT6"),
                            value2=db2.get_byName("END_AMOUNT6"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报7月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT7 is not NULL ","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"07").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT7"),
                            value2=db2.get_byName("END_AMOUNT7"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报8月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT8 is not NULL ","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"08").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT8"),
                            value2=db2.get_byName("END_AMOUNT8"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报9月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT9 is not NULL ","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"09").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT9"),
                            value2=db2.get_byName("END_AMOUNT9"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报10月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT10 is not NULL ","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"10").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT10"),
                            value2=db2.get_byName("END_AMOUNT10"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报11月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT11 is not NULL ","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"11").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT11"),
                            value2=db2.get_byName("END_AMOUNT11"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报12月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT12 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT12"),
                            value2=db2.get_byName("END_AMOUNT12"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报3月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT_Q1 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"03").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Q1"),
                            value2=db2.get_byName("END_AMOUNT_Q1"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报6月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT_Q2 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Q2"),
                            value2=db2.get_byName("END_AMOUNT_Q2"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报9月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT_Q3 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"09").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Q3"),
                            value2=db2.get_byName("END_AMOUNT_Q3"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报12月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT_Q4 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Q4"),
                            value2=db2.get_byName("END_AMOUNT_Q4"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 半年报6月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT_Y1 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"半年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Y1"),
                            value2=db2.get_byName("END_AMOUNT_Y1"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 半年报12月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT_Y2 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"半年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Y2"),
                            value2=db2.get_byName("END_AMOUNT_Y2"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 年报12月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%D%' and INIT_AMOUNT_Y is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="6",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Y"),
                            value2=db2.get_byName("END_AMOUNT_Y"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
            # CF
        db2= DB2()
        db2.db_conn()
        # 月报1月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT1 is not NULL ","CUS_COM_CF_ITEMS")
        # for i in range(0,1393):
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"01").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT1"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # # 月报2月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT2 is not NULL ","CUS_COM_CF_ITEMS")
        # for i in range(0,3380):
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"02").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT2"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报3月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT3 is not NULL ","CUS_COM_CF_ITEMS")
        # for i in range(0,60000):
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"03").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT3"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报4月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT4 is not NULL ","CUS_COM_CF_ITEMS")
        # for i in range(0,60000):
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"04").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT4"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报5月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT5 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"05").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT5"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报6月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT6 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT6"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报7月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT7 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"07").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT7"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报8月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT8 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"08").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT8"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报9月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT9 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"09").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT9"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报10月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT10 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"10").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT10"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报11月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT11 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"11").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT11"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报12月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT12 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT12"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报3月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT_Q1 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"03").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Q1"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报6月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT_Q2 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Q2"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报9月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT_Q3 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"09").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Q3"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报12月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT_Q4 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Q4"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 半年报6月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT_Y1 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"半年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Y1"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 半年报12月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT_Y2 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"半年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Y2"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 年报12月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%F%' and ITEM_AMOUT_Y is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="8",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Y"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
      
     db2= DB2()
        db2.db_conn()
        # 月报1月
        db2.exesql("select * from CUS_COM_BS_ITEMS  where ITEM_ID LIKE '%Z%' and INIT_AMOUNT1 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"01").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT1"),
                            value2=db2.get_byName("END_AMOUNT1"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报2月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT2 is not NULL ","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"02").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT2"),
                            value2=db2.get_byName("END_AMOUNT2"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报3月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT3 is not NULL ","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"03").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT3"),
                            value2=db2.get_byName("END_AMOUNT3"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报4月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT4 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"04").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT4"),
                            value2=db2.get_byName("END_AMOUNT4"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报5月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT5 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"05").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT5"),
                            value2=db2.get_byName("END_AMOUNT5"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报6月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT6 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT6"),
                            value2=db2.get_byName("END_AMOUNT6"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报7月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT7 is not NULL ","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"07").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT7"),
                            value2=db2.get_byName("END_AMOUNT7"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报8月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT8 is not NULL ","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"08").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT8"),
                            value2=db2.get_byName("END_AMOUNT8"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报9月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT9 is not NULL ","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"09").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT9"),
                            value2=db2.get_byName("END_AMOUNT9"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报10月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT10 is not NULL ","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"10").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT10"),
                            value2=db2.get_byName("END_AMOUNT10"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报11月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT11 is not NULL ","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"11").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT11"),
                            value2=db2.get_byName("END_AMOUNT11"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报12月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT12 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT12"),
                            value2=db2.get_byName("END_AMOUNT12"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报3月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT_Q1 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"03").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Q1"),
                            value2=db2.get_byName("END_AMOUNT_Q1"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报6月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT_Q2 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Q2"),
                            value2=db2.get_byName("END_AMOUNT_Q2"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报9月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT_Q3 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"09").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Q3"),
                            value2=db2.get_byName("END_AMOUNT_Q3"))
            self.session.add(data)
            db2.get_next()
        self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报12月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT_Q4 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Q4"),
                            value2=db2.get_byName("END_AMOUNT_Q4"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 半年报6月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT_Y1 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"半年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Y1"),
                            value2=db2.get_byName("END_AMOUNT_Y1"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 半年报12月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT_Y2 is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"半年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Y2"),
                            value2=db2.get_byName("END_AMOUNT_Y2"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 年报12月
        db2.exesql("select * from CUS_COM_BS_ITEMS where ITEM_ID LIKE '%Z%' and INIT_AMOUNT_Y is not NULL","CUS_COM_BS_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="1",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Y"),
                            value2=db2.get_byName("END_AMOUNT_Y"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
            # FI
        db2= DB2()
        db2.db_conn()
        # 月报1月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT1 is not NULL ","CUS_COM_FI_ITEMS")
        # for i in range(0,1393):
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"01").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT1"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # # 月报2月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT2 is not NULL ","CUS_COM_FI_ITEMS")
        # for i in range(0,3380):
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"02").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT2"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报3月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT3 is not NULL ","CUS_COM_FI_ITEMS")
        # for i in range(0,60000):
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"03").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT3"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报4月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT4 is not NULL ","CUS_COM_FI_ITEMS")
        # for i in range(0,60000):
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"04").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT4"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报5月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT5 is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"05").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT5"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报6月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT6 is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT6"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报7月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT7 is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"07").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT7"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报8月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT8 is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"08").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT8"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报9月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT9 is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"09").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT9"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报10月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT10 is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"10").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT10"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报11月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT11 is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"11").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT11"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报12月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT12 is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT12"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报3月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT_Q1 is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"03").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Q1"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报6月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT_Q2 is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Q2"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报9月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT_Q3 is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"09").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUT_Q3"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报12月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT_Q4 is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Q4"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 半年报6月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT_Y1 is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"半年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Y1"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 半年报12月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT_Y2 is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"半年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Y2"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 年报12月
        db2.exesql("select * from CUS_COM_FI_ITEMS where ITEM_ID LIKE '%C%' and ITEM_AMOUT_Y is not NULL ","CUS_COM_FI_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="4",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Y"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
            # CF
        db2= DB2()
        db2.db_conn()
        # 月报1月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT1 is not NULL ","CUS_COM_CF_ITEMS")
        # for i in range(0,1393):
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"01").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT1"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # # 月报2月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT2 is not NULL ","CUS_COM_CF_ITEMS")
        # for i in range(0,3380):
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"02").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT2"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报3月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT3 is not NULL ","CUS_COM_CF_ITEMS")
        # for i in range(0,60000):
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"03").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT3"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报4月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT4 is not NULL ","CUS_COM_CF_ITEMS")
        # for i in range(0,60000):
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"04").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT4"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报5月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT5 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"05").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT5"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报6月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT6 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT6"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报7月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT7 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"07").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT7"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报8月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT8 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"08").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT8"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报9月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT9 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"09").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT9"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报10月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT10 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"10").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT10"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报11月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT11 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"11").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT11"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报12月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT12 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT12"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报3月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT_Q1 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"03").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Q1"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报6月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT_Q2 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Q2"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报9月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT_Q3 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"09").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Q3"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报12月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT_Q4 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Q4"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 半年报6月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT_Y1 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"半年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Y1"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 半年报12月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT_Y2 is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"半年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Y2"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 年报12月
        db2.exesql("select * from CUS_COM_CF_ITEMS where ITEM_ID LIKE '%X%' and ITEM_AMOUT_Y is not NULL ","CUS_COM_CF_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="3",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("ITEM_AMOUT_Y"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        # PL
        db2= DB2()
        db2.db_conn()
        # 月报1月
        db2.exesql("select * from CUS_COM_PL_ITEMS  where ITEM_ID LIKE '%L%' and INIT_AMOUNT1 is not NULL","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"01").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT1"),
                            value2=db2.get_byName("END_AMOUNT1"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报2月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT2 is not NULL ","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"02").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT2"),
                            value2=db2.get_byName("END_AMOUNT2"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报3月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT3 is not NULL ","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"03").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT3"),
                            value2=db2.get_byName("END_AMOUNT3"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报4月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT4 is not NULL","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"04").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT4"),
                            value2=db2.get_byName("END_AMOUNT4"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报5月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT5 is not NULL","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"05").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT5"),
                            value2=db2.get_byName("END_AMOUNT5"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报6月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT6 is not NULL","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT6"),
                            value2=db2.get_byName("END_AMOUNT6"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报7月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT7 is not NULL ","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"07").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT7"),
                            value2=db2.get_byName("END_AMOUNT7"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报8月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT8 is not NULL ","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"08").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT8"),
                            value2=db2.get_byName("END_AMOUNT8"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报9月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT9 is not NULL ","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"09").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT9"),
                            value2=db2.get_byName("END_AMOUNT9"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报10月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT10 is not NULL ","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"10").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT10"),
                            value2=db2.get_byName("END_AMOUNT10"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报11月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT11 is not NULL ","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"11").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT11"),
                            value2=db2.get_byName("END_AMOUNT11"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 月报12月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT12 is not NULL","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"月报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT12"),
                            value2=db2.get_byName("END_AMOUNT12"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报3月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT_Q1 is not NULL","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"03").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Q1"),
                            value2=db2.get_byName("END_AMOUNT_Q1"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报6月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT_Q2 is not NULL","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Q2"),
                            value2=db2.get_byName("END_AMOUNT_Q2"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报9月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT_Q3 is not NULL","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"09").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Q3"),
                            value2=db2.get_byName("END_AMOUNT_Q3"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 季报12月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT_Q4 is not NULL","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"季报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Q4"),
                            value2=db2.get_byName("END_AMOUNT_Q4"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 半年报6月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT_Y1 is not NULL","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"半年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"06").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Y1"),
                            value2=db2.get_byName("END_AMOUNT_Y1"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 半年报12月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT_Y2 is not NULL","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"半年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Y2"),
                            value2=db2.get_byName("END_AMOUNT_Y2"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
        db2= DB2()
        db2.db_conn()
        # 年报12月
        db2.exesql("select * from CUS_COM_PL_ITEMS where ITEM_ID LIKE '%L%' and INIT_AMOUNT_Y is not NULL","CUS_COM_PL_ITEMS")
        while db2.is_end() == False:
            cus_id = self.session.query(Party).filter(Party.no.like(db2.get_byName("CUS_ID").strip()+'%')).first()
            if cus_id ==None:
                db2.get_next()
                continue;
            rec_id = self.session.query(ReportRecord).filter(ReportRecord.report_period==u"年报").filter(ReportRecord.year_month==db2.get_byName("RPT_YEAR").strip()+"12").filter(ReportRecord.company_id==cus_id.id).first()
            log.debug(rec_id);
            if rec_id ==None:
                db2.get_next()
                continue;
            data = ReportData(record_id=rec_id.id,
                            report_id="2",
                            item_id=item_map[db2.get_byName("ITEM_ID").strip()],
                            value1=db2.get_byName("INIT_AMOUNT_Y"),
                            value2=db2.get_byName("END_AMOUNT_Y"))
            self.session.add(data)
            db2.get_next()
            self.session.commit()
    def tearDown(self):
        self.session.commit() 
        log.debug("Over")

