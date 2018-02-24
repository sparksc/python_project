/**
 * tparatype Controller
 */
function tparatypeController($scope,$rootScope, $filter, SqsReportService,tparaService,permissionService) {
    
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
        SqsReportService.info('paratype', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    //查询功能

    //添加参数
    var element = angular.element('#add_modal_type');
    $scope.save = function() {
        $scope.newdata = {};
        element.modal('show');
    };
    $scope.do_save = function(){
        $scope.newdata.type_status = "启用";
        tparaService.type_save({'newdata':$scope.newdata}).success(function(resp){
            alert(resp.data);
            if(resp.data=='添加成功'){
                element.modal('hide');
	            do_search();
            }
        });
    };
    //修改参数
    var upelement = angular.element('#up_modal_type');
    $scope.update = function(row) {
        $scope.updata = {};
        $scope.updata.id = row[perkey];
        $scope.updata.type_module = row[0];
        $scope.updata.type_name = row[1];
        $scope.updata.type_detail = row[3];
        upelement.modal('show');
    };
    $scope.do_update = function(){
        tparaService.type_update({'updata':$scope.updata}).success(function(resp){
            alert(resp.data);
            if(resp.data=='修改成功'){
                upelement.modal('hide');
	            do_search();
            }
        });
    };

    //修改状态
    var perkey = 5;
    $scope.change_status = function(row){
        var updata = {}
        if(row[perkey-1]=='启用')
            updata.type_status ='禁用'
        else
            updata.type_status ='启用'
        updata.id = row[perkey]
        tparaService.type_update({'updata':updata}).success(function(resp){
            alert(resp.data);
            if(resp.data=='修改成功'){
	            do_search();
            }
        });

    };
   $scope.add_header = function(row){
        $rootScope.forward(row[0]+row[1]+"_属性配置",'views/tpara/tparaheader.html',{'para_type_id':row[perkey]}); 
   };

   $scope.add_para = function(row){
        $rootScope.forward(row[0]+row[1]+'_详情','views/tpara/tparadetail.html',{'para_type_id':row[perkey]}); 
   };
    
   
   $scope.add_menu = function(row){
      if(confirm("确认加入菜单？")){
        var menudata = {}
        menudata.parent_menu =row[0];
        menudata.url = 'views/tpara/tparadetail.html?para_type_id='+row[perkey];
        menudata.name = row[1];
        permissionService.para_menu_save({'menudata':menudata}).success(function(resp){
            alert(resp.data)
        });
      }
   };

};

tparatypeController.$inject = ['$scope','$rootScope', '$filter', 'SqsReportService','tparaService','permissionService'];

angular.module('YSP').service('tparatypeController', tparatypeController);
