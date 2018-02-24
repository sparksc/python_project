/**
 * tparatype Controller
 
*/
function reportmagController($scope,$rootScope, $filter, SqsReportService,reportmagService,permissionService) {
    //查询功能
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };
    $scope.search = function() {
        do_search();
    };
   function do_search(){ 
        params = $scope.cust_search;
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        SqsReportService.info('reportmag', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    //查询功能
    $scope.search();
    //添加参数
    var elementadd = angular.element('#add_reportmag');
    $scope.save = function() {
        $scope.newdata = {};
        elementadd.modal('show');
    };
    $scope.do_save = function(){
        reportmagService.type_save({'newdata':$scope.newdata}).success(function(resp){
            alert(resp.data);
            if(resp.data=='添加成功'){
                elementadd.modal('hide');
	            $scope.search();
            }
        });
    };
    //修改参数
    var upelement = angular.element('#up_reportmag');
    $scope.update = function(row) {
        $scope.updata = {};
        console.log(row)
        $scope.updata.id = row[2];
        $scope.updata.report_name = row[0];
        $scope.updata.report_script = row[1];
        upelement.modal('show');
    };
    $scope.do_update = function(){
        reportmagService.type_update({'updata':$scope.updata}).success(function(resp){
            alert(resp.data);
            if(resp.data=='修改成功'){
                upelement.modal('hide');
	            $scope.search();
            }
        });
    };

   $scope.add_para = function(row){
        $rootScope.forward(row[0]+row[1]+'_详情','views/tpara/tparadetail.html',{'reportmag_id':row[2]}); 
   };
    
   
   $scope.add_menu = function(row){
      if(confirm("确认加入菜单？")){
        $scope.menudata = {};
        $scope.menudata.location = 'views/tpara/tparadetail.html?reportmag_id='+row[2];
        $scope.menudata.name = row[0];
        reportmagService.menu_save({'menudata':$scope.menudata}).success(function(resp){
            alert(resp.data)
        });
      }
   };

};

reportmagController.$inject = ['$scope','$rootScope', '$filter', 'SqsReportService','reportmagService','permissionService'];

angular.module('YSP').service('reportmagController', reportmagController);
