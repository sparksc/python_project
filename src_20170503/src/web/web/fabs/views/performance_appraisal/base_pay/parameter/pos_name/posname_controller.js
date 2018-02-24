/**
 * PosName Controller
 */
ysp.controller('posNameController', function($scope, $rootScope,  basicSalaryService){
    var load = function () {
		basicSalaryService.posname_load().success(function (reps) {
			$scope.items = reps.data;
		});
    };
    $scope.search = function () {
        load();
    };

    /** modal process **/
    var element_edit = angular.element('#posname_edit_modal');
	$scope.hiddenid = {show:false};

    $scope.edit_save = function(){
		if ($scope.edit_posname=="" || $scope.edit_money==""){alert("输入不能为空！");}
		else{ 
			basicSalaryService.posname_edit_save({'item_id':$scope.edit_item_id,'dxmc':$scope.edit_posname,'money':$scope.edit_money}).success(function(resp){
				alert(resp.data);
				element_edit.modal('hide');
				load();
			});
		};
    };
    $scope.del = function(net){
        var r=confirm("确定删除？");
        if(r==true){
           netService.net_del({'net_id':net.net_id}).success(function(resp){
              alert(resp.data);
              load_nets();
           });
        }
        else{alert("取消删除");}
    };

    $scope.to_edit = function(item){
		element_edit.modal('show');
		$scope.edit_posname = item.dxmc;
		$scope.edit_money = item.money;
		$scope.edit_item_id = item.item_id;
    };
});



