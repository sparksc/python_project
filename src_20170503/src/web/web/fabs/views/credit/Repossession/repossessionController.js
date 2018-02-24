ysp.controller('repossessionController', function($scope, $rootScope, loanService, RepossessionService){
/* Query fiveLevel */
    $scope.rental='未租售';
    $scope.tableHead=['申请编号',  '客户编号','客户名称', '交易ID', '审批状态', '操作'];
    $scope.tableMessage='请点击查询'; 
    $scope.queryCond = {};
    $scope.tableData = {};
    $scope.queryRepossession = function(){
        RepossessionService.query().success(function(resp){
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
    $scope.newRepossession = function(){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchLoanModal']").modal({backdrop: 'static',});
    };
    $scope.edit_flag = $scope.edit_flag != undefined? $scope.edit_flag:1;
    $scope.data = $scope.data != undefined? $scope.data:{};
  
    $scope.onDetail = function(d){
        $scope.rental="未租售";
        var htmlContent = '<div ng-include="'+'\'views/credit/Repossession/info.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var cust_name = d.party.name
        var tabName = cust_name+'的贷款以物抵债详情';
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'data':d,'rental':$scope.rental} );
    };
    $scope.onDetailre = function(d){
        $scope.rental="租售";
        var htmlContent = '<div ng-include="'+'\'views/credit/Repossession/info.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var cust_name = d.party.name
        var tabName = cust_name+'的贷款以物抵债详情';
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'data':d,'rental':$scope.rental} );
    };
    $scope.onDelete = function(id){
        if (confirm("确定撤销分类申请吗？")) {  
            RepossessionService.deleteById(id).then(function(){
                $scope.queryRepossession();
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
            $scope.rental="未租售";
            $scope.loanTableData =  resp.data;
        });
    };
    $scope.searchLoan_rental = function(){
        RepossessionService.query().success(function(resp){
                $scope.rental="租售";
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
            var cust_name = $scope.chosenLoan.party.name;
            var tabName = cust_name+'的贷款以物抵债申请';
            var htmlContent = '<div ng-include="'+'\'views/credit/Repossession/info.html' +'\'" ></div>';
            var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'data':$scope.chosenLoan,'rental':$scope.rental});
        }

    };

    $scope.loanSearchCancel = function(){
        $scope.chosenLoan = null;
        $scope.loanTableData = {};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchLoanModal']").modal('hide');
    };

})

ysp.controller('repossessionBaseController', function($scope,$rootScope, $compile, loanService,userService,RepossessionService,approvalService){
    $scope.edit_flag = true;
    $scope.subTabIndex = 0;
    $scope.currIndex = 0;
    $scope.subTab = {}; //check if open the same tab
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
        if($scope.user_groups.indexOf('客户经理') != -1){
            $scope.user='客户经理' ;
        }

    });
    /* 以物抵债右侧Tab增加相关  开始 */
    if ($scope.rental == '未租售') {
        $rootScope.addSubTab(0, '以物抵债', '<div ng-include="' + '\'views/credit/Repossession/repossession_info.html' + '\'"></div>', {}, false);
        $rootScope.addSubTab(1, '会议纪要', '<div ng-include="' + '\'views/credit/Repossession/meeting.html' + '\'"></div>', {}, false);
        $rootScope.addSubTab(2, '审查意见', '<div ng-include="' + '\'views/credit/Repossession/comments.html' + '\'"></div>', {}, false);
        $rootScope.addSubTab(3, '出租请示', '<div ng-include="' + '\'views/credit/Repossession/instructions.html' + '\'"></div>', {}, false);
        $rootScope.addSubTab(4, '风险报告', '<div ng-include="' + '\'views/credit/Repossession/report.html' + '\'"></div>', {}, false);
        $rootScope.addSubTab(5, '影像资料', '<div ng-include="' + '\'views/credit/Repossession/image.html' + '\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    } else if ($scope.rental == '租售') {
        $rootScope.addSubTab(0, '以物抵债租售', '<div ng-include="' + '\'views/credit/Repossession/rental_info.html' + '\'"></div>', {}, false);
        $rootScope.addSubTab(1, '会议纪要', '<div ng-include="' + '\'views/credit/Repossession/meeting.html' + '\'"></div>', {}, false);
        $rootScope.addSubTab(2, '审查意见', '<div ng-include="' + '\'views/credit/Repossession/comments.html' + '\'"></div>', {}, false);
        $rootScope.addSubTab(3, '出租请示', '<div ng-include="' + '\'views/credit/Repossession/instructions.html' + '\'"></div>', {}, false);
        $rootScope.addSubTab(4, '风险报告', '<div ng-include="' + '\'views/credit/Repossession/report.html' + '\'"></div>', {}, false);
        $rootScope.addSubTab(5, '影像资料', '<div ng-include="' + '\'views/credit/Repossession/image.html' + '\'"></div>', {}, false);
        $rootScope.subTabFocus(0);
    }
    $scope.savereport=function(){
        console.log($scope.data);
        console.log("---------");
        RepossessionService.savereport($scope.data.redata).success(function(resp){
            alert("保存成功");
        });
    }
    /* 以物抵债右侧Tab增加相关  结束 */


    if($scope.application_id){
          RepossessionService.query_by_id($scope.application_id).success(function(resp){
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

    $scope.onSubmit = function(){
        if ($scope.data.repossession.id){
            RepossessionService.submit($scope.data).success(function(resp){
                 alert("申请已提交!")
                 $scope.edit_flag = true;
            })
        }else{
            RepossessionService.save_submit($scope.data).success(function(resp){
                alert("申请已提交!")
                $scope.edit_flag = true;
                $scope.data.repossession=resp.data.repossession
                //    $rootScope.tabClose($scope.tabId);
                })
        }
    };
    $scope.onSave = function(){
        if ($scope.data.repossession.id){
            RepossessionService.update($scope.data).success(function(resp){
                if (resp.data.data.success){
                    alert("数据已更新!");
                    $scope.edit_flag = true;
                }else{
                    alert("数据更新失败");
                }
            });
        }else{
            RepossessionService.save($scope.data).success(function(resp){
                $scope.data.repossession = resp.data.repossession;
                $scope.data.application = resp.data.application;
                if ($scope.data.repossession){
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

