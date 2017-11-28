# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import django.utils.timezone as timezone

# Create your models here.
class Branch(models.Model):
    """分支机构信息"""
    name = models.CharField(max_length=128, null=False, blank=False)
    serial = models.CharField(max_length=128, null=False, blank=False)
    is_active = models.CharField(max_length=16, null=False, blank=False)

class User(AbstractUser):
    """可登录人员信息表基本信息表 PS:username 为 柜员/管理员 编号"""
    DEFAULT_ID=1
    name = models.CharField(max_length=64, null=False, blank=False)
    branch = models.ForeignKey(Branch, null=False, blank=False , verbose_name="u_bpk",default=1, on_delete=models.SET_DEFAULT)
    tel = models.CharField(max_length=64, null=False, blank=False)
    status = models.CharField(max_length=32, null=False, blank=False)
    remark = models.TextField()
    fingerprint = models.CharField(max_length=512, null=True, blank=True)
    # headimg = models.CharField(max_length=200, null=True, blank=True)
    # certimg = models.CharField(max_length=200, null=True, blank=True)


class MajorInfo(User):
    pass

class AssistInfo(User):
    pass

class BranchInfo(models.Model):
    """支行列表"""
    serial = models.CharField(max_length=32, null=False, blank=False)
    name = models.CharField(max_length=200, null=True, blank=True)


class CarInfo(models.Model):
    """车辆信息表"""
    #serial = models.CharField(max_length=128, null=False, blank=False) # 车辆编号
    number_plate = models.CharField(max_length=128, null=False, blank=False) # 车牌号
    img_serial = models.CharField(max_length=200, null=True, blank=True) # 车辆图像序号
    is_active = models.CharField(max_length=16, null=False, blank=False) # 车辆是否存在


class AmbangInfo(models.Model):
    """安邦人员信息表"""
    name = models.CharField(max_length=128, null=False, blank=False)
    img_serial = models.CharField(max_length=200, null=True, blank=True) # 图像序号
    is_active = models.CharField(max_length=16, null=False, blank=False) # 是否存在

class RouteInfo(models.Model):
    """路线信息表"""
    name = models.CharField(max_length=128, null=False, blank=False)
    routes = models.ManyToManyField(Branch) 
    modify_date = models.DateField(auto_now=True) 
    is_active = models.CharField(max_length=16, null=False, blank=False)    


class Cashbox(models.Model):
    """钱箱列表"""
    DEFAULT_ID = 1
    #/0废弃/1在库/2领用/3在途/4使用/
    ABANDON=0
    ATSTOCK=1
    TOKEN=2
    ONWAY=3
    USE=4
    serial = models.CharField(max_length=128, null=False, blank=False)
    kind = models.CharField(max_length=128, null=False, blank=False)
    status = models.CharField(max_length=128, null=False, blank=False)#/0废弃/1在库/2领用/3在途/4使用/
    branch = models.ForeignKey(Branch, null=False, blank=False , verbose_name="u_bpk")
    remark = models.CharField(max_length=128,null=False)
    is_active = models.CharField(max_length=16, null=False, blank=False)


class CashboxaplInfo(models.Model):
    #申请状态apl_status
    WCHECK=0 #待复核/teller
    APPLED=1 #已申请/teller   待审批/admin
    PASSED=2 #已审批/admin  审批通过/admin 路线已分配  

    """尾箱申请信息列表"""
    date = models.DateField(default=timezone.now)  #申请配送时间
    branch = models.ForeignKey(Branch, null=False, blank=False, verbose_name="branch_related") #申请网点
    cashboxs = models.ManyToManyField( Cashbox, default = Cashbox.DEFAULT_ID ) #申请钱箱集合
    package_num = models.SmallIntegerField( null=False, blank=False, default=0 ) #封包数量
    apl_status = models.CharField(max_length=128, null=False, blank=False) #申请状态
    aplteller = models.CharField(max_length=128, null=False, blank=False, default=0) #申请柜员
    confteller = models.CharField(max_length=128, null=False, blank=False, default=0) #复核柜员
    
    morning_task_status = models.CharField(max_length=128, null=False, blank=False) #早接状态：初始化--》安邦人员身份验证---》送待确认-->交接确认-->封包收到确认
    package_task_status = models.CharField(max_length=128, null=False, blank=False) #封包状态：初始化--》安邦人员身份验证---》交接--->确认

    night_task_status = models.CharField(max_length=128, null=False, blank=False) #晚接状态：初始化-->提交-->安邦人员身份验证---》交接确认-->安邦确认
    is_active = models.CharField(max_length=16, null=False, blank=False)


class RoutePlan(models.Model):
    """
        路线安排
        选择线路，日期后，根据线路+日期 查询出满足条件的钱箱申请集合
    """
    route = models.ForeignKey(RouteInfo, null=False, blank=False)
    car_info= models.ForeignKey(CarInfo, null=False, blank=False)#车辆信息

    majors = models.ManyToManyField(MajorInfo, blank=False)#主办人员集合,主办人员必须录入了指纹
    assists = models.ManyToManyField(AssistInfo, blank=False)#协办人员集合
    ambs = models.ManyToManyField(AmbangInfo,  blank=False)#押运人员集合
    cinfo = models.ManyToManyField(CashboxaplInfo, blank=False)#柜员申请钱箱信息

    morning_task_status = models.CharField(max_length=128, null=False, blank=False) #早接状态：初始化--》安邦人员确认--》出库---》出库确认-->已送达（所有网点送达后修改状态）
    task_task_status = models.CharField(max_length=128, null=False, blank=False)    #晚接状态：初始化--》安邦人员验证-->上交--》交接完成
