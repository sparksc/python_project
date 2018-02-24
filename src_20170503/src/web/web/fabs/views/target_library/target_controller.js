/**
 *  *  * Users Controller
 *   *   */

ysp.controller('targetController', function($scope, $rootScope,  targetService, SqsReportService){
    
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    $scope.tableMessage = "请点击查询";

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        $scope.tableMessage = "正在查询";
		params=$scope.cust_search;
        SqsReportService.info('targetlib', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            };
        });
    };
    $scope.search();

	/**
	var load_targets = function () {
        targetService.targets({'name':$scope.search_name}).success(function (reps) {
            $scope.targets = reps.data;
        });
    };
    $scope.search = function () {
        load_targets();
    };**/

    $scope.model = ['年','季'];
    $scope.model1 = ['定性','定量'];
    $scope.model2 = ['机构','员工','岗位'];
    $scope.save = function(){
            targetService.target_save({'add_freq':$scope.modal_add_freq,'add_type':$scope.modal_add_type,'add_name':$scope.modal_add_name,'add_objtype':$scope.modal_add_objtype,'add_desc':$scope.modal_add_desc,'add_src':$scope.modal_add_src}).success(function(resp){
                alert(resp.data);
                add_element.modal('hide');
                $scope.search();
                $scope.modal_add_freq = ''
                $scope.modal_add_type = ''
                $scope.modal_add_name = ''
                $scope.modal_add_objtype = ''
                $scope.modal_add_desc = ''
                $scope.modal_add_src = ''

        });
    };
    $scope.to_delete = function(target){
      if(confirm("确认要删除？")){
        targetService.target_delete({'delete_id':target[6]}).success(function(resp){
            alert(resp.data);
            $scope.search();
        });
      }
    };
    
    $scope.to_edit = function(target){
        element.modal('show');
        $scope.modal_edit_id = target[6]; 
        $scope.modal_edit_freq = target[0];
        $scope.modal_edit_type = target[1];
        $scope.modal_edit_name = target[2];
        $scope.modal_edit_objtype = target[3];
        $scope.modal_edit_desc = target[4];
        $scope.modal_edit_src = target[5];
        
    };

    $scope.edit_save = function(){
        targetService.target_edit_save({'edit_id':$scope.modal_edit_id,'edit_freq':$scope.modal_edit_freq,'edit_type':$scope.modal_edit_type,'edit_name':$scope.modal_edit_name,'edit_objtype':$scope.modal_edit_objtype,'edit_desc':$scope.modal_edit_desc,'edit_src':$scope.modal_edit_src}).success(function(resp){
            alert(resp.data);
            element.modal('hide');
            $scope.search();
        });
    };


    /** modal process **/
    var element = angular.element('#equip_edit_modal');
    var add_element=angular.element('#seim_add_modal');

    $scope.add=function(){
	    add_element.modal('show');
	}
  
});
