/**
 * MainMan Controller 客户号主办客户经理修改
 */
function MainManController($scope, $attrs, $filter, SqsReportService,branchmanageService,gsgxckService,$rootScope,custhkService) {
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
	    $("div[name='loading']").modal("show");
        params = $scope.cust_search;
        //params.org_no = $rootScope.user_session.branch_code;
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        console.log(params)
        SqsReportService.info('MainMan', params).success(function(resp) {
	    $("div[name='loading']").modal("hide");
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    $scope.find_users = function(){
        branchmanageService.users({'branch_id':$scope.cust_search.org.role_id}).success(function(reps){
        $scope.model2 =reps.data;
                });
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
    
    //更改主办客户经理按钮
    $scope.change = function(row){
        $scope.staff=null;
        $scope.cust_no = row[3];
        $scope.org_no = row[0];
        $scope.typ = row[2];
        custhkService.get_manlist({'cust_no':row[3],'org_no':row[0], 'typ':row[2]}).success(function(reps){
            $scope.manlist=reps.data;
        });
        $('#change_modal').modal("show");
    };

    $scope.save = function(){
        if($scope.staff==null){
            alert('主办客户经理不能为空');
        }
        custhkService.change_main({'cust_no':$scope.cust_no,'org_no':$scope.org_no,'staff_code':$scope.staff.user_name, 'typ':$scope.typ}).success(function(reps){
            alert(reps.data);
            $scope.search();
        });
        $('#change_modal').modal("hide");
    }
};

MainManController.$inject = ['$scope', '$attrs', '$filter', 'SqsReportService','branchmanageService','gsgxckService','$rootScope','custhkService'];

angular.module('YSP').service('MainManController', MainManController);

