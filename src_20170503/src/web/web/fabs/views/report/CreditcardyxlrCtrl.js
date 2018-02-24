/**
 * creditcardyxlr Controller
 */
function creditcardyxlrController($scope,store, $filter, $rootScope, SqsReportService,accthkService,dictdataService,custhkService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.tableMessage1 = "请输入卡号";
    $scope.cust_search = {};
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/accthk1?export=1&TYP="+encodeURI("信用卡");
    //$scope.cust_search.e_p_OPEN_DATE = moment();
    $scope.newstaffdata= {};
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        $("div[name='loading']").modal("show");
        console.log($rootScope.user_session)
        params = $scope.cust_search;
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/accthk1?export=1&TYP="+encodeURI("信用卡");
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        //if (params.JGBH){
        //    params.JGBH = params.JGBH.branch_code;
        //}
        //if (params.GLDXBH){
        //    params.GLDXBH = params.GLDXBH.user_name;
        //}
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        params.TYP = "信用卡";
        params.ORG_NO = $rootScope.user_session.branch_code;
        SqsReportService.info('accthklr', params).success(function(resp) {
            $("div[name='loading']").modal("hide");
            $scope.data = resp;
            $scope.data.header=["日期","机构号","机构名","员工号","员工名","卡号","类型","占比(%)","状态","操作"]
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };

    $scope.add = function(){
    $scope.newdata={};
    $scope.newstaffdata={};
    $scope.add_zh = '';
    $('#check_creditcardyxlr').show();
    $('#creditcardyxlr_modal').modal('show');
    $('#creditcardyxlr_new_add_button').hide();
    $('#creditcardyxlr_save_edit_button').hide();
    $scope.tableMessage1 = "请输入卡号";
    };
    $scope.check = function(account){
        if(account == null||account == ''){
            $scope.tableMessage1="卡号不能为空"
        }
        else{
        SqsReportService.info('accthk2',{'ACCOUNT_NO':account}).success(function(resp){
        $scope.newdata=resp;
        console.log(resp)
        if (($scope.newdata.rows || []).length > 0) {
                $scope.tableMessage1 = "";
            SqsReportService.info('accthk1',{'ACCOUNT_NO':account,'TYP':"信用卡",'ORG_NO':$rootScope.user_session.branch_code}).success(function(resp) {
               $scope.newstaffdata = resp;
                    if ((resp.rows || []).length > 0) {
                        $scope.newstaffdata[0] = resp.rows[0][1];
                        $scope.newstaffdata[1] = resp.rows[0][1];
                        $scope.newstaffdata[2] = resp.rows[0][4];
                        $scope.newstaffdata[3] = resp.rows[0][5].toString();
                        $scope.newstaffdata[4] = resp.rows[0][6].toString();
                        $scope.tableMessage1 = "该卡的当前录入业绩期间在系统中已经存在营销挂钩关系，请检查！";
                        $('#creditcardyxlr_new_add_button').hide();
                    } else {
                        $scope.tableMessage1 = "未查询到营销人员";
                        $scope.newstaffdata = {};
                        $scope.newstaffdata[0] = $rootScope.user_session.user_code;
                        $scope.newstaffdata[1] = $rootScope.user_session.user_name; 
                        $scope.newstaffdata[2] = 100;
                        $scope.newstaffdata[3] = moment();
                        $scope.newstaffdata[4] = "2099-12-31";

                        $('#creditcardyxlr_new_add_button').show();
                    }
            });
                
            } else {
                $scope.tableMessage1 = "未查询到此卡";
                $('#creditcardyxlr_new_add_button').hide();
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
        nsd["start_date"]=$scope.newstaffdata[3].format("YYYYMMDD");
        nsd["org_no"]=$rootScope.user_session.branch_code;
        nsd["end_date"]="20991231";
        nsd["src"]="前端录入";
        nsd["typ"]="信用卡";
        console.log(nsd)
        var nd = {"newdata":nsd};
        accthkService.save(nd).success(function (reps){
        $scope.search(); 
        $('#creditcardyxlr_modal').modal('hide');
        });
    };
    $scope.to_edit = function(row){
    
    SqsReportService.info('accthk2',{'ACCOUNT_NO':row[5]}).success(function(resp){
    $scope.newdata=resp;
    $scope.tableMessage1 = "";
    }
    );
    
    $('#check_creditcardyxlr').hide();
    $('#creditcardyxlr_modal').modal('show');
    $('#creditcardyxlr_new_add_button').hide();
    $('#creditcardyxlr_save_edit_button').show();
    $scope.newstaffdata[0] = row[3];
    $scope.newstaffdata[1] = row[4];
    $scope.newstaffdata[2] = 100;
    $scope.newstaffdata[3] = moment(row[8].toString());
    $scope.newstaffdata[4] = row[9].toString();
    $scope.newstaffdata[6] = row[11];
    };
    $scope.edit_save = function(){
        var nsd ={};
        console.log($scope.newstaffdata)
        nsd["etl_date"]=moment().format("YYYYMMDD");
        nsd["manager_no"]=$scope.newstaffdata[3];
        nsd["percentage"]=100;
        nsd["org_no"]=$rootScope.user_session.branch_code;
        nsd["start_date"]=$scope.newstaffdata[3].format("YYYYMMDD");
        nsd["end_date"]="20991231";
        nsd["src"]="前端修改";
        nsd["typ"]="信用卡";
        nsd["id"]=$scope.newstaffdata[6]
        //console.log(nsd)
        var nd = {"newdata":nsd};
        accthkService.update(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#creditcardyxlr_modal').modal('hide');
        });
        
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
    var nsd={};
    nsd["id"]=row[12];
    var nd = {"newdata":nsd};
        accthkService.delete(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#creditcardyxlr_modal').modal('hide');
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


   $scope.get_staff_name = function(){  //录入时 输入员工号,员工名回显
        custhkService.get_staff_name({'user_name':$scope.newstaffdata[0]}).success(function(resp){
            $scope.newstaffdata[1] = resp.data.name;
        });
   }

};

creditcardyxlrController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','accthkService','dictdataService','custhkService'];

angular.module('YSP').service('creditcardyxlrController', creditcardyxlrController);
