/**
 * PosPreMove Controller
 */
function PosPreMoveController($scope, $attrs, $filter, SqsReportService,branchmanageService,gsgxckService,$rootScope) {

    $scope.init = function (){
        $rootScope.addSubTab(0,'提交','<div ng-include="\'views/manage/PosPreMove.html\'"> </div>',{},false,{'status':'预提交审批'}); 
        $rootScope.addSubTab(1,'POS转移','<div ng-include="\'views/manage/PosPreMove.html\'"> </div>',{},false,{'status':'正常'}); 
        $rootScope.subTabFocus(1);
    }
    if($attrs.init == 'yes'){
        $scope.init();
        return ;
    }
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
   // $scope.cust_search.e_p_OPEN_DATE = moment();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
            $scope.parse_paginfo($scope.data.actions);
        });
    };
    
    $scope.parse_paginfo = function(actions){

        //   console.log(actions);
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
        params['status'] = $scope.status;
        if (params.manager){
            params.manager_no = params.manager.user_name;
        }
        else{
            params.manager_no = "";
        }
        params.typ = 'POS'
        $scope.data = {};
        $scope.total_count = 0;
        $scope.cur_page = 1;
        $scope.tableMessage = "正在查询";
        console.log(params)
        SqsReportService.info('CustMove', params).success(function(resp) {
            $("div[name='loading']").modal("hide");
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
	//}
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
   
    $scope.choseArr = [];
    $scope.checked_row = function(row_id, rows){
          if($scope.choseArr.indexOf(row_id)==-1){
             $scope.choseArr.push(row_id);
          }else{
             $scope.choseArr.splice($scope.choseArr.indexOf(row_id), 1);
          }


          $scope.checkedAllFlag = true;
          angular.forEach(rows, function(item){
               if($scope.choseArr.indexOf(item[0])==-1){
                  $scope.checkedAllFlag = false;
              }
          });
    }
    $scope.isChecked = function(row_id){
         return $scope.choseArr.indexOf(row_id) != -1; 
    }
    $scope.checkedAll = function(checkedFlag, rows){
         angular.forEach(rows, function(item){
             if(checkedFlag){
                 if($scope.choseArr.indexOf(item[0])==-1){
                    $scope.choseArr.push(item[0]);
                 }
             }else{
                 $scope.choseArr.splice($scope.choseArr.indexOf(item[0]), 1);
             }
         });
    }
    var move_element =angular.element(document.getElementById($scope.subTabId)).find('#move_ckgsplzy1');
    //批量移交功能
	$scope.add_start_date = moment().add(1,'days');
	$scope.add_end_date = moment("2099-12-30","YYYY-MM-DD");
    $scope.batch_move = function() {
        if($scope.choseArr.length == 0) 
        {
            alert('请先选择客户信息');
            return;
        }

        $scope.note='';
        $scope.total_exist_avg_amount = "正在查询";
        $scope.total_add_avg_amount = "正在查询";
        $scope.total_balance = "正在查询";
        $scope.total_sum = "正在查询";

        console.log($scope.choseArr[0])
        $scope.init_branches1();
        if ($rootScope.user_session.branch_code.charAt(0) != 'M'){
            $scope.cust_search.org_tar = $rootScope.user_session.branch_code;
            $scope.find_users_by_branches1();
            }
        gsgxckService.get_top_cust({'id':$scope.choseArr[0]}).success(function (reps) {
            console.log(reps.data)
            $scope.top_org = reps.data[0].org_no;    
            branchmanageService.branch({'org':$scope.top_org}).success(function (reps) {
                $scope.add_org=reps.data[0].branch_name;
                console.log("element",$rootScope);
                gsgxckService.batch_account_move_sum_with_hook({'update_key':$scope.choseArr,'follow_cust':'客户号优先'}).success(function (reps) {
                    $scope.total_sum = reps.data.total_sum;
                    $scope.staff = reps.data.staff;
                    move_element.modal('show');
                });

                add_start_date = moment().format('YYYY-MM-DD');
                $scope.add_manager = '';
                $scope.top_id = reps.data[0].role_id;
            }); 
        });
    };
    $scope.newdata = {};
    $scope.batch_move_before = function(){
        if($scope.choseArr.length == 0) 
        {
            alert('请先选择客户信息');
            return;
        }
        gsgxckService.batch_cust_move_before({'update_key':$scope.choseArr}).success(function(resp){
            $scope.search();
            alert(resp.data+'\n条数:'+$scope.choseArr.length);
            $scope.choseArr =[];
        });
    };
    $scope.batch_move_delete = function(){
        if($scope.choseArr.length == 0) 
        {
            alert('请先选择客户信息');
            return;
        }
        gsgxckService.batch_cust_move_delete({'update_key':$scope.choseArr}).success(function(resp){
            $scope.search();
            alert(resp.data);
            $scope.choseArr = [];
        });
    };

    $scope.do_batch_move = function(){

        if($scope.add_manager== null || $scope.add_manager== '')
        {
            alert('请先选择机构和柜员');
            return;
        }
        $scope.newdata.end_date = moment().format('YYYY-MM-DD');
        $scope.newdata.org_no = $scope.org_tar;        
        $scope.newdata.manager_no = $scope.add_manager.user_name;
        $scope.newdata.start_date = $scope.add_start_date.format('YYYY-MM-DD');
        $scope.newdata.end_date = $scope.add_end_date.format('YYYY-MM-DD');
        $("div[name='loading']").modal("show");
        gsgxckService.batch_cust_move({'typ':'POS','note':$scope.note,'update_key':$scope.choseArr,'from_teller_no':$scope.staff,'to_teller_no':$scope.add_manager.user_name}).success(function(resp){
            alert(resp.data);
            move_element.modal('hide');
	        $scope.search();
            //$("div[name='loading']").modal("hide")
            $scope.choseArr = [];
            $scope.checkedAllFlag = false;
        }).error(function(resp){
        $("div[name='loading']").modal("hide")
        })
    };
    $scope.find_users_by_branches = function(){
        branchmanageService.find_users_by_branches({'branch_id':$scope.cust_search.ORG_NO}).success(function(reps){
            $scope.model2 =reps.data;
       });
    };

    $scope.show_lt_modal = function(trigger_elem){
        //"#tab_"+ $scope.tabId + "_content"
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

        $scope.cust_search.manager = null;
        $scope.cust_search.manager_no = null;
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

    $scope.show_lt_modal1 = function(trigger_elem){
        var modal = $("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal1']")
        modal.modal({backdrop:"static",keybord:false});
        move_element.modal("hide");
        //$("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal1']").modal("show");
    }
    $scope.ztreeBtmClose = function(){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal1']").modal("hide");
        move_element.modal("show");
    }

    var Loan_element = angular.element('#Loan_choseModal');
    $scope.find_users_by_branches1 = function(){
        branchmanageService.find_users_by_branches({'branch_id':$scope.cust_search.org_tar}).success(function(reps){
            $scope.model5 =reps.data;
       });
    };

    $scope.ztreeBtmConfirm1 = function(){
        var treeObj = $.fn.zTree.getZTreeObj("loan_type_tree1" + $scope.tabId);
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
        $("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal1']").modal("hide");
        $scope.add_manager = null;
        $scope.add_manager_no = null;
        move_element.modal("show");
        $scope.find_users_by_branches1();
    }

    $scope.choose_branch_type1 = function(branch_code, branch_name, branch_level){
        $scope.cust_search.org_tar= branch_code.replace(/(^\s*)|(\s*$)/g, "");
        //$scope.ltSelected = false;
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
   
    $scope.isManager = function() {
        $scope.flag=false;
        branch_no = $rootScope.user_session.branch_code;
        if (branch_no.charAt(0) == 'M'||branch_no == '966000')
            $scope.flag=true;
    }
    $scope.isManager();

};

PosPreMoveController.$inject = ['$scope', '$attrs', '$filter', 'SqsReportService','branchmanageService','gsgxckService','$rootScope'];

angular.module('YSP').service('PosPreMoveController', PosPreMoveController);

