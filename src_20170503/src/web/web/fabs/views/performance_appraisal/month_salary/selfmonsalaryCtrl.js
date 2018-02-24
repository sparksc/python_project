/**
 * Khjlajzb Controller
 */
function selfmonsalaryController($scope, $filter, SqsReportService,store,branchmanageService,depappointService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.tdate = moment();

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

        if(params.tdate instanceof moment){
            params.tjrq = params.tdate.format('YYYY-MM-DD');
        }
        else{
            params.tjrq = '';
        
        }

        if($scope.yybljg_dis){
            params.jgbh = $scope.yybljg_dis.branch_code;
        }


        $scope.data = {};
 
        $scope.tableMessage = "正在查询";
        params.yggh = store.getSession("user_name");

        SqsReportService.info('selfmonsalary', params).success(function(resp) {
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
             $scope.branchs=reps.data;
         
        });
    };
   

};

selfmonsalaryController.$inject = ['$scope', '$filter', 'SqsReportService','store','branchmanageService','depappointService'];

angular.module('YSP').service('selfmonsalaryController', selfmonsalaryController);
