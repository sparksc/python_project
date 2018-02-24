/**
 * DepaSwc Controller
 */
function DepaSwcController($scope, $attrs, $filter, SqsReportService,branchmanageService,gsgxckService,$rootScope,accthkService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.login_branch_no = $rootScope.user_session.branch_code;
    $scope.cust_search.login_teller_no = $rootScope.user_session.user_code;

    $scope.checkedAllFlag = false;
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.checkedAllFlag = false;
            $scope.data = resp;
            $scope.parse_paginfo($scope.data.actions);
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
        params = $scope.cust_search;
        params.typ = '存款'
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        SqsReportService.info('depswi', params).success(function(resp) {
	    $("div[name='loading']").modal("hide");
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
	//}
    };
    $scope.find_users2 = function(){
            branchmanageService.users({'branch_id':$scope.top_id}).success(function(reps){
                    $scope.model5 =reps.data;
            });
    };

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
               if($scope.choseArr.indexOf(item[10])==-1){
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
                 if($scope.choseArr.indexOf(item[10])==-1){
                    $scope.choseArr.push(item[10]);
                 }
             }else{
                 $scope.choseArr.splice($scope.choseArr.indexOf(item[10]), 1);
             }
         });
    }
    var element =angular.element(document.getElementById($scope.subTabId)).find('#move_DepaPreMove1');

    $scope.switch_pri = function(){
        if($scope.choseArr.length == 0) 
        {
               alert('请先选择账户信息');
               return;
        }
        if(! window.confirm('是否执行此操作')){
            return ;
        }
 
        accthkService.switch_pri({'update_key':$scope.choseArr}).success(function(reps){
            alert(reps.data);
            $scope.search();
            $scope.checkedAllFlag = false;
            $scope.choseArr =[];
        });
    }
};

DepaSwcController.$inject = ['$scope', '$attrs', '$filter', 'SqsReportService','branchmanageService','gsgxckService','$rootScope','accthkService'];

angular.module('YSP').service('DepaSwcController', DepaSwcController);

