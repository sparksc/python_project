/**
 * Newdepappoint Controller
 */
function NewdepappointController($scope, $filter, SqsReportService,store,branchmanageService,depappointService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    //$scope.cust_search.d_date = moment().subtract(1,'days');
    $scope.cust_search.d_date = moment();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    function do_search(){
        params = $scope.cust_search;
        if(params.d_date instanceof moment){
            params.yyrq = params.d_date.format('YYYYMMDD');
        }
        else{
            params.yyrq = '';
        }
	    params.yggh = store.getSession("user_name");   
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        SqsReportService.info('newdepappoint', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    $scope.search = function() {
        do_search();
    }

    do_search();
    
    var add_modal = angular.element('#add_newdepappoint');
    $scope.delay = 7;
    $scope.newdata = {};
    $scope.newdata.yyrq_dis = moment();
    $scope.newdata.yyblrq_dis = moment().add(1,'days');
    $scope.newdata.yyyxrq = moment().add($scope.delay,'days').format('YYYYMMDD');

    $scope.add = function(){
        add_modal.modal('show');

    	function find_branchs(){
    	    branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
    	    $scope.model1=reps.data;
    	    });
    	};
    	find_branchs();    
    };

    $scope.find_users = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.jgbh){role_id=$scope.model1[i].role_id;}
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
        $scope.cust_search.ygbh = null;
    }
    function check_insert(data){
        if(!(data.yyblrq_dis instanceof moment)){
            alert('请选择日期');
            return false;
        };
        if(!data.yybljg_dis){
            alert('请选择机构');
            return false;
        };
        if(!data.khmc){
            alert('请输入客户名称');
            return false;
        };
        if(!data.yyckje || isNaN(data.yyckje)){
            alert('存款金额必须输入，且为数字');
            return false;
        };
        
             return true;
    };
    $scope.do_save = function(){
        var xxx = check_insert($scope.newdata);
        if(!check_insert($scope.newdata)){
            return; 
        }
        depappointService.exist({'keydata':{'khmc':$scope.newdata.khmc,'yybljg':$scope.newdata.yybljg_dis.branch_code}}).success(function(reps){
             if(!reps.data){
                alert('有效期内在同一机构不允许预约同一客户');
             }
             else{
                $scope.newdata.yyrq = $scope.newdata.yyrq_dis.format('YYYYMMDD');
                $scope.newdata.yyblrq = $scope.newdata.yyblrq_dis.format('YYYYMMDD');
                $scope.newdata.ck_type ='1';
                $scope.newdata.yybljg =$scope.newdata.yybljg_dis.branch_code;
                $scope.newdata.bz ='1';
                //$scope.newdata.yyyxrq = moment().add(7,'days').format('YYYYMMDD');
                $scope.newdata.yggh = store.getSession('user_name');
                $scope.newdata.jgbh = store.getSession('branch_code');
                $scope.newdata.jgmc = store.getSession('branch_name');
                $scope.newdata.ygxm = store.getSession('name');
                $scope.newdata.typ = '存款';
		console.log($scope.newdata)
                depappointService.save({'newdata':$scope.newdata}).success(function(reps){
                    add_modal.modal('hide');
                    alert(reps.data);
                    do_search();
                });
             }
        });
    };

    $scope.delete = function(id){
      if(confirm("确认要删除？")){
        depappointService.delete({'id':id}).success(function(reps){
            alert(reps.data);
            do_search();
        });
      } 
    };
};

NewdepappointController.$inject = ['$scope', '$filter', 'SqsReportService','store','branchmanageService','depappointService'];

angular.module('YSP').service('NewdepappointController', NewdepappointController);
