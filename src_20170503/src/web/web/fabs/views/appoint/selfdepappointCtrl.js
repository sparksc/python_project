/**
 * SelfDepAppoint Controller
 */
function SelfDepAppointController($scope, $filter, SqsReportService,store,branchmanageService,depappointService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.d_date = moment();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    function do_search(){
        params = $scope.cust_search;
        if(params.d_date instanceof moment){
            params.yyrq = params.d_date.format('YYYY-MM-DD');
        }
        else{
            params.yyrq = '';
        }
	    params.yggh = store.getSession("user_name");   
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        SqsReportService.info('selfdepappoint', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    $scope.search = function() {
        do_search();
    }

    do_search();
};

SelfDepAppointController.$inject = ['$scope', '$filter', 'SqsReportService','store','branchmanageService','depappointService'];

angular.module('YSP').service('SelfDepAppointController', SelfDepAppointController);
