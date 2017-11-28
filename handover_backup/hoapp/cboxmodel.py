class CboxApplyInfo(models.Model):
    """钱箱申请列表"""
    WAITING_CHECK = '1'
    APPLYING = '2'
    APPLYING_SUCCESS = '3'
    STATUS_CHOICES =(
                ( WAITING_CHECK, 'WAITING_CHECK' ), #柜员端：待复核
                ( APPLYING, 'APPLYING' ),       #柜员端：已申请/管理员：待审批
                ( APPLYING_SUCCESS, 'APPLYING_SUCCESS' ), #柜员端：申请成功/管理员：已审批
            )
    branch = models.CharField(max_length=128, null=False, blank=False)
    last_carton_nu = models.SmallIntegerField(null=False, blank=False) # 尾箱个数
    warehouse_nu = models.SmallIntegerField(null=False, blank=False)  #入库数
    escort_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=2, null=False, blank=False, 
            choices=STATUS_CHOICES, 
            default=WAITING_CHECK )
    is_active = models.CharField(max_length=16, null=False, blank=False)
