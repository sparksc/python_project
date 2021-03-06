/**
 * SqsDemo Controller
 */
function SqsDemoController($scope, $filter, SqsReportService) {
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
        params.p_P_DATE = params.e_p_P_DATE.format('YYYYMMDD');
        SqsReportService.info('100001', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };

};

SqsDemoController.$inject = ['$scope', '$filter', 'SqsReportService'];

angular.module('YSP').service('SqsDemoController', SqsDemoController);
