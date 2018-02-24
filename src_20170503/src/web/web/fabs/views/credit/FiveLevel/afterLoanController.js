ysp.controller('afterLoanBaseController', function($scope, $rootScope, loanService, FiveCategoryService){
/* Query fiveLevel */
    $scope.FCtableHead=['分类申请编号',  '客户编号','客户名称', '交易ID', '认定级别', '审批状态', '操作'];
    $scope.tableMessage='请点击查询'; 
    $scope.queryCond = {};
    $scope.tableData = {};
    $scope.queryFiveCategory = function(){
        FiveCategoryService.query(
                $scope.queryCond.cate_type,
                $scope.queryCond.cate_id,
                $scope.queryCond.cus_id,
                $scope.queryCond.gty_main_method,
                $scope.queryCond.app_status,
                $scope.queryCond.transaction_id,
                $scope.queryCond.issue_date,
                $scope.queryCond.due_date
            ).success(function(resp){
                $scope.tableData = resp.data;
                if($scope.tableData.length > 0){
                    $scope.tableMessage=''; 
                }else{
                    $scope.tableMessage='未查询到数据'; 
                }
            }
        );
    };
    $scope.clearFCQuery = function(){
        $scope.queryCond = {};
        $scope.tableData = {};
    };    

/* New FiveLevel */
    $scope.newFiveCategory = function(){
        var d = new Date();
        $scope.curr_date = d.getFullYear() + '-' + d.getMonth() + '-' + d.getDay();
        $scope.confirmBtnDisabled = false;
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchLoanModal']").modal({backdrop: 'static',});
    };

/* FiveLevel Apply */
    $scope.btn_edit_flag = $scope.btn_edit_flag != undefined? $scope.btn_edit_flag:true;
    $scope.edit_flag = $scope.edit_flag != undefined? $scope.edit_flag:1;
    $scope.FC = $scope.FC != undefined? $scope.FC:{};
  
/* FiveLevel Operate */
    $scope.onDetail = function(d){
        var htmlContent = '<div ng-include="'+'\'views/credit/FiveLevel/info.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var cust_name = d.party.name
        var tabName = cust_name+'的贷款五级分类申请';
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'FC':d} );
    };
    $scope.onDelete = function(id){
        if (confirm("确定撤销分类申请吗？")) {  
            FiveCategoryService.deleteById(id).then(function(){
                $scope.queryFiveCategory();
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
    $scope.clearLoanSearch = function(){
        $scope.loan_search = {};
        $scope.loanTableData = {};
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
        if($scope.chosenLoan == null){alert('请先选择要进行分类的贷款');}
        else {
            $("#tab_"+ $scope.tabId + "_content").find("div[name='searchLoanModal']").modal('hide');
            $scope.confirmBtnDisabled = true;
            $scope.chosenLoan.credit_level={};
            var cust_name = $scope.chosenLoan.party.name;
            var tabName = cust_name+'的贷款五级分类申请';
            var htmlContent = '<div ng-include="'+'\'views/credit/FiveLevel/info.html' +'\'" ></div>';
            var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'FC':$scope.chosenLoan});
        }

    };

    $scope.loanSearchCancel = function(){
        $scope.chosenLoan = null;
        $scope.loanTableData = {};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchLoanModal']").modal('hide');
    };

})

