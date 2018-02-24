/**
 * Manager_ebank Controller
 */
function mancomController($scope, $filter, SqsReportService, permissionService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "点击查询";
    $scope.cust_search = {};
    $scope.cust_search.S_DATE=moment();
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
        console.log($scope.model1)
        });
    };
    find_branchs();
    $scope.find_users = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.BRANCH_CODE){role_id=$scope.model1[i].role_id;}
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
        $scope.cust_search.SALE_CODE = null;
    }
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };   
    $scope.search = function() {
        params = {};
        $scope.tableMessage = "正在查询";
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/man_com?export=1";
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            if(key=='S_DATE')
                params['S_DATE']=params['S_DATE'].format("YYYYMMDD");
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        SqsReportService.info('man_com',params).success(function(resp) {
            $scope.data = resp;
         console.log(resp)
	    if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查到数据";
            }
        });
    }
    $scope.to_edit = function(row) {
    $scope.target ={};
    $scope.target.staff_no = row[0];
    $scope.target.staff_name = row[1];
    $scope.target.branch = row[2];
    $scope.target.password = row[3];
    $scope.target.uid=row[4];
    $scope.target.fid=row[5];
    $scope.target.oid=row[6];
    console.log(row)
	$('#myModal_p').modal('show');
    };
    $scope.userupdate = function(target) {//target表示待编辑的那行数据
        var new_data = {'newdata':target};
        //new_data['newdata']=target;//把list对象放到key为newdata的字典里
	    permissionService.user_update(new_data).success(function(resp) {
            alert(resp.data);//resp是个object对象，对象的属性data，成功更新这条记录就返回data值更新成功。
            $scope.search();
            $('#myModal_p').modal('hide');
        });                
    };
    $scope.add = function(){
        $scope.ntarget = {};
        var modal = $('#s_r_modal_p');
        modal.modal('show');
    };
    $scope.usersave = function(ntarget){
        var new_data = {'newdata':ntarget};
	permissionService.user_save(new_data).success(function(resp) {
         alert(resp.data);
         $('#s_r_modal_p').modal('hide');
         $scope.search();
        });                
    };
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/man_com?export=1";
};

mancomController.$inject = ['$scope', '$filter', 'SqsReportService', 'permissionService','branchmanageService'];

angular.module('YSP').service('OrgebankController', OrgebankController); 
