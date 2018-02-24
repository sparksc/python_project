/**
 * Ygbranjxxc Controller
 */
function YgbranjxxcController($scope, $filter, SqsReportService,store,branchmanageService) {
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

    function do_search() {
        params = $scope.cust_search;
        if(params.e_p_P_DATE instanceof moment){
            params.t_tjrq = params.e_p_P_DATE.format('YYYYMMDD');
        }
        else{
            params.t_tjrq = '';
        }
        /*if($scope.p_P_ORGID){
            params.t_jgbh = $scope.p_P_ORGID.branch_code;
        }
        if($scope.p_P_SALEID){
            params.t_yggh = $scope.p_P_SALEID;
        }*/
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        //params.p_P_DATE = params.e_p_P_DATE.format('YYYYMMDD');
	    params.t_yggh = store.getSession("user_name");
        console.log(params)
        SqsReportService.info('empselfannual', params).success(function(resp) {
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
    /*function init(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function(reps){
            $scope.branchs=reps.data;
            do_search();
        });
    };
    init();
    */
};

YgbranjxxcController.$inject = ['$scope', '$filter', 'SqsReportService','store','branchmanageService'];

angular.module('YSP').service('YgbranjxxcController', YgbranjxxcController);
