/**
 * 员工岗位维护 Controller
 */
function XtengCtrl($scope, $filter, SqsReportService,poConService,bguService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
	
    };

    $scope.tableMessage = "请点击查询";
    $scope.groups = function(){
        poConService.groups().success(function(resp){
            $scope.groups =resp.data;
            
        });
    };
    $scope.groups();
    $scope.cust_search = {};
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };
    $scope.search = function() {
    $scope.params = {};   
    $scope.params.group_name = $scope.cust_search.group_name;
    if($scope.cust_search.type_name){
        $scope.params.type_name = $scope.cust_search.type_name.type_name;
    }
    
    SqsReportService.info('station_edit', $scope.params).success(function(resp) {
    $scope.data = resp;
    if (($scope.data.rows || []).length > 0) {
    $scope.tableMessage = "";
    } else {
    $scope.tableMessage = "未查询到数据";
    }
    });
    };

    $scope.save = function(){
        $scope.params2 = {};  
        if($scope.add_date.x1){
            $scope.params2.x1 = $scope.add_date.x1;
        } else { $scope.params2.x1=null}  
        if($scope.add_date.x2){
            $scope.params2.x2 = $scope.add_date.x2.type_name;
            $scope.params2.x3 = $scope.add_date.x2.type_code;
        }  else { 
            $scope.params2.x2=null
            $scope.params2.x3=null
        } 
        poConService.group_save({'add_date':$scope.params2}).success(function(resp){
                alert(resp.data);
                add_element.modal('hide');
                    search();
        });
        $scope.search();
    };
    $scope.type_save = function(){
        poConService.type_add({'type_code':$scope.type_code,'type_name':$scope.type_name}).success(function(resp){
                alert(resp.data);
                type_add_element.modal('hide');
                $scope.search();
        });
    };
    $scope.to_edit = function(row){
        element.modal('show');
        $scope.up_date={};
        $scope.up_date.x1 = row[0];
        $scope.up_date.x2 = row[1];
        $scope.up_date.x3 = row[2];
        $scope.update.x3 = row[2];
        $scope.up_date.x4 = row[3];
        $scope.up_date.x5 = row[4];
    };
    $scope.edit_save= function(){
        console.log($scope.up_date)
        console.log($scope.groups)
        console.log($scope.updatex3)
         
        if($scope.updatex3){
            $scope.up_date.x3 = $scope.updatex3.type_name;
        }  else {
            $scope.up_date.x3=null
        } 
        poConService.group_edit_save({'up_date':$scope.up_date}).success(function(resp){
            alert(resp.data);
            element.modal('hide');
            $scope.search();
        });
        $scope.search();
    };
    
    $scope.to_delete = function(row){
          if(confirm("确认要删除？")){
          poConService.group_delete({'delete_id':row[0]}).success(function(resp){
              alert(resp.data);
              $scope.search();            
          });
    } };


    /** modal process **/
    var element = angular.element('#group_edit_modal');
    var add_element=angular.element('#group_add_modal');
    var type_add_element=angular.element('#group_type_add_modal');
    var check_element=angular.element('#group_check_modal');
    $scope.add=function(){
         $scope.add_date={};
         add_element.modal('show');
        }
    $scope.type_add=function(){
         $scope.type={};
         type_add_element.modal('show');
        }

};
XtengCtrl.$inject = ['$scope', '$filter', 'SqsReportService','poConService','bguService'];

angular.module('YSP').service('XtengCtrol', XtengCtrl);
