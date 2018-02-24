/**
 * DepSing Controller
 */
function DepCustController($scope, $rootScope, $attrs, $filter, SqsReportService,branchmanageService,gsgxckService,$rootScope,custHookMagService) {

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
        params['status'] = $scope.status;
        if (params.org){
            params.org_no = params.org.branch_code;
        }
        else{
            params.org_no = null;
        }
        if (params.manager){
            params.manager_no = params.manager.user_name;
        }
        else{
            params.manager_no = null;
        }
        params.manager_no = $rootScope.user_session.user_code;
        params.org_no = $rootScope.user_session.branch_code;
        params.typ = '存款'
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        SqsReportService.info('depCust', params).success(function(resp) {
            $scope.data = resp;
            $scope.data.header.push("详情");
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
   
    
    var element = angular.element('#custMoveModal');
    $scope.change = function(row) {
            $scope.row=row;
            $scope.move_id = row[9];
            $scope.move_percentage = row[5];
            element.modal('show');
            branchmanageService.branch({'org':$scope.row[0]}).success(function (reps) {
                $scope.top_id = reps.data[0].role_id; 
                $scope.find_users2();
                });
    };
    
    $scope.save = function(row) {
            movedata = {};
            movedata['type'] = '客户号分润';
            movedata['move_id'] = $scope.row[9];
            movedata['cust_no'] = $scope.row[4];
            movedata['percentage'] = $scope.move_percentage;
            movedata['from_teller'] = $scope.row[2];
            movedata['to_teller'] = $scope.to_staff.user_name;
            movedata['balance'] = $scope.row[6];
            movedata['org_no'] = $scope.row[0];
            movedata['date_id'] = moment().format('YYYYMMDD');
    
            custHookMagService.single_move_cust({'movedata':movedata}).success(function(reps){
                            alert(reps.data);
                            element.modal('hide');
                            $scope.search();
                            });
    }

};

DepCustController.$inject = ['$scope', '$rootScope', '$attrs', '$filter', 'SqsReportService','branchmanageService','gsgxckService','$rootScope','custHookMagService'];

angular.module('YSP').service('DepCustController', DepCustController);

