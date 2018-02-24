/**
 * pagemain Controller
 */
function pagemainController($scope, $filter, SqsReportService, permissionService) {
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
        params = {};
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!='')params[key]=$scope.cust_search[key]
        }
            //console.log(params);
            //console.log('22222222222222222222222')
        SqsReportService.info('allmenu',params).success(function(resp) {
            $scope.data = resp;
            //console.log('------------------------')
            //console.log(resp)
	    if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    $scope.to_edit = function(row) {
    $scope.target ={};
    $scope.target.id = row[0];
    $scope.target.pagename = row[1];
    $scope.target.url = row[2];
    $scope.target.parentid = row[3];
	$('#myModal_p').modal('show');
    };
    $scope.menuupdate = function(target) {//target表示待编辑的那行数据
        var new_data = {'newdata':target};
        console.log(target)
        //new_data['newdata']=target;//把list对象放到key为newdata的字典里
        console.log(new_data)
	    permissionService.menu_update(new_data).success(function(resp) {
            alert(resp.data);//resp是个object对象，对象的属性data，成功更新这条记录就返回data值更新成功。
            $scope.search();
            $('#myModal_p').modal('hide');
        });                
    };
    $scope.add = function(){
        $scope.ntarget = {};
        var modal = $('#s_r_modal_p');
        modal.modal('show');
    };
    $scope.menusave = function(ntarget){
         console.log(ntarget)
	permissionService.menu_save(ntarget).success(function(resp) {
         alert(resp.data);
         $('#s_r_modal_p').modal('hide');
         $scope.search();
        });                
    };
};

pagemainController.$inject = ['$scope', '$filter', 'SqsReportService', 'permissionService'];

angular.module('YSP').service('pagemainController', pagemainController);
