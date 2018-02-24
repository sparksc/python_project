/**
 * Permission Controller
 */

function permissionControler($scope, $rootScope, permissionService) {

    var load_groups = function() {
        permissionService.groups_permission({
            'group_name': $scope.group_name
        }).success(function(reps) {
            $scope.group_list = reps.data;
        });
    };

    $scope.search = function() {
        load_groups();
    };
    var element = angular.element('#permission_modal');
    var tree_ele = angular.element('#test_loan_type_modal');
    $scope.permission_menu_selected = [];

    var Nodes=[];
    function search_nodes(ids, nodes, add, del)
    {
        for (var idx in nodes)
        {
            if(nodes[idx].children && nodes[idx].children.length > 0)
            {
                search_nodes(ids, nodes[idx].children, add, del);
            }else{
                if(nodes[idx].checked && ! ids[nodes[idx].id])
                {
                    del.push(nodes[idx].id);
                }
                if(!nodes[idx].checked && ids[nodes[idx].id])
                {
                    add.push(nodes[idx].id);
                }
            }
        }
    }
    $scope.ztreeBtmConfirm = function(){
        var ztobj = $.fn.zTree.getZTreeObj("loan_type_tree"+$scope.tabId);
        var nodes = ztobj.getCheckedNodes(true);
        var ids = {};
        for (var idx in nodes)
        {
            ids[nodes[idx].id] = true;
        }
        var add = [];
        var del = [];
        search_nodes(ids, Nodes, add, del);
        permissionService.save_permission_list({'group_id': $scope.modal_group_id, 'all': ids, 'add': add, 'del': del}).success(function (resp) {
            alert(resp.data);
        });
    }

    $scope.init_branches = function(group_data){
        var tree_html = '<ul id="loan_type_tree'+$scope.tabId+'" class="ztree"> </ul>';
        angular.element($('#tab_'+ $scope.tabId + '_content').find("div[name='for_lt_tree']")).append(tree_html);
        var setting = { 
            check:{
                enable:true
            }   
        };  
        Nodes=[];
        var data = []; 
        //查询数据库
        permissionService.get_permission_list(group_data).success(function (resp) {
            data = resp.data;
            show_permissions(data)
            $.fn.zTree.init($("#loan_type_tree"+$scope.tabId), setting, Nodes);
        });
        //生成业务类型列表
        function show_permissions(data){
            for(var i = 0 ; i < data.length ; ++i){
                var One = new Object();
                pro_arr = data[i];//.child_node;
                One.children=new Array();
                if(pro_arr.childs.length>0){
                    pro_arr = pro_arr.childs;
                    One.name = data[i].node_name.trim();
                    One.id = data[i].node_code;
                    One.pId = data[i].parent_code;
                    var chk_idx = 0;
                    for (var j = 0 ; j < pro_arr.length; ++j){
                        var Two = new Object();
                        Two.children = new Array();
                        if (pro_arr[j].childs.length > 0)
                        {
                            pro_arr_j = pro_arr[j].childs;
                            Two.name=pro_arr[j].node_name.trim();
                            Two.id=pro_arr[j].node_code;
                            Two.pId=pro_arr[j].node_code;
                            var chk_idx_k = 0;
                            for(var k = 0; k < pro_arr_j.length; ++k)
                            {
                                var Tre = new Object();
                                Tre.name=pro_arr_j[k].node_name.trim();
                                Tre.id=pro_arr_j[k].node_code;
                                Tre.pId=pro_arr_j[k].node_code;
                                Tre.checked = pro_arr_j[k].checked;
                                if (Tre.checked) chk_idx_k++;
                                Two.children.push(Tre);
                            }
                            if (chk_idx_k != 0){
                                Two.checked = true;
                                chk_idx ++;
                            }
                        }else{
                            Two.name=pro_arr[j].node_name.trim();
                            Two.id=pro_arr[j].node_code;
                            Two.pId=pro_arr[j].node_code;
                            Two.checked = pro_arr[j].checked;
                            if (Two.checked) chk_idx++;
                        }
                        One.children.push(Two);
                    }
                    if(chk_idx != 0)
                    {
                        One.checked = true;
                    }
                }else{
                    One.name = data[i].node_name.trim();
                    One.id = data[i].node_code;
                    One.pId = data[i].parent_code;
                    One.checked = data[i].checked;
                }
                Nodes.push(One);
            }
        }   
    }   


    $scope.edit = function(group) {
        //$scope.init_branches();
        //tree_ele.modal('show');
        //return ;
        //element.modal('show');
        $scope.permission_menu_selected = [];

        $scope.modal_group_name = group.group_name;
        $scope.modal_group_id = group.id;
        /*----start---------------------------------------*/
        $scope.init_branches({'group_id': group.id});
        tree_ele.modal('show');
        /*----end-----------------------------------------*/
        //permissionService.group_menus_select({
        //    'group_id': group.id
        //}).success(function(resp) {
        //    $scope.menus = resp.data;
        //    angular.forEach($scope.menus, function(menu, key) {
        //        if (menu.group_id) {
        //            $scope.permission_menu_selected.push(menu.menu_id);
        //        }
        //        $scope.permission_old=[];
        //        $scope.permission_old=$scope.permission_menu_selected;
        //    });
        //});

    };


    $scope.save = function() {
        permissionService.group_menus_save({
            'old_group_id': $scope.permission_old,
            'group_id': $scope.modal_group_id,
            'menus': $scope.permission_menu_selected
        }).success(function(resp) {
            alert(resp.data);
            element.modal('hide');
        });
    };
};

permissionControler.$inject = ['$scope', '$rootScope', 'permissionService'];

angular.module('YSP').service('permissionControler', permissionControler);
