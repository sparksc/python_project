/**
 * cdyxlr Controller
 */
function cdgggxlrController($scope,store, $filter, $rootScope, SqsReportService,accthkService,dictdataService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    
    $scope.tableMessage = "请点击查询";
    $scope.tableMessage1 = "请输入账号";
    $scope.cust_search = {};
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/accthk1?export=1&TYP="+encodeURI("存款");
    //$scope.cust_search.e_p_OPEN_DATE = moment();
    $scope.newstaffdata= {};
    $scope.newstaffdata[3] = moment();
    $scope.newstaffdata[4] = moment();
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        console.log($rootScope.user_session)
        params = $scope.cust_search;        
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/accthk1?export=1&TYP="+encodeURI("存款");
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
 
        $scope.data = {};
        $scope.tableMessage = "正在查询";
            params.TYP = "存款";
            params['STATUS'] = "正常";
        SqsReportService.info('acctcusthk1', params).success(function(resp) {
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
    $('#check_cdyxlr').show();
    $('#cdyxlr_modal').modal('show');
    $('#cdyxlr_new_add_button').hide();
    $('#cdyxlr_save_edit_button').hide();
    $scope.tableMessage1 = "请输入账号";
    $scope.tiltle ='录入' 
    $scope.newstaffdata = [];
    $scope.newstaffdata[5] = "存贷挂钩";
    };
    $scope.check = function(account){
        if(account == null||account == ''){
            $scope.tableMessage1="账号不能为空"
        }
        else{
        SqsReportService.info('accthk2',{'ACCOUNT_NO':account}).success(function(resp){
        $scope.newdata=resp;
        console.log(resp)
        if (($scope.newdata.rows || []).length > 0) {
                $scope.tableMessage1 = "";
            SqsReportService.info('accthk1',{'ACCOUNT_NO':account,'TYP':"存款",'STATUS':"正常"}).success(function(resp) {
               $scope.newstaffdata = resp;
                    if ((resp.rows || []).length > 0) {
                        $scope.newstaffdata[0] = resp.rows[0][3];
                        $scope.newstaffdata[1] = resp.rows[0][4];
                        $scope.newstaffdata[2] = resp.rows[0][7];
                        $scope.newstaffdata[3] = resp.rows[0][10].toString();
                        $scope.newstaffdata[4] = resp.rows[0][11].toString();
                        $scope.newstaffdata[5] = resp.rows[0][5];
                        $scope.newstaffdata[6] = resp.rows[0][8];
                        $scope.newstaffdata[7] = resp.rows[0][10];
                        $scope.tableMessage1 = "该账号当前录入业绩期间在系统中已经存在营销挂钩关系，请检查！";
                        $('#cdyxlr_new_add_button').hide();
                    } else {
                        $scope.tableMessage1 = "未查询到营销人员";
                        $scope.newstaffdata = {};
                        $scope.newstaffdata[0] = $rootScope.user_session.user_code;
                        $scope.newstaffdata[1] = $rootScope.user_session.user_name; 
                        $scope.newstaffdata[3] = moment();
                        $scope.newstaffdata[4] = "2099-12-31";
                        $scope.newstaffdata[5] = "存贷挂钩";
                        $scope.newstaffdata[6] = "正常";

                        $('#cdyxlr_new_add_button').show();
                    }
            });
                
            } else {
                $scope.tableMessage1 = "未查询到此账号";
                $('#cdyxlr_new_add_button').hide();
            }
        });
        }
    };

    $scope.save = function(){
        console.log($scope.newstaffdata)
        var nsd ={};
        nsd["etl_date"]=moment().format("YYYYMMDD");
        nsd["manager_no"]=$scope.newstaffdata[0];
        nsd["percentage"]=$scope.newstaffdata[2];
        nsd["account_no"]=$scope.newdata.rows[0][0];
        nsd["org_no"]=$rootScope.user_session.branch_code;
        nsd["start_date"]=$scope.newstaffdata[3].format("YYYYMMDD");
        nsd["end_date"]="20991231";
        nsd["hook_type"]=$scope.newstaffdata[5];
        nsd["status"]=$scope.newstaffdata[6];
        nsd["makeup"]=$scope.newstaffdata[7];
        nsd["src"]="前端录入";
        nsd["typ"]="存款";
        console.log(nsd)
        var nd = {"newdata":nsd};
        accthkService.save(nd).success(function (reps){
        $scope.search(); 
        $('#cdyxlr_modal').modal('hide');
        });
    };
    $scope.to_edit = function(row){
    //console.log(row) 
    $scope.tiltle ='编辑' 
    SqsReportService.info('accthk2',{'ACCOUNT_NO':row[2]}).success(function(resp){
    $scope.newdata=resp;
    $scope.tableMessage1 = "";
    }
    );
    
    $('#check_cdyxlr').hide();
    $('#cdyxlr_modal').modal('show');
    $('#cdyxlr_new_add_button').hide();
    $('#cdyxlr_save_edit_button').show();
    $scope.newstaffdata[0] = row[2];
    $scope.newstaffdata[1] = row[3];
    $scope.newstaffdata[2] = row[7];
    console.log($scope.newstaffdata[2])
    $scope.newstaffdata[3] = moment(row[8].toString());
    $scope.newstaffdata[4] = row[9].toString();
    $scope.newstaffdata[5] = row[6];
    $scope.newstaffdata[6] = row[10];
    $scope.newstaffdata[7] = row[11];
    $scope.newstaffdata[8] = row[12];
    };
    $scope.edit_save = function(){
        var nsd ={};
        nsd["etl_date"]=moment().format("YYYYMMDD");
        nsd["percentage"]=$scope.newstaffdata[2];
        nsd["start_date"]=$scope.newstaffdata[3].format("YYYYMMDD");
        nsd["end_date"]="20991231";
        nsd["src"]="前端修改";
        nsd["typ"]="存款";
        nsd["id"]=$scope.newstaffdata[8]
        //console.log(nsd)
        var nd = {"newdata":nsd};
        accthkService.update(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#cdyxlr_modal').modal('hide');
        });
        
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
        var nsd={};
        nsd["etl_date"]=moment().format("YYYYMMDD");
        nsd["end_date"]=moment().format("YYYYMMDD");
        nsd["src"]="前端删除";
        nsd["typ"]="存款";
        nsd["status"]="删除";
        nsd["id"]=row[11];
        var nd = {"newdata":nsd};
            accthkService.update(nd).success(function (reps){
                //console.log(reps) 
                $scope.search(); 
                $('#cdyxlr_modal').modal('hide');
            });
        }
    };

    function find_dict(){
	dictdataService.get_dict({'dict_type':'CKTYPE'}).success(function (reps) {
        $scope.model3=reps.data;
	});	
    }
    //find_dict();    
    $scope.searchEle = function(){
        imageService.pdfile_query($scope.applicationId,'elec_arch').success(function(resp){
                $scope.pdf_list  = resp.data;      
                console.log(resp.data);
        });
    }
    $scope.upload_excel = function(){
        console.log($scope.tabId)
        var files = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#elec_arch").prop('files');
        var token = store.getSession("token");
        var form = new FormData();
        console.log(files)
        for(var i = 0 ; i < files.length ; ++i){
            console.log('---',files[i]);
            form.append('files',files[i]);
        }
        form.append('application_id',$scope.applicationId)
        form.append('about','elec_arch')
        $.ajax({
            type: "POST",
            url : base_url+"/accthk/upload/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("x-session-token", token);
            },   
            success: function(msg){
                console.log(msg);
                alert(msg.data);
            }    
        });  
    }    



};

cdgggxlrController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','accthkService','dictdataService'];

angular.module('YSP').service('cdgggxlrController', cdgggxlrController);
