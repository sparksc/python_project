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
from ..model import Branch,Menu,User,UserBranch,Burank


class BurankService():
    """ Target Service  """

    def save(self,**kwargs):
        try:
             self.ckyy = ['syear','srank','remarks']
             newdata =  kwargs.get('newdata')
             data ={}
             for k,v in newdata.items():
                 if k in self.ckyy :
                     data[k] = v
                 if k == 'syear' and int(v)<2014:
                    return u"不能输入2014年以前的数据"
             g.db_session.add(Burank(**data))
             return u"ok"
        except Exception, e:
            print type(e), Exception, 'BurankService:save error'
            return str(e)

    def delete(self,**kwargs):
        try:
             self.ckyy = ['syear','srank','remarks','id']
             newdata =  kwargs.get('newdata')
             pid = newdata.get('id')
             g.db_session.query(Burank).filter(Burank.id == pid).delete()
             return u"ok" 
        except Exception, e:
            print type(e), Exception, 'BurankService:delete error'
            return str(e)


    def update(self,**kwargs):
        try:
            syear = kwargs.get("syear") 
            srank = kwargs.get("srank")
            remarks = kwargs.get("remarks")
            pid = kwargs.get("id")
            g.db_session.query(Burank).filter(Burank.id == pid).update({Burank.syear:syear,Burank.srank:srank,Burank.remarks:remarks})
            return u"ok"  
        except Exception, e:
             print type(e), Exception, 'BurankService:update error'
             return str(e)
    
    def upload(self, filepath, filename):
            try:
                data = xlrd.open_workbook(filepath)
                sheet = data.sheet_by_index(0)
                nrows = sheet.nrows
                if nrows in [0,1,2]:
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
                    srank =str(int(sheet.cell(r, 1).value))
                    remarks = str(sheet.cell(r, 2).value)
                
                    if len(syear) < 4:
                        e = u'第'+str(r+1)+u'行请填写正确所属年份'
                        raise Exception(e)
                    if srank == '' or float(srank) < 0:
                        e = u'第'+str(r+1)+u'行请填写正确排名'
                        raise Exception(e)
                    if int(syear) < int(2014):
                        e = u'第'+str(r+1)+u'不能导入2014年以前的数据'
                        raise Exception(e)
                    
                    syear=int(syear[0:4])
                    temp = {'syear': syear,
                            'srank': srank,
                            'remarks': remarks
                    }
                    fdata = g.db_session.query(Burank).filter(Burank.syear == syear).first()
                    if fdata:
                        return str(syear)+u'年份数据已存在'

                    all_msg.append(temp)
                    key = str(syear)
                    if key in souser:
                        return u'第'+str(r+1)+u'行，该年已存在请勿重复导入'
                    else:
                        souser.append(key)

                except ValueError, e:
                    g.db_session.rollback()
                    return u'第'+str(r + 1) + u'行有错误'+str(e)+u"请检查所属年份是否正确,排名是否包含非法字符"
                except IndexError,e:
                    g.db_session.rollback()
                    return u'第'+str(r+1)+u'行有错误,请检查列数'
                except Exception, e:
                    g.db_session.rollback()
                    return u'第' + str(r + 1) + u'行有错误'+str(e)
            
            for i in range(0,len(all_msg)):
                g.db_session.add(Burank(**all_msg[i]))
            return u'导入成功'
