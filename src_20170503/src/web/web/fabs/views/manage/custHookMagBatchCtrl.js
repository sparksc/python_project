/**
 * custHookMag Controller
 * 客户挂钩批量转移
 */
function custHookMagBatchController($scope, $filter, SqsReportService,branchmanageService,custHookMagService) {
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
        SqsReportService.info('cust_hook_mag', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
	//}
    };
    $scope.find_users = function(){
        branchmanageService.users({'branch_id':$scope.cust_search.org.role_id}).success(function(reps){
            $scope.model2 =reps.data;
       });
    };
    $scope.find_users2 = function(){
        branchmanageService.users({'branch_id':$scope.top_id}).success(function(reps){
            $scope.model5 =reps.data;
       });
    };

    var element = angular.element('#custHookBatchMoveModal');
    function find_branchs(){
	    branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
            $scope.model1=reps.data;
	    })	
    }
    find_branchs();
   
   //全选与单选功能，全选为当前页面,prkey声明主键
    $scope.choseArr=[];
    $scope.oneflag =false;
    $scope.master =false;
    var prkey = 0;
    $scope.selectall = function(master,data){
        if(master){
            $scope.onefalg =true;
            for(rowvalue in data){
                $scope.choseArr.push(data[rowvalue][prkey]);
            }
        }
        else{
            $scope.onefalg =false;
            $scope.choseArr =[];
        }
    };
    $scope.chkone = function(row,oneflag){
        var hasin = $scope.choseArr.indexOf(row[prkey]);
        if(oneflag&&hasin==-1){
            $scope.choseArr.push(row[prkey])
        }
        if(!oneflag&&hasin>-1){
            $scope.choseArr.pop(row[prkey])
        }
    };
    //批量移交功能
	$scope.add_start_date = moment().add(1,'days');
	$scope.add_end_date = moment("2099-12-30","YYYY-MM-DD");
    $scope.batch_move = function() {
        if($scope.choseArr.length == 0) 
        {
            alert('请先选择客户信息');
            return;
        }
        console.log($scope.choseArr[0])
        custHookMagService.get_top({'id':$scope.choseArr[0]}).success(function (reps) {
            $scope.top_org = reps.data[0].org_no;    
            branchmanageService.branch({'org':$scope.top_org}).success(function (reps) {
                $scope.add_org=reps.data[0].branch_name;
                element.modal('show');
                add_start_date = moment().format('YYYY-MM-DD');
                $scope.add_manager = '';
                $scope.top_id = reps.data[0].role_id;
                $scope.find_users2();
            }); 
        });
    };
    $scope.newdata = {};
    $scope.do_batch_move = function(){
        $scope.newdata.end_date = moment().format('YYYY-MM-DD');
        $scope.newdata.org_no = $scope.add_org.branch_code;        
        $scope.newdata.manager_no = $scope.add_manager.user_name;
        $scope.newdata.start_date = $scope.add_start_date.format('YYYY-MM-DD');
        $scope.newdata.end_date = $scope.add_end_date.format('YYYY-MM-DD');
        console.log($scope.newdata.start_date)
        console.log($scope.newdata.end_date)
        custHookMagService.batch_cust_move({'newdata':$scope.newdata,'update_key':$scope.choseArr}).success(function(resp){
            alert(resp.data);
            element.modal('hide');
	        $scope.search();
        });
    };
};

custHookMagBatchController.$inject = ['$scope', '$filter', 'SqsReportService','branchmanageService','custHookMagService'];
angular.module('YSP').service('custHookMagBatchController', custHookMagBatchController);
