/**
 * monsalary Controller
 */
function monsalaryController($scope,$rootScope, $filter, SqsReportService,monsalaryService,store,branchmanageService,depappointService,dictdataService) {
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

    var params ={};
    $scope.find_users = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.jgbh){role_id=$scope.model1[i].role_id;}
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 =reps.data;
        });
        target.ygxm='';
    };
    $scope.find_names = function(target){
        target.ygxm='';
        for(i in $scope.model2)
            if($scope.model2[i].user_name == target.yggh )target.ygxm = $scope.model2[i].name;
    };
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
         do_search();
    
    };
    //添加，保存
    
    $scope.ntarget = {};
    $scope.ntarget.tjrq = moment();
    $scope.add = function(){
        $('#p_i_modal_add').modal('show');
    
    
    };

    $scope.save = function(ntarget) {
        if(ntarget.tjrq instanceof moment){
            ntarget.tjrq = ntarget.tjrq.format('YYYY-MM-DD');}
   

            monsalaryService.save({'ntarget':$scope.ntarget}).success(function(resp) {
            alert(resp.data);
            $scope.search();
            $('#p_i_modal_edit').modal('hide');
            $('#p_i_modal_add').modal('hide');
            });
    };


    //修改
    
    $scope.updatatype = function(row) {
        $scope.updata = {};
        $scope.updata.para_id = row[15];
        $scope.updata.tjrq = row[0];
        $scope.updata.jgbh = row[1];
        $scope.updata.jgmc = row[2];

        $scope.updata.yggh = row[3];
        $scope.updata.ygxm = row[4];

        $scope.updata.je1 = row[5];
        $scope.updata.je2 = row[6];
        $scope.updata.je4 = row[8];

        $scope.updata.je5 = row[9];
        $scope.updata.je6 = row[10];
        $scope.updata.je7 = row[11];

        $scope.updata.je8 = row[12];
        $scope.updata.je9 = row[13];


        $('#p_i_modal_edit').modal('show');
    };

     $scope.do_update = function(){
        monsalaryService.update({'updata':$scope.updata}).success(function(resp){
            alert(resp.data);
            if(resp.data=='修改成功'){
                $('#p_i_modal_edit').modal('hide');
                $('#p_i_modal_add').modal('hide');
                do_search();
            }
        });
     };



    //初始化机构编号
    init();
    //查询
    function do_search(){
         params = $scope.cust_search;

        if(params.tdate instanceof moment){
            params.tjrq = params.tdate.format('YYYY-MM-DD');
        }
        else{
            params.tjrq = '';
        }
        params.jgbh = $scope.cust_search.jgbhh;
        params.yggh = $scope.cust_search.ygghh;
        $scope.data = {};
        $scope.tableMessage = "正在查询";

        SqsReportService.info('monsalary', params).success(function(resp) {
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
             $scope.model3=reps.data;
         
        });
    };
   
    $scope.find_user = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.jgbhh){role_id=$scope.model1[i].role_id;}
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model4 = reps.data;
        });
        $scope.cust_search.ygghh = null;
    }

};

monsalaryController.$inject = ['$scope','$rootScope', '$filter', 'SqsReportService','monsalaryService','store','branchmanageService','depappointService','dictdataService'];

angular.module('YSP').service('monsalaryController', monsalaryController);
