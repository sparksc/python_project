ysp.controller('approalController', function($scope, $rootScope,approvalService){
     $scope.tableHead=['序号','环节','岗位','人员','意见','详情','时间']; 
     $scope.tableData=[];
     approvalService.query($scope.$parent.applicationId).success(function(resp){
          $scope.tableData=resp.data; 
     });
     $scope.saveReport=function(){
          approvalService.save_report($scope.$parent.applicationId).success(function(resp){
              if(resp.data.success){
                  document.getElementById("approval_report").src = resp.data.src;
                  document.getElementById("approval_report").style.display = 'block';
              }else{
                  alert(resp.data.msg);
              } 

          });    
     } 
});

ysp.controller('riskController', function($scope, $rootScope,approvalService){
     $scope.edit_flag=true;
     approvalService.query_risk($scope.$parent.applicationId).success(function(resp){
         $scope.risk_approve=resp.data.risk_info;
         $scope.flag=resp.data.flag;
         if(resp.data.risk_info){
             if(resp.data.risk_info.file_path) {
                 document.getElementById("risk_report").src =resp.data.risk_info.src;
                 document.getElementById("risk_report").style.display = 'block';
             }
         }
     });
     $scope.save=function(){
         if($scope.risk_approve.id){
             approvalService.update_risk($scope.risk_approve).success(function(resp){
                 alert('更新成功');
                 $scope.edit_flag=true;
             });
         }else{ 
             $scope.risk_approve.application_id=$scope.$parent.applicationId
             $scope.risk_approve.cust_type=$scope.customer.type_code;
             approvalService.save_risk($scope.risk_approve).success(function(resp){
                 alert('保存成功');
                 $scope.risk_approve.id=resp.data.id;
                 $scope.edit_flag=true;
             });
         }
     }
     $scope.edit=function(){
            $scope.edit_flag=false;
     }
     $scope.saveReport=function(){
          if($scope.edit_flag==false){
             alert('请先保存');
          }else{
              approvalService.save_risk_report($scope.risk_approve.id).success(function(resp){
                  if(resp.data.success){
                      $scope.risk_approve.file_path=resp.data.src;
                      document.getElementById("risk_report").src = resp.data.src;
                      document.getElementById("risk_report").style.display = 'block';
                  }else{
                      alert(resp.data.msg);
                  } 
              });    
          }
     } 

});

