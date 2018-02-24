/**
 * Zhgybranzb Controller
 *综合柜员本人按年考核指标
 */
function ZhgybranzbController($scope, $filter, SqsReportService,store) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.e_p_P_DATE = moment();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {

        params = $scope.cust_search;
        if(params.e_p_P_DATE instanceof moment){
            params.tjrq = params.e_p_P_DATE.format('YYYY-MM-DD');
        }
        else{
            params.tjrq = '';
        }
        $scope.data = {};
 
        $scope.tableMessage = "正在查询";
        params.yggh = store.getSession("user_name");
        SqsReportService.info('teller_self_y_check', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };

};


ZhgybranzbController.$inject = ['$scope', '$filter', 'SqsReportService','store'];

angular.module('YSP').service('ZhgybranzbController', ZhgybranzbController);
