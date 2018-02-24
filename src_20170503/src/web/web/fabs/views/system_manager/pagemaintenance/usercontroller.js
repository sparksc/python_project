/**
 * user Controller
 */
function userController($scope, $rootScope,$filter, SqsReportService, permissionService,branchmanageService,staff_statusService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    function get_group_type(){
        staff_statusService.get_group_type().success(function(reps){
            $scope.grouptypemodel = reps.data[0]  
            $scope.ryxz=$scope.grouptypemodel.人员性质
            $scope.bb1=$scope.grouptypemodel.部门
            $scope.zwgz=$scope.grouptypemodel.职务
            $scope.khjllb=$scope.grouptypemodel.客户经理类别
            $scope.aqybz=["是","否"]
            $scope.zzzt=["待入职","在职","退休","辞职","内退"]
        });       
    };
    get_group_type();

    $scope.find_users = function(target){
        $scope.cust_search.SALE_CODE=null;
        $scope.cust_search.STAFF_NAME=null;
        $scope.cust_search.POSITION=null;
        $scope.cust_search.DEPARTMENT=null;
        $scope.his_flag();
        if(!target){
            return;
        }
        var role_id = target.role_id;
        //for(i in $scope.model1){
        //    if($scope.model1[i].branch_code == target.BRANCH_CODE){role_id=$scope.model1[i].role_id;}
        //    if($scope.model1[i].branch_code == target.branch_code){role_id=$scope.model1[i].role_id;}
        //    if($scope.model1[i].branch_name == target){role_id=$scope.model1[i].role_id;}
        //}
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
        branchmanageService.branchgroup({'branch_id':role_id}).success(function(reps){
            $scope.bb = reps.data;
        });
    };  


    find_branchs();
    $scope.show_lt_modal = function(trigger_elem){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal']").modal("show");
    } 
    $scope.choose_branch_type = function(branch_code, branch_name, branch_level){
        $scope.cust_search.org= branch_code.replace(/(^\s*)|(\s*$)/g, "");
        $scope.cust_search.branch_name = branch_name.replace(/(^\s*)|(\s*$)/g, "");
        $scope.cust_search.branch_level = branch_level.replace(/(^\s*)|(\s*$)/g, "");
        $scope.ltSelected = false;
        console.log($scope.cust_search.org); 
        console.log($scope.cust_search.branch_name); 
        console.log($scope.cust_search.branch_level); 
    }

    $scope.find_users_by_branches = function(){
        branchmanageService.find_users_by_branches({'branch_id':$scope.cust_search.org}).success(function(reps){
            $scope.model2 =reps.data;
       });
    };

    $scope.ztreeBtmConfirm = function(){
        var treeObj = $.fn.zTree.getZTreeObj("loan_type_tree" + $scope.tabId);
        var nodes = treeObj.getCheckedNodes(true);
        var msg = "";
        for(var i=0; i< nodes.length; i++)
        {
            //if (nodes[i].id.charAt(0) == 'M')
            //{
             //   continue
            //}
            msg = msg + nodes[i].id + ",";
            //msg += nodes[i].id + ":" + nodes[i].name + ":" + nodes[i].pId + "\n";
        }
        res_msg = msg.substring(0, msg.length - 1)
        $scope.cust_search.org= res_msg;

        $scope.find_users_by_branches();
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
    
    
    //全选与单选功能，全选为当前页面,prkey声明主键
    $scope.choseArr=[];
    $scope.oneflag =false;
    $scope.master =false;
    var prkey = 4;
    $scope.selectall = function(master,data){
        if(master){
            $scope.onefalg =true;
            for(rowvalue in data){
                $scope.choseArr.push(data[rowvalue][prkey]);
            }
        }
        else{
            $scope.onefalg =false;
            $scope.choseArr =[];
        }
    };
    $scope.chkone = function(row,oneflag){
        var hasin = $scope.choseArr.indexOf(row[prkey]);
        if(oneflag&&hasin==-1){
            $scope.choseArr.push(row[prkey])
        }
        if(!oneflag&&hasin>-1){
            $scope.choseArr.pop(row[prkey])
        }
    };

    var load_groups = function() {
           permissionService.groups_permission({
                        'group_name':'' 
           }).success(function(reps) {
            $scope.group_list = reps.data;
        });
     };
    //load_groups();

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
        //console.log($scope.model1)
        });
    };
    find_branchs();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };   
    $scope.search = function() {
        $scope.tableMessage = "正在查询";
        params = {};
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!='')params[key]=$scope.cust_search[key]
        }
            //console.log(params);
            //console.log('22222222222222222222222')
        SqsReportService.info('userpermission',params).success(function(resp) {
            $scope.data = resp;
            //console.log('------------------------')
            //console.log(resp)
	    if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    $scope.to_edit = function(row) {
    $scope.target ={};
    $scope.target.staff_no = row[0];
    $scope.target.staff_name = row[1];
    $scope.target.branch = row[2];
    $scope.target.password = row[6];
    $scope.target.uid=row[7];
    $scope.target.fid=row[8];
    $scope.target.oid=row[9];
	$('#myModal_zg').modal('show');
    };
    $scope.userupdate = function(target) {//target表示待编辑的那行数据
        var new_data = {'newdata':target};
        console.log(target)
        //new_data['newdata']=target;//把list对象放到key为newdata的字典里
        console.log(new_data)
	    permissionService.user_update(new_data).success(function(resp) {
            alert(resp.data);//resp是个object对象，对象的属性data，成功更新这条记录就返回data值更新成功。
            $scope.search();
            $('#myModal_zg').modal('hide');
        });                
    };
    $scope.init_user_pwd = function(target){
        var new_data = {'newdata':target};
        permissionService.init_user_pwd(new_data).success(function(resp) {        
            alert(resp.data);
            $scope.search();
            $('#myModal_zg').modal('hide');
        });
    };
    $scope.add = function(){
        $scope.ntarget = {};
        var modal = $('#s_r_modal_zg');
        modal.modal('show');
    };
    $scope.permission_group_save = function(){
        // console.log($scope.choseArr);
        // console.log($scope.modal_user_id);
         //console.log($scope.permission_group_selected);
         //console.log($scope.old_groups);
      //  var new_data = {'newdata':ntarget};
	permissionService.user_permission_group_save({
           'old_groups':$scope.old_groups,
           'user_id':$scope.modal_user_id,
           'groups': $scope.permission_group_selected
           }).success(function(resp) {
         alert(resp.data);
         $('#s_r_modal_zg').modal('hide');
         $scope.search();
        });               
    };

    $scope.to_permission = function(row) {
    $scope.target ={};
    $scope.target.staff_no = row[0];
    $scope.target.staff_name = row[1];
    $scope.target.branch = row[2];
    $scope.target.password = row[6];
    $scope.target.uid=row[7];
    $scope.target.fid=row[8];
    //console.log(row)
	$('#s_r_modal_zg').modal('show');
    

    $scope.permission_group_selected = [];
    $scope.old_groups=[];

    $scope.modal_user_id=row[7]
    permissionService.user_permission_group_select({
                       'user_id':$scope.modal_user_id 
            }).success(function(resp) {
                    $scope.group_list = resp.data;

                    angular.forEach($scope.group_list, function(grp, key) {

                   if (grp.usergroup_id) {
                         $scope.permission_group_selected.push(grp.group_id);
                         $scope.old_groups.push(grp.group_id);
                            }
                            
                     });
        });
                                                                                                                                                

    };
};

userController.$inject = ['$scope','$rootScope','$filter', 'SqsReportService', 'permissionService','branchmanageService','staff_statusService'];

angular.module('YSP').service('userController', userController);
