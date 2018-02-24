ysp.controller('creditLevelController', function($scope, $rootScope,CustomerSearchService,creditLevelService){
    $scope.customerListTH = ['客户编号', '客户名称', '证件类型', '证件号码', '客户类型'];
    $scope.cust_search = {'cert_type':'身份证'};
    $scope.chosenCust = null;
    //$scope.cust_search.cust_type='resident'; 
    $scope.custTableData=[];
    $scope.searchCustomer = function(){
        CustomerSearchService.query_persons($scope.cust_search.cust_no, $scope.cust_search.cust_name,$scope.cust_search.cert_type,$scope.cust_search.cert_no).success(function(resp){
             $scope.custTableData =  resp.data;
        });
    };
     $scope.searchCompany = function(){
        CustomerSearchService.query_companys($scope.cust_search.cust_no, $scope.cust_search.cust_name,$scope.cust_search.cert_type,$scope.cust_search.cert_no).success(function(resp){
             $scope.custTableData =  resp.data;
        });
    };
    
    $scope.person_level=function(party){
        //alert(100);
        creditLevelService.query_level_person(party.id).success(function(resp){
            alert(resp.data);
        });
    }


    /* New creditLevel */
    $scope.newCreditLevel = function(){
        var d = new Date();
        $scope.curr_date = d.getFullYear() + '-' + d.getMonth() + '-' + d.getDay();
        $scope.confirmBtnDisabled = false;
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal({backdrop: 'static',});
    }

    $scope.choseCustomer = function(cust, $event){
        $scope.chosenCust = cust;
        var obj = event.srcElement;
        var oTr = obj.parentNode;
        var tableObj = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content'))
                        .find("table[name='custListTable']")[0];
        for(var i=1; i<tableObj.rows.length; i++){ 
            tableObj.rows[i].style.backgroundColor = "";   
            tableObj.rows[i].tag = false;   
        }
        oTr.style.backgroundColor = "#87CEFA";   
    };
    $scope.custSearchConfirm = function(){
        $scope.confirmBtnDisabled = true;
        if($scope.chosenCust == null){alert('请先选择申请的客户');};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal('hide');

        var cust_id = $scope.chosenCust.cust_info.role_id;
        var cust_name = $scope.chosenCust.party.name;
        var tabName = cust_name+'的等级评估';
        var htmlContent = '<div ng-include="'+'\'views/credit/creditLevel/creditLevelPerson.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        console.log($scope.chosenCust.party);
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'cust_id':$scope.chosenCust.party.id,'apply_type':'新增'});
    };


    $scope.custSearchCancel = function(){
        $scope.chosenCust = null;
        $scope.custTableData = {};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal('hide');
    };
 

});


ysp.controller('creditLevelPersonController', function($scope, $rootScope,commonService){
    $scope.tableHead=['指标名称','得分','评分标准','备注']
    console.log($scope.cust_id); 
    commonService.create_person_level($scope.cust_id,{}).success(function(resp){
       console.log(resp.data); 
       $scope.dataList = resp.data;
    }); 

    $scope.showTable=function(){
        
            

    }
});
