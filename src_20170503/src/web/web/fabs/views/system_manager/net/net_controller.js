/**
 * Nets Controller
 */
//function netControler($scope,netService){
ysp.controller('sysNetController', ['$scope', '$rootScope', 'netService', function($scope, $rootScope,  netService){
    var load_nets = function () {
        netService.nets().success(function (reps) {
         $scope.nets = reps.data;
        });
    };
    $scope.search = function () {
        load_nets();
    };

    /** modal process **/
    var element_edit = angular.element('#edit_net_modal');
    var element_add = angular.element('#add_net_modal');


    $scope.add_save = function(){
        var tel=/^(0[0-9]{2,3}\-)?([2-9][0-9]{6,7})+(\-[0-9]{1,4})?$/; 
        if ($scope.add_net_id=="" || $scope.add_net_name==""|| $scope.add_net_address=="" || $scope.add_net_tel=="" ){alert("输入不能为空！");}
        else if(isNaN($scope.add_net_id)){alert("编号必须为数字！");}
        else if(!tel.test($scope.add_net_tel)){alert("电话格式不正确！");}
        else {  
               netService.net_add_save({'net_id':$scope.add_net_id,'net_name':$scope.add_net_name,'net_address':$scope.add_net_address,'net_tel':$scope.add_net_tel}).success(function(resp){
               alert(resp.data);
               element_add.modal('hide');
               load_nets();
           });
        }
    };
    $scope.edit_save = function(){
      var tel=/^(0[0-9]{2,3}\-)?([2-9][0-9]{6,7})+(\-[0-9]{1,4})?$/;
      if ($scope.edit_net_id=="" || $scope.edit_net_name==""|| $scope.edit_net_address=="" || $scope.edit_net_tel=="" ){alert("输入不能为空！");}
      else if(!tel.test($scope.edit_net_tel)){alert("电话格式不正确！");}
       
      else{ 
        netService.net_edit_save({'net_id':$scope.edit_net_id,'net_name':$scope.edit_net_name,'net_address':$scope.edit_net_address,'net_tel':$scope.edit_net_tel}).success(function(resp){
            alert(resp.data);
            element_edit.modal('hide');
            load_nets();
        });
      }
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

    $scope.to_edit = function(net){
        element_edit.modal('show');
        $scope.edit_net_id = net.net_id;
        $scope.edit_net_name = net.net_name;
        $scope.edit_net_address = net.net_address;
        $scope.edit_net_tel = net.net_tel;
    };
    $scope.add = function(){
        element_add.modal('show');
        $scope.add_net_id ="";
        $scope.add_net_name = "";
        $scope.add_net_address ="";
        $scope.add_net_tel = "";

    };
}]);



