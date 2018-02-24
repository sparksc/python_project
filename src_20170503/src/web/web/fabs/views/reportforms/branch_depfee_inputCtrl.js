/**
 * branchdepfeeinput Controller
 */
function branchdepfeeinputController($scope,store, $filter, $rootScope, SqsReportService,subbranchdepfeeinputService,branchmanageService) {
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
       for(var i in $scope.model1){
       if($scope.model1[i].branch_code==target)
           $scope.newstaffdata[1]=$scope.model1[i].branch_name;     
       } 
    }
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
        });
    };
    find_branchs();
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
        SqsReportService.info('branch_depfee_input', params).success(function(resp) {
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
    $('#branchdepfeeinput_modal').modal('show');
    $('#branchdepfeeinput_new_add_button').show();
    $('#branchdepfeeinput_save_edit_button').hide();
    };
    
    $scope.save = function(){
        console.log($scope.newstaffdata)
        var nsd ={};
        nsd["org_code"]=$scope.newstaffdata[0];
        nsd["org_name"]=$scope.newstaffdata[1];
        nsd["be_year"]=$scope.newstaffdata[2];
        nsd["fee"]=$scope.newstaffdata[3];
        nsd["input_level"]="branch";
        console.log(nsd)
        var nd = {"newdata":nsd};
        subbranchdepfeeinputService.save(nd).success(function (reps){
        $scope.search(); 
        $('#branchdepfeeinput_modal').modal('hide');
        });
    };
    $scope.to_edit = function(row){
    $('#branchdepfeeinput_modal').modal('show');
    $('#branchdepfeeinput_new_add_button').hide();
    $('#branchdepfeeinput_save_edit_button').show();
    $scope.newstaffdata[0] = row[0];
    $scope.newstaffdata[1] = row[1];
    $scope.newstaffdata[2] = row[2];
    $scope.newstaffdata[3] = row[3];
    $scope.newstaffdata[4] = row[4];
    };
    $scope.edit_save = function(){
        var nsd ={};
        console.log($scope.newstaffdata)
        nsd["org_code"]=$scope.newstaffdata[0];
        nsd["org_name"]=$scope.newstaffdata[1];
        nsd["be_year"]=$scope.newstaffdata[2];
        nsd["fee"]=$scope.newstaffdata[3];
        nsd["input_level"]="branch";
        nsd["id"]=$scope.newstaffdata[4];
        var nd = {"newdata":nsd};
        subbranchdepfeeinputService.update(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#branchdepfeeinput_modal').modal('hide');
        });
        
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
    var nsd={};
    nsd["id"]=row[4];
    var nd = {"newdata":nsd};
        subbranchdepfeeinputService.delete(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#branchdepfeeinput_modal').modal('hide');
        });
        }
    };


};

branchdepfeeinputController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','subbranchdepfeeinputService','branchmanageService'];

angular.module('YSP').service('branchdepfeeinputController', branchdepfeeinputController);
