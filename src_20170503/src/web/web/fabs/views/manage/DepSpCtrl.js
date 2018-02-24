/**
 * depsp Controller
 * 存款类录入审批(客户号录入及账号录入)
 */
function depspController($scope,$rootScope, $filter, SqsReportService,branchmanageService,accthkService,custhkService,gsgxckService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.type = '存款客户号录入';
    $scope.flag='cust';
    $scope.cust_search.login_branch_no = $rootScope.user_session.branch_code;
    $scope.cust_search.login_teller_no = $rootScope.user_session.user_code;
    $scope.checkedAllFlag = false;
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
            $scope.checkedAllFlag = false;
            $scope.parse_paginfo($scope.data.actions);
        });
    };

    $scope.onAction1 = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.detail_data = resp;
        });
    };

    $scope.parse_paginfo = function(actions){

        for (var i in actions){
            var action = actions[i];
            var act = action.action;
            var info = action.conversation_id;
            var pairs = info.split("&")
            for(var j in pairs){
                if (pairs[j].indexOf('total_count')!=-1){
                    $scope.total_count = pairs[j].split('=')[1];
                }
                if (pairs[j].indexOf('page')!=-1){
                    var page = pairs[j].split('=')[1];
                    if ( act === "previous"){
                        $scope.cur_page = parseInt(page) + 1;
                    }
                    if ( act === "next"){
                        $scope.cur_page = parseInt(page) - 1;
                    }
                }
            }

        }
    }
    $scope.search = function() {
        $("div[name='loading']").modal("show");
        if(!$scope.cust_search.type){
            alert('请选择审批类型!');
            return;
        }
        params = $scope.cust_search;
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        params.STATUS = '录入待审批'
        if($scope.cust_search.type=='存款客户号录入'){
            $scope.detail_flag = false;
            params.TYP='存款'
            SqsReportService.info('custsp',params).success(function(resp) {
            $("div[name='loading']").modal("hide");
                $scope.data = resp;
                if (($scope.data.rows || []).length > 0) {
                    $scope.parse_paginfo($scope.data.actions);
                    $scope.tableMessage = "";
                } else {
                    $scope.tableMessage = "未查询到数据";
                }
            });
        }
        if($scope.cust_search.type=='理财客户号录入'){
            $scope.detail_flag = false;
            params.TYP='理财'
            SqsReportService.info('custsp',params).success(function(resp) {
                $("div[name='loading']").modal("hide");
                $scope.data = resp;
                if (($scope.data.rows || []).length > 0) {
                    $scope.parse_paginfo($scope.data.actions);
                    $scope.tableMessage = "";
                } else {
                    $scope.tableMessage = "未查询到数据";
                }
            });
        }
        if($scope.cust_search.type=='存款账号录入'){
            $scope.flag='acct';
            $scope.detail_flag = true;
            params.TYP='存款'
            SqsReportService.info('acctsp',params).success(function(resp) {
                $("div[name='loading']").modal("hide");
                $scope.data = resp;
                if (($scope.data.rows || []).length > 0) {
                    $scope.parse_paginfo($scope.data.actions);
                    $scope.tableMessage = "";
                } else {
                    $scope.tableMessage = "未查询到数据";
                }
            });
        }
        if($scope.cust_search.type=='理财流水号录入'){
            $scope.flag='acct';
            $scope.detail_flag = true;
            params.TYP='理财'
            SqsReportService.info('acctsp',params).success(function(resp) {
                $("div[name='loading']").modal("hide");
                $scope.data = resp;
                if (($scope.data.rows || []).length > 0) {
                    $scope.parse_paginfo($scope.data.actions);
                    $scope.tableMessage = "";
                } else {
                    $scope.tableMessage = "未查询到数据";
                }
            });
        }
        if($scope.cust_search.type=='存款汇集户账号录入'){
            $scope.flag='parent';
            $scope.detail_flag = true;
            SqsReportService.info('parentsp',params).success(function(resp) {
                $("div[name='loading']").modal("hide");
                $scope.data = resp;
                if (($scope.data.rows || []).length > 0) {
                    $scope.parse_paginfo($scope.data.actions);
                    $scope.tableMessage = "";
                } else {
                    $scope.tableMessage = "未查询到数据";
                }
            });
        }


        $scope.choseArr=[];
    };
    $scope.detail = function(id){
        params ={'ORG':$scope.data.rows[id][2],'SALE_CODE':$scope.data.rows[id][4],'CUST_IN_NO':$scope.data.rows[id][13],'TYP':$scope.data.rows[id][10]}
        SqsReportService.info('acctsp_detail', params).success(function(resp) {
            $scope.detail_data = resp;
            $('#tab_'+ $scope.tabId + '_content').find("#depsp_detail_modal").modal("show");
            //if (($scope.detail_data.rows || []).length > 0) {
            //    $scope.tableMessage = "";
            //} else {
            //    $scope.tableMessage = "未查询到数据";
            //}

        });
    };
    $scope.find_users = function(){
        branchmanageService.users({'branch_id':$scope.cust_search.org.role_id}).success(function(reps){
            $scope.model2 =reps.data;
       });
    };
    $scope.find_users2 = function(){
        branchmanageService.users({'branch_id':$scope.add_org.role_id}).success(function(reps){
            $scope.model5 =reps.data;
       });
    };

    var element = angular.element('#custHookBatchMoveModal');
    function find_branchs(){
    branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
            $scope.model1=reps.data;
    })
    }
    find_branchs();
   
    $scope.choseArr = [];
    $scope.checked_row = function(row_id, rows){
          if($scope.choseArr.indexOf(row_id)==-1){
             $scope.choseArr.push(row_id);
          }else{
             $scope.choseArr.splice($scope.choseArr.indexOf(row_id), 1);
          }


          $scope.checkedAllFlag = true;
          angular.forEach(rows, function(item){
               if($scope.choseArr.indexOf(item[0])==-1){
                  $scope.checkedAllFlag = false;
              }
          });
    }
    $scope.isChecked = function(row_id){
         return $scope.choseArr.indexOf(row_id) != -1; 
    }
    $scope.checkedAll = function(checkedFlag, rows){
         angular.forEach(rows, function(item){
             if(checkedFlag){
                 if($scope.choseArr.indexOf(item[0])==-1){
                    $scope.choseArr.push(item[0]);
                 }
             }else{
                 $scope.choseArr.splice($scope.choseArr.indexOf(item[0]), 1);
             }
         });
    }
    $scope.approve = function() {
        $scope.newdata = {};

        if($scope.flag=='acct'){
            accthkService.approve({'update_key':$scope.choseArr,'start_date':moment().format('YYYYMMDD')}).success(function(resp){
                $scope.search();
                $scope.checkedAllFlag = false;
                alert(resp.data); 
                add_element.modal('hide');
            });
        }else if($scope.flag=='cust'){
            custhkService.approve({'update_key':$scope.choseArr,'start_date':moment().format('YYYYMMDD')}).success(function(resp){
                $scope.search();
                alert(resp.data); 
                $scope.checkedAllFlag = false;
                add_element.modal('hide');
            });
        }else{
            accthkService.parent_approve({'update_key':$scope.choseArr,'start_date':moment().format('YYYYMMDD')}).success(function(resp){
                $scope.search();
                alert(resp.data); 
                $scope.checkedAllFlag = false;
                add_element.modal('hide');
            });
        }
    }
    $scope.deny = function() {
        $scope.newdata = {};

        if($scope.flag=='acct'){
            accthkService.deny({'update_key':$scope.choseArr}).success(function(resp){
                alert(resp.data); 
                add_element.modal('hide');
                $scope.search();
                $scope.checkedAllFlag = false;
            });
        }else if($scope.flag=='cust'){
            custhkService.deny({'update_key':$scope.choseArr}).success(function(resp){
                $scope.search();
                $scope.checkedAllFlag = false;
                alert(resp.data); 
                add_element.modal('hide');
            });
        }else{
            accthkService.parent_deny({'update_key':$scope.choseArr}).success(function(resp){
                $scope.search();
                alert(resp.data); 
                $scope.checkedAllFlag = false;
                add_element.modal('hide');
            });
        }
    }
    var add_element=angular.element('#depsp_modal');
    $scope.get=function(){
        if($scope.choseArr.length == 0) 
        {
            alert('请先选择审批信息');
            return;
        }
        $scope.reason="";
        add_element.modal('show');
    }
    $scope.switch_f = function(){

        if($scope.cust_search.type=='存款客户号录入' || $scope.cust_search.type=='理财客户号录入'){
            $scope.flag='cust';
        }else if($scope.cust_search.type=='存款账号录入' || $scope.cust_search.type=='理财流水号录入'){ 
            $scope.flag='acct';
        }else{
            $scope.flag='parent';
        }
    }
};

depspController.$inject = ['$scope','$rootScope', '$filter', 'SqsReportService','branchmanageService','accthkService','custhkService','gsgxckService'];
angular.module('YSP').service('depspController', depspController);
