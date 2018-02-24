/**
 * SqsDemo Controller
 */
function branchmanageCtrl($scope, $filter,branchmanageService, SqsReportService,staff_statusService,poConService,bguService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
	
    };
    
    var old_gid;

    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
        });
    };
    find_branchs();    
    $scope.tableMessage = "请点击查询";
    $scope.groups = function(){
        poConService.groups().success(function(resp){
            $scope.groups =resp.data;
            
        });
    };
    $scope.groups();
    function get_group_type(){
        staff_statusService.get_group_department().success(function(reps){
            $scope.bb=reps.data;
            console.log($scope.bb)
        }); 
    };
    get_group_type();
    $scope.cust_search = {};
        $scope.onAction = function(conversation_id, action) {
            SqsReportService.action(conversation_id, action).success(function(resp) {
                $scope.data = resp;
            });
        };
        $scope.search = function() {
        
        $scope.params = $scope.cust_search;   
        
        SqsReportService.info('department', $scope.params).success(function(resp) {
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
            $scope.params2.x2 = $scope.add_date.x2.role_id;
            $scope.params2.x3 = $scope.add_date.x2.branch_code;
        }  else { 
            $scope.params2.x2=null
            $scope.params2.x3=null
        } 

        poConService.department_save({'add_date':$scope.params2}).success(function(resp){
                alert(resp.data);
                add_element.modal('hide');
        $scope.search();
        });
    };
    $scope.to_edit = function(row){
        element.modal('show');
        $scope.up_date={};
        $scope.up_date.x1 = row[0];
        $scope.up_date.x2 = row[4];
        $scope.up_date.x3 = row[3];
        $scope.up_date.x4 = row[3];
        $scope.up_date.x5 = row[4];
        old_gid=row[4];
    };
    $scope.edit_save= function(){
         $scope.up_date.x4 = old_gid;
         poConService.department_edit_save({'up_date':$scope.up_date}).success(function(resp){
            alert(resp.data);
            element.modal('hide');
        $scope.search();
        });
    };
    
    $scope.to_delete = function(row){
          if(confirm("确认要删除？")){
          poConService.department_delete({'delete_id':row[0]}).success(function(resp){
              alert(resp.data);
          $scope.search();            
          });
    } };


    /** modal process **/
    var element = angular.element('#branch_edit_modal');
    var add_element=angular.element('#branch_add_modal');
    $scope.add=function(){
         $scope.add_date={};
         add_element.modal('show');
        }

};
branchmanageCtrl.$inject = ['$scope', '$filter','branchmanageService', 'SqsReportService','staff_statusService','poConService','bguService'];

angular.module('YSP').service('branchmanageCtrol', branchmanageCtrl);
