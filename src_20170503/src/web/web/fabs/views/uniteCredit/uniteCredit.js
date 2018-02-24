/*
 *统一授信
 */
ysp.controller('uniteCreditController',function($scope,$rootScope,UniteService){

    $scope.tableHead=['授信时间', '支行名称', '授信期限','操作'];
    $scope.tableData=[];
    $scope.tableMessage = '请点击查询';
    /* New Application */
    $scope.newApplication = function(){
        var d = new Date();
        $scope.curr_date = d.getFullYear() + '-' + d.getMonth() + '-' + d.getDay();
        var tabName = '统一授信申请';
        var htmlContent = '<div ng-include="'+'\'views/uniteCredit/uniteCreditInfo.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {});
 
        //$scope.confirmBtnDisabled = false;
        //$("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal({backdrop: 'static',});
    };
    $scope.queryList=function(){
        UniteService.unite_credit_queryList({}).success(function(rsp){
            $scope.tableData = rsp.data;
            console.log(rsp.data);
        });
    }
    $scope.applicationDetail = function(id,application_id){
        var tabName = '授信详情';
        var htmlContent = '<div ng-include="'+'\'views/uniteCredit/uniteCreditInfo.html' +'\'" ></div>';
        var eventObj = {'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        $rootScope.addTab(tabName, htmlContent, eventObj, true, {'uni_id':id,'application_id':application_id});
    }
});

ysp.controller('uniteCreditApplicationController',function($scope,UniteService,$compile,approvalService){

     // 保存
     $scope.Save = function(){
            var items=[];
            for(var i in $scope.models){
                items.push($scope.models[i].uni_cre);
            }
            //var postData ={'tab':$scope. ,'items':$scope}
            console.log(items);
            UniteService.unite_credit_update({'items':items}).success(function(rsp){
                console.log(rsp.data);
                if (rsp.data.success){
                    $scope.btn_flow_flag = true
                    alert('更新成功');
                }
            });
     }   
     // 进流程
     $scope.inFlow = function(){
            UniteService.inflow($scope.uni_id).success(function(resp){
                 alert(resp.data.msg);
            });
     }   
    // 生成统一授信 
     $scope.Create = function(){
            $scope.create();
     }   
     $scope.create = function(){
        UniteService.unite_credit_create().success(function(resp){
            $scope.data = resp.data
            console.log($scope.data);
            $scope.uni_id = $scope.data.uni_cre_tb.id;
            $scope.btn_save_flag = true;
            $scope.btn_create_flag = false;
            $scope.showData();  
        });
    }
    $scope.query = function(id){
         UniteService.unite_credit_query(id).success(function(resp){
            $scope.data = resp.data
            console.log($scope.data);
            $scope.showData();  
        });
    }
    $scope.query_by_app = function(app_id){
         UniteService.query_by_app(app_id).success(function(resp){
            $scope.data = resp.data.un_tb
            console.log(resp.data.application);
            $scope.showData();  
        });
    }

    function Max(Item){
        var value = 0;
        if (Item.ples.length > value) //担保物数量
            value =Item.ples.length;
        if (Item.guas.length > value) //保证担保数量
            value =Item.ples.length;
        if (Item.ple_loans.length > value) //抵质押贷款数量
            value =Item.ple_loans.length;
        if (Item.gua_loans.length > value) //保证贷款数量
            value =Item.ple_loans.length;
        if (Item.bills.length > value) //票据数量
            value =Item.bills.length;
        return value;
    }
    $scope.showData = function(){
        var dataL = $scope.data.uni_cre_itms;
        $scope.models = $scope.data.uni_cre_itms;
        for(var i in dataL){
            var item = dataL[i]
            var h = Max(item);
            //console.log(models[i].uni_cre.finance);
            for(var k = 0 ; k < h ; ++k){

                var tr_html = "<tr>";
                if(k == 0){
                    tr_html = tr_html + "<td rowspan=\""+h+"\" style=\"vertical-align: middle;\" >"+ i +"</td>" + 
                    "<td rowspan=\""+h+"\" style=\"vertical-align: middle;\">"+ item.uni_cre.name +"</td>" + 
                    "<td rowspan=\""+h+"\" style=\"vertical-align: middle;\">"+ item.uni_cre.corp_name +"</td>"+  
                    "<td rowspan=\""+h+"\" style=\"vertical-align: middle;\"><input type=\"text\" style=\"width:100%;\" ng-model=\"models["+i+"].uni_cre.finance\"/></td>"; 
                }
            
                if(item.ples.length){ 
                    tr_html = tr_html + "<td>"+ item.ples[k].pledge_good +"</td>" + 
                    "<td>"+ item.ples[k].pledge_nums +"</td>" + 
                    "<td>"+ item.ples[k].single+"</td>" + 
                    "<td>"+ item.ples[k].total +"</td>" +
                    "<td>"+ item.ples[k].single_r +"</td>" + 
                    "<td>"+ item.ples[k].total_r +"</td>";
                }else{
                    tr_html = tr_html +
                    "<td></td>" + 
                    "<td></td>" + 
                    "<td></td>" + 
                    "<td></td>" + 
                    "<td></td>"; 
                }

                if(item.guas.length){
                     tr_html = tr_html +"<td>"+ item.guas[k].gua_person_name +"</td>" + 
                                        "<td>"+ item.guas[k].gua_limit +"</td>" ; 
                }else{
                     tr_html = tr_html +"<td></td>" + 
                                        "<td></td>" ; 
                }

                if(item.ple_loans.length){
                     tr_html = tr_html +"<td>"+ item.ple_loans[k].loan_left +"</td>" + 
                                        "<td>"+ item.ple_loans[k].term +"</td>";
                }else{

                     tr_html = tr_html +"<td></td>" + 
                                        "<td></td>" ;
                }

                if(item.gua_loans.length){
                     tr_html = tr_html +"<td>"+ item.gua_loans[k].gua_loan_left +"</td>" + 
                                        "<td>"+ item.gua_loans[k].gua_term +"</td>";
                }else{
                     tr_html = tr_html +"<td></td>" + 
                                        "<td></td>" ;
                }

                if(item.bills.length && item.bills[k]){
                        tr_html = tr_html +"<td>"+ item.bills[k].amount +"</td>" ;
                }else{
                     tr_html = tr_html +"<td ></td>";
                }
                if (k==0){
                    tr_html = tr_html + "<td rowspan=\""+h+"\" style=\"vertical-align: middle;\" >"+ item.uni_cre.most_limt_b +"</td>" + 
                    "<td rowspan=\""+h+"\" style=\"vertical-align: middle;\" ><input type=\"text\" style=\"width:100%;\" ng-model=\"models["+i+"].uni_cre.most_limt\"/></td>" + 
                    "<td rowspan=\""+h+"\" style=\"vertical-align: middle;\" ><input type=\"text\" style=\"width:100%;\" ng-model=\"models["+i+"].uni_cre.loan\" /></td>" + 
                    "<td rowspan=\""+h+"\" style=\"vertical-align: middle;\" ><input type=\"text\" disabled=\"true\" style=\"width:100%;\"  value=\"{{models["+i+"].uni_cre.most_limt - models["+i+"].uni_cre.loan}}\" /></td>" + 
                    "<td rowspan=\""+h+"\" style=\"vertical-align: middle;\" ><textarea rows=\""+h+"\" style=\"width:100%;\" ng-model=\"models["+i+"].uni_cre.remark\" > </textarea></td>";
                }
                tr_html = tr_html + "</tr>"
                //console.log(tr_html);
                var contentTemplate = angular.element(tr_html);
                var contentElement = $compile(contentTemplate)($scope);
                console.log($scope.tabId)
                angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find('#uniteCeditTable').append(contentElement);
            }
        
        }
    }
    $scope.approve = function(form_data){
        approvalService.approve($scope.application_id, {'comment_type':'同意', 'comment':$scope.result})
        .success(function(resp){
            $scope.submitedFlag = true;
            $scope.next_step=resp.data.next_step;
            $("#tab_"+ $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");

        }); 
    }   
    $scope.reject = function(){
        approvalService.approve($scope.application_id, {'comment_type':'不同意', 'comment':$scope.result})
            .success(function(resp){
                $scope.submitedFlag = true;
                alert('提交成功'); 
            }); 
    
    };  
   if($scope.application_id){
       $scope.btn_save_flag = false;
       $scope.btn_create_flag = false;
       $scope.btn_flow_flag = false;
       $scope.approveActivityFlag = true;
       $scope.query_by_app($scope.application_id);
   }else{
        if($scope.uni_id){
            $scope.btn_save_flag = true;
             $scope.btn_create_flag = false;
             $scope.btn_flow_flag = true;
             $scope.query($scope.uni_id);
         }
         else{
            $scope.btn_save_flag = false;
             $scope.btn_create_flag = true;
             $scope.btn_flow_flag = false;
         }
   }
});

