/**
 * Phone Controller
 */
ysp.controller('PhoneController', function($scope, $rootScope,bankInputService,SqsReportService){

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
        bankInputService.branches().success(function(reps){
            $scope.branches =reps.data;
        });
    };
    $scope.branches();
    $scope.search = function() {
        $scope.tableMessage = "正在查询";
        params=$scope.cust_search;
        if(params.date instanceof moment){
            params.drrq = params.date.format('YYYY-MM-DD');
        }else {
            params.drrq = '';
        };
        if(params.branch!=null){
            params.jgbh = params.branch.branch_code;
        }else {
            params.jgbh = '';
        };
        SqsReportService.info('phoneinput', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            };
        });
    };
    $scope.types=["手机银行","e银行"];
    $scope.add_date = moment();
    $scope.edit_date = moment();
    var element_edit = angular.element('#phone_edit_modal');
    var element_add = angular.element('#phone_add_modal');
  
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


    $scope.type_change = function () {
		if($scope.add_type=="手机银行" || $scope.edit_type=="手机银行"){
			$scope.phone.show = true;
			$scope.e.show = false;
		}else{
			$scope.e.show = true;
			$scope.phone.show = false;
		}
    }
    $scope.add = function(){
        $scope.edit_type='';
    	element_add.modal('show');
		$scope.e={show:false};
		$scope.phone={show:false};
		$scope.add_user=''
		$scope.add_type=''
		$scope.add_e_dev=''
		$scope.add_e_act=''
		$scope.add_phone_dev=''
		$scope.add_phone_act=''
		bankInputService.branches().success(function (reps){
			$scope.branches = reps.data;
		});
    };
    $scope.add_save = function (){
	if(!(isNaN($scope.add_phone_dev))){
	 if(!(isNaN($scope.add_phone_act))){
	  if(!(isNaN($scope.add_e_dev))){
	    if(!(isNaN($scope.add_e_act))){
	      if ($scope.add_branch=="" || $scope.add_user==""||$scope.add_type=='' ){alert("输入不能为空！");}
	      else{
			element_add.modal('hide');
			add_date=$scope.add_date.format('YYYY-MM-DD');
			bankInputService.add_save({'drrq':add_date,'jgbh':$scope.add_branch.branch_code,'yggh':$scope.add_user.user_name,'ygxm':$scope.add_user.name,'sj_fzs':$scope.add_phone_dev,'sj_hys':$scope.add_phone_act,'eyh':$scope.add_e_dev,'eyhhy':$scope.add_e_act}).success(function (reps){
				alert(reps.data);
				$scope.search();
			});
	      };
	   }else{alert('发展数、活跃数必须为数字')};
	  }else{alert('发展数、活跃数必须为数字')};
	 }else{alert('发展数、活跃数必须为数字')};
	}else{alert('发展数、活跃数必须为数字')};
    };
    $scope.edit_save = function (){
		edit_date=$scope.edit_date.format('YYYY-MM-DD');
		bankInputService.edit_save({'item_id':$scope.item_id,'drrq':edit_date,'jgbh':$scope.edit_branch.branch_code,'yggh':$scope.edit_user.user_name,'ygxm':$scope.edit_user.name,'sj_fzs':$scope.edit_phone_dev,'sj_hys':$scope.edit_phone_act,'eyh':$scope.edit_e_dev,'eyhhy':$scope.edit_e_act}).success(function (reps){
			alert(reps.data);
			$scope.search();
	    	element_edit.modal('hide');
		});
    };

    $scope.edit = function(item){
    $scope.add_type='';
	element_edit.modal('show');
	$scope.idno={show:false};
	$scope.e={show:false};
	$scope.phone={show:false};
	bankInputService.branches().success(function (reps){
		bankInputService.branch_order({'branch_id':item[1]}).success(function (rep){
			i=rep.data;
			$scope.edit_branch = reps.data[i];
		});
		$scope.branches = reps.data;
	});
	bankInputService.persons({'branch_code':item[1]}).success(function(reps){
		bankInputService.person_order({'user_id':item[3],'branch_code':item[1]}).success(function (rep){
			num=rep.data;
			$scope.edit_user = reps.data[num];
		});
		$scope.persons =reps.data;
	});
	$scope.edit_type = '';
	$scope.edit_phone_dev = item[5];
	$scope.edit_phone_act = item[6];
	$scope.edit_e_dev = item[7];
	$scope.edit_e_act = item[8];
	$scope.item_id = item[9];

    };
    $scope.del = function(item){
	var r=confirm("确定删除？");
	if(r==true){
           bankInputService.del({'item_id':item[9]}).success(function(resp){
              alert(resp.data);
              $scope.search();
           });
        }
        else{alert("取消删除");}
    };

});




