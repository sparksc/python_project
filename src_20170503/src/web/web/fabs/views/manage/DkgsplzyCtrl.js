/**
 * dkgsplzy Controller
 */
function dkgsplzyController($scope, $filter, SqsReportService,branchmanageService,dkgsgxxzService,staffrelationService,dictdataService) {
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
        if (params.jgbh){
            params.jgbh = params.JGBH.branch_code;
        }
        else{
            params.JGBH = null;
        }
        params.GLDXBH =null;
        if (params.GLDXBH){
            var filterdata ={};
            filterdata.staff_code = params.GLDXBH.user_name;
            staffrelationService.simple_select({'filterdata':filterdata}).success(function(reps2){
            params.yygh = params.GLDXBH.user_name;
            if(reps2.data){
                params.gldxbh = reps2.data[0].staff_cms_code;
            }
            sqs_search(params);
        });
        }
        else{
            sqs_search(params);
        }
	//}
    };
    function sqs_search(params){
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        SqsReportService.info('loanmanagemove', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    }
    $scope.find_users = function(){
        branchmanageService.users({'branch_id':$scope.cust_search.JGBH.role_id,'is_khjl':1}).success(function(reps){
        $scope.model2 =reps.data;
                });
    };
    $scope.find_users2 = function(){
            branchmanageService.users({'branch_id':$scope.add_jgbh.role_id,'is_khjl':1}).success(function(reps){
                    $scope.model5 =reps.data;
            });
    };

    var element = angular.element('#add_dkgsplzy');
    function find_branchs(){
	branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
	});	
    };
    find_branchs();
   
   //全选与单选功能，全选为当前页面,prkey声明主键
    $scope.choseArr=[];
    $scope.oneflag =false;
    $scope.master =false;
    var prkey = 13;
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
	$scope.add_glqsrq = moment().add(1,'days');
	$scope.add_gljsrq = moment("2099-12-30","YYYY-MM-DD");
    $scope.batch_move = function() {
        if($scope.choseArr.length == 0) alert('请先选择账户');
        branchmanageService.branchs({}).success(function (reps) {
            $scope.model1=reps.data;
            element.modal('show');
            add_drrq = moment();
	        $scope.add_ygh = '';
	        $scope.newdata.glje1 = 100;
	    });	
    };
    $scope.newdata = {};
    $scope.do_batch_move = function(){
        var filterdata ={};
        filterdata.staff_code = $scope.add_ygh.user_name;
        staffrelationService.simple_select({'filterdata':filterdata}).success(function(reps2){

            $scope.newdata.drrq = moment().format('YYYY-MM-DD');
            $scope.newdata.jgbh = $scope.add_jgbh.branch_code;        
            $scope.newdata.gldxbh = reps2.data[0].staff_cms_code;;
            $scope.newdata.glrq1 = $scope.add_glqsrq.format('YYYY-MM-DD');
            $scope.newdata.glrq2 = $scope.add_gljsrq.format('YYYY-MM-DD');
            $scope.newdata.newflag = 0;
            dkgsgxxzService.do_batch_move({'newdata':$scope.newdata,'update_key':$scope.choseArr}).success(function(resp){
                alert(resp.data);
                element.modal('hide');
	            $scope.search();
            });
        });
    };
};

dkgsplzyController.$inject = ['$scope', '$filter', 'SqsReportService','branchmanageService','dkgsgxxzService','staffrelationService','dictdataService'];

angular.module('YSP').service('dkgsplzyController', dkgsplzyController);
