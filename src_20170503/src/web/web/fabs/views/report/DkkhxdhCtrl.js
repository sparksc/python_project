ysp.controller('dkkhxdhController',['$scope','$rootScope', '$filter', 'SqsReportService','dkkhxdhService','branchmanageService',function($scope,$rootScope, $filter, SqsReportService,dkkhxdhService,branchmanageService) {
    $scope.newdata={};
    $scope.updata={};
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.find_org = function(paradata){
        paradata.third_org_name='';
        for(i in $scope.model1)
            if($scope.model1[i].branch_code == paradata.third_org_code)paradata.third_org_name = $scope.model1[i].branch_name;
    };
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
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        SqsReportService.info('dkkhxdh', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    function init(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
             $scope.model1=reps.data;
        });
    };
    var addmodal = angular.element('#dkkhxdh_s_r_modal1');
    $scope.save = function(){
        addmodal.modal('show');
	$scope.newdata={};
    };
    $scope.do_save = function(newdata){
        dkkhxdhService.khh_save({'newdata':$scope.newdata}).success(function(resp){
            alert(resp.data);
            if(resp.data=='添加成功'){
                addmodal.modal('hide');
                do_search();
            }
        });
    };
    var modmodal = angular.element('#dkkhxdh_s_r_modal');
    $scope.update = function(row) {
        $scope.updata.id = row[5];
        $scope.updata.account_name = row[0];
	for(i in $scope.model1){
		if($scope.model1[i].branch_code == row[1]){
			$scope.updata.third_org_code = $scope.model1[i].branch_code;
			$scope.updata.third_org_name = $scope.model1[i].branch_name;
		}
	}
        $scope.updata.cust_seq = row[3];
        $scope.updata.cust_seq2 = row[4];
        modmodal.modal('show');
    };
    $scope.do_update = function(){
        dkkhxdhService.khh_update({'updata':$scope.updata}).success(function(resp){
            alert(resp.data);
                if(resp.data=='修改成功'){
                    modmodal.modal('hide');
                    do_search();
                }
        });
    };
    $scope.dele = function(row){
        if(confirm("确认要删除？")){
          dkkhxdhService.khh_delete({'delete_id':row[5]}).success(function(resp){
                alert(resp.data);
                do_search();
          });
        }    
     };
}]);




