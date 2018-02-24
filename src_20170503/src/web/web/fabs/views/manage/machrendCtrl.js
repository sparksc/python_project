/**
 *  machrend  Controller
 */
function machrendController($scope, $rootScope, $attrs, $filter, SqsReportService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    
    $scope.add_start_date = moment();
    $scope.add_end_date = moment();

    
    $scope.cust_search = {};
    $scope.cust_search.login_branch_no = $rootScope.user_session.branch_code;
    $scope.cust_search.login_teller_no = $rootScope.user_session.user_code;
    $scope.tableMessage = "请点击查询";
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/machrend?export=1";

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
    $scope.cust_search.hide = 1;
    $scope.search = function() {
        $("div[name='loading']").modal("show");
        params = $scope.cust_search;
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/machrend?export=1";
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
                params[key]=$scope.cust_search[key];
                $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]

            }
        }

        SqsReportService.info('machrend', params).success(function(resp) {
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
    $scope.current_user = '';
    $scope.permission = function(){
        branchmanageService.permission({'user_name':$rootScope.user_session.user_code}).success(function(reps){
            $scope.current_user = reps.data;
        });
    };
    $scope.permission();
    
    //显示按钮
    $scope.show = function (item){
        if($scope.current_user){
            var r = confirm("确定显示？");
            if(r == true){
                branchmanageService.show({'cust_id':item[8]}).success(function(reps){
                    alert(reps.data);
                    $scope.search();
                })
            }else{
                alert("取消显示");
            }
        }else{
            alert('此用户无权限！');
        }
    };
    //隐藏按钮
    $scope.hide = function (item) {
        if($scope.current_user){
            var r = confirm("确定隐藏？");
            if(r == true){
                branchmanageService.hide({'cust_id':item[8]}).success(function(reps){
                    alert(reps.data);
                    $scope.search();
                })
            }else{
                alert("取消隐藏");
            }
        }else{
            alert('此用户无权限！');
        }
    };
    var move_element =angular.element(document.getElementById($scope.subTabId)).find('#move_modal');
    $scope.do_allot = function () {
        if($scope.add_manager==''||$scope.add_manager==null){
            alert("请选择柜员移交");
            return;
        };
        branchmanageService.do_allot({'typ':'贷款','cust_id':$scope.cust_id,'to_teller_no':$scope.add_manager.user_name}).success(function(reps){
            alert(reps.data);
            move_element.modal("hide");
            $scope.search();
        })
    }
    $scope.allot = function(item) {
        if ($scope.current_user){
            $scope.add_manager = '';
            $scope.cust_id = item[8];
            branchmanageService.show_org({'cust_id':item[8]}).success(function(reps){
                $scope.cust_search.org_tar = reps.data;
                $scope.find_users_by_branches1();
            })
            move_element.modal("show");
        }else{
            alert('此用户无权限！');
        }
    };
    var modal1 = $("#"+ $scope.subTabId).find("div[name='loan_type_modal1']");
    $scope.show_lt_modal1 = function(trigger_elem){
        modal1.modal("show");
        move_element.modal("hide");
    };
    $scope.ztreeBtmClose1 = function () {
        modal1.modal("hide");
        move_element.modal("show");
    };
    $scope.find_users_by_branches1 = function(){
        branchmanageService.find_users_by_branches({'branch_id':$scope.cust_search.org_tar}).success(function(reps){
            $scope.model5 =reps.data;
       });
    };
    $scope.ztreeBtmConfirm1 = function(){
        var treeObj = $.fn.zTree.getZTreeObj("loan_type_tree1" + $scope.subTabId);

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
        $scope.cust_search.org_tar= res_msg;
        modal1.modal("hide");
        move_element.modal("show");   
        $scope.find_users_by_branches1();
        $scope.add_manager = null;
        $scope.add_manager_no= null;
    };
    $scope.choose_branch_type1 = function(branch_code, branch_name, branch_lecel){
        $scope.cust_search.org_tar = branch_code.replace(/(^\s*)|(\s*$)/g, "");
        $scope.ltSelected = false;
    };
    $scope.init_branches1 = function(){
        var tree_html = '<ul id="loan_type_tree1'+$scope.subTabId+'" class="ztree"> </ul>';
        angular.element($('#'+ $scope.subTabId).find("div[name='for_lt_tree1']")).append(tree_html);
        var setting = {
            check:{
                enable:true
            }
        };
        if ($rootScope.branch_list != null){
            $.fn.zTree.init($("#loan_type_tree1"+$scope.subTabId),setting,$rootScope.branch_list);
            return;
        }
        var Nodes=[];
        var data = [];
        //查询数据库
	    branchmanageService.get_branch_list({'branch_code':$rootScope.user_session.branch_code}).success(function (resp) {
            data = resp.data;
            show_branches(data)
            $.fn.zTree.init($("#loan_type_tree1"+$scope.subTabId), setting, Nodes);
	    })
            $.fn.zTree.init($("#loan_type_tree1"+$scope.subTabId), setting, Nodes);
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
            };
        };
    };
    $scope.init_branches1();
    $scope.find_users = function(){
        branchmanageService.users({'branch_id':$scope.cust_search.ORG_NO.role_id}).success(function(reps){
            $scope.model2 =reps.data;
       });
    };
    $scope.find_users_by_branches = function(){
        branchmanageService.find_users_by_branches({'branch_id':$scope.cust_search.ORG_NO}).success(function(reps){
            $scope.model2 =reps.data;
       });
    };

    $scope.show_lt_modal = function(trigger_elem){
        //$("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal']").modal("show");
        $("#"+$scope.subTabId).find("div[name='loan_type_modal']").modal("show");
    }

    var element = angular.element('#cust_hookSearchModal');
    //查找对应页面
    $scope.choose_branch_type = function(branch_code, branch_name, branch_level){
        $scope.cust_search.ORG_NO = branch_code.replace(/(^\s*)|(\s*$)/g, "");
        $scope.cust_search.branch_name = branch_name.replace(/(^\s*)|(\s*$)/g, "");
        $scope.cust_search.branch_level = branch_level.replace(/(^\s*)|(\s*$)/g, "");
        $scope.ltSelected = false;
    }

    $scope.ztreeBtmConfirm = function(){
        var treeObj = $.fn.zTree.getZTreeObj("loan_type_tree" + $scope.subTabId);
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
        $scope.cust_search.ORG_NO = res_msg;

        $scope.find_users_by_branches();
    }

    $scope.init_branches = function(){
        var tree_html = '<ul id="loan_type_tree'+$scope.subTabId+'" class="ztree"> </ul>';
        angular.element($('#'+ $scope.subTabId).find("div[name='for_lt_tree']")).append(tree_html);
        var setting = {
            check:{
                enable:true
            }
        }; 

        if ($rootScope.branch_list != null)
        {
            $.fn.zTree.init($("#loan_type_tree"+$scope.subTabId), setting, $rootScope.branch_list);
            return;
        }

        var Nodes=[];
        var data = [];
        //查询数据库
	    branchmanageService.get_branch_list({'branch_code':$rootScope.user_session.branch_code}).success(function (resp) {
            data = resp.data;
            show_branches(data)
            $.fn.zTree.init($("#loan_type_tree"+$scope.subTabId), setting, Nodes);
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
};

machrendController.$inject = ['$scope', '$rootScope', '$attrs', '$filter', 'SqsReportService','branchmanageService'];

angular.module('YSP').service('machrendController', machrendController);

