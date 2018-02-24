/**
 * LoanPreMove Controller
 */
function staffAllHookController($scope, $attrs, $filter, SqsReportService,branchmanageService,gsgxckService,$rootScope) {

    $scope.setOrg = function(val){
        $scope.cust_search.org = val

    }
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
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/StaffAllHook?export=1&login_branch_no="+$rootScope.user_session.branch_code+"&login_teller_no"+$rootScope.user_session.user_code;

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
        params = [];
        if($scope.cust_search.manager==null||$scope.cust_search.manager==""||$scope.cust_search.org==""||$scope.cust_search.org==null) 
        {
            alert('请先选择机构号和柜员号');
            return; } 
        params = $scope.cust_search;
        $("div[name='loading']").modal("show");
        if (params.manager){
            params.manager_no = params.manager;
        }
        else{
            params.manager_no = "";
        }
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/StaffAllHook?export=1";
        console.log($scope.cust_search)
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
                params[key]=$scope.cust_search[key];
                $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        SqsReportService.info('StaffAllHook', params).success(function(resp) {
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
    $scope.find_users = function(){
        branchmanageService.users({'branch_id':$scope.cust_search.org.role_id}).success(function(reps){
        $scope.model2 =reps.data;
                });
    };
     $scope.find_users2 = function(){
            branchmanageService.users({'branch_id':$scope.top_id}).success(function(reps){
                    $scope.model5 =reps.data;
            });
    };

    
    function find_branchs(){
	    branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
            $scope.model1=reps.data;
	    })	
    }
    find_branchs();
   
    var move_element = angular.element('#move_all');
    //批量移交功能
	$scope.add_start_date = moment().add(1,'days');
	$scope.add_end_date = moment("2099-12-30","YYYY-MM-DD");
    $scope.batch_move = function() {
        if($scope.cust_search.org.split(",").length>1)
        {
            alert('转移机构号只能选一个');
            return;
        }
        if($scope.cust_search.manager==null) 
        {
            alert('请先选择柜员信息');
            return;
        }
        $scope.note='';
        $scope.init_branches1();
        if ($rootScope.user_session.branch_code.charAt(0) != 'M'){
                $scope.cust_search.org_tar = $rootScope.user_session.branch_code;
        }
        move_element.modal('show');
    };
    $scope.do_batch_move = function(){
        if($scope.cust_search.org_tar.split(",").length>1)
        {
            alert('转移机构号只能选一个');
            return;
        }
        if($scope.add_manager==null || $scope.add_manager==''){

            alert('请先选择柜员信息');
            return;
        }
        else{
                $("div[name='loading']").modal("show");
                gsgxckService.staff_all_hook_batch_move({'note':$scope.note,'from_branch_no':$scope.cust_search.org_tar, 'from_teller_no':$scope.cust_search.manager,'to_teller_no':$scope.add_manager.user_name}).success(function(resp){
                $scope.search();
                alert('移交成功');
                move_element.modal('hide');
            }).error(function(resp){
            $("div[name='loading']").modal("hide");
            });
         }
    };

    $scope.find_users_by_branches = function(){ 
        $scope.add_manager=$scope.cust_search.org 
        branchmanageService.find_users_by_branches({'branch_id':$scope.cust_search.org}).success(function(reps){
            $scope.model2 =reps.data;
            console.log($scope.model2)
       });
    };
    $scope.find_users_by_branches1 = function(){
        branchmanageService.find_users_by_branches({'branch_id':$scope.cust_search.org_tar}).success(function(reps){
            $scope.model5 =reps.data;
            $scope.add_manager='';
       });
    };

    $scope.show_lt_modal = function(trigger_elem){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal']").modal("show");
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
        $scope.cust_search.org= res_msg;
        $scope.cust_search.org_tar=res_msg;
        $scope.find_users_by_branches();
        $scope.find_users_by_branches1();
        $scope.cust_search.manager = null;
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

        //if ($rootScope.branch_list != null)
        //{
        //    $.fn.zTree.init($("#loan_type_tree"+$scope.subTabId), setting, $rootScope.branch_list);
        //    return;
        //}

        //查询数据库
	    branchmanageService.get_branch_list({'branch_code':$rootScope.user_session.branch_code}).success(function (resp) {
            data = resp.data;
            show_branches(data)
            $.fn.zTree.init($("#loan_type_tree"+$scope.tabId), setting, Nodes);
	    })
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

    $scope.show_lt_modal1 = function(trigger_elem){
        var modal = $("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal1']")
        modal.modal({backdrop:"static",keybord:false});
        element1.modal("hide");
        //$("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal1']").modal("show");
    }

    var element1 = angular.element('#Move_ChoseModal');

    $scope.ztreeBtmConfirm1 = function(){
        var treeObj = $.fn.zTree.getZTreeObj("loan_type_tree1" + $scope.tabId);
        var nodes = treeObj.getCheckedNodes(true);
        var msg = "";
        if(nodes.length >2)
        {
            alert("移交时只能选一个机构号");
            return;
        }
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
        $scope.cust_search.org_tar= res_msg;
        $scope.find_users_by_branches1();
        element1.modal("show");
    }

    $scope.choose_branch_type1 = function(branch_code, branch_name, branch_level){
        $scope.cust_search.org_tar= branch_code.replace(/(^\s*)|(\s*$)/g, "");
        //$scope.ltSelected = true;
    }

    $scope.init_branches1 = function(){
        var tree_html = '<ul id="loan_type_tree1'+$scope.tabId+'" class="ztree"> </ul>';
        angular.element($('#tab_'+ $scope.tabId + '_content').find("div[name='for_lt_tree1']")).append(tree_html);
        var setting = {
            check:{
                enable:true
            }
        }; 
        var Nodes=[];
        var data = [];

        if ($rootScope.branch_list != null)
        {
            $.fn.zTree.init($("#loan_type_tree1"+$scope.subTabId), setting, $rootScope.branch_list);
            return;
        }

        //查询数据库
	    branchmanageService.get_branch_list({'branch_code':$rootScope.user_session.branch_code}).success(function (resp) {
            data = resp.data;
            show_branches(data)
            $.fn.zTree.init($("#loan_type_tree1"+$scope.tabId), setting, Nodes);
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
                        Two.click="choose_branch_type1(this, '"+pro_arr[j].child_branch.branch_code+"', '"+Two.name+"','"+pro_arr[j].child_branch.branch_level+"')";
                        One.children.push(Two);
                    }
                }else{
                    One.name = data[i].child_branch.branch_name.trim();
                    One.id = data[i].child_branch.branch_code;
                    One.pId = data[i].parent_branch.branch_code;
                    One.click="choose_branch_type1(this, '"+data[i].child_branch.branch_code+"', '"+One.name+"','"+data[i].child_branch.branch_level+"')";
                }
                Nodes.push(One);
            }
        }
    }
   
};

staffAllHookController.$inject = ['$scope', '$attrs', '$filter', 'SqsReportService','branchmanageService','gsgxckService','$rootScope'];

angular.module('YSP').service('staffAllHookController', staffAllHookController);

