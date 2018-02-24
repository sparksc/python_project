/**
 * staff status Controller
 */
function staff_statusController($scope, $filter, SqsReportService,staff_statusService,dictdataService) {
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
    
        SqsReportService.info('000039').success(function(resp) {
            $scope.data = resp;
	    if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    
    $scope.update = function(target) {
    var uptar=[];
    for(var p in target){
    uptar[p]=target[p];
    }
    for(i in $scope.dict_data){
        if($scope.dict_data[i].value == uptar[2])uptar[2]=$scope.dict_data[i].key;
    }
        staff_statusService.update_ws(uptar).success(function(resp){
            alert(resp.data);
        } );
    };
function find_dict(){
    dictdataService.get_dict({'dict_type':'WS'}).success(function (reps) {
            $scope.dict_data=reps.data;
             })
    }
    find_dict();

                                                    
    
};

staff_statusController.$inject = ['$scope', '$filter','SqsReportService','staff_statusService','dictdataService'];

angular.module('YSP').service('staff_statusController', staff_statusController);
