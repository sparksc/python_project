/**
 *  *  * Users Controller
 *   *   */

ysp.controller('branchmanageController', ['$scope', '$rootScope', 'branchmanageService', function($scope, $rootScope,  branchmanageService){
    var load_branchs = function () {
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
            $scope.branchs = reps.data;
        });
    };
    $scope.search = function () {
        load_branchs();
    };
    $scope.model1 = ['定性','定量']
    $scope.model2 = ['','是','否']	
    $scope.save = function(){
       /* if ($scope.modal_add_id==""){alert("行政村编号不能为空！请重新输入！");}
        else if ($scope.modal_add_name==""){alert("行政村名称不能为空！请重新输入！");}
        else if ($scope.modal_add_type==""){alert("设备类型不能为空！请重新输入！");}
        else if ($scope.modal_add_department==""){alert("所属商户不能为空！请重新输入！");}
        else if ($scope.modal_add_address==""){alert("设备地址不能为空！请重新输入！");}
        else if ($scope.modal_add_phone==""){ alert("联系电话不能为空！请重新输入！");
            if ($scope.modal_add_phone!==""){
            var pn=$scope.modal_add_phone;
	    var mobile = /^1[3|5|8]\d{9}$/ , phone = /^0\d{2,3}-?\d{7,8}$/;
	    if (mobile.test(pn) || phone.test(pn)){
               return
	    }else{
	        alert("输入联系电话格式不正确，请重新输入！");
	    }    
	    }
	}
        else{
            console.log("111111111");*/
	if ($scope.modal_add_parentid){
            branchmanageService.branch_save({'add_code':$scope.modal_add_code,'add_name':$scope.modal_add_name,'add_totalname':$scope.modal_add_totalname,'add_isloan':$scope.modal_add_isloan,'add_parentid':$scope.modal_add_parentid.role_id}).success(function(resp){
                alert(resp.data);
                add_element.modal('hide');
                load_branchs();
                $scope.modal_add_code = ''
                $scope.modal_add_name = ''
                $scope.modal_add_totalname = ''
                $scope.modal_add_isloan = ''
                $scope.modal_add_parentid = ''
	});
	}
	else{
            branchmanageService.branch_save({'add_code':$scope.modal_add_code,'add_name':$scope.modal_add_name,'add_totalname':$scope.modal_add_totalname,'add_isloan':$scope.modal_add_isloan}).success(function(resp){
                alert(resp.data);
                add_element.modal('hide');
                load_branchs();
                $scope.modal_add_code = ''
                $scope.modal_add_name = ''
                $scope.modal_add_totalname = ''
                $scope.modal_add_isloan = ''
                $scope.modal_add_parentid = ''
	    
        });
	}
       /* }*/
    };
    $scope.to_delete = function(branch){
      if(confirm("确认要删除？")){
        branchmanageService.branch_delete({'delete_id':branch.role_id}).success(function(resp){
            alert(resp.data);
            load_branchs();
        });
      }
    };
    
    $scope.to_edit = function(branch){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
            $scope.model3=reps.data;
	if (branch.parent_id !==null){
        branchmanageService.ords({'pid':branch.parent_id}).success(function (rep) {
        console.log(rep.data);
	i=rep.data;	
        element.modal('show');
        $scope.modal_edit_id = branch.role_id; 
        $scope.modal_edit_code = branch.branch_code;
        $scope.modal_edit_name = branch.branch_name;
        $scope.modal_edit_totalname = branch.branch_totalname;
        $scope.modal_edit_isloan = branch.is_loan_branch;
        $scope.modal_edit_parentid = reps.data[i];
	});
	}else{
        element.modal('show');
        $scope.modal_edit_id = branch.role_id; 
        $scope.modal_edit_code = branch.branch_code;
        $scope.modal_edit_name = branch.branch_name;
        $scope.modal_edit_totalname = branch.branch_totalname;
        $scope.modal_edit_isloan = branch.is_loan_branch;
       // $scope.modal_edit_parentid = reps.data[0];
	}
        });
    };
    $scope.to_check = function(branch){
	if (branch.parent_id !==null){
        branchmanageService.check_branchs({'name':branch.parent_id}).success(function (reps) {
             p_branch=reps.data;
        
       // console.log(branch.parent_id);
       // console.log(p_branch);
        check_element.modal('show');
        $scope.modal_check_id = branch.role_id;
        $scope.modal_check_code = branch.branch_code;
        $scope.modal_check_name = branch.branch_name;
        $scope.modal_check_totalname = branch.branch_totalname;
        $scope.modal_check_isloan = branch.is_loan_branch;
        $scope.modal_check_parentid = branch.parent_id;
        $scope.modal_check_parentcode = p_branch[0].branch_code;
        $scope.modal_check_parentname = p_branch[0].branch_name;
        $scope.modal_check_parenttotalname = p_branch[0].branch_totalname;
        $scope.modal_check_parentisloan = p_branch[0].is_loan_branch;
	});
	}else{
        check_element.modal('show');
        $scope.modal_check_id = branch.role_id;
        $scope.modal_check_code = branch.branch_code;
        $scope.modal_check_name = branch.branch_name;
        $scope.modal_check_totalname = branch.branch_totalname;
        $scope.modal_check_isloan = branch.is_loan_branch;	    
	}
    };

    $scope.edit_save = function(){
      /*  if ($scope.modal_edit_id==""){alert("行政村编号不能为空！请重新输入！");}
        else if ($scope.modal_edit_name==""){alert("行政村名称不能为空！请重新输入！");}
        else if ($scope.modal_edit_type==""){alert("设备类型不能为空！请重新输入！");}
        else if ($scope.modal_edit_department==""){alert("所属商户不能为空！请重新输入！");}
        else if ($scope.modal_edit_address==""){alert("设备地址不能为空！请重新输入！");}
        else if ($scope.modal_edit_phone==""){ alert("联系电话不能为空！请重新输入！");
            if ($scope.modal_edit_phone!==""){
            var epn=$scope.modal_edit_phone;
            var mobile = /^1[3|5|8]\d{9}$/ , phone = /^0\d{2,3}-?\d{7,8}$/;
            if (mobile.test(epn) || phone.test(epn)){
               return
            }else{
                alert("输入联系电话格式不正确，请重新输入！");
            }
            }
        }
        else{*/
	if ($scope.modal_edit_parentid)
        branchmanageService.branch_edit_save({'edit_id':$scope.modal_edit_id,'edit_code':$scope.modal_edit_code,'edit_name':$scope.modal_edit_name,'edit_totalname':$scope.modal_edit_totalname,'edit_isloan':$scope.modal_edit_isloan,'edit_parentid':$scope.modal_edit_parentid.role_id}).success(function(resp){
            alert(resp.data);
            element.modal('hide');
            load_branchs();
        });
      /* }*/
    };


    /** modal process **/
    var element = angular.element('#branch_edit_modal');
    var add_element=angular.element('#branch_add_modal');
    var check_element=angular.element('#branch_check_modal');
    $scope.add=function(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
	    $scope.model=reps.data;
        });	    
	 add_element.modal('show');
	}
  
}]);