ysp.controller('afterLoanController', function($scope, $compile, loanService,userService,FiveCategoryService,approvalService){
    $scope.subTabIndex = 0;
    $scope.currIndex = 0;
    $scope.subTab = {}; //check if open the same tab
    if($scope.application_id){
          FiveCategoryService.query_by_id($scope.application_id).success(function(resp){
                $scope.FC = resp.data;  
          });
    }
    $scope.onSubmit = function(){
        if ($scope.FC.credit_level.id){
            FiveCategoryService.submit($scope.FC).success(function(resp){
                 alert("申请已提交!")
                 $scope.btn_edit_flag = false;
                 $scope.edit_flag = 0;
            })
        }else{
            FiveCategoryService.save_submit($scope.FC).success(function(resp){
                alert("申请已提交!")
                $scope.btn_edit_flag = false;
                $scope.edit_flag = 0;
                $scope.FC.credit_level=resp.data.credit_level 
                //    $rootScope.tabClose($scope.tabId);
                })
        }
    };
    $scope.onSave = function(){
        if ($scope.FC.credit_level.id){
            FiveCategoryService.update($scope.FC).then(function(resp){
                if (resp.data.data.success){
                    alert("数据已更新!")
                    $scope.btn_edit_flag = false;
                    $scope.edit_flag = 0;
                }else{
                    alert("数据更新失败");
                }
            })
        }else{
            FiveCategoryService.save($scope.FC).success(function(resp){
                $scope.FC.credit_level = resp.data.credit_level;
                if ($scope.FC.credit_level){
                    alert("数据已保存!")
                    $scope.btn_edit_flag = false;
                    $scope.edit_flag = 0;
                }else{
                    alert("数据保存失败");
                }
            })
        }
    };
    $scope.onEdit = function(){
        $scope.btn_edit_flag = true;
        $scope.edit_flag = 1;
    };
    $scope.approve = function(){
        if(!$scope.application_id){
             $scope.application_id=$scope.FC.application.id;
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
    $scope.onEvaluate = function(){
        $scope.FC.credit_level.sys_cate_level = '关注'
    };
    var defaultEvent = {
        'on':function(){
            return true;
        }
    };
    $scope.addSubTab = function(tabName, htmlContent, eventObj, autoFocus){
        var t = new Object();
        t.index = $scope.subTabIndex;
        t.tabName = tabName;
        t.htmlContent = htmlContent;
        t.createEvent = eventObj.create? eventObj.create:defaultEvent;
        t.closeEvent = eventObj.close? eventObj.close:defaultEvent;
        t.focusEvent = eventObj.focus? eventObj.focus:defaultEvent;
        t.loseFocusEvent = eventObj.loseFocus? eventObj.loseFocus:defaultEvent;

        $scope.subTab[t.index] = t;
        var tabContentId = $scope.subTabCreate(t);
        $scope.subTabIndex = $scope.subTabIndex + 1;       

        if (autoFocus == true){
            $scope.changeFocus(t.index);
        }
        return t.index;
    }; 
    
    $scope.subTabCreate = function(tabObj){
        succ_flag = $scope.subTab[tabObj.index].createEvent.on();
        if(succ_flag==true){
            var tabId = 'loan_tab_' + $scope.$id + '_' + tabObj.index;
            var tabName = tabObj.tabName;
            var tabContentId = tabId + '_content';
            var tabHtml = '<li id="'+ tabId +'" ng-click="changeFocus('+tabObj.index+')"> <a href="#'+ tabContentId +'" data-toggle="tab">'+ tabName +'</a></li>';
            var tabContentHtml = '<div class="tab-pane" id="'+ tabContentId +'"></div>';
            baseScope = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("div[name='tabContent']").scope();
            scope = baseScope.$new();
            var tabTemplate = angular.element(tabHtml);
            var tabElement = $compile(tabTemplate)(scope);
            var contentTemplate = angular.element(tabObj.htmlContent);
            var contentElement = $compile(contentTemplate)(scope);

            angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("ul[name='tab']").append(tabElement);
            angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("div[name='tabContent']").append(tabContentHtml);
            angular.element(document.getElementById(tabContentId)).append(contentElement);

            return tabContentId;
        }else{
            alert("tab 创建失败");
        };
    };
        
    $scope.changeFocus = function(focus_tabId){
        $scope.subTabLoseFocus($scope.currIndex);
        $scope.subTabFocus(focus_tabId);
        $scope.currIndex = focus_tabId;
    };

    $scope.subTabLoseFocus = function(index){
        succ_flag = $scope.subTab[index].loseFocusEvent.on();
        if(succ_flag==true){
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index)).removeClass("ng-scope active").addClass("ng-scope");
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index + '_content')).removeClass("tab-pane active").addClass("tab-pane");
        }else{
            alert("失焦失败！");
        }
    };

    $scope.subTabFocus = function(index){
        succ_flag = $scope.subTab[index].focusEvent.on();
        if(succ_flag==true){
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index)).addClass("active");
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index + '_content')).removeClass("tab-pane").addClass("tab-pane active");
        }else{
            alert("聚焦失败！");
        }
    };

    $scope.subTabClose = function(index){
        succ_flag = $scope.subTab[index].closeEvent.on();
        if(succ_flag==true){
            if(index == $scope.currIndex){
                var prevElement = angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index)).prev();
                var nextElement = angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' +index)).next();
                if (prevElement.length > 0){
                    $scope.changeFocus(prevElement.attr('id').split('_')[3]);
                }else if(nextElement.length > 0 ){
                    $scope.changeFocus(nextElement.attr('id').split('_')[3]);
                }else{
                    $scope.changeFocus(0);
                }
            }
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' +index)).remove();
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' +index+'_content')).remove();
            delete $scope.subTab[index];
        }else{
            alert("关闭失败！");
        }
    };

    $scope.addDB = function(){
        $scope.addSubTab('担保信息', '<button class="btn btn-default"> 担保的界面显示 </button>', {}, false);
    };

    $scope.init = function(){
/*
        $scope.addSubTab('贷款五级分类', '<div ng-include="'+'\'views/credit/FiveLevel/FL_info.html' +'\'"></div>', {}, false);
        $scope.addSubTab('贷款信息', '<div ng-include="'+'\'views/credit/loanInfo.html' +'\'"></div>', {}, false);
        $scope.addSubTab('客户信息', '<div ng-include="'+'\'views/customer/person/index.html' +'\'"></div>', {}, false);
        $scope.addSubTab('担保信息', '<div ng-include="'+'\'views/credit/GuaranteeInformation/guaranty/index.html' +'\'"></div>', {}, false);
        $scope.addSubTab('调查报告', '<div ng-include="'+'\'views/credit/report.html' +'\'"></div>', {}, false);
        $scope.addSubTab('财务报表', '<div ng-include="'+'\'views/credit/financialStatements.html' +'\'"></div>', {}, false);
        $scope.subTabFocus(0);
*/
    };

})

