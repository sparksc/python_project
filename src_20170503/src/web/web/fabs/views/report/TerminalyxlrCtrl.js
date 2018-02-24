/**
 * terminalyxlr Controller
 */
function terminalyxlrController($scope,store, $filter, $rootScope, SqsReportService,custhkService,branchmanageService) {
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
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        params.ORG_NO = $rootScope.user_session.branch_code;
        SqsReportService.info('mach_input', params).success(function(resp) {
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
        $scope.newdata={};
        $scope.newstaffdata={};
        $scope.add_zh = '';
        $scope.input_teller_no = '';
        $scope.input_teller_name = '';
        $('#check_terminalyxlr').show();
        $('#terminalyxlr_modal').modal('show');
        $('#terminalyxlr_new_add_button').hide();
        $('#terminalyxlr_save_edit_button').hide();
        $scope.tableMessage1 = "请输入机具编号";
    };
    $scope.check = function(account){
        if(account == null||account == ''){
            $scope.tableMessage1="机具编号不能为空"
        }
        else{
            SqsReportService.info('atm_input',{'ATM_NO':account}).success(function(resp){
            $scope.newdata=resp;
            console.log(resp)
            if (($scope.newdata.rows || []).length > 0) {
                $scope.tableMessage1 = "";
                SqsReportService.info('atmrendcheck',{'CUST_IN_NO':account,'TYP':"机具",'ORG_NO':$rootScope.user_session.branch_code}).success(function(resp) { //检查是否存在待认定
                    $scope.newstaffdata = resp;
                    if ((resp.rows || []).length > 0) {
                        $scope.tableMessage1 = "";
                        $('#terminalyxlr_new_add_button').show();
                    } else {
                        $scope.tableMessage1 = "待认定数据不存在或已经存在认定关系，请检查！";
                        $('#terminalyxlr_new_add_button').hide();
                    }
            });
                
            } else {
                $scope.tableMessage1 = "未查询到此机具信息";
                $('#terminalyxlr_new_add_button').hide();
            }
        });
        }
    };

    $scope.save = function(){
        console.log($scope.newstaffdata)
        console.log($scope.input_teller_no)
        console.log($rootScope.user_session.branch_code)
        custhkService.check_manager({'staff':[$scope.input_teller_no],'org_no':$rootScope.user_session.branch_code,'cust_no':$scope.add_zh,'typ':'ATM'}).success(function (reps){
            if(reps.data=='0'){
                alert('请输入本网点员工!')
                return;
            }
            else{
            custhkService.ssave_with_cust_hook({"cust_hook_id": $scope.newstaffdata.rows[0][0], "manager_no": $scope.input_teller_no}).success(function (reps){
            $scope.search();
            $('#terminalyxlr_modal').modal('hide');
            });
            }   
        });
    };
    $scope.to_edit = function(row){
        $scope.tableMessage1 = "";
        $('#check_terminalyxlr').hide();
        $('#terminalyxlr_modal').modal('show');
        $('#terminalyxlr_new_add_button').hide();
        $('#terminalyxlr_save_edit_button').show();

        $scope.input_teller_no = row[2];
        $scope.input_teller_name = row[3];
        $scope.newstaffdata[6] = row[9];
    };

    $scope.edit_save = function(){
        if ($scope.input_teller_no == null || $scope.input_teller_no == '' || $scope.input_teller_name == null || $scope.input_teller_name == '')
        {
            alert('请输入员工信息')
            return;
        }
        var nsd ={};
        console.log($scope.newstaffdata)
        nsd["etl_date"]=moment().format("YYYYMMDD");
        nsd["manager_no"]= $scope.input_teller_no;
        nsd["id"]=$scope.newstaffdata[6]
        var nd = {"newdata":nsd};
        custhkService.update(nd).success(function (reps){
            $scope.search(); 
            $('#terminalyxlr_modal').modal('hide');
        });
    };

    $scope.delete = function(row){
    if(confirm("确认删除？")){
        var nsd={};
        nsd["id"]=row[9];
        var nd = {"newdata":nsd};
        custhkService.delete(nd).success(function (reps){
            $scope.search(); 
            $('#terminalyxlr_modal').modal('hide');
        });
        }
    };

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
            url : base_url+"/custhk/upload/",
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
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
        });
    };
    find_branchs();    
    $scope.find_users = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.ORG_NO){role_id=$scope.model1[i].role_id;}
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
        $scope.cust_search.STAFF_CODE = null;
    }

   $scope.get_staff_name = function(){  //录入时 输入员工号,员工名回显
        custhkService.get_staff_name({'user_name':$scope.input_teller_no}).success(function(resp){
            $scope.input_teller_name = resp.data.name;
        });
   }

};

terminalyxlrController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','custhkService','branchmanageService'];

angular.module('YSP').service('terminalyxlrController', terminalyxlrController);
