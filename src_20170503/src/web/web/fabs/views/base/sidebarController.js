ysp.controller('sidebarController', ['$scope', '$rootScope', '$http', 'permissionService', function ($scope, $rootScope, $http, permissionService) {
    $scope.$on('$includeContentLoaded', function () {
        Layout.initSidebar(); // init sidebar
        Layout.setSidebarMenuActiveLink('set', $('#sidebar_menu_link_profile'));
    });

    $scope.customer_tab = {};
    $scope.loan_tab = {};
    $scope.task_tab = {};

    $scope.addPersonCustomer = function () {
        $rootScope.forward('新增个人客户', 'views/customer/person/pre_add.html');
    };
    $scope.addCompanyCustomer = function () {
        $rootScope.forward('新增对公客户', 'views/customer/company/com_add.html');
    };

    $scope.customerInfoDetail = function (cust) {
        var cust_id = cust.id;
        var cust_name = cust.name;
        var cust_type = cust.type_code;
        var tabName = cust_name + '的客户信息';
        var htmlContent = 'views/customer/person/index.html';
        if(cust_type == 'company'){
            var htmlContent = 'views/customer/company/index.html';
        }
        $rootScope.forward(tabName, htmlContent, {'customer': cust});
    };

    $scope.loanApplication = function(cust){
        var cust_state=cust.state;
        alert (cust_state);
        if (cust_state=='完善'){
            var cust_id = cust.id;
            var cust_name = cust.name;
            var apply_type='';
            if(cust.type_code == 'company'){
                apply_type='对公业务申请'
                var tabName = cust_name+'的贷款申请';
                $rootScope.forward(tabName,'views/credit/companyCredit/companyCreditInfo.html',{'customer':cust});

            }else{
                apply_type='个人业务申请'
                var tabName = cust_name+'的贷款申请';
                $rootScope.forward(tabName,'views/credit/personCredit/personCreditInfo.html',{'customer':cust});

            }
        }else{
            alert('客户信息不完善,请完善后再做申请')
        }
    };

    $scope.dealCredit = function (task) {
        var tabName = '商用房抵押转贷大表处理';
        $rootScope.forward(tabName, 'views/credit/CommercialCredit/index.html', {'task': task});
    };

    $scope.taskApplication = function (task) {
        var cust_id = task.party_id;
        var cust_name = task.cust_name;
        var tabName = cust_name + '的' + task.activity.activity_name;
        var page = task.activity.activity_page;
        if (task.product_code.substring(0,1) == '8'){
            $rootScope.forward(task.activity_name,'views/credit/sameBusiness/detail.html', {'applicationId':task.application_id,
                'product_name':task.product_name,'product_page':task.product_page,'product_code':task.product_code,'application_status':task.activity.activity_name,'activity_status':task.activity.activity_status});
        }else if (task.product_code.substring(0,3) == '705'){
            $rootScope.forward(tabName,'views/credit/invest/detail.html', {'applicationId':task.application_id,
                'product_name':task.product_name,'product_page':task.product_page,'product_code':task.product_code,'application_status':task.activity.activity_name,'activity_status':task.activity.activity_status});
        }else if (task.product_code.substring(0,2) == '95'){
            $rootScope.forward(tabName,'views/uniteCredit/uniteCreditInfo.html', {'application_id':task.application_id,
                'product_name':task.product_name,'product_page':task.product_page,'product_code':task.product_code,'application_status':task.activity.activity_name,'activity_status':task.activity.activity_status});
        }else if(task.product_code=='961'){
            $rootScope.forward(tabName,'views/credit/FiveLevel/info.html', {'application_id':task.application_id});
        }else if(task.product_code=='971'){
            $rootScope.forward(tabName,'views/credit/Repossession/info.html', {'application_id':task.application_id});
        }else if(task.product_code=='972'){//展期
            $rootScope.forward(tabName,'views/credit/Extension/info.html', {'application_id':task.application_id});
        }else if(task.product_code=='973'){//授信金额调整
            $rootScope.forward(tabName,'views/credit/adjustment/info.html', {'application_id':task.application_id});
        }else if(task.product_code=='974'){//贷款核销
            $rootScope.forward(tabName,'views/credit/auditsale/info.html', {'application_id':task.application_id});
        }else{
            if(page){
                $rootScope.forward(tabName,'views/credit/pageDistribute/index.html', {'applicationId':task.application_id, 'customer':{'id':task.party_id, 'name':task.cust_name,'no':task.cust_no,'type_code':task.type_code},'product_name':task.product_name,'product_page':task.product_page,'product_code':task.product_code,'application_status':task.activity.activity_name,'activity_status':task.activity.activity_status,'activity_page':page,'role':task.role});
            }else{
                $rootScope.forward(tabName,'views/credit/index.html', {'applicationId':task.application_id, 'customer':{'id':task.party_id, 'name':task.cust_name,'no':task.cust_no,'type_code':task.type_code},
                    'product_name':task.product_name,'product_page':task.product_page,'product_code':task.product_code,'application_status':task.activity.activity_name,'activity_status':task.activity.activity_status});
            }
        }
    };

    /*Fetch Menu in database table name [Menu] */
    permissionService.user_permission_menu_dump().success(function (resp) {
        $scope.menus = resp.data;
    });


}]);
