/**
 * EBank Controller
 */
ysp.controller('EBankController', function($scope, $rootScope,bankInputService,SqsReportService){
    var load = function () {
//		bankInputService.e_load().success(function (reps) {
//		$scope.items = reps.data;
//   	     });
//  
        params=$scope.cust_search;
        params.DRRQ = "";
        if($scope.cust_search.e_p_P_DATE instanceof moment)
        params.DRRQ = $scope.cust_search.e_p_P_DATE.format("YYYY-MM-DD");
    SqsReportService.info('ebank', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });

    };

    $scope.add_wh_date = moment();
    $scope.add_kh_date = moment();
    $scope.edit_date = moment();
    $scope.cust_search = {};
    $scope.cust_search.e_p_P_DATE = moment();
    var element_edit = angular.element('#ebank_edit_modal');
    var element_add = angular.element('#ebank_add_modal');
  

    $scope.search = function () {
        load();
    };


    $scope.add_persons = function(){
		bankInputService.persons({'branch_code':$scope.add_branch.branch_code}).success(function(reps){
		$scope.persons =reps.data;
		});
		$scope.add_user='';
    };
    $scope.edit_persons = function(){
		bankInputService.persons({'branch_code':$scope.edit_branch.branch_code}).success(function(reps){
		$scope.persons =reps.data;
		});
    };


    $scope.add = function(){
    	element_add.modal('show');
		$scope.add_user=''
		$scope.add_branch=''
		$scope.add_object_id=''
		$scope.add_object_name=''
		bankInputService.branches().success(function (reps){
			$scope.branches = reps.data;
		});
    };
    $scope.add_save = function (){
	if ($scope.add_object_id=="" || $scope.add_object_name==""|| $scope.add_branch=="" || $scope.add_user=="" ){alert("输入不能为空！");}
	else{
		element_add.modal('hide');
		wh_date=$scope.add_wh_date.format('YYYY-MM-DD');
		kh_date=$scope.add_kh_date.format('YYYY-MM-DD');
		bankInputService.e_add_save({'drrq':wh_date,'jgbh':$scope.add_branch.branch_code,'yggh':$scope.add_user.user_name,'ygxm':$scope.add_user.name,'dxbh':$scope.add_object_id,'dxmc':$scope.add_object_name,'clrq':kh_date}).success(function (reps){
			alert(reps.data);
			load();
		});
	};
    };
    $scope.edit_save = function (){
		element_edit.modal('hide');
		edit_date=$scope.edit_date.format('YYYY-MM-DD');
		bankInputService.e_edit_save({'item_id':$scope.item_id,'drrq':edit_date,'jgbh':$scope.edit_branch.branch_code,'yggh':$scope.edit_user.user_name,'ygxm':$scope.edit_user.name,'dxbh':$scope.edit_object_id,'dxmc':$scope.edit_object_name}).success(function (reps){
			alert(reps.data);
			load();
		});
    };

    $scope.edit = function(item){
		element_edit.modal('show');
		$scope.idno={show:false};
		bankInputService.branches().success(function (reps){
			$scope.branches = reps.data;
			var results = reps.data;
			for (var i=0;i<results.length;i++){
				if(results[i].branch_code==item[1]){
					$scope.edit_branch=results[i];
					break;
				};
			};
		});
		bankInputService.persons({'branch_code':item[1]}).success(function(reps){
			$scope.persons =reps.data;
			var results = reps.data;
			for (var i=0;i<results.length;i++){
				if(results[i].user_name==item[5]){
					$scope.edit_user=results[i];
					break;
				};
			};
        });
	$scope.edit_object_name = item[3];
	$scope.edit_object_id = item[2];
	$scope.item_id = item[7];

    };
    $scope.del = function(item){
		var r=confirm("确定删除？");
		if(r==true){
           bankInputService.del({'item_id':item[7]}).success(function(resp){
              alert(resp.data);
              load();
           });
        }
        else{alert("取消删除");}
    };

});




