ysp.controller('commTaskController', function($scope, $rootScope,creditService, commTaskService){
    console.log($scope.task)
    $scope.customer_tab={}
    $scope.loan_tab={}
    $scope.task_head=['客户编号','借款人名称','法定代表人','抵押物','抵押面积','评估单价','评估总值','他项权号码','他项权证期限','担保额','授信额','授信期限','贷款金额','本抵押物项下最高贷款金额','抵借比例(申报)','核定(年)','执行利率种类(申报)','利率(申报)','支付方式','最高限额','抵借比例(核定)','贷后单价','执行利率种类(核定)','利率(核定)','备注','发放日期','发放金额','操作']
    $scope.edit_flag = true;
    
    //TODO:提交后不能修改
    $scope.onSubmit = function(){
          commTaskService.approve({'application':$scope.task}).success(function(resp){
                $scope.submitedFlag = true;
                alert('提交成功');
          });
    };
    $scope.onEdit = function(){
        $scope.edit_flag = false;
    };

    $scope.onCancel = function(){
        $scope.edit_flag = true;
    };
    $scope.onSave = function(){
        $scope.edit_flag = true;
    };
    $scope.showCust = function(cust){
       var cust_id = cust.id;
       var cust_name = cust.name;
       var cust_type = cust.type_code;
       var tabName = cust_name+'的客户信息';
       var eventObj = {
            'close':{
                'changeNav': "TODO:根据显示页面来显示Nav的active",
                'on':function(){
                    angular.element("#accordion").children(".collapse.in").find(".active").removeClass('active');
                    return true;
                }
            }
        };
       var htmlContent = '<div ng-include="'+'\'views/customer/person/index.html' +'\'" ></div>';
       if(cust_type == 'company'){
               var htmlContent = '<div ng-include="'+'\'views/customer/company/index.html' +'\'" ></div>';
       }
       if($scope.customer_tab[cust_id] == undefined || $rootScope.tab[$scope.customer_tab[cust_id]] == undefined){
           var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':cust});
           $scope.customer_tab[cust_id] = tab_id;
       }else{
           alert("用户信息标签已打开");
       }
    }
    $scope.loanInfo = function(data,value){
        var cust=data.party;
        var cust_id = cust.id;
        var cust_name = cust.name;
        var tabName = cust_name+'的贷款申请';
        var eventObj = {};
        var htmlContent = '<div ng-include="'+'\'views/credit/index.html' +'\'"></div>';
        if($scope.loan_tab[cust_id] == undefined || $rootScope.tab[$scope.loan_tab[cust_id]] == undefined){
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'applicationId':data.application.id,'application_status':'下月到期','customer':cust, 'product_name':'商用房抵押贷款','product_code':data.application.product_code});
            $scope.loan_tab[cust_id] = tab_id; 
        }else{
            alert("用户贷款标签已打开");
        }   
    } 
})
.service('commTaskService', function($http){
    return{
       approve:function(applications){
            return $http.post(base_url+'/credit_application/bat_approve/',applications);
        }, 
    }
})
