/**
 * branch_grade_jdg Controller
 */
function branch_grade_reportController($scope,store, $filter, $rootScope, SqsReportService,branch_grade_reportService,branchmanageService) {
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
        
        SqsReportService.info('branch_grade_report', params).success(function(resp) {
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
    $scope.calculate = function(){
        $("div[name='loading']").modal("show");
        $scope.get_score();
        $scope.search();
        $("div[name='loading']").modal("hide");
    }
    $scope.to_edit = function(row){
        $('#edit_modal').modal('show');
        $scope.org_name = row[2];
        $scope.name = row[4];
        $scope.adj_grade = row[53]
        $scope.item_id = row[55];
    };
    $scope.edit_save = function(){
        if($scope.adj_grade==''){
            alert("信息未填完全,请检查!");
            return;
        }
        branch_grade_reportService.update({'item_id':$scope.item_id,'adj_grade':$scope.adj_grade}).success(function (reps){
            $scope.search(); 
            $('#edit_modal').modal('hide');
            alert(reps.data)
        });
    };
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
        $scope.cust_search.SALE_CODE = null;
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
        branch_grade_reportService.get_score({'1':'1'}).success(function(reps){
            $scope.score = reps.data;
            alert(reps.data);
        })
    }
    $scope.add_grade = function(){
        branch_grade_reportService.add_grade({'1':'1'}).success(function(reps){
            alert(reps.data);
        })
    }
};
branch_grade_reportController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','branch_grade_reportService','branchmanageService'];

angular.module('YSP').service('branch_grade_reportController', branch_grade_reportController);
