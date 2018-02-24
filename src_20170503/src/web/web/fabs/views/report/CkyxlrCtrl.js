/**
 * ckyxlr Controller
 */
function ckyxlrController($scope,store, $filter, $rootScope, SqsReportService,accthkService,dictdataService,custhkService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.spring=[0];
    $scope.tableMessage = "请点击查询";
    $scope.tableMessage1 = "请输入账号";
    $scope.cust_search = {};
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/accthk1?export=1&TYP="+encodeURI("存款");
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
        $scope.total_count = 0;
        $scope.cur_page = 1;
        params = $scope.cust_search;        
        params.FOLLOW_CUST = '账号优先'
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/accthk1?export=1&TYP="+encodeURI("存款");
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
 
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        params.TYP = "存款";
        params.ORG_NO = $rootScope.user_session.branch_code;
        SqsReportService.info('accthklr', params).success(function(resp) {
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
        $('#check_ckyxlr').show();
        $('#chk_btn').show()
        $('#ckyxlr_modal').modal('show');
        $('#Ckyxlr_input').hide();
        $('#Ckyxlr_edit').hide();
        $('#ckyxlr_new_add_button').hide();
        $('#ckyxlr_save_edit_button').hide();
        $('#add_staff_button').hide();
        $('#remove_staff_button').hide();
        $scope.tableMessage1 = "请输入账号";
    };
    $scope.check = function(account,flag){
        if(account == null||account == ''){
            $scope.tableMessage1="账号不能为空"
        }
        else{

        search_no=[];
        if(flag)
            search_no['ACCOUNT_NO']=account;
        else
            search_no['CARD_NO']=account;
        SqsReportService.info('accthk3',search_no).success(function(resp){
        $scope.newdata=resp;
        if (($scope.newdata.rows || []).length > 0) {
        console.log(resp.rows[0][4])
        console.log($rootScope.user_session.branch_code)
            account=resp.rows[0][0];
            if(resp.rows[0][4]!=$rootScope.user_session.branch_code){
                $scope.tableMessage1 = "请录入本网点账户!";
                $('#ckyxlr_new_add_button').hide();
            }
            else{
                $scope.tableMessage1 = "";
                SqsReportService.info('acctcheck',{'account':account,'typ':"存款",'org_no':$rootScope.user_session.branch_code}).success(function(resp) {
                $scope.newstaffdata = resp;
                    if ((resp.rows || []).length > 0) {
                        $scope.tableMessage1 = "该账号的当前录入业绩期间在系统中已经存在挂钩关系或占比已达到100，请检查！"+"员工"+resp.rows[0][1]+"拥有该业绩";
                        $('#ckyxlr_new_add_button').hide();
                    } else {
                        $('#Ckyxlr_input').show();
                        $('#add_staff_button').show();
                        $('#remove_staff_button').show();
                        $scope.tableMessage1 = "可以认定，请输入认定员工信息";
                        $scope.newstaffdata = {};
                        $scope.newstaffdata[2] = 100;
                        $('#ckyxlr_new_add_button').show();
                    }
                });
            }
            } else {
                $scope.tableMessage1 = "未查询到此存款账号";
                $('#ckyxlr_new_add_button').hide();
            }
        });
        }
    };

    $scope.save = function(){
        var per=0;
        var staff=[];
        for (var i=0;i<$scope.spring.length;i++){
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
 
        accthkService.check_manager({'staff':staff,'org_no':$rootScope.user_session.branch_code,'account_no':$scope.newdata.rows[0][0],'typ':'存款'}).success(function (reps){
            if(reps.data=='0'){
                alert('请输入本网点员工!')
                return;
                }
            else{
                var nnsd ={};
                for (var i=0;i<$scope.spring.length;i++){
                    var nsd={}
                    nsd["etl_date"]=moment().format("YYYYMMDD");
                    nsd["manager_no"]=$scope.newstaffdata[i*4+0];
                    nsd["percentage"]=$scope.newstaffdata[i*4+2];
                    nsd["account_no"]=$scope.newdata.rows[0][0];
                    nsd["cust_in_no"]=$scope.newdata.rows[0][1];
                    nsd["note"]=$scope.newdata.rows[0][3];
                    nsd["org_no"]=$rootScope.user_session.branch_code;
                    nsd["status"]="录入待审批";
                    nsd["hook_type"]="管户";
                    nsd["typ"]="存款";
                    nsd["follow_cust"]="账号优先";
                    nsd["src"]=reps.data;
                    nnsd[i]=nsd
                    }
                console.log(nnsd)
                accthkService.ssave({"newdata":nnsd}).success(function (reps){
                    $('#ckyxlr_modal').modal('hide');
                    alert('录入成功！');
                    $scope.search(); 
                });
            }
        });
    };
    $scope.to_edit = function(row){
        SqsReportService.info('accthk3',{'ACCOUNT_NO':row[5]}).success(function(resp){
            $scope.newdata=resp;
            $scope.tableMessage1 = "";
        }
    );
    
        $('#chk_btn').hide();
        $('#check_ckyxlr').hide();
        $('#Ckyxlr_input').hide();
        $('#Ckyxlr_edit').show();
        $('#ckyxlr_modal').modal('show');
        $('#ckyxlr_new_add_button').hide();
        $('#ckyxlr_save_edit_button').show();
        $scope.newstaffdata[0] = row[3];
        $scope.newstaffdata[1] = row[4];
        $scope.newstaffdata[2] = row[7];
        $scope.newstaffdata[6] = row[9];
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
        accthkService.check_manager({'staff':[$scope.newstaffdata[0]],'org_no':$rootScope.user_session.branch_code,'account_no':$scope.newdata.rows[0][0],'typ':'存款'}).success(function (reps){
            if(reps.data=='0'){
                alert('请输入本网点员工!')
                return;
            }
            else{
                var nsd ={};
                nsd["etl_date"]=moment().format("YYYYMMDD");
                nsd["manager_no"]=$scope.newstaffdata[0];
                nsd["percentage"]=$scope.newstaffdata[2];
                nsd["account_no"]=$scope.newdata.rows[0][0];
                nsd["org_no"]=$rootScope.user_session.branch_code;
                nsd["src"]="前端修改";
                nsd["typ"]="存款";
                nsd["id"]=$scope.newstaffdata[6]
                var nd = {"newdata":nsd};
                accthkService.supdate(nd).success(function (reps){
                    if(reps.data=='0'){
                        alert('占比大于100,请检查!')
                        return;
                    }
                    $('#ckyxlr_modal').modal('hide');
                    alert('修改成功！');
                    $scope.search(); 
                });
            }
        });
    };

    $scope.delete = function(row){
        if(confirm("确认删除？")){
        var nsd={};
        nsd["id"]=row[9];
        nsd["org_no"]=row[1];
        nsd["account_no"]=row[5];
        nsd["percent"]=row[7];
        var nd = {"newdata":nsd};
        accthkService.sdelete(nd).success(function (reps){
            $scope.search(); 
            $('#ckyxlr_modal').modal('hide');
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
        var token = store.getSession("token");
        var form = new FormData();
        for(var i = 0 ; i < files.length ; ++i){
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
                alert(msg.data);
            }    
        });  
    }    

   $scope.get_staff_name = function(tt){  //录入时 输入员工号,员工名回显
        custhkService.get_staff_name({'user_name':$scope.newstaffdata[tt*4+0]}).success(function(resp){
            $scope.newstaffdata[tt*4+1] = resp.data.name;
        });
   }
   $scope.uget_staff_name = function(){  //修改时 输入员工号,员工名回显
        custhkService.get_staff_name({'user_name':$scope.newstaffdata[0]}).success(function(resp){
            $scope.newstaffdata[1] = resp.data.name;
        });
   }
   $scope.addstaff = function(){  
       $scope.spring.push($scope.spring[$scope.spring.length-1]+1);
   }
   $scope.removestaff = function(){  
       if($scope.spring.length!=1){
           $scope.spring.pop();
       }
   }

};

ckyxlrController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','accthkService','dictdataService','custhkService'];

angular.module('YSP').service('ckyxlrController', ckyxlrController);
