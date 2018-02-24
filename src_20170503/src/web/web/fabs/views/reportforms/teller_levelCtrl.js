/**
 * teller_levelController
 */
function teller_levelController($scope,$rootScope, $filter, SqsReportService,store,branchmanageService,depappointService,teller_levelService) {
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
    $scope.cust_search.DATE_ID = moment();
    $scope.newstaffdata = {};
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.parse_paginfo($scope.data.actions);
            $scope.data = resp;
        });
    };
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/compsleep?export=1"+"&DATE_ID="+ $scope.cust_search.DATE_ID.format("YYYYMMDD") + "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code;
    $scope.search = function() {
        do_search(); 

    };

    init();

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
    $scope.filterInt = function(value){
        if(/^([0-9]+)$/.test(value))
            return true;
        return false;
    };

    function do_search(){
        $("div[name='loading']").modal("show");
        params = $scope.cust_search;

        if(params["SYEAR"]){
            if(!$scope.filterInt(params["SYEAR"])){
                alert('请输入合法年份,如2016.');
            }
        }

        $scope.data = {};
        params.login_branch_no = $rootScope.user_session.branch_code;
        params.login_teller_no = $rootScope.user_session.user_code;
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/compsleep?export=1"+"&DATE_ID="+ $scope.cust_search.DATE_ID.format("YYYYMMDD") + "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code;
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
                params[key]=$scope.cust_search[key];           
                $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }

        SqsReportService.info('teller_level', params).success(function(resp) {
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
    
    $scope.calculate = function(){
        $("div[name='loading']").modal("show");
        teller_levelService.calculate({}).success(function(resp){
            $scope.search();
            alert(resp.data);
            $("div[name='loading']").modal("hide");
        });                                                        
    };
   
    $scope.affirm = function(){
        $("div[name='loading']").modal("show");
        teller_levelService.affirm({}).success(function(resp){
            $scope.search();
            alert(resp.data);
            $("div[name='loading']").modal("hide");
       }); 
    };
    $scope.change_level = function(row){
         $('#teller_level_modal').modal('show');
         $('#teller_level_new_add_button').hide();
         $('#teller_level_save_edit_button').show();
         console.log(row);
         $scope.newstaffdata[0] = row[40];
         $scope.newstaffdata[1] = row[43];
         console.log($scope.newstaffdata);
    };
    $scope.change_save = function(){
        var nsd = {};
        if($scope.newstaffdata[0] == ''){
            alert("不能为空!");
            return;
        }
        console.log($scope.newstaffdata);
        nsd["adj_level"]=$scope.newstaffdata[0];
        nsd["item_id"]=$scope.newstaffdata[1];
        console.log(nsd);
        teller_levelService.change_save(nsd).success(function (reps){
            $scope.search();
            $('#teller_level_modal').modal('hide');
            alert(reps.data)
        });
    };
    $scope.find_users = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.jgbhh){role_id=$scope.model1[i].role_id;}
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
        $scope.cust_search.ygghh = null;
    }
    function init(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
            $scope.model1=reps.data;
        });
    };


    $scope.find_users_by_branches = function(){
        branchmanageService.find_users_by_branches({'branch_id':$scope.cust_search.org}).success(function(reps){
            $scope.model2 =reps.data;
       });
    };

    $scope.show_lt_modal = function(trigger_elem){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal']").modal("show");
    }

    var element = angular.element('#cust_hookSearchModal');
    //查找对应页面
    $scope.choose_branch_type = function(branch_code, branch_name, branch_level){
        $scope.cust_search.org= branch_code.replace(/(^\s*)|(\s*$)/g, "");
        $scope.cust_search.branch_name = branch_name.replace(/(^\s*)|(\s*$)/g, "");
        $scope.cust_search.branch_level = branch_level.replace(/(^\s*)|(\s*$)/g, "");
        $scope.ltSelected = false;
        console.log($scope.cust_search.org); 
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
        $scope.cust_search.org= res_msg;

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

    $scope.isManager = function() {
        $scope.flag=false;
        branchmanageService.get_user_permission({'user_id':$rootScope.user_session.user_id}).success(function(reps){
            if(reps.data>0)$scope.flag=true;
        });    
    }
    $scope.isManager();
};

teller_levelController.$inject = ['$scope', '$rootScope','$filter', 'SqsReportService','store','branchmanageService','depappointService','teller_levelService'];
angular.module('YSP').service('teller_levelController', teller_levelController);
