ysp.controller('creditController', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/loanBaseInfo.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'担保信息', '<div ng-include="'+'\'views/credit/GuaranteeInformation/index.html' +'\'"></div>', {}, false);
        //$rootScope.addSubTab(2,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        if($scope.customer.type_code== 'resident'){
              $rootScope.addSubTab(3,'客户信息', '<div ng-include="'+'\'views/customer/person/index.html' +'\'"></div>', {}, false);
        }else{
              $rootScope.addSubTab(3,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        }
        $rootScope.subTabFocus(0);
    };

});
ysp.controller('preAprove', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/loanBaseInfo.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        if($scope.customer.type_code== 'resident'){
              $rootScope.addSubTab(2,'客户信息', '<div ng-include="'+'\'views/customer/person/index.html' +'\'"></div>', {}, false);
        }else{
              $rootScope.addSubTab(2,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        }
        $rootScope.addSubTab(3,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };

});

ysp.controller('writeReport', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/loanBaseInfo.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(1,'担保信息', '<div ng-include="'+'\'views/credit/GuaranteeInformation/index.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(2,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        if($scope.customer.type_code== 'resident'){
              $rootScope.addSubTab(4,'客户信息', '<div ng-include="'+'\'views/customer/person/index.html' +'\'"></div>', {}, false);
        }else{
              $rootScope.addSubTab(4,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        }
        $rootScope.addSubTab(5,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});

ysp.controller('riskApprove', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/loanBaseInfo.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(1,'担保信息', '<div ng-include="'+'\'views/credit/GuaranteeInformation/index.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(2,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        if($scope.customer.type_code== 'resident'){
              $rootScope.addSubTab(4,'客户信息', '<div ng-include="'+'\'views/customer/person/index.html' +'\'"></div>', {}, false);
        }else{
              $rootScope.addSubTab(4,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        }
        $rootScope.addSubTab(5,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(6,'风险评价', '<div ng-include="'+'\'views/credit/CreditApproval/risk_index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});
ysp.controller('examineApprove', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/loanBaseInfo.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(6,'审查意见', '<div ng-include="'+'\'views/credit/CreditApproval/examine_index.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(1,'担保信息', '<div ng-include="'+'\'views/credit/GuaranteeInformation/index.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(2,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        if($scope.customer.type_code== 'resident'){
              $rootScope.addSubTab(4,'客户信息', '<div ng-include="'+'\'views/customer/person/index.html' +'\'"></div>', {}, false);
        }else{
              $rootScope.addSubTab(4,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        }
        $rootScope.addSubTab(5,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);

        $rootScope.subTabFocus(0);
    };
});
ysp.controller('groupApprove', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/loanBaseInfo.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(6,'审查意见', '<div ng-include="'+'\'views/credit/CreditApproval/examine_index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'担保信息', '<div ng-include="'+'\'views/credit/GuaranteeInformation/index.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(2,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        if($scope.customer.type_code== 'resident'){
              $rootScope.addSubTab(4,'客户信息', '<div ng-include="'+'\'views/customer/person/index.html' +'\'"></div>', {}, false);
        }else{
              $rootScope.addSubTab(4,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        }
        $rootScope.addSubTab(5,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);


        $rootScope.addSubTab(7,'风险评价', '<div ng-include="'+'\'views/credit/CreditApproval/risk_index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});
ysp.controller('loanApplication', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'放款信息', '<div ng-include="'+'\'views/credit/loanEndInfo.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(1,'支付信息', '<div ng-include="'+'\'views/credit/loanMoneyPay/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(2,'担保信息', '<div ng-include="'+'\'views/credit/GuaranteeInformation/index.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(3,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(4,'审查意见', '<div ng-include="'+'\'views/credit/CreditApproval/examine_index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(5,'风险评价', '<div ng-include="'+'\'views/credit/CreditApproval/risk_index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(6,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        if($scope.customer.type_code== 'resident'){
              $rootScope.addSubTab(7,'客户信息', '<div ng-include="'+'\'views/customer/person/index.html' +'\'"></div>', {}, false);
        }else{
              $rootScope.addSubTab(7,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        }
        $rootScope.addSubTab(8,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
       $rootScope.subTabFocus(0);
    };
});



ysp.controller('loan', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'放款信息', '<div ng-include="'+'\'views/credit/loan.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});


//贴现申请  贴现支行审查
ysp.controller('discountAppInfo', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        if($scope.user_groups.indexOf('客户经理') != -1){
             $scope.user='客户经理' ;
        }    
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/discount/discountBaseInfo.html' +'\'"></div>', {}, false); 
        $rootScope.addSubTab(1,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false); 
        $rootScope.subTabFocus(0);
    };  
});

//贴现预审
ysp.controller('discountPreAprove', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        if($scope.user_groups.indexOf('客户经理') != -1){
             $scope.user='客户经理' ;
        }
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/discount/discountBaseInfo.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});
//贴现撰写调查报告
ysp.controller('discountWriteReport', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        if($scope.user_groups.indexOf('客户经理') != -1){
            $scope.user='客户经理' ;
        }
        if($scope.application_status.indexOf('贴现撰写调查报告') != -1){
            $scope.application_status='贴现撰写调查报告';
        }
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/discount/discountBaseInfo.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(2,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(4,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});
//贴现支行审查
ysp.controller('discountRiskApprove', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        if($scope.user_groups.indexOf('客户经理') != -1){
             $scope.user='客户经理' ;
        }
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/discount/discountBaseInfo.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(2,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(4,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(5,'风险评价', '<div ng-include="'+'\'views/credit/CreditApproval/risk_index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});

//贴现支行风险评价
ysp.controller('discountExamineApprove', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        if($scope.user_groups.indexOf('客户经理') != -1){
             $scope.user='客户经理' ;
        }
        if($scope.application_status.indexOf('贴现支行风险评价') != -1){
            $scope.application_status='贴现支行风险评价';
        }
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/discount/discountBaseInfo.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'风险评价', '<div ng-include="'+'\'views/credit/CreditApproval/risk_index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(2,'审查意见', '<div ng-include="'+'\'views/credit/CreditApproval/examine_index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(4,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(5,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(6,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(7,'风险评价', '<div ng-include="'+'\'views/credit/CreditApproval/risk_index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});

ysp.controller('discountGroupApprove', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        if($scope.user_groups.indexOf('客户经理') != -1){
             $scope.user='客户经理' ;
        }
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/discount/discountBaseInfo.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(6,'审查意见', '<div ng-include="'+'\'views/credit/CreditApproval/examine_index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(2,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(4,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(5,'风险评价', '<div ng-include="'+'\'views/credit/CreditApproval/risk_index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});

//贴现信息录入 支行长审批
ysp.controller('discountBill', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        if($scope.user_groups.indexOf('客户经理') != -1){
             $scope.user='客户经理' ;
        }
        $scope.init();
    });
    $scope.$on('bill_kind',function(event,msg){
        $scope.$broadcast('dis_bill_kind',msg);
    }); 

    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/discount/discountAppInfo.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'票据录入', '<div ng-include="'+'\'views/credit/discount/billing.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(2,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(4,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(5,'票据影像', '<div ng-include="'+'\'views/credit/image/billImage.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(6,'合同税票影像', '<div ng-include="'+'\'views/credit/image/elecImage.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(7,'风险评价', '<div ng-include="'+'\'views/credit/CreditApproval/risk_index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(8,'审批意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});

//贴现放款
ysp.controller('discountLoanTask', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        if($scope.user_groups.indexOf('客户经理') != -1){
             $scope.user='客户经理' ;
        }
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/discount/discountApp.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'票据录入', '<div ng-include="'+'\'views/credit/discount/billing.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(2,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(4,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(5,'票据影像', '<div ng-include="'+'\'views/credit/image/billImage.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(6,'合同税票影像', '<div ng-include="'+'\'views/credit/image/elecImage.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(7,'风险评价', '<div ng-include="'+'\'views/credit/CreditApproval/risk_index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(8,'审批意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(9,'支付信息', '<div ng-include="'+'\'views/credit/loanMoneyPay/index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});

ysp.controller('extensionPage', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'贷款信息', '<div ng-include="'+'\'views/credit/Extension/extension_info.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(2,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        if($scope.customer.type_code== 'resident'){
              $rootScope.addSubTab(3,'客户信息', '<div ng-include="'+'\'views/customer/person/index.html' +'\'"></div>', {}, false);
        }else{
              $rootScope.addSubTab(3,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        }
        $rootScope.addSubTab(4,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };

});

//签发申请
ysp.controller('acceptanceAppInfo', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'签票信息', '<div ng-include="'+'\'views/credit/acceptanceBill/accBillApplication.html' +'\'"></div>', {}, false); 
        $rootScope.addSubTab(1,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(2,'担保信息', '<div ng-include="'+'\'views/credit/GuaranteeInformation/index.html' +'\'"></div>', {}, false);

        //$rootScope.addSubTab(3,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});

//签发预审
ysp.controller('acceptancePreApprove', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'签票信息', '<div ng-include="'+'\'views/credit/acceptanceBill/accBillApplication.html' +'\'"></div>', {}, false); 
        $rootScope.addSubTab(1,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        
        $rootScope.addSubTab(4,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
        //$rootScope.addSubTab(3,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});

//签发撰写调查报告
ysp.controller('acceptanceWriteReport', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;    
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        if($scope.user_groups.indexOf('客户经理') != -1){
             $scope.user='客户经理' ;
        }
        $scope.init();    
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'签票信息', '<div ng-include="'+'\'views/credit/acceptanceBill/accBillApplication.html' +'\'"></div>', {}, false); 
        $rootScope.addSubTab(2,'担保信息', '<div ng-include="'+'\'views/credit/GuaranteeInformation/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(4,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(6,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(7,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});
//签发 风险评价
ysp.controller('acceptanceRiskApprove', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){

        $rootScope.addSubTab(0,'签票信息', '<div ng-include="'+'\'views/credit/acceptanceBill/accBillApplication.html' +'\'"></div>', {}, false); 
        $rootScope.addSubTab(6,'风险评价', '<div ng-include="'+'\'views/credit/CreditApproval/risk_index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'担保信息', '<div ng-include="'+'\'views/credit/GuaranteeInformation/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(2,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(4,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(5,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});


ysp.controller('acceptanceExamineApprove', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){

        $rootScope.addSubTab(0,'签票信息', '<div ng-include="'+'\'views/credit/acceptanceBill/accBillApplication.html' +'\'"></div>', {}, false); 
        $rootScope.addSubTab(6,'审查意见', '<div ng-include="'+'\'views/credit/CreditApproval/examine_index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(6,'风险评价', '<div ng-include="'+'\'views/credit/CreditApproval/risk_index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'担保信息', '<div ng-include="'+'\'views/credit/GuaranteeInformation/index.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(2,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(4,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(5,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);

        $rootScope.subTabFocus(0);
    };
});

//签发 审贷小组审议
ysp.controller('acceptanceGroupApprove', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'签票信息', '<div ng-include="'+'\'views/credit/acceptanceBill/accBillApplication.html' +'\'"></div>', {}, false); 

        $rootScope.addSubTab(6,'审查意见', '<div ng-include="'+'\'views/credit/CreditApproval/examine_index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'担保信息', '<div ng-include="'+'\'views/credit/GuaranteeInformation/index.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(2,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(4,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(5,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);


        $rootScope.addSubTab(7,'风险评价', '<div ng-include="'+'\'views/credit/CreditApproval/risk_index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});


//签发 票据录入
ysp.controller('acceptanceLoanApplication', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'签票信息', '<div ng-include="'+'\'views/credit/acceptanceBill/accBillLoanApplication.html' +'\'"></div>', {}, false); 
        $rootScope.addSubTab(7,'承兑汇票清单', '<div ng-include="'+'\'views/credit/acceptanceBill/listBill.html' +'\'"></div>', {}, false); 

        $rootScope.addSubTab(6,'审查意见', '<div ng-include="'+'\'views/credit/CreditApproval/examine_index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(1,'担保信息', '<div ng-include="'+'\'views/credit/GuaranteeInformation/index.html' +'\'"></div>', {}, false);

        $rootScope.addSubTab(2,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(3,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(4,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(5,'流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);


        $rootScope.addSubTab(8,'风险评价', '<div ng-include="'+'\'views/credit/CreditApproval/risk_index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});



//签发放款
ysp.controller('acceptanceLoan', function($scope,$rootScope,userService){
    /*tab动态增加功能*/
    $scope.customer=$scope.$parent.customer;
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        if($scope.user_groups.indexOf('客户经理') != -1){
             $scope.user='客户经理' ;
        }
        $scope.init();
    });
    $scope.init = function(){
        $rootScope.addSubTab(0,'签票信息', '<div ng-include="'+'\'views/credit/acceptanceBill/accBillLoan.html' +'\'"></div>', {}, false); 
        $rootScope.addSubTab(1,'承兑汇票清单', '<div ng-include="'+'\'views/credit/acceptanceBill/listBill.html' +'\'"></div>', {}, false); 
        $rootScope.addSubTab(2,'担保信息', '<div ng-include="'+'\'views/credit/GuaranteeInformation/index.html' +'\'"></div>', {}, false); 
        $rootScope.addSubTab(3,'调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(4,'客户信息', '<div ng-include="'+'\'views/customer/company/index.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(6,'影像信息', '<div ng-include="'+'\'views/credit/image/image.html' +'\'"></div>', {}, false);
        $rootScope.addSubTab(7,'审批意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    };
});
