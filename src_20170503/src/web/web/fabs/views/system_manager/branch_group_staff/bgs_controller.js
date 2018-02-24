/**
 * Branch Group User Controller
 */
ysp.controller('BgsController', function($scope, $rootScope, bgsService, SqsReportService ){

	$scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };


    $scope.branches = function(){
		bgsService.f_branches().success(function(reps){
			$scope.f_branches =reps.data;
        });
    };
    $scope.groups = function(){
		bgsService.groups().success(function(reps){
			$scope.groups =reps.data;
        });
    };
    $scope.branches();
	$scope.groups();
    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.sdate = moment();
    $scope.cust_search.edate = moment();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        params = $scope.cust_search;
		if(params.sdate instanceof moment){
        	params.startdate = params.sdate.format('YYYY-MM-DD');
		}else {
			params.startdate = '';
		};
		if(params.edate instanceof moment){
        	params.enddate = params.edate.format('YYYY-MM-DD');
		}else {
			params.enddate = '';
		};
		if(params.branch!=null){
			params.branch_name = params.branch.branch_name;
		}else {
			params.branch_name = '';
		};
		if(params.group!=null){
			params.group_name = params.group.group_name;
		}else {
			params.group_name = '';
		};
        SqsReportService.info('000103', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            };
        });
    };



    $scope.show_sbranch = function(){
		$scope.second = {show:true};
	};
    $scope.show_tbranch = function(){
		$scope.third = {show:true};
	};

	$scope.find_users = function(){
		bgsService.find_users({'branch_name':$scope.cust_search.branch_name.branch_name}).success(function(resp){
			$scope.users = resp.data;
		});
	};
    /** modal process **/
    var element_edit = angular.element('#bgu_edit_modal1');
    var element_add = angular.element('#bgu_add_modal1');
    $scope.startdate = moment();
	$scope.enddate = moment();

	$scope.add_save = function(){
	  if($scope.startdate instanceof moment){
		startdate=$scope.startdate.format('YYYY-MM-DD');
		bgsService.find_user({'user_id':$scope.add_user_id}).success(function(resp){
			num = resp.data;
			if(num==0){
				alert('员工编号不存在');
			}else if($scope.add_third_branch==null){
				alert('机构未选全');
			}else if($scope.add_group==null){
				alert('岗位未选择');
			}else{
				bgsService.add_save({'user_id':$scope.add_user_id,'startdate':startdate,'group_id':$scope.add_group.id,'branch_id':$scope.add_third_branch.role_id}).success(function(resp){
					num = resp.data;
					if(num == 1){
						alert('该用户正是该岗位');
					}else if (num == 4){
						alert('该用户不能更换机构（原机构还在任职）');
					}else {
						alert('添加成功');
						element_add.modal('hide');
						$scope.search();	
					};
				});
			};		
		});
	  }else{
		alert('开始时间未选择');
	  };
	};
	
	$scope.edit_save = function(){
		if($scope.enddate instanceof moment){
			enddate=$scope.enddate.format('YYYY-MM-DD');
			bgsService.edit_save({'enddate':enddate,'group_id':$scope.group_id}).success(function(resp){
				alert(resp.data);
				element_edit.modal('hide');
				$scope.search();	
			});
		}else{
			alert('结束时间不能为空');
		};
	};

    $scope.add = function(){
		$scope.second = {show:false};
		$scope.third = {show:false};
		element_add.modal('show');
    	$scope.startdate = moment();
		bgsService.f_branches().success(function(reps){
			$scope.f_branches =reps.data;
        }); 
		bgsService.groups().success(function(reps){
			$scope.groups =reps.data;
        }); 
		$scope.add_user_id= null;
		$scope.add_first_branch = null;
		$scope.add_second_branch = null;
		$scope.add_third_branch = null;
		$scope.add_group = null;
    };
		
    $scope.edit = function(item){
		element_edit.modal('show');
		$scope.enddate = moment();
		$scope.group_id = item[6];
      /*  //数据的回显
		bguService.f_branches().success(function(reps){
			$scope.f_branches =reps.data;
            var results = reps.data;
            for (var i=0;i<results.length;i++){
                if(results[i].branch_name==item[2]){
                    $scope.edit_third_branch=results[i];
					for(var i=0;i<results.length;i++){
						if(results[i].role_id==$scope.edit_third_branch.parent_id){
							$scope.edit_second_branch=results[i];
							for(var i=0;i<results.length;i++){
								if(results[i].role_id==$scope.edit_second_branch.parent_id){
									$scope.edit_first_branch=results[i];
								};
							};
						};
					};
                };
            };
        }); 
		bguService.groups().success(function(reps){
			$scope.groups =reps.data;
			var results = reps.data;
			for(var i=0;i<results.length;i++){
				if(results[i].group_name==item[3]){
					$scope.edit_group = results[i];
				};
			};
        });*/
		$scope.edit_user_id= item[0];
		$scope.edit_user_name = item[1];
    };
});




