/**
 *  *  * Users Controller
 *   *   */

ysp.controller('contract_checkController', function($scope, $rootScope,  contract_checkService, SqsReportService ){
  
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.pe_date = moment();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };
    $scope.objects = function(){
          contract_checkService.objects().success(function(reps){
          $scope.objects =reps.data;
         })
    };
	$scope.objects();
    $scope.search = function() {
        $scope.tableMessage = "正在查询";
        params=$scope.cust_search;
        if(params.pe_date instanceof moment){
            params.date = params.pe_date.format('YYYY-MM-DD');
        }else {
            params.date = '';
        };
        if(params.branch!=null){
            params.pe_object = params.branch.branch_code;
        }else {
            params.pe_object = '';
        };
        SqsReportService.info('concheck', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            };
        });
    };
    $scope.redirect =function (arg) {
        var id=arg[6];
        var name=arg[1]
        var abc='合约查看-'+name
        console.log(id)
        
        $scope.forward(abc,'views/con_check/index.html',{'item':arg});
    };

});
