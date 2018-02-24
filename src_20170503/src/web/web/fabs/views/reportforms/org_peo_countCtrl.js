/**
 * man_grade_jdg Controller
 */
function org_peo_countController($scope,store, $filter, $rootScope, SqsReportService,org_levelService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.flag_tdate={};
    $scope.cust_search.login_branch_no = $rootScope.user_session.branch_code;
    $scope.cust_search.login_teller_no = $rootScope.user_session.user_code;
    $scope.cust_search.tdate = moment();
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/org_peo_count?export=1"+ "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code;
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

    $scope.filterInt = function(value){
        if(/^[0-9]+$/.test(value))
            return true;
        return false;
    };
    $scope.filterNum = function(value){
        if(/^[0-9]+(\.[0-9]+)?$/.test(value))
            return true;
        return false;
    }

    $scope.search = function() {
        $("div[name='loading']").modal("show");
        if($scope.cust_search.kyear instanceof moment){
          $scope.cust_search.kyear = $scope.cust_search.kyear.format("YYYY");
        }
        
        params = $scope.cust_search;
        $scope.total_count = 0;
        $scope.cur_page = 1;

        console.log(params);
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/org_peo_count?export=1"+ "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code;
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!='' && $scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        SqsReportService.info('org_peo_count', params).success(function(resp) {
            $("div[name='loading']").modal("hide");
            $scope.data = resp;
            console.log($scope.data)
            if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions)
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    $scope.add = function(){
        $scope.kyear = '';
        $scope.org_no = '';
        $scope.org_name = '';
        $scope.peo_count= '';
        $scope.remarks = '';

        $('#org_peo_count').modal('show');
    };
    $scope.save = function(){
        if($scope.kyear == ''||$scope.org_no==''||$scope.org_name==''||$scope.peo_count==''){
            alert("信息未填完全,请检查!");
            return;
        }

        if(!$scope.filterInt($scope.kyear)){
            alert("请输入合法年份，如2016");
            return;
        }

        if(!$scope.filterNum($scope.peo_count)){
            alert("请输入合法数值");
            return;
        }

       
        org_levelService.count_save({'kyear':$scope.kyear,'org_no':$scope.org_no,'org_name':$scope.org_name,'peo_count':$scope.peo_count,'remarks':$scope.remarks}).success(function (reps){
            $scope.search(); 
            $('#org_peo_count').modal('hide');
            alert(reps.data)
        });
    };
    $scope.del = function(row){
        if(confirm("确认删除？")){
            org_levelService.conunt_del({'row_id':row[5]}).success(function(reps){
                alert(reps.data);
                $scope.search();
            })
        }else{
            alert("确认取消？");
        }
    }
    $scope.to_edit = function(row){
        $('#org_peo_edit_modal').modal('show');
        $scope.kyear = row[0];
        $scope.org_no = row[1];
        $scope.org_name = row[2];
        $scope.peo_count= row[3];
        $scope.remarks = row[4];
        $scope.item_id = row[5];
    };
    $scope.edit_save = function(){
        if($scope.kyear == ''||$scope.org_no==''||$scope.org_name==''||$scope.peo_count==''){
            alert("信息未填完全,请检查!");
            return;
        }
        if(!$scope.filterNum($scope.peo_count)){
            alert("请输入合法数值");
            return;
        }
        
        if(!$scope.filterInt($scope.kyear)){
            alert("请输入合法年份，如2016");
            return;
        }   
        else{
            $scope.kyear=$scope.kyear;
        }
        org_levelService.count_edit_save({'item_id':$scope.item_id,'kyear':$scope.kyear,'org_no':$scope.org_no,'org_name':$scope.org_name,'peo_count':$scope.peo_count,'remarks':$scope.remarks}).success(function (reps){
            $scope.search(); 
            $('#org_peo_edit_modal').modal('hide');
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
            url : base_url+"/org_level/count_upload/",
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
    $scope.change_name = function(target){
       if(target == null){$scope.org_name='';$scope.user_name='';$scope.name='';}
       for(var i in $scope.model1){
            if($scope.model1[i].branch_code==target){
                $scope.org_name=$scope.model1[i].branch_name;
                branchmanageService.users({'branch_id':$scope.model1[i].role_id}).success(function(reps){
                    $scope.model2 = reps.data;
                    });
            }
        }
    }
    $scope.change_name2 = function(target){
       if(target == null)$scope.name='';
       for(var i in $scope.model2){
            if($scope.model2[i].user_name==target){
                $scope.name=$scope.model2[i].name;
            }
       } 
    }
    $scope.find_branches = function(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function(reps){
            $scope.model1 = reps.data;
            console.log($scope.model1);
        })
    }
    $scope.find_branches();
};
org_peo_countController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','org_levelService','branchmanageService'];

angular.module('YSP').service('org_peo_countController', org_peo_countController);
