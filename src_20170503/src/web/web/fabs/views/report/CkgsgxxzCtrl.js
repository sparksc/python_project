/**
 * gxxz Controller
 */
function gxxzController($scope, $filter, SqsReportService,branchmanageService,gsgxckService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.e_p_OPEN_DATE = moment();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {

        params = $scope.cust_search;
	if(params.e_p_OPEN_DATE instanceof moment){
            params.p_p_OPEN_DATE = params.e_p_OPEN_DATE.format('YYYYMMDD');
	}
	else{
	    params.p_p_OPEN_DATE = "";
	    params.e_p_OPEN_DATE = "";
	}
	$scope.data = {};
	$scope.tableMessage = "正在查询";
        SqsReportService.info('000050', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    $scope.add_khrq = moment().format('YYYY-MM-DD');
    $scope.add_glqsrq = moment();
    $scope.add_gljsrq = moment();
    $scope.add = function(row) {
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
            $scope.model1=reps.data;
        element.modal('show');
	$scope.add_zhbh = row[2];
	$scope.add_zhxh = row[3];
	$scope.add_khh = row[6];
	$scope.add_gsbl = 100;
	$scope.add_glqsrq = moment();
	$scope.add_gljsrq = moment("2099-12-30","YYYY-MM-DD");
	$scope.add_khmc = row[4];
	$scope.add_cklx = $scope.model3[0];
	});	
    }
    $scope.save = function(){
        gsgxckService.add_save({'add_khrq':$scope.add_khrq,'add_jgbh':$scope.add_jgbh.branch_code,'add_zhbh':$scope.add_zhbh,'add_zhxh':$scope.add_zhxh,'add_ygh':$scope.add_ygh.user_name,'add_khh':$scope.add_khh,'add_gsbl':$scope.add_gsbl,'add_glqsrq':$scope.add_glqsrq.format('YYYY-MM-DD'),'add_gljsrq':$scope.add_gljsrq.format('YYYY-MM-DD'),'add_khmc':$scope.add_khmc,'add_cklx':$scope.add_cklx.key}).success(function(resp){
            alert(resp.data);
            element.modal('hide');
	    $scope.search();
        });
    };
    $scope.find_users = function(){
        branchmanageService.users({'branch_id':$scope.add_jgbh.role_id}).success(function(reps){
        $scope.model2 =reps.data;
//	console.log(reps.data)
                });
    }; 
    function find_branchs(){
	branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model4=reps.data;
	//console.log(reps.data);
	})	
    }
    find_branchs();   
    var element = angular.element('#add_modal_ckgsxz');
     scope.model3 = [{'key':'1','value':'自营存款'},{'key':'2','value':'分配存款'},{'key':'3','value':'特殊存款'}];
};

gxxzController.$inject = ['$scope', '$filter', 'SqsReportService','branchmanageService','gsgxckService'];

angular.module('YSP').service('gxxzController', gxxzController);
