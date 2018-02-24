/**
 *数据权限
 */
function groupdataCtrl($scope, $filter, SqsReportService, permissionService,dictdataService,postmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.element_add = angular.element('#groupdata');
    
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    }; 

    //查找岗位序列
    $scope.search_post='';
    $scope.find_posts= function(){
        if ($scope.search_post_name!=null){
            $scope.search_post=$scope.search_post_name;
        }
        postmanageService.posts({'search_post':$scope.search_post}).success(function (reps) {
            $scope.post_model=reps.data;
            var post_list=[];
            var post_object=$scope.post_model;
            for(option in post_object){
                var post = post_object[option];
                var post_name = post['post_name']
                post_list.push(post_name);
            }
/*
            $('#post_search').typeahead({
                source:post_list,
                matcher:function(item){
                    return true;
                }
            });
*/
        });
    };

    $scope.find_posts();
    //sqs查询
    $scope.search = function() {
        $scope.params = {};
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''){
                $scope.params[key]=$scope.cust_search[key]
            }
        }
        $scope.tableMessage = "正在查询";
        $scope.data = {};
        SqsReportService.info('groupdata',$scope.params).success(function(resp) {
            $scope.data = resp;
	    if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    function get_dict(){
        $scope.dictdata={};
        dictdataService.get_dicts({'l_dict_type':['data_type','auth_type']}).success(function (resp){
           $scope.dictdata=resp.data;
           $scope.authdata=$scope.dictdata.auth_type;
           $scope.edata=$scope.dictdata.data_type;
        });
    };
    get_dict();

    //新增
    $scope.add = function(){
        $scope.element_add.modal('show');
        $scope.add_date={};
        $scope.ishow=false;
        $scope.titlestr="添加";
        $scope.func_submit = $scope.add_save;
    };
    $scope.add_save = function (){
        permissionService.groupdata_save({'add_date':$scope.add_date}).success(function (resp){
            alert(resp.data);
            $scope.search();
            $scope.element_add.modal('hide');
        }); 
    };

    //修改
    $scope.to_edit = function(item){
        $scope.element_add.modal('show');
        $scope.ishow=true;
        $scope.titlestr="修改";
        $scope.func_submit = $scope.edit_save;
        $scope.add_date={};
        $scope.add_date.id=item[0];
        for (var r in $scope.post_model){
            if (item[2]==$scope.post_model[r].post_name){
                $scope.add_date.group_id=$scope.post_model[r].post_id
            }
        };
        $scope.add_date.data_type=$scope.dictdata.data_type.v2k[item[3]];
        $scope.add_date.auth_type=$scope.dictdata.auth_type.v2k[item[4]];
    };

    $scope.edit_save = function (){
        var updata=$scope.add_date;
        permissionService.groupdata_edit({'up_date':updata}).success(function (resp){
            alert(resp.data);
            $scope.search();
            $scope.element_add.modal('hide');
        });
    };

    //删除
    $scope.to_delete = function(item){
        var r=confirm("确定删除？");
        if (r==true){
            permissionService.groupdata_delete({'id':item[0]}).success(function (resp){
                alert(resp.data);
                $scope.search();
            });
        }
        else{alert("取消删除");}
    };
};



groupdataCtrl.$inject = ['$scope', '$filter', 'SqsReportService', 'permissionService','dictdataService','postmanageService'];

angular.module('YSP').service('groupdataCtrl', groupdataCtrl);
