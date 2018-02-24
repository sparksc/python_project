ysp.controller('auditsaleController', function($scope, $rootScope, loanService, AuditsaleService){
    /* Query fiveLevel */
    $scope.tableHead=['申请编号',  '客户编号','客户名称', '交易ID', '审批状态', '操作'];
    $scope.tableMessage='请点击查询';
    $scope.queryCond = {};
    $scope.tableData = {};
    $scope.queryAuditsale = function(){
        AuditsaleService.query().success(function(resp){
                $scope.tableData = resp.data;
                if($scope.tableData.length > 0){
                    $scope.tableMessage='';
                }else{
                    $scope.tableMessage='未查询到数据';
                }
            }
        );
    };
    /* New */
    $scope.newAuditsale = function(){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchLoanModal']").modal({backdrop: 'static',});
    };
    $scope.edit_flag = $scope.edit_flag != undefined? $scope.edit_flag:1;
    $scope.data = $scope.data != undefined? $scope.data:{};

    $scope.onDetail = function(d){
        var htmlContent = '<div ng-include="'+'\'views/credit/Auditsale/info.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var cust_name = d.party.name;
        var tabName = cust_name+'的贷款授信金额详情';
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'data':d} );

    };
    $scope.onDelete = function(id){
        if (confirm("确定撤销分类申请吗？")) {
            AuditsaleService.deleteById(id).then(function(){
                $scope.queryAuditsale();
            })
        }
    };

    /* Loan Search */
    $scope.loanListTH = ['交易ID', '客户编号', '客户名称', '贷款金额', '发放日期', '到期日期'];
    $scope.loan_search = {};
    $scope.loanTableData = {};
    $scope.chosenLoan = null;
    $scope.searchLoan = function(){
        loanService.query_list().success(function(resp){
            $scope.loanTableData =  resp.data;
        });
    };
    $scope.choseLoan = function(loan, $event){
        $scope.chosenLoan = loan;
        var obj = event.srcElement;
        var oTr = obj.parentNode;
        var tableObj = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content'))
            .find("table[name='loanListTable']")[0];
        for(var i=1; i<tableObj.rows.length; i++){
            tableObj.rows[i].style.backgroundColor = "";
            tableObj.rows[i].tag = false;
        }
        oTr.style.backgroundColor = "#87CEFA";
    };
    $scope.loanSearchConfirm = function(){

        if($scope.chosenLoan == null){alert('请先选中要申请的贷款');}
        else {
            $("#tab_"+ $scope.tabId + "_content").find("div[name='searchLoanModal']").modal('hide');
            $scope.chosenLoan.credit_level={};
            console.log("------------");
            console.log($scope.chosenLoan);
            console.log("============");
            var cust_name = $scope.chosenLoan.party.name;
            var tabName = cust_name+'的贷款授信金额申请';
            var htmlContent = '<div ng-include="'+'\'views/credit/Auditsale/info.html' +'\'" ></div>';
            var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'data':$scope.chosenLoan});
        }


    };

    $scope.loanSearchCancel = function(){
        $scope.chosenLoan = null;
        $scope.loanTableData = {};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchLoanModal']").modal('hide');
    };

})

ysp.controller('auditsaleBaseController', function($scope, $compile, loanService,userService,AuditsaleService,approvalService){
    $scope.edit_flag = true;
    $scope.subTabIndex = 0;
    $scope.currIndex = 0;
    $scope.subTab = {}; //check if open the same tab
    if($scope.application_id){
        AuditsaleService.query_by_id($scope.application_id).success(function(resp){
            $scope.data = resp.data;
        });
    }
    $scope.approve = function(){
        if(!$scope.application_id){
            $scope.application_id=$scope.data.application.id;
        }
        approvalService.approve($scope.application_id, {'comment_type':'同意', 'comment':$scope.result})
            .success(function(resp){
                $scope.submitedFlag = true;
                $scope.next_step=resp.data.next_step;
                if($scope.next_step.length>0){
                    $("#tab_"+ $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
                }else{
                    alert('审批完成');
                }
            });
    }

    if($scope.application_id){
        AuditsaleService.query_by_id($scope.application_id).success(function(resp){
            $scope.data = resp.data;
        });
    }
    $scope.onSubmit = function(){
        if ($scope.data.auditsale.id){
            AuditsaleService.submit($scope.data).success(function(resp){
                alert("申请已提交!")
                $scope.edit_flag = true;
            })
        }else{
            AuditsaleService.save_submit($scope.data).success(function(resp){
                alert("申请已提交!")
                $scope.edit_flag = true;
                $scope.data.auditsale=resp.data.auditsale
                //    $rootScope.tabClose($scope.tabId);
            })
        }
    };
    $scope.onSave = function(){
        console.log($scope.data);
        if ($scope.data.auditsale.id){
            AuditsaleService.update($scope.data).then(function(resp){
                if (resp.data.data.success){
                    alert("数据已更新!")
                    $scope.edit_flag = true;
                }else{
                    alert("数据更新失败");
                }
            });
        }else{
            AuditsaleService.save($scope.data).success(function(resp){
                $scope.data= resp.data;
                $scope.data.application = resp.data.application;
                if ($scope.data){
                    alert("数据已保存!")
                    $scope.edit_flag = true;
                }else{
                    alert("数据保存失败");
                }
            })
        }

    };
    $scope.onEdit = function(){
        $scope.edit_flag = false;
    };
    $scope.approve = function(){
        if(!$scope.application_id){
            $scope.application_id=$scope.data.application.id;
        }
        approvalService.approve($scope.application_id, {'comment_type':'同意', 'comment':$scope.result})
            .success(function(resp){
                $scope.submitedFlag = true;
                $scope.next_step=resp.data.next_step;
                if($scope.next_step.length>0){
                    $("#tab_"+ $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
                }else{
                    alert('审批完成');
                }
            });
    }
})

