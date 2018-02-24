/**
 * Ygbrajjxxc Controller
 */
function YgbrajjxxcController($scope, $filter, SqsReportService,store) {
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
    function do_search(){
        params = $scope.cust_search;
        if(params.e_p_P_DATE instanceof moment){
            params.t_tjrq = params.e_p_P_DATE.format('YYYYMMDD');
        }
        else{
            params.t_tjrq = '';
        }
        $scope.data = {};
        $scope.tableMessage = "正在查询";
	    params.t_yggh = store.getSession("user_name");
        console.log(params)
        SqsReportService.info('empselfquarterly', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    $scope.search = function(){
        do_search();
    }
};

YgbrajjxxcController.$inject = ['$scope', '$filter', 'SqsReportService','store'];

angular.module('YSP').service('YgbrajjxxcController', YgbrajjxxcController);
