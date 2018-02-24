/**
 * handmain Controller
 */
function handmainController($scope,store, $filter, $rootScope, SqsReportService,handmainService,branchmanageService) {
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
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/handmain?export=1" + "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code;
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


    $scope.newstaffdata= {};
    $scope.change_name = function(target){
        if(target == null){$scope.newstaffdata[2]='';}
        for(var i in $scope.model1){
            if($scope.model1[i].branch_code==target){
                $scope.newstaffdata[2]=$scope.model1[i].branch_name;     
                branchmanageService.users({'branch_id':$scope.model1[i].role_id}).success(function(reps){
                    $scope.model3 = reps.data;
                    });
            }
        } 
    }
    $scope.change_name1 = function(target){
        if(target == null)$scope.newstaffdata[5]='';
        for(var i in $scope.model3){
            if($scope.model3[i].user_name==target){
                $scope.newstaffdata[5]=$scope.model3[i].name;     
            }
        } 
    }
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
        });
    };
    find_branchs();    
    $scope.find_users = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.ORG_CODE){role_id=$scope.model1[i].role_id;}
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
        $scope.cust_search.STAFF_CODE = null;
    }

    $scope.search = function() {
        console.log($rootScope.user_session)
        $("div[name='loading']").modal("show");
        if($scope.cust_search.SYEAR && $scope.cust_search.SYEAR instanceof moment){
          $scope.cust_search.SYEAR = $scope.cust_search.SYEAR.format("YYYY");
        }

        params = $scope.cust_search;
        $scope.total_count = 0;
        $scope.cur_page = 1;
        console.log(params);
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/handmain?export=1&login_branch_no="+$rootScope.user_session.branch_code;
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!='' && $scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        
        SqsReportService.info('handmain', params).success(function(resp) {
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
        $scope.newstaffdata={};
        $scope.newstaffdata[0]='';
        $scope.newstaffdata[1]='';
        $scope.newstaffdata[2]='';
        $scope.newstaffdata[3]='';
        $scope.newstaffdata[4]='';
        //$scope.cust_search.tdate=moment();
        $('#handmain_modal').modal('show');
        $('#handmain_new_add_button').show();
        $('#handmain_save_edit_button').hide();
    };
    
    $scope.save = function(){
        if($scope.newstaffdata[0] == null||$scope.newstaffdata[1]==null||$scope.newstaffdata[2]==null||$scope.newstaffdata[3]==null){
            alert("信息未填完全,请检查!");
            return;
        }
        if(!$scope.filterInt($scope.newstaffdata[0])){
            alert("请输入合法年份，如2016");
            return;
        }
        if(!$scope.filterNum($scope.newstaffdata[3])){
            alert("请输入合法数值");
            return;
        }

       /* $scope.newstaffdata[0]  = $scope.newstaffdata[0].format("YYYY");*/
        console.log($scope.newstaffdata);
        var nsd ={};
        nsd["syear"]=$scope.newstaffdata[0];
        nsd["org_code"]=$scope.newstaffdata[1];
        nsd["org_name"]=$scope.newstaffdata[2];
        nsd["org_count"]=$scope.newstaffdata[3];
        nsd["remarks"]=$scope.newstaffdata[4];
        var SYEAR = $scope.newstaffdata[0],
            ORG_CODE = $scope.newstaffdata[1],
            ORG_NAME = $scope.newstaffdata[2];
        //判断数据库中是否存在syear数据
        params = {'SYEAR':SYEAR,'ORG_CODE':ORG_CODE}; 
        SqsReportService.info('handmain', params).success(function(resp) {
            $scope.data = resp;
            console.log($scope.data)
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
                $scope.search()
                alert(ORG_NAME.replace(/\s+/g,"")+SYEAR+"年份的数据已存在");
                $('#handmain_modal').modal('hide');
            } else{
                $scope.tableMessage = ""
                console.log(nsd)
                var nd = {"newdata":nsd};
                handmainService.save(nd).success(function (reps){
                    $scope.search(); 
                    $('#handmain_modal').modal('hide');
                });
            }
        });
    };
    $scope.to_edit = function(row){
         $('#handmain_edit_modal').modal('show');
         $('#handmain_new_add_button').hide();
         $('#handmain_save_edit_button').show();
         $scope.newstaffdata[0] = row[0];
         $scope.newstaffdata[1] = row[1];
         $scope.newstaffdata[2] = row[2];
         $scope.newstaffdata[3] = row[3];
         $scope.newstaffdata[4] = row[4];
         $scope.newstaffdata[5] = row[5];
         console.log($scope.newstaffdata);
    };
    $scope.edit_save = function(){
        if($scope.newstaffdata[0]==null||$scope.newstaffdata[1]==null||$scope.newstaffdata[2]==null||$scope.newstaffdata[3]==null){
            alert("信息未填完全,请检查!");
            return;
        }
        if(!$scope.filterInt($scope.newstaffdata[0])){
            alert("请输入合法年份，如2016");
            return;
        }   
        if(!$scope.filterNum($scope.newstaffdata[3])){
            alert("请输入合法数值");
            return;
        }   
        var nsd ={};
        
        if($scope.newstaffdata[0] instanceof moment){
            $scope.newstaffdata[0]=$scope.newstaffdata[0].format("YYYY");
        }
        else{
            $scope.newstaffdata[0]=$scope.newstaffdata[0];
        }
        console.log($scope.newstaffdata)
        nsd["syear"]=$scope.newstaffdata[0];
        nsd["org_code"]=$scope.newstaffdata[1];
        nsd["org_name"]=$scope.newstaffdata[2];
        nsd["org_count"]=$scope.newstaffdata[3];
        nsd["remarks"]=$scope.newstaffdata[4];
        nsd["id"]=$scope.newstaffdata[5];
        var nd = {"newdata":nsd};
        console.log(nd);
        handmainService.update(nd).success(function (reps){
            $scope.search(); 
            $('#handmain_edit_modal').modal('hide');
        });
        
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
    var nsd={};
    nsd["id"]=row[5];
    var nd = {"newdata":nsd};
        handmainService.delete(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#handmain_modal').modal('hide');
        });
        }
    };

    function find_dict(){
	branchmanageService.get_dict({'dict_type':'CKTYPE'}).success(function (reps) {
        $scope.model3=reps.data;
	});	
    }
    //find_dict();    
    $scope.searchEle = function(){
        imageService.pdfile_query($scope.applicationId,'elec_arch').success(function(resp){
                $scope.pdf_list  = resp.data;      
                console.log(resp.data);
        });
    }
    
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
        console.log(files)
        for(var i = 0 ; i < files.length ; ++i){
            console.log('---',files[i]);
            form.append('files',files[i]);
        }
        form.append('application_id',$scope.applicationId)
        form.append('about','elec_arch')
        $.ajax({
            type: "POST",
            url : base_url+"/handmain/upload/",
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
        $scope.cust_search.ORG_CODE= res_msg;

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
};

handmainController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','handmainService','branchmanageService'];

angular.module('YSP').service('handmainController', handmainController);
