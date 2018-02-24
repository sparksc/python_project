/**
 * Jgzb Controller
 */
function JgzbController($scope, $filter, SqsReportService,branchmanageService) {
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
        if($scope.p_P_ORGID){
            params.t_jgbh = $scope.p_P_ORGID.branch_code;
        }
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        //params.p_P_DATE = params.e_p_P_DATE.format('YYYYMMDD');
        //delete params.e_p_P_DATE;
        console.log(params)
        //SqsReportService.info('orgtarget', params).success(function(resp) {
        SqsReportService.info('orgindex', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
            console.log($scope.data.header);
        });
    };
    $scope.search = function(){
        do_search();
    }
    function init(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function(reps){
            $scope.branchs=reps.data;
            do_search();
        });
    };
    init();
};

JgzbController.$inject = ['$scope', '$filter', 'SqsReportService','branchmanageService'];

angular.module('YSP').service('JgzbController', JgzbController);
