/**
 * Yganjxxc Controller
 */
function YganjxxcController($scope, $filter, SqsReportService,branchmanageService) {
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
    var params = {};
    $scope.find_users = function(target){
        //if(!target.jgbh){target.yggh =null;}
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.jgbh){role_id=$scope.model1[i].role_id;}
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
        $scope.cust_search.yggh = null;
    }
    function do_search() {
        params = $scope.cust_search;
        if(params.e_p_P_DATE instanceof moment){
            params.t_tjrq = params.e_p_P_DATE.format('YYYYMMDD');
        }
        else{
            params.t_tjrq = '';
	    }
        if($scope.cust_search.jgbh){
            params.t_jgbh = $scope.cust_search.jgbh;
        }
        else{
            params.t_jgbh = ''; 
        } 
        if($scope.cust_search.yggh){
            params.t_yggh = $scope.cust_search.yggh;
        }
        else{
            params.t_yggh = '';
        }
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        console.log(params)
        SqsReportService.info('empannualsalary', params).success(function(resp) {
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
    function init(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function(reps){
            $scope.model1=reps.data;
            do_search();
        });
    };
    init();
};

YganjxxcController.$inject = ['$scope', '$filter', 'SqsReportService','branchmanageService'];

angular.module('YSP').service('YganjxxcController', YganjxxcController);
