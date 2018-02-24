/**
 * CustomerDetailInfo Controller
 */
function CustomerDetailInfoController($scope, $filter, ReportInfoService) {
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
        ReportInfoService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.searchCustomer = function() {

        params = $scope.cust_search;
        params.p_P_DATE = params.e_p_P_DATE.format('YYYYMMDD');
        ReportInfoService.info('客户详细信息', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };

};

CustomerDetailInfoController.$inject = ['$scope', '$filter', 'ReportInfoService'];

angular.module('YSP').service('CustomerDetailInfoController', CustomerDetailInfoController);