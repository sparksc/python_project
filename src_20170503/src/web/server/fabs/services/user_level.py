#-*-coding:utf-8-*-
import datetime,xlrd
from flask import json, g,current_app
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all,aliased
from ..base import utils
from ..model import CustHook, UserLevel, Branch,User,UserBranch,UserGroup,Group
import datetime


class User_levelService():
    def add_save(self, **kwargs):
        try:
            syear = kwargs.get('syear')
            org_code = kwargs.get('org_code')
            user_code = kwargs.get('user_code')
            task_level = kwargs.get('task_level')
            civilized_service = kwargs.get('civilized_service')
            task_errorrate = kwargs.get('task_errorrate')
            cust_satisfaction = kwargs.get('cust_satisfaction')
            work_year = kwargs.get('work_year')
            bankterm_year = kwargs.get('bankterm_year')
            violation_score = kwargs.get('violation_score')
            remarks = kwargs.get('remarks')
            
            fx = g.db_session.query(User).join(UserGroup,UserGroup.user_id==User.role_id).join(Group,Group.id==UserGroup.group_id).filter(User.user_name==user_code).filter(Group.group_name.like('%柜员%')).filter(Group.group_type_code=='1000').first()
            if not fx:
                return u'不存在该柜员！'
            g.db_session.add(UserLevel(syear=syear,org_code=org_code,user_code=user_code,task_level=task_level,civilized_service=civilized_service,task_errorrate=task_errorrate,cust_satisfaction=cust_satisfaction,work_year=work_year,bankterm_year=bankterm_year,violation_score=violation_score,remarks=remarks))
            return u'保存成功';
        except Exception, e:
            return u'保存失败'+str(e)

    def edit_save(self, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            syear = kwargs.get('syear')
            org_code = kwargs.get('org_code')
            user_code = kwargs.get('user_code')
            task_level = kwargs.get('task_level')
            civilized_service = kwargs.get('civilized_service')
            task_errorrate = kwargs.get('task_errorrate')
            cust_satisfaction = kwargs.get('cust_satisfaction')
            work_year = kwargs.get('work_year')
            bankterm_year = kwargs.get('bankterm_year')
            violation_score = kwargs.get('violation_score')
            remarks = kwargs.get('remarks')

            g.db_session.query(UserLevel).filter(UserLevel.id == item_id).update({UserLevel.syear:syear,UserLevel.org_code:org_code,UserLevel.user_code:user_code,UserLevel.task_level:task_level,UserLevel.civilized_service:civilized_service,UserLevel.task_errorrate:task_errorrate,UserLevel.cust_satisfaction:cust_satisfaction,UserLevel.work_year:work_year,UserLevel.bankterm_year:bankterm_year,UserLevel.remarks:remarks,UserLevel.violation_score:violation_score})
            return u'编辑成功'
        except Exception, e:
            return u'编辑失败'
    def delete(self, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            g.db_session.query(UserLevel).filter(UserLevel.id == item_id).delete()
            return u'删除成功'
        except Exception, e:
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
        all_msg = []
        souser = []
        for r in range(1, nrows):
            try:
                syear = str(int(sheet.cell(r, 0).value))
                org_code =str(int(sheet.cell(r, 1).value))
                org_name = str(sheet.cell(r, 2).value)
                user_code =str(int(sheet.cell(r, 3).value))
                user_name = str(sheet.cell(r, 4).value)
                task_level = str(sheet.cell(r,5).value)
                civilized_service = str(float(sheet.cell(r,6).value))
                task_errorrate = str(float(sheet.cell(r,7).value))
                cust_satisfaction = str(float(sheet.cell(r,8).value))
                work_year = str(int(sheet.cell(r,9).value))
                bankterm_year = str(int(sheet.cell(r,10).value))
                violation_score = str(float(sheet.cell(r,11).value))
                remarks = str(sheet.cell(r, 12).value)

                syear = syear[0:4]
                if len(syear) < 4:
                    e = u'第'+str(r+1)+u'行请填写正确所属年份'
                    raise Exception(e)
                if len(org_code) < 6 or len(org_code) > 7:
                    e = u'第'+str(r+1)+u'行请填写正确的机构号'
                    raise Exception(e)
                if len(user_code) != 7:
                    e = u'第'+str(r+1)+u'行请填写正确的员工号'
                    raise Exception(e)
                if task_level.strip() == '':
                    raise Exception(u'请填写市业务知识技能达标(级)')
                if civilized_service.strip() == '':
                    raise Exception(u'优质文明服务扣分(分)')
                if task_errorrate.strip() == '':
                    raise Exception(u'业务差错率(‰)')
                if cust_satisfaction.strip() == '':
                    raise Exception(u'客户满意度(%)')
                if work_year.strip() == '':
                    raise Exception(u'行龄')
                if bankterm_year.strip() == '':
                    raise Exception(u'临柜工作经验(年)')
                if violation_score.strip() == '':
                    raise Exception(u'请填写违规积分(分)')
                
                fx = g.db_session.query(User).join(UserGroup,UserGroup.user_id==User.role_id).join(Group,Group.id==UserGroup.group_id).filter(User.user_name==user_code).filter(Group.group_name.like('%柜员%')).filter(Group.group_type_code=='1000').first()
                if not fx:
                    return u'不存在该柜员！'
                #判断员工与机构是否关联
                tbranch = g.db_session.query(UserBranch).join(User,User.role_id==UserBranch.user_id).join(Branch,Branch.role_id==UserBranch.branch_id).filter(Branch.branch_code == org_code).filter(User.user_name == user_code).first()
                if not tbranch:
                     return u'第'+str(r+1)+u'行，该机构中没有该用户'
                               
                temp = {'syear': syear,
                        'org_code': org_code,
                        'user_code': user_code,
                        'task_level':task_level,
                        'civilized_service':civilized_service,
                        'task_errorrate':task_errorrate,
                        'cust_satisfaction':cust_satisfaction,
                        'work_year':work_year,
                        'bankterm_year':bankterm_year,
                        'violation_score':violation_score,
                        'remarks':remarks
                        }

                #判断该员工的证书录入是否重复
                fdata = g.db_session.query(UserLevel).filter(UserLevel.syear==syear).filter(UserLevel.org_code == org_code).filter(UserLevel.user_code==user_code).first()
                if fdata:
                    return u'第'+str(r+1)+u'行，该年此员工的已录入，请勿重复录入'

                all_msg.append(temp)
                key = str(syear) + str(org_code) + str(user_code)
                if key in souser:
                    return u'第'+str(r+1)+u'行，该年此员工的已存在，请勿重复导入'
                else:
                    souser.append(key)
            except ValueError, e:
                g.db_session.rollback()
                return u'第'+str(r + 1) + u'行有错误'+str(e)+u"请检查所属年份,机构和柜员号是否正确,或者优质文明服务扣分(分)等是否包含非法字符"
            except IndexError,e:
                g.db_session.rollback()
                return u'第'+str(r+1)+u'行有错误,请检查列数'
            except Exception, e:
                g.db_session.rollback()
                print Exception, ':', e
                return u'第' + str(r + 1) + u'行有错误'+str(e)

        for i in range(0,len(all_msg)):
            g.db_session.add(UserLevel(**all_msg[i]))
            
        return u'导入成功'
   
