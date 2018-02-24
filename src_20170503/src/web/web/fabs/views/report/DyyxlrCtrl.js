/**
 * dyyxlr Controller
 */
function dyyxlrController($scope,$rootScope,store, $filter, $rootScope, SqsReportService,custhkService,dictdataService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.tableMessage1 = "请输入客户号";
    $scope.cust_search = {};
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/custhk1?export=1&TYP="+encodeURI("电子银行");
    $scope.newstaffdata= {};
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
            $scope.parse_paginfo($scope.data.actions);
        });
    };

    $scope.parse_paginfo = function(actions){
        for (var i in actions){
            var action = actions[i];
            var act = action.action;
            var info = action.conversation_id;
            var pairs = info.split("&")
            for(var j in pairs){
                if (pairs[j].indexOf('total_count')!=-1){
                    $scope.total_count = pairs[j].split('=')[1];
                }
                if (pairs[j].indexOf('page')!=-1){
                    var page = pairs[j].split('=')[1];
                    if ( act === "previous"){
                        $scope.cur_page = parseInt(page) + 1;
                    }
                    if ( act === "next"){
                        $scope.cur_page = parseInt(page) - 1;
                    }
                }
            }
        }
    }

    $scope.search = function() {
        $("div[name='loading']").modal("show");
        console.log($rootScope.user_session)
        params = $scope.cust_search;
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/custhk1?export=1&TYP="+encodeURI("电子银行");
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        params.TYP = "电子银行";
        params.ORG_NO = $rootScope.user_session.branch_code;
        SqsReportService.info('ebkcusthklr', params).success(function(resp) {
            $("div[name='loading']").modal("hide");
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions);
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
    $('#check_dyyxlr').show();
    $('#dyyxlr_modal').modal('show');
    $('#dyyxlr_new_add_button').hide();
    $('#dyyxlr_save_edit_button').hide();
    $scope.tableMessage1 = "请输入客户号";
    };
    $scope.check = function(account){
        if(account == null||account == ''){
            $scope.tableMessage1="客户号不能为空"
        }
        else{
        SqsReportService.info('custhk2',{'CUST_NO':account}).success(function(resp){
        $scope.newdata=resp;
        console.log(resp)
        if (($scope.newdata.rows || []).length > 0) {
                $scope.tableMessage1 = "";
            SqsReportService.info('custhk1',{'CUST_NO':account,'TYP':"电子银行",'ORG_NO':$rootScope.user_session.branch_code}).success(function(resp) {
               $scope.newstaffdata = resp;
                    if ((resp.rows || []).length > 0) {
                        $scope.newstaffdata[0] = resp.rows[0][2];
                        $scope.newstaffdata[1] = resp.rows[0][3];
                        $scope.newstaffdata[2] = resp.rows[0][4];
                        $scope.newstaffdata[3] = resp.rows[0][5].toString();
                        $scope.newstaffdata[4] = resp.rows[0][6].toString();
                        $scope.tableMessage1 = "该客户的当前录入业绩期间在系统中已经存在认定关系，请检查！";
                        $('#dyyxlr_new_add_button').hide();
                    } else {
                        $scope.tableMessage1 = "可以认定，请输入认定员工信息";
                        $scope.newstaffdata = {};
                        $scope.newstaffdata[0] = $rootScope.user_session.user_code;
                        $scope.newstaffdata[1] = $rootScope.user_session.user_name; 
                        $scope.newstaffdata[2] = 100;
                        $scope.newstaffdata[3] = moment();
                        $scope.newstaffdata[4] = "2099-12-31";

                        $('#dyyxlr_new_add_button').show();
                    }
            });
                
            } else {
                $scope.tableMessage1 = "未查询到此客户";
                $('#dyyxlr_new_add_button').hide();
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
        nsd["cust_no"]=$scope.newdata.rows[0][0];
        nsd["cust_in_no"]=$scope.newdata.rows[0][3];
        nsd["org_no"]=$rootScope.user_session.branch_code;
        nsd["start_date"]=$scope.newstaffdata[3].format("YYYYMMDD");
        nsd["end_date"]="20991231";
        nsd["src"]="前端录入";
        nsd["typ"]="电子银行";
        nsd["note"]=$scope.newdata.rows[0][2];
        console.log(nsd)
        var nd = {"newdata":nsd};
        custhkService.save(nd).success(function (reps){
            $scope.search(); 
            $('#dyyxlr_modal').modal('hide');
            alert("录入成功")   
        });
    };
    $scope.to_edit = function(row){
    SqsReportService.info('custhk2',{'CUST_NO':row[4]}).success(function(resp){
    $scope.newdata=resp;
    $scope.tableMessage1 = "";
    }
    );
    
    $('#check_dyyxlr').hide();
    $('#dyyxlr_modal').modal('show');
    $('#dyyxlr_new_add_button').hide();
    $('#dyyxlr_save_edit_button').show();
    $scope.newstaffdata[0] = row[2];
    $scope.newstaffdata[1] = row[3];
    $scope.newstaffdata[2] = row[4];
    $scope.newstaffdata[3] = moment(row[5].toString());
    $scope.newstaffdata[4] = row[6].toString();
    $scope.newstaffdata[6] = row[9];
    };
    $scope.edit_save = function(){
        var nsd ={};
        console.log($scope.newstaffdata)
        nsd["etl_date"]=moment().format("YYYYMMDD");
        nsd["manager_no"]=$scope.newstaffdata[0];
        nsd["cust_no"]=$scope.newdata.rows[0][0];
        nsd["org_no"]=$rootScope.user_session.branch_code;
        var nd = {"newdata":nsd};
        custhkService.ebk_update(nd).success(function (reps){
        $scope.search(); 
        $('#dyyxlr_modal').modal('hide');
        });
        
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
    var nsd={};
    nsd["org_no"]=row[0];
    nsd["manager_no"]=row[2];
    nsd["cust_no"]=row[4];
    var nd = {"newdata":nsd};
        custhkService.ebk_delete(nd).success(function (reps){
        $scope.search(); 
        $('#dyyxlr_modal').modal('hide');
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
        if(files.length==0)
        {
            alert("请先选择对应的文件内容,再导入!")
            return;
        }
        $("div[name='loading']").modal("show");
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
            url : base_url+"/custhk/upload_per_ebank/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("x-session-token", token);
            },   
            success: function(msg){
                $("div[name='loading']").modal("hide");
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

dyyxlrController.$inject = ['$scope','$rootScope','store', '$filter', '$rootScope', 'SqsReportService','custhkService','dictdataService'];

angular.module('YSP').service('dyyxlrController', dyyxlrController);
