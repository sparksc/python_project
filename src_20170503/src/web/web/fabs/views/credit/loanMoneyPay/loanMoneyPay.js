ysp.controller('loanMoneyPay',function($scope,contractService,creditService,loanService){
    $scope.data={
                  'lend_transaction':{},
                  'application_info':{},
                  'transaction_info':{},
                  'customer':{},
                  'check':'',
                };
    $scope.payment={};

    $scope.applicationId=$scope.$parent.applicationId;
    $scope.havecontractList=[];
    $scope.no='';
    loanService.query_lend($scope.applicationId).success(function(resp){
             $scope.data.lend_transaction=resp.data.lend_transaction;
             if($scope.data.lend_transaction && $scope.data.lend_transaction.transaction_id){
             console.log($scope.data.lend_transaction);
             console.log('$scope.data.lend_transaction');
                   contractService.list_query($scope.data.lend_transaction.transaction_id).success(function(resp){
             console.log(resp.data.contracts);
                        $scope.havecontractList=resp.data.contracts;
                   });
             }
    });

    $scope.payDetail =function(d){
        $scope.no = d.contract_no;
        $scope.payment.debt_id = d.debt_id;
        console.log('payment:',$scope.payment);
        contractService.query_payment(d.debt_id).success(function(resp){
            if (resp.data){
                $scope.payment = resp.data;
                $scope.payment.debt_id = d.debt_id;
            }
        });
    }

    $scope.submitPayMethod=function(d){
         if($scope.data.lend_transaction && $scope.data.lend_transaction.transaction_id ){
            if(!$scope.payment.debt_id) alert("选择借据");
            contractService.update_payment($scope.payment.debt_id,$scope.payment).success(function(resp){
               alert(resp.data.msg) 
        
            });

    //          loanService.update($scope.data).success(function(resp){
    //               alert(resp.data.msg);
    //          });
         }else{
               alert('需在审批时填写');
         }
    } 


});
