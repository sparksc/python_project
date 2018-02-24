/**
 * addharvestddharvest Controller
 */
ysp.controller("insuranceController",function ($scope,store, $filter, $rootScope, SqsReportService, insuranceService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.login_branch_no = $rootScope.user_session.branch_code;
    $scope.cust_search.login_teller_no = $rootScope.user_session.user_code;
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/insurance_hand?export=1"+ "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code;
    $scope.newstaffdata= {};    
    $scope.change_name = function(target){
       if(target == null){$scope.newstaffdata[2]='';$scope.newstaffdata[3]='';$scope.newstaffdata[4]='';$scope.newstaffdata[5]='';}
       for(var i in $scope.model1){
            if($scope.model1[i].branch_code==target){
                $scope.newstaffdata[2]=$scope.model1[i].branch_name;
                branchmanageService.users({'branch_id':$scope.model1[i].role_id}).success(function(reps){
                    $scope.model3 = reps.data;
                    });
                $scope.newstaffdata[5]=null;
            }
        }
    }
   
    $scope.change_name2 = function(target){
       if(target == null)$scope.newstaffdata[4]='';
       for(var i in $scope.model3){
            if($scope.model3[i].user_name==target){
                $scope.newstaffdata[4]=$scope.model3[i].name;
            }
       } 
    }
    /*
    $scope.change_name3 = function(target){
        if(target == null){
            $scope.newstaffdata[6]='';
        }
        for(var i in $scope.model4){
            if($scope.model4[i].credential_code==target){
                $scope.newstaffdata[6]=$scope.model4[i].credential_name;
            }
        }
    }
    function find_credentials(){
        account_rankService.credentials({'':null}).success(function(resp){
            $scope.model4=resp.data;
            console.log($scope.model4);
        });
    };
    find_credentials();
    */    
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
            $scope.model1=reps.data;
        });
    };
    
    find_branchs();
    console.log($scope.model1);
    $scope.find_users = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.ORG_CODE){role_id=$scope.model1[i].role_id;}
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
    }
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
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
            $scope.parse_paginfo($scope.data.actions);
        });
    };
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
            console.log('---',files[i]);
            form.append('files',files[i]);
        }
        form.append('application_id',$scope.applicationId)
        form.append('about','elec_arch')
        $.ajax({
            type: "POST",
            url : base_url+"/insurance/upload/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
             request.setRequestHeader("x-session-token", token);
           },
           success: function(msg){
            $scope.search();
            $("div[name='loading']").modal("hide");
            console.log(msg);
            alert(msg.data);
          }
        });
     }



    $scope.search = function() {
        console.log($rootScope.user_session)
        $("div[name='loading']").modal("show");
        params = $scope.cust_search;
        if(params["SYEAR"]){
            if(!$scope.filterInt($scope.cust_search.SYEAR)){
                alert("请输入合法年份，如2016");
                $("div[name='loading']").modal("hide");
                $scope.cust_search.SYEAR='';
                return;
            }
        }
        //console.log(params);
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/insurance_hand?export=1"+ "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code;
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!='' && $scope.cust_search[key]!=null){
                params[key]=$scope.cust_search[key];
                $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        $scope.total_count = 0;
        $scope.cur_page = 1;
        SqsReportService.info('insurance_hand', params).success(function(resp) {
            $("div[name='loading']").modal("hide");
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        } );
    };

    $scope.add = function(){
        $scope.newstaffdata[0]='';
        $scope.newstaffdata[1]='';
        $scope.newstaffdata[2]='';
        $scope.newstaffdata[3]='';
        $scope.newstaffdata[4]='';
        $scope.newstaffdata[5]='';
        $scope.newstaffdata[6]='';
        $('#datainput_modal').modal('show');
        $('#datainput_new_add_button').show();
        $('#datainput_save_edit_button').hide();
    };
    $scope.filterInt = function(value){
        if(/^([0-9]+)$/.test(value))
            return true;
        return false;
    };  
    $scope.add_save = function(){
       // console.log($scope.newstaffdata)
        var nsd ={};
        if($scope.newstaffdata[0] == ''||$scope.newstaffdata[1] == ''  || $scope.newstaffdata[2] == '' || $scope.newstaffdata[3] == '' || $scope.newstaffdata[4] == '' || $scope.newstaffdata[5] == '' || $scope.newstaffdata[6]==''){
            alert("输入不能为空");
            return;
        }
        if(!$scope.filterInt($scope.newstaffdata[0])){
            alert("请输入合法年份，如2016");
            return;
        }
        if($scope.newstaffdata[5] < 0){
            alert("请输入正数");
            return;
        }
        //console.log(typeof($scope.newstaffdata[0]));
        console.log($scope.newstaffdata)
        nsd["syear"]=$scope.newstaffdata[0];
        nsd["org_code"]=$scope.newstaffdata[1];
        nsd["org_name"]=$scope.newstaffdata[2];
        nsd["user_code"]=$scope.newstaffdata[3];
        nsd["user_name"]=$scope.newstaffdata[4];
        nsd["count"]=$scope.newstaffdata[5];
        nsd["remarks"]=$scope.newstaffdata[6];
        var org_code = $scope.newstaffdata[1] ,
            user_code = $scope.newstaffdata[3]
        params = {'ORG_CODE':org_code,'USER_CODE':user_code};
        //console.log(params)
        SqsReportService.info('insurance_hand', params).success(function(resp) {
            $scope.data = resp;
            console.log($scope.data)
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
                $scope.search()
                alert("该员工已存在");
            }else{
                $scope.tableMessage = ""
                console.log(nsd)
                var nd = {"newdata":nsd};
                insuranceService.add_save(nsd).success(function (reps){
                    $scope.search(); 
                    $('#datainput_modal').modal('hide');
                    alert(reps.data)
                });
            }
         });
       /* console.log(nsd)
        var nd = {"newdata":nsd};*/
        /*
        data_inputService.add_save(nsd).success(function (reps){
            $scope.search(); 
            $('#datainput_modal').modal('hide');
            alert(reps.data);
        });
        */
    };
    $scope.edit = function(row){
        $('#datainput_modal').modal('show');
        $('#datainput_new_add_button').hide();
        $('#datainput_save_edit_button').show();
        $scope.newstaffdata[0] = row[0];
        $scope.newstaffdata[1] = row[1];
        $scope.newstaffdata[2] = row[2];
        $scope.newstaffdata[3] = row[3];
        $scope.newstaffdata[4] = row[4];
        $scope.newstaffdata[5] = row[5];
        $scope.newstaffdata[6] = row[6];
        $scope.newstaffdata[7] = row[7];
    };
    $scope.edit_save = function(){
        var nsd ={};
        if($scope.newstaffdata[0] == ''||$scope.newstaffdata[1] == ''  || $scope.newstaffdata[2] == '' || $scope.newstaffdata[3] == '' || $scope.newstaffdata[4] == '' || $scope.newstaffdata[5] == '' || $scope.newstaffdata[6]==''){
            alert("输入不能为空");
            return;
        }
        if(!$scope.filterInt($scope.newstaffdata[0])){
            alert("请输入合法年份，如2016");
            return;
        }   
        console.log($scope.newstaffdata)
        nsd["syear"]=$scope.newstaffdata[0];
        nsd["org_code"]=$scope.newstaffdata[1];
        nsd["org_name"]=$scope.newstaffdata[2];
        nsd["user_code"]=$scope.newstaffdata[3];
        nsd["user_name"]=$scope.newstaffdata[4];
        nsd["counts"]=$scope.newstaffdata[5];
        nsd["remarks"]=$scope.newstaffdata[6];
        nsd["item_id"]=$scope.newstaffdata[7];
        /*
        var nd = {"newdata":nsd};*/
        insuranceService.edit_save(nsd).success(function (reps){
             $scope.search(); 
             $('#datainput_modal').modal('hide');
             alert(reps.data)
        });
        
    };
    $scope.del = function(item){
         //console.log(item[6]);
         if(confirm("确认删除？")){
             console.log(item[7]);     
             insuranceService.del({"item_id":item[7]}).success(function (reps){
             //console.log(reps) 
                 $scope.search(); 
                 $('#datainput_modal').modal('hide');
                 alert(reps.data)
             });
         }
         else{
            alert("取消删除");
         }
    };

     $scope.find_users_by_branches = function(){
        branchmanageService.find_users_by_branches({'branch_id':$scope.cust_search.ORG_CODE}).success(function(reps){
            $scope.model2 =reps.data;
       });
    };

    $scope.show_lt_modal = function(trigger_elem){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal']").modal("show");
    }

    var element = angular.element('#cust_hookSearchModal');
    //查找对应页面
    $scope.choose_branch_type = function(branch_code, branch_name, branch_level){
        $scope.cust_search.ORG_CODE= branch_code.replace(/(^\s*)|(\s*$)/g, "");
        $scope.cust_search.branch_name = branch_name.replace(/(^\s*)|(\s*$)/g, "");
        $scope.cust_search.branch_level = branch_level.replace(/(^\s*)|(\s*$)/g, "");
        $scope.ltSelected = false;
        console.log($scope.cust_search.ORG_CODE); 
        console.log($scope.cust_search.branch_name); 
        console.log($scope.cust_search.branch_level); 
    }

    $scope.ztreeBtmConfirm = function(){
        var treeObj = $.fn.zTree.getZTreeObj("loan_type_tree" + $scope.tabId);
        var nodes = treeObj.getCheckedNodes(true);
        var msg = "";
        for(var i=0; i< nodes.length; i++)
        {
            if (nodes[i].id.charAt(0) == 'M')
            {
                continue
            }
            msg = msg + nodes[i].id + ",";
            //msg += nodes[i].id + ":" + nodes[i].name + ":" + nodes[i].pId + "\n";
        }
        res_msg = msg.substring(0, msg.length - 1)
        $scope.cust_search.ORG_CODE= res_msg;

        $scope.find_users_by_branches();
        $scope.cust_search.USER_CODE = null;
        console.log(res_msg);
    }

    $scope.init_branches = function(){
        var tree_html = '<ul id="loan_type_tree'+$scope.tabId+'" class="ztree"> </ul>';
        angular.element($('#tab_'+ $scope.tabId + '_content').find("div[name='for_lt_tree']")).append(tree_html);
        var setting = {
            check:{
                enable:true
            }
        }; 
        var Nodes=[];
        var data = [];
        //查询数据库
	    branchmanageService.get_branch_list({'branch_code':$rootScope.user_session.branch_code}).success(function (resp) {
            data = resp.data;
            show_branches(data)
            $.fn.zTree.init($("#loan_type_tree"+$scope.tabId), setting, Nodes);
	    })
        console.log(data); 
        //生成业务类型列表
        function show_branches(data){
            for(var i = 0 ; i < data.length ; ++i){
                var One = new Object();
                pro_arr = data[i].child_branch;
                One.children=new Array();
                if(pro_arr.length>0){
                    One.name = pro_arr[0].parent_branch.branch_name.trim();
                    One.id = pro_arr[0].parent_branch.branch_code;
                    One.pId = data[i].parent_branch.branch_code;
                    for (var j = 0 ; j < pro_arr.length; ++j){
                        var Two = new Object();
                        Two.name=pro_arr[j].child_branch.branch_name.trim();
                        Two.id=pro_arr[j].child_branch.branch_code;
                        Two.pId=pro_arr[j].parent_branch.branch_code;
                        Two.click="choose_branch_type(this, '"+pro_arr[j].child_branch.branch_code+"', '"+Two.name+"','"+pro_arr[j].child_branch.branch_level+"')";
                        One.children.push(Two);
                    }
                }else{
                    One.name = data[i].child_branch.branch_name.trim();
                    One.id = data[i].child_branch.branch_code;
                    One.pId = data[i].parent_branch.branch_code;
                    One.click="choose_branch_type(this, '"+data[i].child_branch.branch_code+"', '"+One.name+"','"+data[i].child_branch.branch_level+"')";
                }
                Nodes.push(One);
            }
        }
    }
    $scope.init_branches();

    $scope.isManager = function() {
        $scope.flag=false;
        branchmanageService.get_user_permission({'user_id':$rootScope.user_session.user_id}).success(function(reps){
            if(reps.data>0)$scope.flag=true;
        });    
    }
    $scope.isManager();

});