ysp.controller('examineController', function($scope, $rootScope,approvalService){
     $scope.edit_flag=true;
     approvalService.query_examine($scope.$parent.applicationId).success(function(resp){
         console.log(resp);
         $scope.flag=resp.data.flag;
         if(resp.data.examine_info){
             if(resp.data.examine_info.file_path) {
                 document.getElementById("examine_report").src = resp.data.examine_info.src;
                 document.getElementById("examine_report").style.display = 'block';
             }
         }

         $scope.examine_approve=resp.data.examine_info;
          if(!$scope.examine_approve){
              $scope.examine_approve={};
              $scope.examine_approve.credit_type='个人经营性贷款';
              $scope.examine_approve.remark="经审查，借款人年龄符合我行规定，身份证、户口、婚姻情况证明等手续齐全；借款用途否符合个人经营性贷款相关规定；借款人收入稳定，还款来源可靠；抵押物为 （提取贷款信息中的抵押物信息），建筑面积          平方米,抵借比例符合我行相关规定。经审贷会审议，同意发放该笔贷款。\n 建议： 发放贷款时，为抵押物办理合法有效的抵押手续；严格按照贷款资金支付流程相关规定进行贷款资金支付；按照相关规定进行贷后跟踪检查。"
         } 

     });
     $scope.changeRemark =function(){
          if($scope.examine_approve.credit_type=='个人经营性贷款'){
              $scope.examine_approve.remark="经审查，借款人年龄符合我行规定，身份证、户口、婚姻情况证明等手续齐全；>借款用途否符合个人经营性贷款相关规定；借款人收入稳定，还款来源可靠；抵押物为 （提取贷款信息中的抵押物信息），建筑面积          平方米,抵借比例符合我行相关规定。经审贷会审议，同意发放该笔贷款。\n 建议： 发放贷款时，为抵押物办理合法有效的抵押手续；严格按照贷款资金支付流程相关规定进行贷款资金支付；按照相关规定进行贷后跟踪检查。";
          }else if($scope.examine_approve.credit_type=='流动资金贷款'){
              $scope.examine_approve.remark="经审查，该借款人具有主体资格，产品符合国家产业政策，从财务指标看，该企业具有一定的偿债能力；从资金测算来看，贷款申请额度较为合理；贷款用途符合流动资金贷款相关规定；抵押资产合规、有效、足值，抵借比例符合我行相关规定。经审贷会审议同意发放该笔贷款或签发敞口银行承兑汇票。\n 建议：发放贷款或签发银行承兑汇票时，为抵押物办理合法有效的抵押手续；严格按照贷款资金支付流程相关规定进行贷款资金支付；按照相关规定进行贷后跟踪检查。" ;
          }else if($scope.examine_approve.credit_type=='担保公司担保贷款'){
              $scope.examine_approve.remark="经审查，该借款人具有主体资格，产品符合国家产业政策，从财务指标看，该企业具有一定的偿债能力；从资金测算来看，贷款申请额度较为合理；贷款用途符合流动资金贷款相关规定；保证人具有担保资格，符合担保条件。经审贷会审议同意发放该笔贷款或签发敞口银行承兑汇票。\n 建议：发放贷款或签发银行承兑汇票时，为担保人办理合法有效的担保手续；严格按照贷款资金支付流程相关规定进行贷款资金支付；按照相关规定进行贷后跟踪检查。";
          }else if($scope.examine_approve.credit_type=='保费贷款'){
              $scope.examine_approve.remark="经审查，借款人年龄符合我行规定，身份证、户口、婚姻情况证明等手续齐全；借款用途符合《保费贷款操作规程》相关规定；借款人收入稳定，还款来源可靠；抵借比例符合我行相关规定。经审贷会审议后，同意发放该笔贷款。\n建议： 发放贷款时，严格按照贷款资金支付流程相关规定进行贷款资金支付；按照相关规定进行贷后跟踪检查。";
          }else{
              $scope.examine_approve.remark="经审查，该借款人具有主体资格，产品符合国家产业政策，从财务指标看，该企业具有一定的偿债能力；从资金测算来看，申请敞口额度较为合理；签票用途符合流动资金贷款相关规定；抵押资产合规、有效、足值，抵借比例符合我行相关规定。同意经审贷会审议通过后，签发该笔银行承兑汇票。\n 建议：签发银行承兑汇票，为抵押物办理合法有效的抵押手续，按照贷后检查规定进行签发后跟踪检查。";
          }
     }
     $scope.save=function(){
         if($scope.examine_approve.id){
             approvalService.update_examine($scope.examine_approve).success(function(resp){
                 alert('更新成功');
                 $scope.edit_flag=true;
             });
         }else{ 
             $scope.examine_approve.application_id=$scope.$parent.applicationId
             approvalService.save_examine($scope.examine_approve).success(function(resp){
                 alert('保存成功');
                 $scope.examine_approve.id=resp.data.id;
                 $scope.edit_flag=true;
             });
         }
     }
     $scope.edit=function(){
            $scope.edit_flag=false;
     }
     $scope.saveReport=function(){
          approvalService.save_examine_report($scope.examine_approve.id).success(function(resp){
              if(resp.data.success){
                  $scope.examine_approve.file_path=resp.data.src;
                  document.getElementById("examine_report").src = resp.data.src;
                  document.getElementById("examine_report").style.display = 'block';
              }else{
                  alert(resp.data.msg);
              } 

          });    
     } 

});
