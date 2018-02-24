ysp.controller('con_checkController', function($scope, $rootScope,  con_checkService, SqsReportService){
/**
 *  var load_con_checks = function () {
        con_checkService.con_checks({'id':$scope.id}).success(function (reps) {
            $scope.con_checks = reps.data;
       
         });
    };
    $scope.search = function () {
        console.log($scope.id)
        load_con_checks();
    };
**/


	$scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    $scope.tableMessage = "请点击查询";

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        $scope.tableMessage = "正在查询";
        params.contract_id = $scope.item[6];
        params.pei_freq = $scope.item[3];
        params.object_type = $scope.item[0];
        SqsReportService.info('con_check', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            };
        });
    };
    $scope.search();
})
