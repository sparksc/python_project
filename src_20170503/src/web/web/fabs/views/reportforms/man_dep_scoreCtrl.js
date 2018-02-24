/**
 * Manager_ebank Controller
 */
function mandepscoreController($scope, $filter, SqsReportService, permissionService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "点击查询";
    $scope.cust_search = {};
    $scope.cust_search.S_DATE=moment();
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
        });
    };
    find_branchs();    
    $scope.find_users = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.BRANCH_CODE){role_id=$scope.model1[i].role_id;}
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
        $scope.cust_search.SALE_CODE = null;
    }

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.parse_paginfo($scope.data.actions);
            $scope.data = resp;
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
        params = {};
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/man_dep_sco?export=1a";
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            if(key=='S_DATE')
                params['S_DATE']=params['S_DATE'].format("YYYYMMDD");
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        SqsReportService.info('man_dep_sco',params).success(function(resp) {
            $scope.data = resp;
         console.log(resp)
	    if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查到数据";
            }
        });
    }

    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/man_dep_sco?export=1a"+"&S_DATE="+moment().format('YYYYMMDD');
};

mandepscoreController.$inject = ['$scope', '$filter', 'SqsReportService', 'permissionService','branchmanageService'];

angular.module('YSP').service('OrgebankController', OrgebankController); 
