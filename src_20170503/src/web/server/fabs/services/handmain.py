# -*- coding: utf-8 -*-
"""
    yinsho.services.SeimService
    #####################

    yinsho SeimService module
"""
import datetime
from flask import json, g
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all
import xlrd
from ..base import utils
from ..model import Branch,Menu,User,UserBranch,Hand_Maintain


class HandmainService():
    """ Target Service  """

    def save(self,**kwargs):
        try:
             self.ckyy = ['syear','org_code','org_name','org_count','remarks',]
             newdata =  kwargs.get('newdata')
             data ={}
             for k,v in newdata.items():
                 if k in self.ckyy :
                     if k=='org_count':
                        if float(v)<0:
                            return "请填写正确的人数"
                        v=str( float(v) )
                     if k=='syear':
                        v=int(str(v)[0:4] )
                     data[k] = v
                     fdata = g.db_session.query(Hand_Maintain).filter(Hand_Maintain.syear == newdata['syear'],Hand_Maintain.org_code == newdata['org_code']).first()
                     if fdata:
                         return u'机构所在年份数据已存在'
             g.db_session.add(Hand_Maintain(**data))
             return u"ok"
        except Exception, e:
            Exception, 'HandmainService:save'
            return str(e)

    def delete(self,**kwargs):
        try:
             self.ckyy = ['syear','org_code','org_name','org_count','remarks','id']
             newdata =  kwargs.get('newdata')
             pid = newdata.get('id')
             g.db_session.query(Hand_Maintain).filter(Hand_Maintain.id == pid).delete()
             return u"ok" 
        except Exception, e:
            Exception, 'HandmainService:delete'
            return str(e)


    def update(self,**kwargs):
        try:
             self.ckyy = ['syear','org_code','org_name','org_count','remarks','id']
             newdata =  kwargs.get('newdata')
             pid = newdata.get('id')
             newdata.pop('id');
             data ={}
             if newdata['org_count']:
                if float(newdata['org_count'])<0:
                    return "请填写正确的人数"
                newdata['org_count']=str( float(newdata['org_count']) )
             if newdata['syear']:
                newdata['syear']=int(str(newdata['syear'])[0:4])
             g.db_session.query(Hand_Maintain).filter(Hand_Maintain.id == pid).update(newdata)
             return u"ok"  
        except Exception, e:
             Exception, 'HandmainService:update'
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
                    org_code =str(int(sheet.cell(r, 1).value))
                    org_name = str(sheet.cell(r, 2).value)
                    org_count =str(float(sheet.cell(r, 3).value))
                    remarks = str(sheet.cell(r, 4).value)

                    if len(syear)< 4:
                        e = u'第'+str(r+1)+u'行请填写正确所属年份'
                        raise Exception(e)
                    if len(org_code) < 6 or len(org_code) > 7:
                        e = u'第'+str(r+1)+u'行请填写正确的机构号'
                        raise Exception(e)
                    if org_name.strip() == '':
                        e = u'第'+str(r+1)+u'行请填写机构名称'
                        raise Exception(e)
                    if org_count.strip() == '' or float(org_count)<0:
                        e = u'第'+str(r+1)+u'行请填写正确支行人数'
                        raise Exception(e)
                    
                    org_no_value=g.db_session.query(Branch).filter(Branch.branch_code==org_code).all()
                    if not org_no_value:
                        return u'第'+str(r+1)+u"行机构号不正确"

                    syear=int(syear[0:4])
                    temp = {'syear': syear,
                            'org_code': org_code,
                            'org_name': org_name,
                            'org_count': org_count,
                            'remarks': remarks
                    }
                    fdata = g.db_session.query(Hand_Maintain).filter(Hand_Maintain.syear == syear,Hand_Maintain.org_code == org_code).first()
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
                    return u'第'+str(r + 1) + u'行有错误'+str(e)+u"请检查所属年份和机构是否正确,人数是否包含非法字符"
                except IndexError,e:
                    g.db_session.rollback()
                    return u'第'+str(r+1)+u'行有错误,请检查列数'
                except Exception, e:
                    g.db_session.rollback()
                    return u'第' + str(r + 1) + u'行有错误'+str(e)
            
            for i in range(0,len(all_msg)):
                g.db_session.add(Hand_Maintain(**all_msg[i]))
            return u'导入成功'

