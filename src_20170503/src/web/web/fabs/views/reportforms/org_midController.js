/**
 * Orgmid Controller
 */
function OrgmidController($scope, $filter, SqsReportService, permissionService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "点击查询";
    $scope.cust_search = {};
    $scope.cust_search.date = moment();
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
        console.log($scope.model1)
        });
    };
    find_branchs();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };   
    $scope.search = function() {
        params = {};
        $scope.tableMessage = "正在查询";
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/org_mid?export=1";
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            if(key=='date')params['date']=params['date'].format("YYYYMMDD");
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        console.log(params)
        SqsReportService.info('org_mid',params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查到数据";
            }
        });
    }
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/org_mid?export=1"+"&date="+moment().format('YYYYMMDD');
};
OrgmidController.$inject = ['$scope', '$filter', 'SqsReportService', 'permissionService','branchmanageService'];

angular.module('YSP').service('OrgmidController', OrgmidController); 
