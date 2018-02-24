/**
 * Org_ebank Controller
 */
function OrgebankController($scope, $rootScope, $filter, SqsReportService, permissionService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "点击查询";
    $scope.cust_search = {};
    $scope.cust_search.date = moment();
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
        console.log($scope.model1)
        });
    };
    find_branchs();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };   
    $scope.search = function() {
        params = {};        
        $scope.tableMessage = "正在查询";
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/org_ebank?export=1a";
        params.org = $rootScope.user_session.branch_code;
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            if(key=='date')params['date']=params['date'].format("YYYYMMDD");
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        SqsReportService.info('org_ebank',params).success(function(resp) {
            $scope.data = resp;
         console.log(resp)
	    if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查到数据";
            }
        });
    }
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/org_ebank?export=1a"+"&date="+moment().format('YYYYMMDD');

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

OrgebankController.$inject = ['$scope', '$rootScope', '$filter', 'SqsReportService', 'permissionService','branchmanageService'];

angular.module('YSP').service('OrgebankController', OrgebankController); 
