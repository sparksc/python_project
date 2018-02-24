#-*-coding:utf-8-*-
import datetime,xlrd
from flask import json, g, current_app
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all,aliased
from ..base import utils
from ..model.ebank_replace import EBANK_REPLACE_NUM
from ..model import D_DATE,Branch
from decimal import Decimal
import datetime

class Ebank_replaceService():
    def upload(self, filepath, filename):
        try:
            today = datetime.date.today()
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            
            nrows = sheet.nrows
            if nrows in [0, 7]:
                raise Exception(u"导入文件是空文件")
            list = []
        except Exception, e:
            return str(e)
        all_msg = []
        for r in range(7, nrows):
            try: 
                date = str(sheet.cell(1, 0).value)
                m1 = date.split('： ')
                m2 = m1[1]
                if m2 == '':
                    raise Exception(u'请填写excel的日期')
                m3 = int(m2.replace('-',''))
                
                branch_code =str((sheet.cell(r, 1).value)).replace('.0','').replace('.00','').strip()
                if branch_code == '':
                    raise Exception(u'请填写机构号')

                branch_name = str(sheet.cell(r, 2).value)
                atmbh = int(Decimal(str(sheet.cell(r, 3).value))*10000)
                atmtdb = int(Decimal(str(sheet.cell(r, 4).value))*10000)
                atmbdt = int(Decimal(str(sheet.cell(r, 5).value))*10000)
                atm_total =  int(Decimal(str(sheet.cell(r, 6).value))*10000)
                posbh =  int(Decimal(str(sheet.cell(r, 7).value))*10000)
                postdb =  int(Decimal(str(sheet.cell(r, 8).value))*10000)
                posbdt =  int(Decimal(str(sheet.cell(r,9).value))*10000)
                pos_total =  int(Decimal(str(sheet.cell(r, 10).value))*10000)
                ebank_indi =  int(Decimal(str(sheet.cell(r, 11).value))*10000)
                ebank_enterprise =  int(Decimal(str(sheet.cell(r, 12).value))*10000)
                ebank_total =  int(Decimal(str(sheet.cell(r, 13).value))*10000)
                cellphone_bank =  int(Decimal(str(sheet.cell(r, 14).value))*10000)
                tell_bank = int(Decimal(str(sheet.cell(r, 15).value))*10000)
                mess_bank =  int(Decimal(str(sheet.cell(r, 16).value))*10000)
                auto_bank = int(Decimal(str(sheet.cell(r, 17).value))*10000)
                e_pay =  int(Decimal(str(sheet.cell(r, 18).value))*10000)
                alipay_five =  sheet.cell(r, 19).value
                if alipay_five == '':
                    alipay_five = 0.0000
                alipay_five = int(alipay_five * 10000)
                num1 =  int(Decimal(str(sheet.cell(r, 20).value))*10000)
                num2 =  int(Decimal(str(sheet.cell(r, 21).value))*10000)
                term_num =  int(Decimal(str(sheet.cell(r, 41).value))*10000)
                replace_num1 =  round(Decimal(sheet.cell(r,43).value),4)
                replace_num2 =  round(Decimal(sheet.cell(r, 44).value),4)
                replace_amount1 =  round(Decimal(sheet.cell(r, 45).value),4)
                replace_amount2 =  round(Decimal(sheet.cell(r, 46).value),4)

                d = g.db_session.query(D_DATE).filter(D_DATE.ID == m3).first()
                if not d:
                    raise Exception(u'日期有误')

                month_end = g.db_session.query(D_DATE.MONTH_END).filter(D_DATE.ID == m3).first()
                if month_end[0] == 'N':
                    raise Exception(u'excel文件导入日期不是月末，请确认导入日期')

                branch = g.db_session.query(Branch).filter(Branch.branch_code == branch_code).first()
                if not branch:
                    raise Exception(u'第'+str(r+1)+u'行，'+str(branch_code)+'机构不存在')

                fdata = g.db_session.query(EBANK_REPLACE_NUM).filter(EBANK_REPLACE_NUM.DATE == m3).filter(EBANK_REPLACE_NUM.BRANCH_CODE == branch_code).first()
                if fdata:
                    raise Exception ( u'第'+str(r+1)+u'行，'+str(m3)+'月报的'+str(branch_code)+'机构数据已存在')

                temp = {'DATE': m3,
                        'BRANCH_CODE': branch_code,
                        'BRANCH_NAME': branch_name,
                        'ATMBH': atmbh,
                        'ATMTDB': atmtdb,
                        'ATMBDT': atmbdt,
                        'ATM_TOTAL': atm_total,
                        'POSBH': posbh,
                        'POSTDB': postdb,
                        'POSBDT': posbdt,
                        'POS_TOTAL': pos_total,
                        'EBANK_INDI': ebank_indi,
                        'EBANK_ENTERPRISE': ebank_enterprise,
                        'EBANK_TOTAL': ebank_total,
                        'CELLPHONE_BANK': cellphone_bank,
                        'TELL_BANK': tell_bank,
                        'MESS_BANK': mess_bank,
                        'AUTO_BANK': auto_bank,
                        'E_PAY': e_pay,
                        'ALIPAY_FIVE': alipay_five,
                        'NUM1': num1,
                        'NUM2': num2,
                        'TERM_NUM': term_num,
                        'REPLACE_NUM1': replace_num1,
                        'REPLACE_NUM2': replace_num2,
                        'REPLACE_AMOUNT1': replace_amount1,
                        'REPLACE_AMOUNT2': replace_amount2
                        }

                all_msg.append(temp)

            except ValueError, e:
                g.db_session.rollback()
                return u'第'+str(r + 1) + u'行有错误,'+u"请检查该行是否有值为空或包含非法字符"
#            except IndexError,e:
#                g.db_session.rollback()
#                return u'第'+str(r+1)+u'行有错误,请检查列数'
            except Exception, e:
                g.db_session.rollback()
                print Exception, ':', e
                #return u'第' + str(r + 1) + u'行有错误,'+str(e)
                return str(e)

        for i in range(0,len(all_msg)):
            g.db_session.add(EBANK_REPLACE_NUM(**all_msg[i]))

        return u'导入成功'
