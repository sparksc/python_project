/**
 * ckgsdbwh Controller
 */
function ckgsdbwhController($scope, $filter, SqsReportService,branchmanageService,gsgxckService) {
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
        params = $scope.cust_search;
        if (params.org){
            params.org_no = params.org.branch_code;
        }
        else{
            params.org_no = null;
        }
        if (params.manager){
            params.manager_no = params.manager.user_name;
        }
        else{
            params.manager_no = null;
        }
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        SqsReportService.info('000052', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    $scope.add_start_date = moment();
    $scope.add_end_date = moment();
    $scope.change = function(row) {
        $scope.search_org=row[1];
        branchmanageService.branch({'org':$scope.search_org}).success(function (reps) {
            element.modal('show');
            add_start_date = moment();
            $scope.add_org = reps.data[0].branch_name;
            $scope.role_id = reps.data[0].role_id;
            $scope.find_users2();
            $scope.add_id = row[0];
            $scope.add_account_no = row[5];
            $scope.add_percentage = row[6];
            $scope.add_start_date = moment().add(1,'days');
            $scope.add_end_date = moment("2099-12-30","YYYY-MM-DD");
	    });	
    }
    $scope.save = function(){
        mday = moment()
        gsgxckService.account_move({'move_date':mday.format('YYYY-MM-DD'),'move_org_no':$scope.search_org,'move_account_no':$scope.add_account_no,'move_manager_no':$scope.add_manager.user_name,'move_percentage':$scope.add_percentage,'move_start_date':$scope.add_start_date.format('YYYY-MM-DD'),'move_end_date':$scope.add_end_date.format('YYYY-MM-DD'),'move_id': $scope.add_id}).success(function(resp){
            alert(resp.data);
            element.modal('hide');
	    $scope.search();
        });
    };
    $scope.find_users = function(){
            branchmanageService.users({'branch_id':$scope.cust_search.org.role_id}).success(function(reps){
                $scope.model2 =reps.data;
                });
    };
    $scope.find_users2 = function(){
            branchmanageService.users({'branch_id':$scope.role_id}).success(function(reps){
                $scope.model5 =reps.data;
            });
    };

    var element = angular.element('#move_modal_ckdbwh');
    $scope.model3 = [{'key':'1','value':'自营存款'},{'key':'2','value':'分配存款'},{'key':'3','value':'特殊存款'}];
    function find_branchs(){
	branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
	})	
    }
    find_branchs();
};

ckgsdbwhController.$inject = ['$scope', '$filter', 'SqsReportService','branchmanageService','gsgxckService'];

angular.module('YSP').service('ckgsdbwhController', ckgsdbwhController);
