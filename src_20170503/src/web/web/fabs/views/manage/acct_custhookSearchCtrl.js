/**
 *  Dkgggx  Controller
 */
function acct_custhookSearchController($scope, $filter, SqsReportService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.add_start_date=moment();
    $scope.add_end_date=moment();
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/accthk1?export=1";

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        $("div[name='loading']").modal("show");
        params = $scope.cust_search;
        if (params.ORG_NO){
            params.ORG_NO = params.ORG_NO.branch_code;
        }
        else{
            params.ORG_NO = null;
        }
        if (params.MANAGER_NO){
            params.MANAGER_NO = params.MANAGER_NO.user_name;
        }
        else{
            params.MANAGER_NO = null;
        }
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        params['HOOK_TYPE']='存贷挂钩';
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/acctcusthk1?export=1";
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
                params[key]=$scope.cust_search[key];
                $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }

        SqsReportService.info('acctcusthk1', params).success(function(resp) {
            $("div[name='loading']").modal("hide");
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    
    $scope.find_users = function(){
        branchmanageService.users({'branch_id':$scope.cust_search.ORG_NO.role_id}).success(function(reps){
            $scope.model2 =reps.data;
       });
    };
    $scope.find_users2 = function(){
        branchmanageService.users({'branch_id':$scope.add_ORG_NO.role_id}).success(function(reps){
            $scope.model5 =reps.data;
        });
    };

    var element = angular.element('#accounthookSearchModal');
    function find_branchs(){
	    branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
            $scope.model1=reps.data;
	    })
    }
    find_branchs();
};

acct_custhookSearchController.$inject = ['$scope', '$filter', 'SqsReportService','branchmanageService'];

angular.module('YSP').service('acct_custhookSearchController', acct_custhookSearchController);
