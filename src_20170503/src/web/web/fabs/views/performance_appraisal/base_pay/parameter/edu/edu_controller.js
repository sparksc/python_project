/**
 * Edu Controller
 */
ysp.controller('eduController', function($scope, $rootScope,  eduAllowanceService){
    var load = function () {
		eduAllowanceService.edu_load().success(function (reps) {
			$scope.items = reps.data;
		});
    };
    $scope.search = function () {
        load();
    };

    /** modal process **/
    var element_edit = angular.element('#edu_edit_modal');
	$scope.hiddenid = {show:false};

    $scope.edit_save = function(){
		if ($scope.edit_edu=="" || $scope.edit_money==""){alert("输入不能为空！");}
		else{ 
			eduAllowanceService.edu_edit_save({'item_id':$scope.edit_item_id,'dxmc':$scope.edit_edu,'money':$scope.edit_money}).success(function(resp){
				alert(resp.data);
				element_edit.modal('hide');
				load();
			});
		};
    };
    $scope.to_edit = function(item){
		element_edit.modal('show');
		$scope.edit_edu = item.dxmc;
		$scope.edit_money = item.money;
		$scope.edit_item_id = item.item_id;
    };
});



