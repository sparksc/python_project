/**
 * conSet Controller
 * 实际上是conLook Controller
 */
//function perConControler($scope, perConService) {
ysp.controller('conSetController', function($scope, $rootScope,  perConService ,SqsReportService){
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
		params.contract_id = $scope.item[6];
		params.pei_freq = $scope.item[3];
		params.object_type = $scope.item[0];
        SqsReportService.info('peset', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            };
        });
    };

	$scope.search();
	$scope.add = function(item){
         perConService.add({'pe_pei_id':item[6],'contract_id':$scope.item[6]}).success(function(reps){
             alert(reps.data);
             $scope.search();
         })
    }
});




