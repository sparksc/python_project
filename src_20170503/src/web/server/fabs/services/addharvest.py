#-*-coding:utf-8-*-
import datetime,xlrd
from flask import json, g
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all,aliased
from ..base import utils
from ..model import CustHook,Addharvest, Branch,User,UserBranch,User,User_ExtraScore,T_Para_Detail,UserLevel,T_Para_Header,T_Para_Type
import datetime

class AddharvestService():
    def add_save(self, **kwargs):
        try:
            syear = kwargs.get('syear')
            org_code = kwargs.get('org_code')
            user_code = kwargs.get('user_code')
            online_home= kwargs.get('online_home')
            online_buy= kwargs.get('online_buy')
            online_two= kwargs.get('online_two')
            remarks = kwargs.get('remarks')

            g.db_session.add(Addharvest(syear=syear,
                              org_code=org_code,user_code=user_code,online_home= online_home,online_buy=online_buy,online_two=online_two,remarks=remarks))
            return u'保存成功';
        except Exception, e:
            print type(e), Exception, '1111111111111111111111111111111111111111111111'
            return u'保存失败'

    def edit_save(self, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            syear = kwargs.get('syear')
            org_code = kwargs.get('org_code')
            user_code=kwargs.get('user_code')
            online_home= kwargs.get('online_home')
            online_buy= kwargs.get('online_buy')
            online_two= kwargs.get('online_two')
            remarks = kwargs.get('remarks')
            g.db_session.query(Addharvest).filter(Addharvest.id == item_id).update(
                {Addharvest.syear:syear,Addharvest.org_code:org_code,Addharvest.user_code:user_code,Addharvest.online_home:online_home,Addharvest.online_buy:online_buy,Addharvest.online_two:online_two,Addharvest.remarks:remarks})
            return u'编辑成功'
        except Exception, e:
            print type(e),Exception
            return u'编辑失败'
    def delete(self, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            g.db_session.query(Addharvest).filter(Addharvest.id == item_id).delete()
            return u'删除成功'
        except Exception, e:
            print type(e), Exception
            return u'删除失败'    

    def upload(self, filepath, filename):

        print u'正在导入'
        try:
            today = datetime.date.today()
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)
            
            nrows = sheet.nrows
            if nrows in [0, 1]:
                raise Exception(u"导入文件是空文件")
            bill_type_sign = ""
            list = []
        except Exception, e:
            return str(e)
        for r in range(2, nrows):
            try:
                syear = str(sheet.cell(r, 0).value)
                org_code =str(sheet.cell(r, 1).value)
                org_name = sheet.cell(r, 2).value
                user_code =str(int(sheet.cell(r, 3).value))
                user_name = sheet.cell(r, 4).value
                online_home= sheet.cell(r, 5).value
                online_buy=sheet.cell(r, 6).value
                online_two= sheet.cell(r, 7).value
                remarks = sheet.cell(r, 8).value

                if syear.strip() == '':
                    raise Exception(u'请填写所属年份,如2016')
                if org_code.strip() == '':
                    raise Exception(u'请填写机构号')
                if user_code.strip() == '':
                    raise Exception(u'请填写员工号')
                if online_home.strip() == '':
                    raise Exception(u'请填写丰收家上线数')
                if online_buy.strip() == '':
                    raise Exception(u'请填写丰收购上线数')
                if online_two.strip() == '':
                    raise Exception(u'请填写两家上线数')
                tbranch= g.db_session.execute("select bb.branch_code from user_branch ub, f_user fu, branch bb where bb.role_id = ub.branch_id and ub.user_id = fu.role_id and fu.user_name = '%s'"%(user_code)).fetchone()
                if tbranch[0] != org_code:
                    return u'第'+str(r+1)+u'行，该机构中没有该员工'
                                
                temp = {'syear': syear,
                        'org_code': org_code,
                        'user_code': user_code,
                        'online_home':online_home,
                        'online_buy':online_buy,
                        'online_two':online_two,
                        'remarks':remarks
                        }
                fdata = g.db_session.query(Addharvest).filter(Addharvest.syear == syear).filter(Addharvest.org_code == org_code).filter(Addharvest.user_code==user_code).first()

                if fdata:
                    return u'第'+str(r+1)+u'行，该年此员工的已存在已录入，请勿重复录入'
                g.db_session.add(Addharvest(**temp))
            except Exception, e:
                g.db_session.rollback()
                print Exception, ':', e
                return u'第' + str(r + 1) + u'行有错误'

        return u'导入成功'
