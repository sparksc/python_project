/**
 * tparaheader Controller
 */
function tparaheaderController($scope, $filter, SqsReportService,tparaService) {
    $scope.upmodel_id = "upmodel_header_Ctl"+$scope.para_type_id;
    $scope.addmodel_id = "addmodel_header_Ctl"+$scope.para_type_id;
    
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
        params.para_type_id =$scope.para_type_id;
        SqsReportService.info('paraheader', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未添加参数属性，请添加";
            }
        });
    };
    do_search();
    //查询功能

    //添加参数
    $scope.typelist =['smallint','int','bigint','decimal','varchar','date','datetime','time']
    $scope.save = function() {
        var element = angular.element('#'+$scope.addmodel_id);
        $scope.newdata = {};
        element.modal('show');
    };
    $scope.do_save = function(){
        var element = angular.element('#'+$scope.addmodel_id);
        $scope.newdata.header_status = "启用";
        $scope.newdata.para_type_id = $scope.para_type_id;
        tparaService.header_save({'newdata':$scope.newdata}).success(function(resp){
            alert(resp.data);
            if(resp.data=='添加成功'){
                element.modal('hide');
	            do_search();
            }
        });
    };

    //操作
    var perkey = 6;
    $scope.change_status = function(row){
        var updata = {}
        if(row[perkey-1]=='启用')
            updata.header_status ='禁用'
        else
            updata.header_status ='启用'
        updata.id = row[perkey]
        tparaService.header_update({'updata':updata}).success(function(resp){
            alert(resp.data);
            if(resp.data=='修改成功'){
	            do_search();
            }
        });
    };

    $scope.update = function(row) {
        var upelement = angular.element('#'+$scope.upmodel_id);
        $scope.updata = {};
        $scope.updata.header_name = row[0] 
        $scope.updata.header_type = row[2]
        $scope.updata.header_order = row[4]
        $scope.updata.header_detail = row[3] 
        $scope.updata.header_status = row[5]
        $scope.updata.id = row[6]
        upelement.modal('show');
    };
    $scope.do_update = function(){
        var upelement = angular.element('#'+$scope.upmodel_id);
        $scope.updata.para_type_id = $scope.para_type_id;
        tparaService.header_update({'updata':$scope.updata}).success(function(resp){
            alert(resp.data);
            if(resp.data=='修改成功'){
                upelement.modal('hide');
	            do_search();
            }
        });
    };

};

tparaheaderController.$inject = ['$scope', '$filter', 'SqsReportService','tparaService'];

angular.module('YSP').service('tparaheaderController', tparaheaderController);
