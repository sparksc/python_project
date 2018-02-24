/**
 * Khjlajjxxc Controller
 */
function KhjlajjxxcController($scope, $filter, SqsReportService,store,branchmanageService,depappointService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.tdate = moment();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        do_search();
    };
    init();
    function do_search(){
        params = $scope.cust_search;
        if(params.tdate instanceof moment){
            params.tjrq = params.tdate.format('YYYY-MM-DD');
        }
        else{
            params.tjrq = '';
        }
        params.jgbh = $scope.cust_search.jgbhh;
        params.yggh = $scope.cust_search.ygghh;
        $scope.data = {};

        $scope.tableMessage = "正在查询";

        SqsReportService.info('pmanagermpcheck', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };

    $scope.find_users = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.jgbhh){role_id=$scope.model1[i].role_id;}
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
        $scope.cust_search.ygghh = null;
    }
    function init(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
            $scope.model1=reps.data;
        });
    };

};

KhjlajjxxcController.$inject = ['$scope', '$filter','SqsReportService','store','branchmanageService','depappointService'];

angular.module('YSP').service('KhjlajjxxcController', KhjlajjxxcController);
