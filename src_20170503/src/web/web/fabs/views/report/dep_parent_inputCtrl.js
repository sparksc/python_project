/**
 * DepParentInput Controller
 */
function DepParentInputController($scope,store, $filter, $rootScope, SqsReportService,custhkService,accthkService,dictdataService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    $scope.spring=[0];
    $scope.tableMessage = "请点击查询";
    $scope.tableMessage1 = "请输入主账号";
    $scope.cust_search = {};
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/custhk1?export=1&TYP="+encodeURI("汇集户");
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
        params = $scope.cust_search;
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/custhk1?export=1&TYP="+encodeURI("汇集户");
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        params.TYP = "汇集户";
        params.ORG_NO = $rootScope.user_session.branch_code;
        SqsReportService.info('dep_parent_input', params).success(function(resp) {
            $("div[name='loading']").modal("hide");
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
                $scope.parse_paginfo($scope.data.actions);
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };

    $scope.add = function(){
        $scope.spring=[0];
        $scope.newdata={};
        $scope.newstaffdata={};
        $scope.add_zh = '';
        $('#check_ckhjhlr').show();
        $('#ckhjhlr_modal').modal('show');
        $('#Ckhjhlr_input').hide();
        $('#Ckhjhlr_edit').hide();
        $('#ckhjhlr_new_add_button').hide();
        $('#ckhjhlr_save_edit_button').hide();
        $scope.tableMessage1 = "请输入账号";
    };
    $scope.check = function(account){
        $scope.account_no = account
        if(account == null||account == ''){
            $scope.tableMessage1="账号不能为空"
        }
        else{
        SqsReportService.info('dep_parent_check',{'ACCOUNT_NO':account}).success(function(resp){
        $scope.newdata=resp;
        if (($scope.newdata.rows || []).length > 0) {
        console.log(resp.rows[0][4])
        console.log($rootScope.user_session.branch_code)
            if(resp.rows[0][4]!=$rootScope.user_session.branch_code){
                $scope.tableMessage1 = "请录入本网点账户!";
                $('#ckhjhlr_new_add_button').hide();
            }
            else{
                $scope.tableMessage1 = "";
                SqsReportService.info('dep_parent_hkcheck',{'account_no':account,'org_no':$rootScope.user_session.branch_code}).success(function(resp) {
                $scope.newstaffdata = resp;
                    if ((resp.rows || []).length > 0) {
                        $scope.tableMessage1 = "该账号的当前录入业绩期间在系统中已经存在挂钩关系或占比已达到100，请检查！"+"员工"+resp.rows[0][1]+"拥有该业绩";
                        $('#ckhjhlr_new_add_button').hide();
                    } else {
                        $('#Ckhjhlr_input').show();
                        $('#add_staff_button').show();
                        $('#remove_staff_button').show();
                        $scope.tableMessage1 = "可以认定，请输入认定员工信息";
                        $scope.newstaffdata = {};
                        $scope.newstaffdata[2] = 100;
                        $('#ckhjhlr_new_add_button').show();
                    }
                });
            }
            } else {
                $scope.tableMessage1 = "未查询到此汇集户账号";
                $('#ckhjhlr_new_add_button').hide();
            }
        });
        }
    };

    $scope.save = function(){
        var flag=0;
        var per=0;
        var staff=[];

        for (var i=0;i<$scope.spring.length;i++){
            if($scope.newstaffdata[i*4+3]=='是')
                flag=flag+1;
                console.log($scope.newstaffdata[i*4+3])
            if($scope.newstaffdata[i*4+1]==null||$scope.newstaffdata[i*4+1]==''){
                alert('请输入完整的员工信息');
                return;
            }
            if($scope.newstaffdata[i*4+2]==null||$scope.newstaffdata[i*4+2]==''){
                alert('请输入分配比例！');
                return;
            }
            per = per + parseInt($scope.newstaffdata[i*4+2]);
            staff.push($scope.newstaffdata[i*4]);
        }
        if(per>100){
            alert('总比例不能超过100,请检查!')
            return;
            }
        else {
        custhkService.check_manager({'staff':staff,'org_no':$rootScope.user_session.branch_code,'account_no':$scope.newdata.rows[0][0],'typ':'汇集户'}).success(function (reps){
            if(reps.data=='0'){
                alert('请输入本网点员工!')
                return;
                }
            else
                {
                var nnsd ={};
                for (var i=0;i<$scope.spring.length;i++){
                    var nsd ={};
                    if($scope.newstaffdata[i*4+3]=='否'&&$scope.newdata.rows[0][3].substring(0,2)=='82')
                        nsd["hook_type"]='分润'
                    else
                        nsd["hook_type"]='管户';
                    nsd["manager_no"]=$scope.newstaffdata[i*4+0];
                    nsd["percentage"]=$scope.newstaffdata[i*4+2];
                    nsd["account_no"]=$scope.account_no;
                    nsd["note"]=$scope.newdata.rows[0][2];
                    nsd["cust_in_no"]=$scope.newdata.rows[0][3];
                    nsd["status"]="录入待审批";
                    nsd["typ"]="汇集户";
                    nsd["etl_date"]=moment().format("YYYYMMDD");
                    nsd["org_no"]=$rootScope.user_session.branch_code;
                    nsd["src"]=reps.data;
                    var nd = {"newdata":nsd};
                    nnsd[i]=nsd
                    }
                accthkService.parent_save({'newdata':nnsd}).success(function (reps){     //custhook挂钩
                        $('#ckhjhlr_modal').modal('hide');
                        $scope.search(); 
                        alert('录入成功！');
                    });
                }
                });
                }
    };
    $scope.to_edit = function(row){
        SqsReportService.info('dep_parent_check',{'CUST_NO':row[5]}).success(function(resp){
        $scope.newdata=resp;
        $scope.tableMessage1 = "";
        }
        );
        
        $('#Ckhjhlr_input').hide();
        $('#Ckhjhlr_edit').show();
        $('#check_ckhjhlr').hide();
        $('#ckhjhlr_modal').modal('show');
        $('#ckhjhlr_new_add_button').hide();
        $('#ckhjhlr_save_edit_button').show();
        $('#update_per').show();
        if(row[4]=='对私'){
            $('#update_per').hide();
        }
        $scope.newstaffdata[0] = row[2];
        $scope.newstaffdata[1] = row[3];
        $scope.newstaffdata[2] = row[8];
        $scope.newstaffdata[6] = row[10];
    };
    $scope.edit_save = function(){
        if($scope.newstaffdata[1]==null||$scope.newstaffdata[1]==''){
            alert('请输入完整的员工信息');
            return;
        }
        if($scope.newstaffdata[2]==null||$scope.newstaffdata[2]==''){
            alert('请输入分配比例！');
            return;
        }
        custhkService.check_manager({'staff':[$scope.newstaffdata[0]],'org_no':$rootScope.user_session.branch_code,'account_no':$scope.account_no,'typ':'汇集户'}).success(function (reps){
            if(reps.data=='0'){
                alert('请输入本网点员工!')
                return;
            }
        else{
            var nsd ={};
            nsd["etl_date"]=moment().format("YYYYMMDD");
            nsd["manager_no"]=$scope.newstaffdata[0];
            nsd["percentage"]=$scope.newstaffdata[2];
            nsd["account_no"]=account_no;
            nsd["org_no"]=$rootScope.user_session.branch_code;
            nsd["src"]="前端修改";
            nsd["typ"]="汇集户";
            nsd["id"]=$scope.newstaffdata[6]
            var nd = {"newdata":nsd,'date_id':'20150103'};
            accthkService.supdate(nd).success(function (reps){
                if(reps.data==0){
                    alert('占比大于100,请检查!')
                    return;
                }
                $('#ckhjhlr_modal').modal('hide');
                alert('修改成功！');
                $scope.search(); 

            //处理对应账号
            });
        }
        });
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
    var nsd={};
    nsd["id"]=row[10];
    nsd["account_no"]=row[5];
    nsd["manager_no"]=row[2];
    nsd["org_no"]=row[0];
    nsd["percent"]=row[8];
    var nd = {"newdata":nsd};
        accthkService.parent_delete(nd).success(function (reps){
        $scope.search(); 
        $('#ckhjhlr_modal').modal('hide');
        });
        }
    };

    function find_dict(){
	dictdataService.get_dict({'dict_type':'CKTYPE'}).success(function (reps) {
        $scope.model3=reps.data;
	});	
    }

    $scope.searchEle = function(){
        imageService.pdfile_query($scope.applicationId,'elec_arch').success(function(resp){
                $scope.pdf_list  = resp.data;      
        });
    }
    $scope.upload_excel = function(){
        var files = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#elec_arch").prop('files');
        if(files.length==0)
        {
            alert("请先选择对应的文件内容,再导入!");
            return;
        }
        $("div[name='loading']").modal("show");
        var token = store.getSession("token");
        var form = new FormData();
        for(var i = 0 ; i < files.length ; ++i){
            form.append('files',files[i]);
        }
        form.append('application_id',$scope.applicationId)
        form.append('about','elec_arch')
        $.ajax({
            type: "POST",
            url : base_url+"/custhk/upload_per_cust/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("x-session-token", token);
            },   
            success: function(msg){
                $("div[name='loading']").modal("hide");
                alert(msg.data);
            }    
        });  
    }    

    $scope.get_staff_name = function(tt){  //录入时 输入员工号,员工名回显
         custhkService.get_staff_name({'user_name':$scope.newstaffdata[tt*4]}).success(function(resp){
             $scope.newstaffdata[tt*4+1] = resp.data.name;
         });
    }
    $scope.uget_staff_name = function(tt){  //修改时 输入员工号,员工名回显
         custhkService.get_staff_name({'user_name':$scope.newstaffdata[0]}).success(function(resp){
             $scope.newstaffdata[1] = resp.data.name;
         });
    }
    $scope.addstaff = function(){  
        $scope.spring.push($scope.spring[$scope.spring.length-1]+1);
        $scope.newstaffdata[($scope.spring.length-1)*4+3]='否'
    }
    $scope.removestaff = function(){  
        if($scope.spring.length!=1){
            $scope.spring.pop();
        }
    }

};

DepParentInputController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','custhkService','accthkService','dictdataService'];

angular.module('YSP').service('DepParentInputController', DepParentInputController);
