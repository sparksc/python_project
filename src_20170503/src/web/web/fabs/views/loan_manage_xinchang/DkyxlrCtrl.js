/**
 * dkyxlr Controller
 */
function dkyxlrController1($scope, $filter, $rootScope, SqsReportService,gsgxdkService,dictdataService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.tableMessage1 = "";
    $scope.cust_search = {};
   // $scope.cust_search.e_p_OPEN_DATE = moment();
    $scope.newstaffdata= {};
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        console.log($rootScope.user_session)
        params = $scope.cust_search;
        //if (params.JGBH){
        //    params.JGBH = params.JGBH.branch_code;
        //}
        //if (params.GLDXBH){
        //    params.GLDXBH = params.GLDXBH.user_name;
        //}
        $scope.data = {};
        $scope.tableMessage = "正在查询";
            params.GLDXBH = $scope.user_cms_code;
        SqsReportService.info('dkyxlr2', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };

    $scope.add = function(){
    $scope.newdata={};
    $('#check_account').show();
    $('#dkyxlr_modal1').modal('show');
    $('#new_add_button').hide();
    $('#save_edit_button').hide();
    $scope.tableMessage1 = "请输入客户内码";
    };
    $scope.check = function(account){
        if(account == null||account == ''){
            $scope.tableMessage1="客户内码不能为空"
        }
        else{
        SqsReportService.info('dkyxlr1',{'CUST_SEQ':account}).success(function(resp){
        $scope.newdata=resp;
        console.log(resp)
        if (($scope.newdata.rows || []).length > 0) {
                console.log(resp.rows[0][7].toString(),moment().format("YYYYMMDD"),resp.rows[0][7]<moment().format("YYYYMMDD")); 
                if(resp.rows[0][7]<moment().format("YYYYMMDD"))$scope.tableMessage1 = "该合同已经到期";
                else {
                $scope.tableMessage1 = "";
                var str=''+$scope.newdata.rows[0][6];
                $scope.newdata.rows[0][6]=str.substr(0,4)+'-'+str.substr(4,2)+'-'+str.substr(6,2);
                var str=''+$scope.newdata.rows[0][7];
                $scope.newdata.rows[0][7]=str.substr(0,4)+'-'+str.substr(4,2)+'-'+str.substr(6,2);
            
            SqsReportService.info('dkyxlr3',{'FJDXBH':$scope.newdata.rows[0][4]}).success(function(resp) {
               $scope.newstaffdata = resp;
                    if ((resp.rows || []).length > 0) {
                        $scope.newstaffdata = resp.rows[0];
                        $scope.tableMessage1 = "该存款账户的当前录入业绩期间在系统中已经存在营销挂钩关系，请检查！";
                        $('#new_add_button').hide();
                    } else {

                        $scope.tableMessage1 = "未查询到营销人员";
                        $scope.newstaffdata = {};
                        $scope.newstaffdata[0] = $scope.user_cms_code;
                        $scope.newstaffdata[1] = $rootScope.user_session.user_name; 
                        $scope.newstaffdata[2] = 100;
                        $scope.newstaffdata[3] = moment().format("YYYY-MM-DD");
                        $scope.newstaffdata[4] = "2099-12-31";
                        $scope.newstaffdata[5] = $scope.model3[0].key;

                        $('#new_add_button').show();
                    }
            });
            }    
            } else {
                $scope.tableMessage1 = "未查询到此账号";
                $('#new_add_button').hide();
            }
        });
        }
    };

    $scope.save = function(){
        console.log($scope.newstaffdata)
        var nsd ={};
        nsd["drrq"]=moment().format("YYYY-MM-DD");
        nsd["jgbh"]=$rootScope.user_session.branch_code;
        nsd["dxbh"]=$scope.newdata.rows[0][0];
        nsd["gldxbh"]=$scope.newstaffdata[0];
        nsd["glje1"]=$scope.newstaffdata[2];
        nsd["glrq1"]=$scope.newstaffdata[3];
        if($scope.newstaffdata[3] instanceof moment) 
        nsd["glrq1"]=$scope.newstaffdata[3].format("YYYY-MM-DD");
        nsd["glrq2"]=$scope.newstaffdata[4];
        if($scope.newstaffdata[4] instanceof moment) 
        nsd["glrq2"]=$scope.newstaffdata[4].format("YYYY-MM-DD");
        nsd["dk_type"]=$scope.newstaffdata[5];
        nsd["dxxh"]=$scope.newdata.rows[0][3];
        nsd["fjdxbh"]=$scope.newdata.rows[0][4];
        nsd["dxmc"]=$scope.newdata.rows[0][2];
        nsd["newflag"]=0;      
        //console.log(nsd)
        var nd = {"newdata":nsd};
        gsgxdkService.save(nd).success(function (reps){
        $scope.search(); 
        $('#dkyxlr_modal1').modal('hide');
        });
    };
    $scope.to_edit = function(row){
    console.log(row) 
    SqsReportService.info('dkyxlr1',{'CUST_SEQ':row[6]}).success(function(resp){
    $scope.newdata=resp;});
    
    $('#check_account').hide();
    $('#dkyxlr_modal1').modal('show');
    $('#new_add_button').hide();
    $('#save_edit_button').show();
    $scope.newstaffdata[0] = row[1];
    $scope.newstaffdata[1] = row[2];
    $scope.newstaffdata[2] = row[8];
    $scope.newstaffdata[3] = row[9];
    $scope.newstaffdata[4] = row[10];
    for(i in $scope.model3){
    if($scope.model3[i].value==row[11])$scope.newstaffdata[5] = $scope.model3[i].key;
    }
    $scope.newstaffdata[6] = row[12];
    };
    $scope.edit_save = function(){
        var nsd ={};
        nsd["drrq"]=moment().format("YYYY-MM-DD");
        nsd["glje1"]=$scope.newstaffdata[2];
        nsd["glrq1"]=$scope.newstaffdata[3];
        if($scope.newstaffdata[3] instanceof moment) 
        nsd["glrq1"]=$scope.newstaffdata[3].format("YYYY-MM-DD");
        nsd["glrq2"]=$scope.newstaffdata[4];
        if($scope.newstaffdata[4] instanceof moment) 
        nsd["glrq2"]=$scope.newstaffdata[4].format("YYYY-MM-DD");
        nsd["dk_type"]=$scope.newstaffdata[5];
        nsd["para_id"]=$scope.newstaffdata[6];      
        //console.log(nsd)
        var nd = {"newdata":nsd};
        gsgxdkService.update(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#dkyxlr_modal1').modal('hide');
        });
        
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
    var nsd={};
    nsd["para_id"]=row[12];
    nsd["drrq"]=moment().format("YYYY-MM-DD");
    nsd["glrq2"]=moment().format("YYYY-MM-DD");
    var nd = {"newdata":nsd};
        gsgxdkService.update(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#dkyxlr_modal1').modal('hide');
        });
        }
    };

    function find_dict(){
	dictdataService.get_dict({'dict_type':'DKTYPE'}).success(function (reps) {
        $scope.model3=reps.data;
	});	
    SqsReportService.info('000037',{'staff_code':$rootScope.user_session.user_code}).success(function(resp){
        $scope.user_cms_code = resp.rows[0][3];
    }); 
    }
    find_dict();

};

dkyxlrController1.$inject = ['$scope', '$filter', '$rootScope', 'SqsReportService','gsgxdkService','dictdataService'];

angular.module('YSP').service('dkyxlrController1', dkyxlrController1);
