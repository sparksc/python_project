/**
 * Branch Group User Controller
 */
ysp.controller('BguController', function($scope, $rootScope, bguService, SqsReportService ){

	$scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };


    $scope.branches = function(){
		bguService.f_branches().success(function(reps){
			$scope.f_branches =reps.data;
        });
    };
    $scope.groups = function(){
		bguService.groups().success(function(reps){
			$scope.groups =reps.data;
        });
    };
    $scope.branches();
	$scope.groups();
    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.sdate = moment().subtract(1,'years');
    $scope.cust_search.edate = moment("3000-12-31");

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        params = $scope.cust_search;
        $scope.tableMessage = "正在查询";
        /*
		if(params.sdate instanceof moment){
        	params.start_date = params.sdate.format('YYYYMMDD');
		}else {
			params.start_date = '0';
		};
		if(params.edate instanceof moment){
        	params.end_date = params.edate.format('YYYYMMDD');
		}else {
			params.end_date = '30001231';
		};*/
		if(params.user_name!=null){
			params.sale_code = params.user_name;
		}else {
			params.sale_code = '';
		};
        SqsReportService.info('bgu', params).success(function(resp) {
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
		bguService.find_users({'branch_name':$scope.cust_search.branch_name.branch_name}).success(function(resp){
			$scope.users = resp.data;
		});
    };
    /** modal process **/
    var element_edit = angular.element('#bgu_edit_modal');
    var element_add = angular.element('#bgu_add_modal');
    $scope.startdate = moment();
	$scope.enddate = moment();

	$scope.add_save = function(){
	  if($scope.startdate instanceof moment){
		startdate=$scope.startdate.format('YYYY-MM-DD');
        enddate=$scope.enddate.format('YYYY-MM-DD');
		bguService.find_user({'user_id':$scope.add_user_id}).success(function(resp){
			console.log($scope.add_first_branch)
            num = resp.data;
			if(num==0){
				alert('员工编号不存在');
			}else if($scope.add_group==null){
				alert('岗位未选择');
			}else{
                console.log($scope.add_user_id,startdate,enddate,$scope.add_group.id,$scope.add_first_branch.role_id)
				bguService.add_save({'user_id':$scope.add_user_id,'startdate':startdate,'enddate':enddate,'group_id':$scope.add_group.id,'branch_id':$scope.add_first_branch.role_id}).success(function(resp){
					num = resp.data;
                    console.log(resp.data)
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
			bguService.edit_save({'enddate':enddate,'group_id':$scope.group_id}).success(function(resp){
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
        $scope.enddate = moment("3000-12-31");
		bguService.f_branches().success(function(reps){
			$scope.f_branches =reps.data;
        }); 
		bguService.groups().success(function(reps){
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
		$scope.edit_user_id= item[0];
		$scope.edit_user_name = item[1];
    };
});




