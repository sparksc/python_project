ysp.controller('standBookController', function($scope, $rootScope, loanService, standBookService){
/* Query fiveLevel */
    $scope.tableHead=['台账序号',  '放贷支行','借款人名称', '贷款金额', '贷款余额', '诉讼起始时间', '工作状态','操作'];
    $scope.tableMessage='请点击查询'; 
    $scope.queryCond = {};
    $scope.tableData = {};
    $scope.queryStandBook = function(){
        standBookService.query_list().success(function(resp){
                $scope.tableData = resp.data;
                if($scope.tableData.length > 0){
                    $scope.tableMessage=''; 
                }else{
                    $scope.tableMessage='未查询到数据'; 
                }
            }
        );
    };
    $scope.newStandBook = function(){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchLoanModal']").modal({backdrop: 'static',});
    };

/* FiveLevel Operate */
    $scope.onDetail = function(d){
        var htmlContent = '<div ng-include="'+'\'views/credit/StandingBook/info.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var cust_name = d.party.name
        var tabName = cust_name+'的诉讼台账';
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'book':d} );
    };
/* Loan Search */
    $scope.loanListTH = ['交易ID', '客户编号', '客户名称', '合同号', '借据金额', '发放日期', '到期日期'];
    $scope.loan_search = {};
    $scope.loanTableData = {};
    $scope.chosenLoan = null;
    $scope.searchLoan = function(){
        standBookService.query_debt().success(function(resp){
            $scope.loanTableData =  resp.data;
        });
    };
    $scope.clearLoanSearch = function(){
        $scope.loan_search = {};
        $scope.loanTableData = {};
    };
    $scope.exportBook = function(){
        console.log($scope.tableData)
        standBookService.export_book({'data':$scope.tableData}).success(function(resp){
            location.href=resp.data.file;      
        });
    }
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
        if($scope.chosenLoan == null){alert('请先选择一笔借据');}
        else {
            $("#tab_"+ $scope.tabId + "_content").find("div[name='searchLoanModal']").modal('hide');
            var cust_name = $scope.chosenLoan.party.name;
            var tabName = cust_name+'的贷款诉讼台账详情';
            var htmlContent = '<div ng-include="'+'\'views/credit/StandingBook/info.html' +'\'" ></div>';
            var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'book':$scope.chosenLoan});
        }

    };

    $scope.loanSearchCancel = function(){
        $scope.loanTableData = {};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchLoanModal']").modal('hide');
    };

})

ysp.controller('bookInfoController', function($scope, $compile, loanService,userService,standBookService){
    $scope.subTabIndex = 0;
    $scope.currIndex = 0;
    $scope.subTab = {}; //check if open the same tab
    if(!$scope.book.litigation_book){
         $scope.book.litigation_book={}
         $scope.book.litigation_book.status='提起诉讼';
    }
    $scope.onSave = function(){
        if ($scope.book.litigation_book.id){
            standBookService.update($scope.book).then(function(resp){
                 standBookService.query($scope.book.litigation_book.id).success(function(resp){
                    $scope.book.litigation_book = resp.data.litigation_book;
                    alert("数据已更新!")
                    $scope.btn_edit_flag = false;
                    $scope.edit_flag = 0;
                 });
            })
        }else{
            standBookService.save($scope.book).success(function(resp){
                $scope.book.litigation_book = resp.data.litigation_book;
                    alert("数据已保存!")
                    $scope.btn_edit_flag = false;
                    $scope.edit_flag = 0;
            })
        }
    };
    $scope.onEdit = function(){
        $scope.btn_edit_flag = true;
        $scope.edit_flag = 1;
    };
    var defaultEvent = {
        'on':function(){
            return true;
        }
    };

})
ysp.controller('repossessionBookController', function($scope, $rootScope, loanService, standBookService,RepossessionService){
/* Query fiveLevel */
    $scope.tableHead=['台账序号',  '放贷支行','借款人名称', '贷款金额', '抵入时间','操作'];
    $scope.tableMessage='请点击查询'; 
    $scope.queryCond = {};
    $scope.queryStandBook = function(){
        standBookService.query_repossession().success(function(resp){
                $scope.tableData = resp.data;
                if($scope.tableData.length > 0){
                    $scope.tableMessage=''; 
                }else{
                    $scope.tableMessage='未查询到数据'; 
                }
            }
        );
    };
    $scope.newStandBook = function(){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchLoanModal']").modal({backdrop: 'static',});
    };

/* FiveLevel Operate */
    $scope.onDetail = function(d){
        var htmlContent = '<div ng-include="'+'\'views/credit/StandingBook/repossession_book_info.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var cust_name = d.party.name
        var tabName = cust_name+'的以物抵债台账';
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'data':d} );
    };
/* Loan Search */
    $scope.loanListTH = ['申请编号',  '客户编号','客户名称', '交易ID', '审批状态'];
    $scope.loan_search = {};
    $scope.loanTableData = {};
    $scope.chosenLoan = null;
    $scope.searchLoan = function(){
        RepossessionService.query().success(function(resp){
            $scope.loanTableData =  resp.data;
            console.log($scope.loanTableData);
        });
    };
    $scope.clearLoanSearch = function(){
        $scope.loan_search = {};
        $scope.loanTableData = {};
    };
    $scope.exportBook = function(){
        standBookService.export_book({'data':$scope.tableData}).success(function(resp){
            location.href=resp.data.file;      
        });
    }
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
        if($scope.chosenLoan == null){alert('请先选择一笔借据');}
        else {
            $("#tab_"+ $scope.tabId + "_content").find("div[name='searchLoanModal']").modal('hide');
            var cust_name = $scope.chosenLoan.party.name;
            var tabName = cust_name+'的贷款诉讼台账详情';
            var htmlContent = '<div ng-include="'+'\'views/credit/StandingBook/repossession_book_info.html' +'\'" ></div>';
            var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'data':$scope.chosenLoan});
        }
    };
    $scope.exportBook = function(){
        standBookService.export_repossession_book({'data':$scope.tableData}).success(function(resp){
            location.href=resp.data.file;      
        });
    };

    $scope.loanSearchCancel = function(){
        $scope.loanTableData = {};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchLoanModal']").modal('hide');
    };

})

ysp.controller('repossessionBookBaseController', function($scope, $rootScope, loanService, standBookService){
       $scope.edit_flag=true;
       $scope.onSave = function(){
             if(!$scope.data.book){
                 standBookService.save_repossession($scope.data).success(function(resp){
                       alert('保存成功');
                       $scope.edit_flag=true;
                       $scope.data.book=resp.data.book;
                 });
             }else{
                 standBookService.update_repossession($scope.data).success(function(resp){
                       alert('更新成功');
                       $scope.edit_flag=true;
                 });
             } 
       }       
       $scope.onEdit = function(){
             $scope.edit_flag=false;            
       }
});


