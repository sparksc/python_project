ysp.controller('loanApplicationController', function($scope, $rootScope, LOCAService, CustomerSearchService ){
    $scope.loan_tab={};
    var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'', };
    $scope.guaranteeType = ['新发生', '展期', '借旧还新', '资产重组'];
    $scope.lendType = ['个人住房贷款'];
    $scope.tableMessage = '请点击查询';
    $scope.application_status = "放款";

    /* Table Operating Flag */

    /* Query Application */
    $scope.tableHead=['出账流水号','合同流水号', '客户名称', '业务品种', '贷款状态', '币种', '金额','操作'];
    $scope.queryCond = {};
    $scope.tableData = [];
    $scope.queryApplication = function(){
        LOCAService.query(
                $scope.applicationStatus,
                $scope.queryCond.cust_name,
                $scope.queryCond.guarantee_type,
                $scope.queryCond.lend_type,
                $scope.queryCond.ld_ratio,
                $scope.queryCond.start_date,
                $scope.queryCond.end_date
            ).success(function(resp){
                $scope.tableData = resp.data;
                
                $scope.tableData = [{'id':12323,'contract_no':'23432545','cust_name':'张三','product_name':'个人住房贷款','currency':'人民币','amount':'2878','application_status':'贷款申请'}];
                $scope.tableMessage=''; 
                /**
                if($scope.tableData.length > 0){
                }else{
                    $scope.tableMessage='未查询到数据'; 
                }
                */
            }
        );
    };

    $scope.init = function(){
        $scope.queryApplication();
    };
    $scope.tableHead1=['抵押物编号','抵押物类型', '权利人名称', '权证号', '登记人', '登记时机', '登记机构', '更新时间', '操作'];
    // 担保合同申请
    $scope.loca_index = "新增担保信息";

    $scope.guarantee_add = function(applicationStatus, $event){
        angular.element("#accordion").children(".collapse.in").find(".active").removeClass('active');
        angular.element(event.srcElement).addClass('active');
        var tabName = '新增担保信息';
        var eventObj = {
            'close':{
                'changeNav': "TODO:根据显示页面来显示Nav的active",
                'on':function(){
                    angular.element("#accordion").children(".collapse.in").find(".active").removeClass('active');
                    return true;
                }
            }
        };
        var htmlContent = '<div ng-include="'+'\'views/credit/GuaranteeInformation/guaranty/guarantee_add.html' +'\'"></div>';
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'applicationStatus':applicationStatus});
    };
    // 担保合同申请
    $scope.loca_index = "新增抵质押物信息";

    $scope.limits_add = function(applicationStatus, $event){
        angular.element("#accordion").children(".collapse.in").find(".active").removeClass('active');
        angular.element(event.srcElement).addClass('active');
        var tabName = '新增抵质押物信息';
        var eventObj = {
            'close':{
                'changeNav': "TODO:根据显示页面来显示Nav的active",
                'on':function(){
                    angular.element("#accordion").children(".collapse.in").find(".active").removeClass('active');
                    return true;
                }
            }
        };
        var htmlContent = '<div ng-include="'+'\'views/credit/GuaranteeInformation/guaranty/limits_add.html' +'\'"></div>';
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'applicationStatus':applicationStatus});
    };

    /* Application Detail */
    $scope.applicationDetail = function(applicationId){
        LOCAService.detail(applicationId).success(function(resp){
            var data = resp.data;
            var cust_name = resp.data.customer_name;
            var tabName = cust_name+'的贷款申请';
            var htmlContent = '<div ng-include="'+'\'views/credit/index.html' +'\'" ></div>';
            var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':data.party});                       
            var applicationScope = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).scope();
            applicationScope['loan_type'] = '101';
            applicationScope['base_info_display'] = true;
        });

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

    
    /* Submit Application */
    $scope.submitModalData = {};
    $scope.submitTableHead = ['编号', '检查名称', '状态'];
    $scope.submitTableData = [];
    $scope.submitApplication = function(d){
        var cust_id= '2';
        var tabName ='张三的放款申请'
        var htmlContent = '<div ng-include="'+'\'views/loan/loanInfo.html' +'\'"></div>';
        if($scope.loan_tab[cust_id] == undefined || $rootScope.tab[$scope.loan_tab[cust_id]] == undefined){
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'transaction_info':d});
            $scope.loan_tab[cust_id] = tab_id;
        }else{
            alert("用户放款标签已打开");
        }
    };
    $scope.submitConfirmed = function(){
        $scope.submitTableData = [];
    };
    $scope.submitCanceled = function(){
        $scope.submitTableData = [];
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
            $scope.queryApplication();
        }).error(function(){
            alert('取消失败，请重试');
        });
    }

    /* Sign Comment  */
    $scope.signCommentApplicationId = null;
    $scope.signCommentModalData = {};
    $scope.signComment = function(applicationId){
        $scope.signCommentEditFlag = false;
        $scope.signCommentApplicationId = applicationId;
        $scope.signCommentModalData = {};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='signCommentModal']").modal({backdrop: 'static',});
    };
    $scope.signCommentConfirmed = function(){
        LOCAService.signComment($scope.signCommentApplicationId, $scope.signCommentModalData).success(function(resp){
            alert('签署成功！');
            $scope.signCommentApplicationId = null;
            $("#tab_"+ $scope.tabId + "_content").find("div[name='signCommentModal']").modal('hide');
            $scope.signCommentModalData = {};
            $scope.queryApplication();
        }).error(function(){
            alert('签署意见失败，请重试');
        });
    };
    $scope.signCommentEdit = function(){
        LOCAService.updateComment($scope.signCommentApplicationId, $scope.signCommentId, $scope.signCommentModalData).success(function(resp){
            alert('修改成功！');
            $scope.signCommentApplicationId = null;
            $scope.signCommentId = null;
            $scope.signCommentModalData = {};
            $("#tab_"+ $scope.tabId + "_content").find("div[name='signCommentModal']").modal('hide');
            $scope.queryApplication();
        }).error(function(){
            alert('修改签署意见失败，请重试');
        });

    };
    $scope.signCommentCancel = function(){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='signCommentModal']").modal('hide');
            $scope.queryApplication();
    };
    
    $scope.viewSignCommentDetail = function(applicationId, signCommentId){
        $scope.signCommentEditFlag = true;
        LOCAService.viewComment(applicationId, signCommentId).success(function(resp){
            $scope.signCommentApplicationId = applicationId;
            $scope.signCommentId = signCommentId;
            $scope.signCommentModalData = resp.data;
            $("#tab_"+ $scope.tabId + "_content").find("div[name='signCommentModal']").modal({backdrop: 'static',});
        });
    };
})
.filter('applicationStatusFilter', function(){
    return function(item){
        switch(item){
            case 'pending':
                return '未提交';
            case 'reviewing':
                return '审查审批中';
            case 'returned':
                return '退回补充资料';
            case 'approved':
                return '审查通过';
            case 'denied':
                return '被否决';
            case 'canceled':
                return '取消';
            default:
                return '未知';
        }
    }
})
.service('LOCAService', function($http){
    return {
        query:function(application_status, cust_name, guarantee_type, lend_type, ld_ratio, start_date, end_date){
            var cond = '';
            cond = application_status? cond+'application_status='+application_status:cond;
            cond = cust_name ? cond+'cust_name='+cust_name:cond;
            cond = guarantee_type != undefined? cond+'&guarantee_type='+guarantee_type:cond;
            cond = lend_type != undefined? cond+'&lend_type='+lend_type:cond;
            cond = ld_ratio != undefined? cond+'&ld_ratio='+ld_ratio:cond;
            cond = start_date != undefined? cond+'&start_date='+start_date:cond;
            cond = end_date != undefined? cond+'&end_date='+end_date:cond;
            return $http.get(base_url+'/credit_application?'+cond);
        },
        detail:function(applicationId){
            return $http.get(base_url+'/credit_application/'+applicationId);
        },
        cancel:function(applicationId){
            return $http.delete(base_url+'/credit_application/'+applicationId);
        },
        signComment:function(applicationId, data){
            return $http.post(base_url+'/credit_application/'+applicationId+'/sign_comment', data);
        },
        viewComment:function(applicationId, signCommentId){
            return $http.get(base_url+'/credit_application/'+applicationId+'/sign_comment/'+signCommentId);
        },
        updateComment:function(applicationId, signCommentId, data){
            return $http.put(base_url+'/credit_application/'+applicationId+'/sign_comment/'+signCommentId, data);
        }
    }
})

