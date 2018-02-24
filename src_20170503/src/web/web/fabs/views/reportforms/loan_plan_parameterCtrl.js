/**
 * villageinput Controller
 */
function loanplanparameterController($scope,store, $filter, $rootScope, SqsReportService,villageinputService,branchmanageService) {
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
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/loan_plan_parameter?export=1"
    $scope.newstaffdata= {};    
    $scope.change_name = function(target){
       if(target == null){$scope.newstaffdata[2]='';$scope.newstaffdata[3]='';$scope.newstaffdata[4]='';$scope.newstaffdata[5]='';$scope.newstaffdata[6]='';}
       for(var i in $scope.model1){
            if($scope.model1[i].branch_code==target){
                $scope.newstaffdata[2]=$scope.model1[i].branch_name;
                branchmanageService.users({'branch_id':$scope.model1[i].role_id}).success(function(reps){
                    $scope.model3 = reps.data;
                    });
                $scope.newstaffdata[5]=null;
            }
        }
    }
    $scope.change_name2 = function(target){
       if(target == null)$scope.newstaffdata[6]='';
       for(var i in $scope.model3){
            if($scope.model3[i].user_name==target){
                $scope.newstaffdata[6]=$scope.model3[i].name;
            }
       } 
    }
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
        });
    };
    find_branchs();
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
    $scope.find_users = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.org){role_id=$scope.model1[i].role_id;}
        }
        
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
        //$scope.cust_search.SALE_CODE = null;
    }
    $scope.upload_excel = function(){
        var files = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#elec_arch").prop('files');
        if(files.length==0)
        {
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
            url : base_url+"/villageinput/loan_upload/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
             request.setRequestHeader("x-session-token", token);
           },
           success: function(msg){
            $("div[name='loading']").modal("hide");
            console.log(msg);
            alert(msg.data);
            $scope.search()
          }
        });
     }



    $scope.search = function() {
        console.log($rootScope.user_session)
        params = $scope.cust_search;
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        console.log(params)
        SqsReportService.info('loan_plan_parameter', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };

    $scope.add = function(){
    $scope.newstaffdata={};
    $('#villageinput_modal').modal('show');
    $('#villageinput_new_add_button').show();
    $('#villageinput_save_edit_button').hide();
    $scope.show_flag=1
    $scope.edit_flag=false
    };
    
    $scope.save = function(){
        console.log($scope.newstaffdata)
        var nsd ={};
        nsd["bdyear"]=$scope.newstaffdata[0];
        nsd["branch_code"]=$scope.newstaffdata[1];
        nsd["branch__name"]=$scope.newstaffdata[2];
        nsd["third_org_code"]=$scope.newstaffdata[3];
        nsd["third_org_name"]=$scope.newstaffdata[4];
        nsd["manager_code"]=$scope.newstaffdata[5];
        nsd["manager_name"]=$scope.newstaffdata[6];
        nsd["es_p_base"]=$scope.newstaffdata[7];
        nsd["es_p_target"]=$scope.newstaffdata[8];
        nsd["es_c_base"]=$scope.newstaffdata[9];
        nsd["es_nc_base"]=$scope.newstaffdata[10];
        nsd["ave_base"]=$scope.newstaffdata[11];
        nsd["ave_target"]=$scope.newstaffdata[12];
        nsd["cre_m_target"]=$scope.newstaffdata[13];
        nsd["cre__h_target"]=$scope.newstaffdata[14];
        nsd["cre__es_c_h_target"]=$scope.newstaffdata[15];
        nsd["aq_f_base"]=$scope.newstaffdata[16];
        nsd["av"]=$scope.newstaffdata[17];
        nsd["card_base"]=$scope.newstaffdata[18];
        nsd["card_target"]=$scope.newstaffdata[19];
        console.log(nsd)
        if( $scope.newstaffdata[0]==null || $scope.newstaffdata[0]==''){
            alert("年份未填写")
            return
        }
        if( $scope.newstaffdata[1]==null || $scope.newstaffdata[1]=='' ){
            alert("请选择网点编号")
            return
        }
        if ( $scope.newstaffdata[5]==null || $scope.newstaffdata[5]=='' ){
            alert("请选择客户经理名称")
            return
        }
        if ( parseInt( $scope.newstaffdata[7] ) < 0 || $scope.newstaffdata[7]== '' || $scope.newstaffdata[7]==null){
            alert("未填写对私考核基数或对私考核基数为负")
            return 
        }
        if ( parseInt( $scope.newstaffdata[8] ) < 0 || $scope.newstaffdata[8]== '' || $scope.newstaffdata[8]==null){
            alert("未填写对私目标任务或对私目标任务为负")
            return 
        }
        if ( parseInt( $scope.newstaffdata[9] ) < 0 || $scope.newstaffdata[9]== '' || $scope.newstaffdata[9]==null){
            alert("未填写纯公司类贷款考核基数或纯公司类贷款考核基数为负")
            return 
        }
        if ( parseInt( $scope.newstaffdata[10] ) < 0 || $scope.newstaffdata[10]== '' ||$scope.newstaffdata[10]==null){
            alert("未填写非纯公司类贷款考核基数或非纯公司类贷款考核基数为负")
            return 
        }
        if ( parseInt( $scope.newstaffdata[11] ) < 0 || $scope.newstaffdata[11]== '' ||$scope.newstaffdata[11]==null){
            alert("未填写日均贷款增加额考核基数或日均贷款增加额考核基数为负")
            return 
        }
        if ( parseInt( $scope.newstaffdata[12] ) < 0 || $scope.newstaffdata[12]== '' ||$scope.newstaffdata[12]==null){
            alert("未填写日均贷款增加额目标任务或日均贷款增加额目标任务为负")
            return 
        }
        if ( parseInt( $scope.newstaffdata[13] ) >100  || $scope.newstaffdata[13]== '' || $scope.newstaffdata[13]==null){
            alert("未填写余额占比目标或占比目标大于100%")
            return 
        }
        if ( parseInt( $scope.newstaffdata[14] ) >100  || $scope.newstaffdata[14]== '' || $scope.newstaffdata[14]==null){
            alert("未填写户数占比目标或占比目标大于100%")
            return 
        }
         if ( parseInt( $scope.newstaffdata[15] ) < 0  || $scope.newstaffdata[15]== '' || $scope.newstaffdata[15]==null){
            alert("未填写纯公司类贷款信用对公考核基数或基数为负")
            return 
        }
         if ( parseInt( $scope.newstaffdata[16] ) < 0  || $scope.newstaffdata[16]== '' || $scope.newstaffdata[16]==null){
            alert("未填写四级不良考核或占比考核数为负")
            return 
        }
        if ( parseInt( $scope.newstaffdata[18] ) < 0  || $scope.newstaffdata[18]== '' || $scope.newstaffdata[18]==null){
            alert("未填写丰收两卡考核基数或基数为负")
            return 
        }
        if ( parseInt( $scope.newstaffdata[19] ) < 0  || $scope.newstaffdata[19]== '' || $scope.newstaffdata[19]==null){
            alert("未填写丰收两卡目标任务或目标任务为负")
            return 
        }


        var nd = {"newdata":nsd};
        villageinputService.loan_save(nd).success(function (reps){
        alert(reps.data)
        $scope.search(); 
        $('#villageinput_modal').modal('hide');
        });
    };
    $scope.to_edit = function(row){
    $scope.show_flag=2
    $scope.edit_flag=true
    $('#villageinput_modal').modal('show');
    $('#villageinput_new_add_button').hide();
    $('#villageinput_save_edit_button').show();
    $scope.newstaffdata[0] = row[0];
    $scope.newstaffdata[1] = row[1];
    $scope.newstaffdata[2] = row[2];
    $scope.newstaffdata[3] = row[3];
    $scope.newstaffdata[4] = row[4];
    $scope.newstaffdata[5] = row[5];
    $scope.newstaffdata[6] = row[6];
    $scope.newstaffdata[7] = row[7];
    $scope.newstaffdata[8] = row[8];
    $scope.newstaffdata[9] = row[9];
    $scope.newstaffdata[10] = row[10];
    $scope.newstaffdata[11] = row[11];
    $scope.newstaffdata[12] = row[12];
    $scope.newstaffdata[13] = row[13];
    $scope.newstaffdata[14] = row[14];
    $scope.newstaffdata[15] = row[15];
    $scope.newstaffdata[16] = row[16];
    $scope.newstaffdata[17] = row[17];
    $scope.newstaffdata[18] = row[18];
    $scope.newstaffdata[19] = row[19];
    $scope.newstaffdata[20] = row[20];
   
    };
    $scope.edit_save = function(){
        var nsd ={};
        nsd["bdyear"]=$scope.newstaffdata[0];
        nsd["branch_code"]=$scope.newstaffdata[1];
        nsd["branch_name"]=$scope.newstaffdata[2];
        nsd["third_org_code"]=$scope.newstaffdata[3];
        nsd["third_org_name"]=$scope.newstaffdata[4];
        nsd["manager_code"]=$scope.newstaffdata[5];
        nsd["manager_name"]=$scope.newstaffdata[6];
        if($scope.newstaffdata[7].indexOf(",") != -1){
            nsd["es_p_base"]=$scope.newstaffdata[7].replace(new RegExp(',', 'gm'),'');
        }
        else{
            nsd["es_p_base"]=$scope.newstaffdata[7]
        }
        if($scope.newstaffdata[8].indexOf(",") != -1){
           nsd["es_p_target"]=$scope.newstaffdata[8].replace(new RegExp(',', 'gm'),'');
        }           
        else{
           nsd["es_p_target"]=$scope.newstaffdata[8];
        }                                       
        if($scope.newstaffdata[9].indexOf(",") != -1){
           nsd["es_c_base"]=$scope.newstaffdata[9].replace(new RegExp(',', 'gm'),'');
        }           
        else{
           nsd["es_c_base"]=$scope.newstaffdata[9];
        }
        if($scope.newstaffdata[10].indexOf(",") != -1){
           nsd["es_nc_base"]=$scope.newstaffdata[10].replace(new RegExp(',', 'gm'),'');
        }                    
        else{
           nsd["es_nc_base"]=$scope.newstaffdata[10];
        }
        if($scope.newstaffdata[11].indexOf(",") != -1){
           nsd["ave_base"]=$scope.newstaffdata[11].replace(new RegExp(',', 'gm'),'');
        }                   
        else{
           nsd["ave_base"]=$scope.newstaffdata[11];
        }
        console.log(typeof $scope.newstaffdata[11])
        if($scope.newstaffdata[12].indexOf(",") != -1){
           nsd["ave_target"]=$scope.newstaffdata[12].replace(new RegExp(',', 'gm'),'');
        }                   
        else{
           nsd["ave_target"]=$scope.newstaffdata[12];
        }
        console.log(typeof $scope.newstaffdata[15])
        /*
        if($scope.newstaffdata[15].indexOf(",") != -1){
            console.log($scope.newstaffdata[15])
        //   nsd["cre__es_c_h_target"]=$scope.newstaffdata[15].replace(new RegExp(',', 'gm'),'');
        }                  
        else{
           nsd["cre__es_c_h_target"]=$scope.newstaffdata[15];
        }*/
        if($scope.newstaffdata[16].indexOf(",") != -1){
           nsd["aq_f_base"]=$scope.newstaffdata[16].replace(new RegExp(',', 'gm'),'');
        }                   
        else{
           nsd["aq_f_base"]=$scope.newstaffdata[16];
        }
        if($scope.newstaffdata[18].indexOf(",") != -1){
           nsd["card_base"]=$scope.newstaffdata[18].replace(new RegExp(',', 'gm'),'');
        }                   
        else{
           nsd["card_base"]=$scope.newstaffdata[18];
        }
        if($scope.newstaffdata[19].indexOf(",") != -1){
           nsd["card_target"]=$scope.newstaffdata[19].replace(new RegExp(',', 'gm'),'');
        }                   
        else{
           nsd["card_target"]=$scope.newstaffdata[19];
        }
        

        nsd["cre_m_target"]=$scope.newstaffdata[13];
        nsd["cre__h_target"]=$scope.newstaffdata[14];
        nsd["cre__es_c_h_target"]=$scope.newstaffdata[15];
        nsd["av"]=$scope.newstaffdata[17];
        nsd["id"]=$scope.newstaffdata[20];
        
        var nd = {"newdata":nsd};
        villageinputService.loan_update(nd).success(function (reps){
       
        $scope.search(); 
        $('#villageinput_modal').modal('hide');
        });
        
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
    var nsd={};
    nsd["id"]=row[20];
    var nd = {"newdata":nsd};
        villageinputService.loan_delete(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#villageinput_modal').modal('hide');
        });
        }
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



loanplanparameterController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','villageinputService','branchmanageService'];

angular.module('YSP').service('loanplanparameterController', loanplanparameterController);
