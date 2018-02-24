#-*-coding:utf-8-*-
import datetime,xlrd
from flask import json, g,current_app
from sqlalchemy import and_, func, text, or_
from sqlalchemy.orm import joinedload_all,aliased
from ..base import utils
from ..model import Branch,User,UserBranch,T_Para_Detail,UserLevel,T_Para_Header,T_Para_Type,TellerLevel,Group,UserGroup,BranchGroup,FunongCardTarget
from man_gradejdg import Man_gradejdgService
from userreport import UserReport
import datetime

msg = Man_gradejdgService()
ur = UserReport()
local_year,last_year,local_satrday,last_endday = ur.get_year_day()
class Branch_funong_cardService():
    def count_save(self, **kwargs):
        try:
            kyear = kwargs.get('kyear')
            org_no = kwargs.get('org_no')
            org_name = kwargs.get('org_name')
            target= kwargs.get('target')
            remarks = kwargs.get('remarks')
            if float(target)<0:
                return "目标任务不能为负"
 
            fx = g.db_session.query(Branch).filter(Branch.branch_code==org_no).first()
            fy = g.db_session.query(FunongCardTarget).filter(FunongCardTarget.org_no==org_no,FunongCardTarget.kyear==kyear).first()
            if not fx:
                return u'不存在该网点！'
            if fy:
                return u'该网点已存在！'

            g.db_session.add(FunongCardTarget(kyear=kyear, org_no=org_no, target=target, remarks=remarks))
            return u'添加成功！'
        except Exception,e:
            print type(e),Exception,'FunongCardTarget:count_save'
            return str(e)

    def count_edit_save(self, **kwargs):
        try:
            item_id = kwargs.get('item_id')
            kyear = kwargs.get('kyear')
            org_no = kwargs.get('org_no')
            org_name = kwargs.get('org_name')
            target= kwargs.get('target')
            remarks = kwargs.get('remarks')
            if float(target)<0:
                return "目标任务不能为负"

            g.db_session.query(FunongCardTarget).filter(FunongCardTarget.id == item_id).update({FunongCardTarget.kyear:kyear, FunongCardTarget.org_no:org_no,  FunongCardTarget.target:target, FunongCardTarget.remarks:remarks})
            return u'修改成功！'
        except Exception, e:
            return str(e)

    def conunt_del(sel, **kwargs):
        try:
            row_id = kwargs.get('row_id')

            g.db_session.query(FunongCardTarget).filter(FunongCardTarget.id == row_id).delete()

            return u'删除成功！'
        except Exception, e:
            return u'删除失败！'

    def count_upload(self, filepath, filename):
        """
            批量录入
        """
        print '正在导入'
        try:
            data = xlrd.open_workbook(filepath)
            sheet = data.sheet_by_index(0)

            nrows = sheet.nrows
            if nrows in [0, 1]:
                raise Exception(u"警告:文件为空")
            bill_type_sign = ""
            list = []
        except Exception, e:
            return str(e)
        all_msg = []
        souser = []
        for r in range(1, nrows):
            try:
                kyear = str(int(sheet.cell(r, 0).value))
                org_no = str(int(sheet.cell(r, 1).value))
                org_name = str(sheet.cell(r,2).value)
                target = str(float(sheet.cell(r,3).value))
                remarks = str(sheet.cell(r, 4).value)
                kyear = kyear[0:4]
                if len(kyear)<4:
                    e = u'第'+str(r+1)+u'行请填写正确所属年份'
                    raise Exception(e)
                if len(org_no) < 6 or len(org_no) > 7:
                    e = u'第'+str(r+1)+u'行请填写正确的机构号'
                    raise Exception(e)
                if float(target) < 0:
                    e = u'第'+str(r+1)+u'行目标任务不能为负'
                    raise Exception(e)
                
                temp = {'kyear': kyear[0:4],
                        'org_no': org_no,
                        'target': target,
                        'remarks': remarks,
                }
                fx = g.db_session.query(Branch).filter(Branch.branch_code==org_no).first()
                fy = g.db_session.query(FunongCardTarget).filter(FunongCardTarget.org_no==org_no,FunongCardTarget.kyear==kyear).first()
                if not fx:
                    return u'第'+str(r+1)+u'行,机构'+u'不存在该网点！'
                if fy:
                    return u'第'+str(r+1)+u'行,机构'+str(org_no)+u'在'+str(kyear)+u'年数据已存在'
                all_msg.append(temp)
                key = str(kyear)+str(org_no)
                if key in souser:
                    return u'第'+str(r+1)+u'行，该年已存在请勿重复导入'
                else:
                    souser.append(key)
            except ValueError, e:
                g.db_session.rollback()
                return u'第'+str(r + 1) + u'行有错误'+str(e)+u"请检查所属年份和机构号是否正确,目标任务是否包含非法字符"
            except IndexError,e:
                g.db_session.rollback()
                return u'第'+str(r+1)+u'行有错误,请检查列数'
            except Exception, e:
                g.db_session.rollback()
                print Exception, ':', e
                return u'第'+str(r+1)+u'行有问题:'+str(e)
        for i in range(0,len(all_msg)):
            g.db_session.add(FunongCardTarget(**all_msg[i]))
        return u'导入成功'
