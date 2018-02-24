/*贷款申请——增加低质押物*/
ysp.controller('guaranteeInformationController', function ($scope, $rootScope, guaranteeService, guaranteeInfoService, customerService) {
    $scope.tableHead = ['担保资料号', '担保方式', '具体担保方式', '担保金额', '担保合同号', '操作'];
    $scope.application_id = $scope.$parent.applicationId;
    $scope.queryCond = {};
    $scope.tableData = [];
    $scope.guarantee_info = {};

    // 初始化基础信息
    var init_data = function () {
        $scope.guarantee_info.customer_no = $scope.customer.no;                                        // 借款人客户代码
        $scope.guarantee_info.customer_name = $scope.customer.name;                                    // 借款人姓名
        $scope.guarantee_info.branch_name =$rootScope.user_session.branch_code+'-'+ $rootScope.user_session.branch_name;                       // 登记机构
        $scope.guarantee_info.user_name =$rootScope.user_session.user_code+'-'+ $rootScope.user_session.user_name;                           // 登记人

        //Relation Config
        //$scope.guarantee_info.user_id = $rootScope.user_session.user_id;                // 登记人ID
        //$scope.guarantee_info.check_user_id = $rootScope.user_session.user_id;                // 登记人ID
        //$scope.guarantee_info.customer_id = $scope.customer.id;                         // 借款人ID
    };

    $scope.current_date = $rootScope.current_date;


    var query_guarantee = function () {
        guaranteeInfoService.query_infos($scope.application_id).success(function (resp) {
            $scope.tableData = resp.data;
            if (resp.data.length > 0) {
                $scope.tableMessage = '';
            } else {
                $scope.tableMessage = '未查询到数据';
            }
        });
    };


    $scope.save_guarantee = function () {
        $scope.guarantee_info.application_id = $scope.application_id;
        guaranteeInfoService.save($scope.guarantee_info).success(function (resp) {
            alert(resp.data.msg);
            angular.element('#guarantree_modal').modal('hide');
            query_guarantee();
        });
    };
    $scope.detail_guarantee = function (repos) {
        console.log(repos);
        /*if (data.contract) {
            contract_id = data.contract.contract_id;
        } else {
            contract_id = '';
        }
        var cust_name = $scope.customer.name;
        var gty_method = data.guarantee_info.gty_method;
        var tabName = cust_name + '的' + gty_method + '信息详情';
        var htmlContent = '<div ng-include="' + '\'views/credit/GuaranteeInformation/guaranty/index.html' + '\'" ></div>';
        var eventObj = {'create': '', 'focus': '', 'loseFocus': '', 'close': '',};
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {
            'customer': $scope.customer,
            'contract_id': contract_id,
            'gty_info_id': data.guarantee_info.id,
            'gty_detail': data.guarantee_info.gty_detail,
            'gty_method': data.guarantee_info.gty_method,
            'application_status': $scope.application_status
        });*/
        var guarantee_info = repos.guarantee_info;
        var contract_no = repos.contract ? repos.contract.contract_no : null;

        $rootScope.forward($scope.customer.name + guarantee_info.gty_method + '信息('+ guarantee_info.id + ')'
            , 'views/credit/GuaranteeInformation/guaranty/index.html',{'gty_info_id': guarantee_info.id,'contract_no':contract_no,'activity_status':$scope.activity_status});

    };
    $scope.delete_guarantee = function (guarantee_info_id) {
        guaranteeInfoService.del(guarantee_info_id).success(function (resp) {
            alert(resp.data.msg);
            query_guarantee();
        });

    };
    init_data();
    query_guarantee();

    $scope.show_guaranty_modal = function () {
        angular.element('#guarantree_modal').modal('show');
    };
    $scope.flush_guaranty_modal = function () {
        query_guarantee();
    };
    $scope.quote_guaranty_modal = function () {
        angular.element('#quote_guarantree_modal').modal('show');
    };
    $scope.save_contract = function () {
        guaranteeInfoService.query_allinfo( $scope.all_contract_no).success(function (resp) {
            if(resp.data.msg=='合同号存在') {
                $scope.tableData = [];
                $scope.tableData[0] = resp.data;
                $scope.all_contract = resp.data.contract;

                console.log(resp);
                guaranteeInfoService.query_infos($scope.application_id).success(function (resps) {
                    var len = 0;
                    angular.forEach(resps.data, function (data, index, array) {
                        angular.forEach($scope.all_contract, function (datas, indexs, arrays) {
                            if (data.guarantee_info.id == datas.gty_info_id) {
                                len = len + 1;
                            }
                        });
                    });
                    if (len >= 1) {
                        query_guarantee();
                        alert("您已引用过该合同编号，不可重复引用");
                    } else {
                        resp.data.guarantee_info.application_id = $scope.application_id;
                        guaranteeInfoService.save_contract(resp.data, resp.data.contract_id).success(function (resp) {
                            query_guarantee();
                            alert("引用添加成功!");
                        });
                    }
                });

            }else{
                query_guarantee();
                alert("合同不存在");

            }
        });
        /*

         angular.forEach(resp.data, function(data,index,array){
         if(data.contract.contract_no == $scope.all_contract_no){

         console.log(array[index]);

         }
         });s
         */

    };


});


