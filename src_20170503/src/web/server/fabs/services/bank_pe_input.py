# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime
from flask import json, g,current_app
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all
import xlrd
from ..base import utils
from ..model import Branch,Menu,User,UserBranch,Bank_ProfitEarning_Input


class BankProfitEarningService():
    """ Target Service  """

    def save(self,**kwargs):
        try:
             self.ckyy = ['syear','org_code','org_name','year_profit','year_earning']
             newdata =  kwargs.get('newdata')
             data ={}

             for k,v in newdata.items():
                 if k in self.ckyy :
                     if k=='year_profit':
                         v=float(v)
                   
                     if k=='year_earning':
                         v=float(v)
                         if v < 0:
                            return u"年度营业收入不能为负"
                     
                     data[k] = v

                     if k=='syear':
                         syear=v
                     if k=='org_code':
                         org_code=v
                     if k=='org_name':
                         org_name=v
             item  = g.db_session.query(Bank_ProfitEarning_Input).filter(Bank_ProfitEarning_Input.syear == syear).filter(Bank_ProfitEarning_Input.org_code==org_code).first()
             if item:
                return u'添加失败,'+str(syear)+'年'+str(org_name).strip()+'数据已存在'

             g.db_session.add(Bank_ProfitEarning_Input(**data))
             
        except Exception, e:
            g.db_session.rollback()
            print type(e), Exception, 'BankProfitEarningService:save error'
            return str(e)
        return u'添加成功'

    def delete(self,**kwargs):
        try:
             self.ckyy = ['syear','org_code','org_name','year_profit','year_earning','id']
             newdata =  kwargs.get('newdata')
             pid = newdata.get('id')
             g.db_session.query(Bank_ProfitEarning_Input).filter(Bank_ProfitEarning_Input.id == pid).delete()
             return u"删除成功" 
        except Exception, e:
            print type(e), Exception, 'BankProfitEarningService:delete error'
            return str(e)


    def update(self,**kwargs):
        try:
             self.ckyy = ['syear','org_code','org_name','year_profit','year_earning','id']
             newdata =  kwargs.get('newdata')
             pid = newdata.get('id')
             newdata.pop('id');
             year_profit = newdata.get('year_profit')
             year_earning = newdata.get('year_earning')
             if float(year_earning) < 0:
                return u"年度营业收入不能为负" 
             g.db_session.query(Bank_ProfitEarning_Input).filter(Bank_ProfitEarning_Input.id == pid).update({Bank_ProfitEarning_Input.year_profit:year_profit,Bank_ProfitEarning_Input.year_earning:year_earning})
             return u"修改成功"  
        except Exception, e:
             print type(e), Exception, 'BankProfitEarningService:update error'
             return str(e)
    
    def upload(self, filepath, filename):
            print u'正在导入'
            try:
                today = datetime.date.today()
                data = xlrd.open_workbook(filepath)
                sheet = data.sheet_by_index(0)
                nrows = sheet.nrows
                
                if nrows in [0, 1,2]:
                    raise Exception(u"导入文件是空文件")
                
                bill_type_sign = ""
                list = []
            except Exception, e:
                return str(e)
            all_msg = []
            souser = []
            for r in range(2, nrows):
                try:
                    syear = str(int(sheet.cell(r, 0).value))
                    org_code = str(int(sheet.cell(r, 1).value))
                    org_name = str(sheet.cell(r,2).value)
                    year_profit = str(float(''.join(str(sheet.cell(r, 3).value).split(','))))
                    year_earning = str(float(''.join(str(sheet.cell(r, 4).value).split(','))))
                
                    if syear.strip() == '' or len(syear) < 4:
                        e = u'第'+str(r+1)+u'行请填写正确所属年份'
                        raise Exception(e)
                    if org_code.strip() == '' or len(org_code) < 6 or len(org_code) > 7:
                        e = u'第'+str(r+1)+u'行请填写正确的机构号'
                        raise Exception(e)
                    if year_profit.strip() == '':
                        raise Exception(u'请填写年度利润')
                    if year_earning.strip() == '':
                        raise Exception(u'请填写年度营业收入')
                    if float(year_earning) < 0:
                        e = u'第'+str(r+1)+u'行年度营业收入不能为负'
                        raise Exception(e)
                    
                    tbranch = g.db_session.query(Branch).filter(Branch.branch_code == org_code).first()
                    
                    if not tbranch:
                        return u'第'+str(r+1)+u"行机构号不正确"
                    
                    syear=int(syear[0:4])
                    temp = {'syear': syear,
                            'org_code': org_code,
                            'org_name':'',
                            'year_profit': year_profit,
                            'year_earning': year_earning
                    }
                        
                    fdata = g.db_session.query(Bank_ProfitEarning_Input).filter(Bank_ProfitEarning_Input.syear == syear).filter(Bank_ProfitEarning_Input.org_code == org_code).first()
                    if fdata:
                        return u'第'+str(r+1)+u'行机构所在年份数据已存在'

                    all_msg.append(temp)
                    key = str(syear) + str(org_code)
                    if key in souser:
                        return u'第'+str(r+1)+u'行，该年此机构的已存在，请勿重复导入'
                    else:
                        souser.append(key)

                except ValueError, e:
                    g.db_session.rollback()
                    return u'第'+str(r + 1) + u'行有错误'+str(e)+u"请检查年份和机构号是否正确,年度利润和年度营业收入是否包含非法字符"
                except IndexError,e:
                    g.db_session.rollback()
                    return u'第'+str(r+1)+u'行有错误,请检查列数'
                except Exception, e:
                    g.db_session.rollback()
                    return u'第'+str(r + 1) + u'行有错误'+str(e)

            for i in range(0,len(all_msg)):
                g.db_session.add(Bank_ProfitEarning_Input(**all_msg[i]))
            return u"导入成功"
          
