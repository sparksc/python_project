/**
 * conLook Controller
 */
//function perConControler($scope, perConService) {
ysp.controller('conLookController', function($scope, $rootScope,  perConService, SqsReportService){

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
        SqsReportService.info('pelook', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            };
        });
    };
	$scope.search();
	
    var element = angular.element('#set_modal');
	$scope.target_id = '';
    $scope.set = function(target){
		$scope.target_id = target[8];
		$scope.weight_model=target[3];
		$scope.target_model=target[4];
        element.modal('show'); 
    }  

    $scope.save = function() {
         perConService.save({'target_id':$scope.target_id,'item_id':$scope.item[6],'item_weight':$scope.weight_model,'item_target':$scope.target_model}).success(function(reps){
            alert(reps.data)
            element.modal('hide');
            $scope.search();
         });

    };


});




