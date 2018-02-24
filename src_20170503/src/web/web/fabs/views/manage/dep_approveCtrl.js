/**
 * dep_approve Controller
 * 存款审批
 */
function depaprvController($scope, $filter, SqsReportService,branchmanageService,accthkService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
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
        params = $scope.cust_search;
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        SqsReportService.info('dep_approve', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
        $scope.choseArr=[];
	//}
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
   
   //全选与单选功能，全选为当前页面,prkey声明主键
    $scope.choseArr=[];
    $scope.oneflag =false;
    $scope.master =false;
    var prkey = 0;
    $scope.selectall = function(master,data){
        if(master){
            $scope.onefalg =true;
            for(rowvalue in data){
                $scope.choseArr.push(data[rowvalue][prkey]);
            }
        }
        else{
            $scope.onefalg =false;
            $scope.choseArr =[];
        }
    };
    $scope.chkone = function(row,oneflag){
        var hasin = $scope.choseArr.indexOf(row[prkey]);
        if(oneflag&&hasin==-1){
            $scope.choseArr.push(row[prkey])
        }
        if(!oneflag&&hasin>-1){
            $scope.choseArr.pop(row[prkey])
        }
    };
    $scope.approve = function() {
        if($scope.choseArr.length == 0) 
        {
            alert('请先选择客户信息');
            return;
        }
        $scope.newdata = {};
        console.log('hello')
        console.log($scope.choseArr)
        accthkService.approve({'newdata':$scope.newdata,'update_key':$scope.choseArr}).success(function(resp){
            alert(resp.data);
	        $scope.search();
        });
    }
    $scope.deny = function() {
        if($scope.choseArr.length == 0) 
        {
            alert('请先选择客户信息');
            return;
        }
        $scope.newdata = {};
        console.log('hello')
        console.log($scope.choseArr)
        accthkService.deny({'newdata':$scope.newdata,'update_key':$scope.choseArr}).success(function(resp){
            alert(resp.data);
	        $scope.search();
        });
    }
};

depaprvController.$inject = ['$scope', '$filter', 'SqsReportService','branchmanageService','accthkService'];
angular.module('YSP').service('depaprvController', depaprvController);
