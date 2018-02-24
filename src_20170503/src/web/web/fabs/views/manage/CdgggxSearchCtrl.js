/**
 * cdgggxsearch Controller
 */

function cdgggxsearchController($scope, $filter, $rootScope, SqsReportService,cdgggxService,dictdataService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.tableMessage1 = "请输入账号";
    $scope.cust_search = {};
   // $scope.cust_search.e_p_OPEN_DATE = moment();
    $scope.newstaffdata= {};
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        //console.log($rootScope.user_session)
        params = $scope.cust_search;
        //if (params.JGBH){
        //    params.JGBH = params.JGBH.branch_code;
        //}
        //if (params.GLDXBH){
        //    params.GLDXBH = params.GLDXBH.user_name;
        //}
        $scope.data = {};
        $scope.tableMessage = "正在查询";
            params.NO_CHECK_STATUS = 0;
        SqsReportService.info('cdgggxlr1', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };

    
    

    function find_dict(){
    dictdataService.get_dict({'dict_type':'CD_ST'}).success(function (reps) {
        $scope.cd_st=reps.data;
	});
    dictdataService.get_dict({'dict_type':'CD_CK_ST'}).success(function (reps) {
        $scope.cd_ck_st=reps.data;
	});	
    SqsReportService.info('000037',{'staff_code':$rootScope.user_session.user_code}).success(function(resp){
        $scope.user_cms_code = resp.rows[0][3];
    });
    }
    find_dict();

};

cdgggxsearchController.$inject = ['$scope', '$filter', '$rootScope', 'SqsReportService','cdgggxService','dictdataService'];

angular.module('YSP').service('cdgggxsearchController', cdgggxsearchController);
