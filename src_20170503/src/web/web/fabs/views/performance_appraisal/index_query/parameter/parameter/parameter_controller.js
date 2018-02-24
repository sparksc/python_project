/**
 *  *  * Users Controller
 *   *   */

ysp.controller('parameterController', ['$scope', '$rootScope', 'parameterService', function($scope, $rootScope,  parameterService){
    var load_parameters = function () {
            parameterService.parameters({'code':$scope.search_code,'name':$scope.search_name}).success(function (reps) {
                $scope.parameters = reps.data;
            });
    };
    $scope.search = function () {
        load_parameters();
    };

    $scope.save = function(){
        if ($scope.modal_add_code==""){alert("交易代码不能为空！请重新输入！");}
        else if ($scope.modal_add_name==""){alert("交易名称不能为空！请重新输入！");}
        else if ($scope.modal_add_coef==""){alert("折合系数不能为空！请重新输入！");}
        else{
            parameterService.parameter_save({'add_code':$scope.modal_add_code,'add_name':$scope.modal_add_name,'add_coef':$scope.modal_add_coef}).success(function(resp){
                alert(resp.data);
                add_element.modal('hide');
                load_parameters();
                $scope.modal_add_code = ''
                $scope.modal_add_name = ''
                $scope.modal_add_coef = ''

        });
        }
    };
    $scope.to_delete = function(parameter){
      if(confirm("确认要删除？")){
        parameterService.parameter_delete({'delete_id':parameter.id}).success(function(resp){
            alert(resp.data);
            load_parameters();
        });
      }
    };

    $scope.to_edit = function(parameter){
        element.modal('show');
        $scope.modal_edit_id = parameter.id;
        $scope.modal_edit_code = parameter.gldxbh;
        $scope.modal_edit_name = parameter.dxmc;
        $scope.modal_edit_coef = parameter.je1;
        
    };

    $scope.edit_save = function(){
        if ($scope.modal_edit_id==""){alert("ID不能为空！请重新输入！");}
        else if ($scope.modal_edit_code==""){alert("交易代码不能为空！请重新输入！");}
        else if ($scope.modal_edit_name==""){alert("交易名称不能为空！请重新输入！");}
        else if ($scope.modal_edit_coef==""){alert("折合系数不能为空！请重新输入！");}
        else{
        parameterService.parameter_edit_save({'edit_id':$scope.modal_edit_id,'edit_code':$scope.modal_edit_code,'edit_name':$scope.modal_edit_name,'edit_coef':$scope.modal_edit_coef}).success(function(resp){
            alert(resp.data);
            element.modal('hide');
            load_parameters();
        });
       }
    };


    /** modal process **/
    var element = angular.element('#parameter_edit_modal');
    var add_element=angular.element('#parameter_add_modal');

    $scope.add=function(){
	    add_element.modal('show');
	}
  
}]);
