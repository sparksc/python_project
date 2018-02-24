ysp.controller('lineOfCreditApplicationController', function($scope, $rootScope, LOCAService, CustomerSearchService ){
    $scope.guaranteeType = ['新发生', '展期', '借旧还新', '资产重组'];
    $scope.lendType = ['个人住房贷款'];

    /* Query Application */
    $scope.tableHead=['申请书号','客户名称', '业务品种', '主要担保方式', '申请状态', '币种', '金额', '申请人', '申请机构', '操作'];
    $scope.queryCond = {};
    $scope.tableData = [];
    $scope.queryApplication = function(){
        LOCAService.query(
                $scope.queryCond.application_status,
                $scope.queryCond.cust_name,
                $scope.queryCond.guarantee_type,
                $scope.queryCond.lend_type,
                $scope.queryCond.ld_ratio,
                $scope.queryCond.start_date,
                $scope.queryCond.end_date
            ).success(function(resp){
                $scope.tableData = resp.data;
            }
        );
    };
    
    /* Application Detail */
    $scope.applicationDetail = function(applicationId){
        var cust_id = '';
        var cust_name = '';
        var tabName = cust_name+'的贷款申请';
        var htmlContent = '<div ng-include="'+'\'views/credit/index.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':$scope.chosenCust.party});                       
    };

    /* New Application */
    $scope.newApplication = function(){
        var d = new Date();
        $scope.curr_date = d.getFullYear() + '-' + d.getMonth() + '-' + d.getDay();
        $scope.confirmBtnDisabled = false;
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal({backdrop: 'static',});
    };

    // Customer Search
    $scope.customerListTH = ['客户编号', '客户名称', '证件类型', '证件号码', '客户类型'];
    $scope.cust_search = { 'cust_name':'',};
    $scope.chosenCust = null;
    $scope.searchCustomer = function(){
        CustomerSearchService.query('', $scope.cust_search.cust_name).success(function(resp){
            $scope.custTableData =  resp.data;
        });
    };
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
        var tabName = cust_name+'的贷款申请';
        var htmlContent = '<div ng-include="'+'\'views/credit/index.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':$scope.chosenCust.party});
    };

    $scope.custSearchCancel = function(){
        $scope.chosenCust = null;
        $scope.custTableData = {};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal('hide');
    };

    /* Cancel Application */
    $scope.cancelModalData = null;
    $scope.cancelApplication = function(applicationId){
        $scope.cancelId = applicationId;
        $("#tab_"+ $scope.tabId + "_content").find("div[name='cancelConfirmModal']").modal({backdrop: 'static',});
    }
    $scope.cancelConfirmed = function(){
        LOCAService.cancel($scope.cancelId).success(function(resp){
            $scope.cancelId = null;
            $("#tab_"+ $scope.tabId + "_content").find("div[name='cancelConfirmModal']").modal('hide');
        }).error(function(){
            alert('取消失败，请重试');
        });
    }

    /* Sign Comment  */
    $scope.signCommentModalData = null;
    $scope.signComment = function(){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='signCommentModal']").modal({backdrop: 'static',});
    };
    $scope.signCommentConfirmed = function(){
        LOCAService.cancel($scope.cancelId).success(function(resp){
            $scope.cancelId = null;
            $("#tab_"+ $scope.tabId + "_content").find("div[name='signCommentModal']").modal('hide');
        }).error(function(){
            alert('签署意见失败，请重试');
        });
    };
    $scope.signCommentCancel = function(){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='signCommentModal']").modal('hide')
    };
})
.filter('applicationStatusFilter', function(){
    return function(item){
        switch(item){
            case 'pending':
                return '待处理';
            case 'reviewing':
                '审查审批中'
            case 'returned':
                return '退回补充资料'
            case 'approved':
                return '审查通过'
            case 'denied':
                return '被否决'
            case 'canceled':
                return '取消'
            default:
                return '未知'
        }
    }
})

