/**
 * gxxz Controller
 */
function dkgxxzController($scope, $filter, SqsReportService,branchmanageService,dkgsgxxzService,staffrelationService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
   // $scope.cust_search.e_p_OPEN_DATE = moment();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {

        params = $scope.cust_search;
	    if (params.e_p_THIRD_ORG_CODE){
            params.p_p_THIRD_ORG_CODE = params.e_p_THIRD_ORG_CODE.branch_code;
	    }
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        SqsReportService.info('000051', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    $scope.add_drrq = moment().format('YYYY-MM-DD');
    $scope.add_glqsrq = moment();
    $scope.add_gljsrq = moment();
    $scope.add = function(row) {
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
            $scope.model1=reps.data;
            element.modal('show');
	        $scope.add_zh = row[3];
            $scope.add_zhxh = row[4];
            $scope.model2 =[];
	        $scope.add_khh = row[2];
	        $scope.add_gsbl = 100;
	        $scope.add_glqsrq = moment();
	        $scope.add_gljsrq = moment("2099-12-30","YYYY-MM-DD");
	        $scope.add_khmc = row[1];
	});	
    }
    $scope.save = function(){
       // console.log($scope.add_drrq.format('YYYY-MM-DD'))
       
        var filterdata ={};
        filterdata.staff_code = $scope.add_ygh.user_name;
        staffrelationService.simple_select({'filterdata':filterdata}).success(function(reps2){
            var cms_code = '000000';
            if(reps2.data){
                console.log(reps2.data);
                cms_code = reps2.data[0].staff_cms_code;
               }
            if(!cms_code)
                cms_code = '000000';
            dkgsgxxzService.add_save({'add_drrq':$scope.add_drrq,'add_jgbh':$scope.add_jgbh.branch_code,'add_zhbh':$scope.add_zh,'add_zhxh':$scope.add_zhxh,'add_ygh':cms_code,'add_khh':$scope.add_khh,'add_gsbl':$scope.add_gsbl,'add_glqsrq':$scope.add_glqsrq.format('YYYY-MM-DD'),'add_gljsrq':$scope.add_gljsrq.format('YYYY-MM-DD'),'add_khmc':$scope.add_khmc}).success(function(resp){
                alert(resp.data);
                element.modal('hide');
	            $scope.search();
            });
        });
    };
    $scope.find_users = function(){
        branchmanageService.users({'branch_id':$scope.add_jgbh.role_id,'is_khjl':1}).success(function(reps){
            $scope.model2 =reps.data;
        });
    };    
    var element = angular.element('#add_modal_dkgsgx');
    $scope.model3 = ['','1','2','3']
    function find_branchs(){
	branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
	//console.log(reps.data);
	})	
    }
    find_branchs();
};

dkgxxzController.$inject = ['$scope', '$filter', 'SqsReportService','branchmanageService','dkgsgxxzService','staffrelationService'];

angular.module('YSP').service('dkgxxzController', dkgxxzController);
