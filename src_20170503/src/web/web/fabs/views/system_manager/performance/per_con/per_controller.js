/**
 * Perormance Controller
 */
//function perConControler($scope, perConService) {
ysp.controller('perConController', function($scope, $rootScope,  perConService ,SqsReportService){
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.objects = function(){
          perConService.objects().success(function(reps){
          $scope.objects =reps.data;
         }) 
    };
    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.pe_date = moment();
	$scope.objects();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
    	$scope.tableMessage = "正在查询";
        params = $scope.cust_search;
        if(params.pe_date instanceof moment){
            params.date = params.pe_date.format('YYYY-MM-DD');
        }else {
            params.date = '';
        };
        if(params.branch!=null){
            params.pe_object = params.branch.branch_code;
        }else {
            params.pe_object = '';
        };
        SqsReportService.info('pecontract', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            };
        });
    };

    $scope.find_persons = function(){
          perConService.persons({'branch_code':$scope.add_object.branch_code}).success(function(reps){
          $scope.persons =reps.data;
         }) 
    };
    $scope.edit_persons = function(){
          perConService.persons({'branch_code':$scope.edit_object.branch_code}).success(function(reps){
          $scope.persons =reps.data;
         }) 
    };
    $scope.times=['年','季','月']; 
	$scope.type_change = function(){
		if($scope.add_time=='年'){
			$scope.whens = ['本年','下年'];
		}else if($scope.add_time=='季'){
			$scope.whens = ['本季','下季'];
		}else{
			$scope.whens = ['本月','下月']
		};
	};
	
    var element_edit = angular.element('#per_edit_modal');
    var element_add = angular.element('#per_add_modal');

  
    $scope.add_save = function(){
		if($scope.add_time=='年'){
			if($scope.when=='本年'){
				date = moment().endOf('year');
			}else{
				date = moment().add(1,'y').endOf('year');
			};
		}else if($scope.add_time=='季'){
			if($scope.when=='本季'){
				date = moment().endOf('quarter');
			}else{
				date = moment().add(1,'q').endOf('quarter');
			};
		}else{
			if($scope.when=='本月'){
				date = moment().endOf('month');
			}else{
				date = moment().add(1,'m').endOf('month');
			};
		};
		item_date = date.format('YYYY-MM-DD');
		perConService.add_save({'item_type':'机构','item_object':$scope.add_object.branch_code,'item_person':$scope.add_person.role_id,'item_time':$scope.add_time,'item_date':item_date}).success(function(resp){
			alert(resp.data);
			element_add.modal('hide');
			$scope.search();
		});
    };
    $scope.edit_save = function(){
        perConService.edit_save({'item_id':$scope.edit_id,'item_type':'机构','item_object':$scope.edit_object.branch_code,'item_person':$scope.edit_person.role_id,'item_time':$scope.edit_time}).success(function(resp){
            alert(resp.data);
            element_edit.modal('hide');
            $scope.search();
        });
      
    };
    $scope.del = function(item){
        var r=confirm("确定删除？");
        if(r==true){
           perConService.del({'item_id':item[6]}).success(function(resp){
              alert(resp.data);
              $scope.search();
           });
        }
        else{alert("取消删除");}
    };

    $scope.edit = function(item){
		$scope.edit_object="";
		$scope.edit_person="";
		perConService.objects().success(function (reps){
			$scope.objects= reps.data;
            var results = reps.data;
            for (var i=0;i<results.length;i++){
                if(results[i].branch_name==item[1]){
                    $scope.edit_object=results[i];
                    break;
                };
            };
        });
        perConService.persons({'branch_name':item[1]}).success(function(reps){
            $scope.persons =reps.data;
            var results = reps.data;
            for (var i=0;i<results.length;i++){
                if(results[i].name==item[2]){
                    $scope.edit_person=results[i];
                    break;
                };
            };
        });
		$scope.edit_id=item[6];
		$scope.edit_type = item[0];
		$scope.edit_time = item[3];
        element_edit.modal('show');
    };
    $scope.add = function(){
        element_add.modal('show');
        $scope.add_object = "";
        $scope.add_person ="";
        $scope.add_time = "";

    };
    $scope.con_set = function(item){
		name = item[1];
        $scope.forward('合约查看-'+name,'views/system_manager/performance/con_set/index.html',{'item':item});
    }
    $scope.con_look = function(item){
		name = item[1]
        $scope.forward('合约设定-'+name,'views/system_manager/performance/con_look/index.html',{'item':item});
    }
});




