/**
 * Hand Input Controller
 */
ysp.controller('HandController', function($scope, $rootScope,  handInputService,SqsReportService){
  
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.date = moment();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };
    $scope.branches = function(){
        handInputService.branches().success(function(reps){
            $scope.branches =reps.data;
        });
    };
    $scope.branches();
    $scope.search = function() {
        $scope.tableMessage = "正在查询";
        params=$scope.cust_search;
        if(params.date instanceof moment){
            params.drrq = params.date.format('YYYYMMDD');
        }else {
            params.drrq = '';
        };
        if(params.branch!=null){
            params.jgbh = params.branch.branch_code;
        }else {
            params.jgbh = '';
        };
        SqsReportService.info('handinput', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            };
        });
    };
/**
    var load = function () {
	handInputService.load().success(function (reps) {
	$scope.items = reps.data;
        });
    };
**/ 
    var element_edit = angular.element('#hand_edit_modal');
    var element_add = angular.element('#hand_add_modal');

    $scope.add_date = moment();
    $scope.edit_date = moment();

    $scope.add = function(){
        element_add.modal('show');
    	$scope.add_branch = '';
    	$scope.add_rate = '';
    	handInputService.branches().success(function (reps){
	    	$scope.branches = reps.data;
    	});
    };
    $scope.add_save = function (){
        if ($scope.add_branch=="" || $scope.add_rate=="" ){alert("输入不能为空！");}
        else if (isNaN($scope.add_rate)){alert("替代率必须位数字！");}
        else if (0>$scope.add_rate||$scope.add_rate>1){alert("替代率要在0和1之间");}
        else{
	    	element_add.modal('hide');
	    	add_date=$scope.add_date.format('YYYYMMDD');
	    	handInputService.add_save({'drrq':add_date,'jgbh':$scope.add_branch.branch_code,'jytdl':$scope.add_rate}).success(function (reps){
		    	alert(reps.data);
		    	$scope.search();
	    	});
    	};
    };

    $scope.del = function(item){
    	var r=confirm("确定删除？");
    	if(r==true){
           handInputService.del({'item_id':item.item[4]}).success(function(resp){
              alert(resp.data);
              $scope.search();
           });
        }
        else{alert("取消删除");}
    };

    $scope.edit = function(item){
		element_edit.modal('show');
		handInputService.branches().success(function (reps){
			$scope.branches = reps.data;
			var results = reps.data;
            for (var i=0;i<results.length;i++){
                if(results[i].branch_code==item[1]){
                    $scope.edit_branch=results[i];
                    break;
                };
            };
		});
	$scope.edit_rate = item[3];
	$scope.edit_id = item[4];
	
    };
    $scope.edit_save = function (){
        if ($scope.edit_branch=="" || $scope.edit_rate=="" ){alert("输入不能为空！");}
        else if (isNaN($scope.edit_rate)){alert("替代率必须位数字！");}
        else if (0>$scope.edit_rate||$scope.edit_rate>1){alert("替代率要在0和1之间");}
        else{
	    	edit_date=$scope.edit_date.format('YYYYMMDD');
	    	handInputService.edit_save({'item_id':$scope.edit_id,'drrq':edit_date,'jgbh':$scope.edit_branch.branch_code,'jytdl':$scope.edit_rate}).success(function (reps){
	        	alert(reps.data);
	        	$scope.search();
	        	element_edit.modal('hide');    
            });
        };
    };
});




