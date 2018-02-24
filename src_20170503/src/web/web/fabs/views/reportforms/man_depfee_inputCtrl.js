/**
 * mandepfeeinput Controller
 */
function mandepfeeinputController($scope,store, $filter, $rootScope, SqsReportService,subbranchdepfeeinputService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/branch_depfee_input?export=1"
    //$scope.cust_search.e_p_OPEN_DATE = moment();
    $scope.newstaffdata= {};    
    $scope.change_name = function(target){
        if(target == null){$scope.newstaffdata[1]='';$scope.newstaffdata[6]='';$scope.newstaffdata[5]=''}
        for(var i in $scope.model1){
            if($scope.model1[i].branch_code==target){
                $scope.newstaffdata[1]=$scope.model1[i].branch_name;     
                branchmanageService.users({'branch_id':$scope.model1[i].role_id}).success(function(reps){
                    $scope.model3 = reps.data;
                    });
                $scope.newstaffdata[5]=null;
            }
        } 
    }
    $scope.change_name1 = function(target){
        if(target == null)$scope.newstaffdata[6]='';
        for(var i in $scope.model3){
            if($scope.model3[i].user_name==target){
                $scope.newstaffdata[6]=$scope.model3[i].name;     
            }
        } 
    }
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
        });
    };
    find_branchs();    
    $scope.find_users = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.ORG_CODE){role_id=$scope.model1[i].role_id;}
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
        $scope.cust_search.STAFF_CODE = null;
    }
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        console.log($rootScope.user_session)
        params = $scope.cust_search;
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        SqsReportService.info('man_depfee_input', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };

    $scope.add = function(){
    $scope.newstaffdata={};
    $('#mandepfeeinput_modal').modal('show');
    $('#mandepfeeinput_new_add_button').show();
    $('#mandepfeeinput_save_edit_button').hide();
    };
    
    $scope.save = function(){
        console.log($scope.newstaffdata)
        var nsd ={};
        nsd["org_code"]=$scope.newstaffdata[0];
        nsd["org_name"]=$scope.newstaffdata[1];
        nsd["be_year"]=$scope.newstaffdata[2];
        nsd["fee"]=$scope.newstaffdata[3];
        nsd["input_level"]="manager";
        nsd["staff_code"]=$scope.newstaffdata[5];
        nsd["staff_name"]=$scope.newstaffdata[6];
        console.log(nsd)
        var nd = {"newdata":nsd};
        subbranchdepfeeinputService.save(nd).success(function (reps){
        $scope.search(); 
        $('#mandepfeeinput_modal').modal('hide');
        });
    };
    $scope.to_edit = function(row){
    $('#mandepfeeinput_modal').modal('show');
    $('#mandepfeeinput_new_add_button').hide();
    $('#mandepfeeinput_save_edit_button').show();
    $scope.change_name(row[0]);
    $scope.newstaffdata[0] = row[0];
    $scope.newstaffdata[1] = row[1];
    $scope.newstaffdata[2] = row[4];
    $scope.newstaffdata[3] = row[5];
    $scope.newstaffdata[4] = row[6];
    $scope.newstaffdata[5] = row[2];
    $scope.newstaffdata[6] = row[3];
    };
    $scope.edit_save = function(){
        var nsd ={};
        console.log($scope.newstaffdata)
        nsd["org_code"]=$scope.newstaffdata[0];
        nsd["org_name"]=$scope.newstaffdata[1];
        nsd["be_year"]=$scope.newstaffdata[2];
        nsd["fee"]=$scope.newstaffdata[3];
        nsd["input_level"]="manager";
        nsd["id"]=$scope.newstaffdata[4];
        nsd["staff_code"]=$scope.newstaffdata[5];
        nsd["staff_name"]=$scope.newstaffdata[6];
        var nd = {"newdata":nsd};
        subbranchdepfeeinputService.update(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#mandepfeeinput_modal').modal('hide');
        });
        
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
    var nsd={};
    nsd["id"]=row[6];
    var nd = {"newdata":nsd};
        subbranchdepfeeinputService.delete(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#mandepfeeinput_modal').modal('hide');
        });
        }
    };


};

mandepfeeinputController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','subbranchdepfeeinputService','branchmanageService'];

angular.module('YSP').service('mandepfeeinputController', mandepfeeinputController);
