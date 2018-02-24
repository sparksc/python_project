/**
 * adjusttype Controller
 */
function adjusttypeController($scope,$rootScope, $filter, SqsReportService,adjusttypeService,branchmanageService,dictdataService) {
    
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

    init();
    function do_search(){
        
        params = $scope.cust_search;
        var i=0;
        for(i in $scope.adjustSa){
            console.log(i)
            if(params.adjustS==$scope.adjustSa[i].key){
                    params.adjustState = $scope.adjustSa[i].value;
                    break;
                }
            else
                params.adjustState = "";
        }
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        SqsReportService.info('paaa', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
   //初始化 
    function init(){
        dictdataService.get_dict({'dict_type':'tzzxlx'}).success(function (reps) {
                $scope.timestype=reps.data;
                    });
        dictdataService.get_dict({'dict_type':'ywlx'}).success(function (reps) {
                $scope.businesstype=reps.data;
                    });
        dictdataService.get_dict({'dict_type':'zt'}).success(function (reps) {

                $scope.adjustSa=reps.data;
                    });

        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
             $scope.branchs=reps.data;
         
        });
    };
    //
    var tankuang = angular.element('#add_modal_adjust');
        $scope.save = function(){
        $scope.newdata = {};
        tankuang.modal('show');
    };
    //保存
    $scope.do_save = function(){
        $scope.newdata.adjuststate = '录入';
        adjusttypeService.type_save({'newdata':$scope.newdata}).success(function(resp){
            alert(resp.data);
            if(resp.data=='添加成功'){
                tankuang.modal('hide');
                do_search();
            }
        });
    };
    //修改
    var xiugai = angular.element('#up_modal_adjusttypekey');
    $scope.updatatype = function(row) {
        $scope.updata = {};
        $scope.updata.id = row[6];
        $scope.updata.times = row[0];
        for(i in $scope.timestype){
            if($scope.timestype[i].value == row[1])
                $scope.updata.timestype = $scope.timestype[i].key;
        } 
        $scope.updata.institution = row[2];
        for(i in $scope.businesstype){
            if($scope.businesstype[i].value == row[3])
                $scope.updata.businesstype = $scope.businesstype[i].key;
        } 
        $scope.updata.adjustnum = row[4];
        $scope.updata.adjuststate = row[5];
        xiugai.modal('show');
    };
    $scope.do_update = function(){
        adjusttypeService.type_update({'updata':$scope.updata}).success(function(resp){
            alert(resp.data);
                if(resp.data=='修改成功'){
                    xiugai.modal('hide');
                    do_search();
                }
        });
    };
    //删除

    $scope.dele = function(row){
        if(confirm("确认要删除？")){
          adjusttypeService.type_delete({'delete_id':row[6]}).success(function(resp){
                alert(resp.data);
                do_search();
          });
        }    
     };

    
};

adjusttypeController.$inject = ['$scope','$rootScope', '$filter', 'SqsReportService','adjusttypeService','branchmanageService','dictdataService'];

angular.module('YSP').service('adjusttypeController', adjusttypeController);
