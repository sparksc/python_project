/**
 * Khjlbrajzb Controller
 */
function KhjlbrajzbController($scope, $filter, SqsReportService,store) {
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

        params = $scope.cust_search;

        if(params.tdate instanceof moment){
            params.tjrq = params.tdate.format('YYYY-MM-DD');
        }
        else{
            params.tjrq = '';
        }
        $scope.data = {};

        $scope.tableMessage = "正在查询";

	
        params.yggh = store.getSession("user_name");   
        
        SqsReportService.info('pselfmcheck', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };

};

KhjlbrajzbController.$inject = ['$scope', '$filter', 'SqsReportService','store'];

angular.module('YSP').service('KhjlbrajzbController', KhjlbrajzbController);
