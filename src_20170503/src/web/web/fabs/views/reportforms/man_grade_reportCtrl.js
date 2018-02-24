/**
 * man_grade_jdg Controller
 */
function man_grade_reportController($scope,store, $filter, $rootScope, SqsReportService,man_gradejdgService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.grade_model = ['助理客户经理', '初级客户经理', '中级客户经理', '高级客户经理', '资深客户经理']
    $scope.cust_search = {};
    $scope.cust_search.login_branch_no = $rootScope.user_session.branch_code;
    $scope.cust_search.login_teller_no = $rootScope.user_session.user_code;
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/man_grade_report?export=1"+ "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code;
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

    $scope.search = function() {
        $("div[name='loading']").modal("show");
        
        params = $scope.cust_search;
        if(params["kyear"]){
            if(!$scope.filterInt(params["kyear"])){
                alert('请输入合法年份,如2016.');
            }
        }
        $scope.total_count = 0;
        $scope.cur_page = 1;

        console.log(params);
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/man_grade_report?export=1"+ "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code;
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!='' && $scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        SqsReportService.info('man_grade_report', params).success(function(resp) {
            $("div[name='loading']").modal("hide");
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions)
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    $scope.filterInt = function(value){
        if(/^([0-9]+)$/.test(value))
            return true;
        return false;
    };
    $scope.add_true = function(){
        $scope.add_grade();
    }
    $scope.caculate = function(){
        $scope.data = [];
        $("div[name='loading']").modal("show");
        $scope.tableMessage = "正在计算";
        $scope.get_score();
    }
    $scope.to_edit = function(row){
        $('#man_grade_report').modal('show');
        $scope.org_name = row[2];
        $scope.name = row[4];
        $scope.adj_grade = row[37]
        $scope.item_id = row[39];
    };
    $scope.delete=function(row){
         if(confirm("确认删除？")){
            man_gradejdgService.delete_man({'row_id':row[39]}).success(function(reps){
                alert(reps.data);
                $scope.search();
            })
        }else{
            alert("确认取消？");
        }
       
    }
    $scope.edit_save = function(){
        if($scope.org_name==''||$scope.name==''||$scope.adj_grade==''){
            alert("信息未填完全,请检查!");
            return;
        }
        man_gradejdgService.update({'item_id':$scope.item_id,'adj_grade':$scope.adj_grade}).success(function (reps){
            $scope.search(); 
            $('#man_grade_report').modal('hide');
            alert(reps.data)
        });
    };
    $scope.upload_excel = function(){
        //console.log($scope.tabId)
        var files = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#elec_arch").prop('files');
        if(files.length==0) {
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
            url : base_url+"/man_gradejdg/upload/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("x-session-token", token);
            },   
            success: function(msg){
                $scope.search();
                console.log(msg);
                alert(msg.data);
                $("div[name='loading']").modal("hide");
            }    
        });  
    }
    $scope.show_lt_modal = function(trigger_elem){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal']").modal("show");
    }
    $scope.find_users_by_branches = function(){
        branchmanageService.find_users_by_branches({'branch_id':$scope.cust_search.org_no}).success(function(reps){
            $scope.model = reps.data;
        })
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
        $scope.cust_search.org_no= res_msg;

        $scope.find_users_by_branches();
        $scope.cust_search.user_name = null;
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
    $scope.get_score = function(){
        man_gradejdgService.get_score({'1':'1'}).success(function(reps){
            $scope.score = reps.data;
            alert(reps.data);
            $("div[name='loading']").modal("hide");
            $scope.tableMessage = "请点击查询";
        })
    }
    $scope.add_grade = function(){
        man_gradejdgService.add_grade({'1':'1'}).success(function(reps){
            alert(reps.data);
        })
    }
};
man_grade_reportController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','man_gradejdgService','branchmanageService'];

angular.module('YSP').service('man_grade_reportController', man_grade_reportController);
