/**
 * villageinput Controller
 */
function managerOtherWorkDayController($scope,store, $filter, $rootScope, SqsReportService,branchmanageService,hallManagerHanderServer) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.DATE_ID = moment();
    $scope.newstaffdata= {};    
    $scope.cust_search.login_branch_no = $rootScope.user_session.branch_code;
        $scope.cust_search.login_teller_no = $rootScope.user_session.user_code;


    $scope.change_name = function(target){
        if(target == null){$scope.newstaffdata[2]='';$scope.newstaffdata[3]='';$scope.newstaffdata[4]='';}
        for(var i in $scope.model1){
            if($scope.model1[i].branch_code==target){
                $scope.newstaffdata[2]=$scope.model1[i].branch_name;     
                branchmanageService.users({'branch_id':$scope.model1[i].role_id}).success(function(reps){
                    $scope.model3 = reps.data;
                    });
                $scope.newstaffdata[3]=null;
            }
        } 
    }
    $scope.change_name1 = function(target){
        if(target == null)$scope.newstaffdata[4]='';
        for(var i in $scope.model3){
            if($scope.model3[i].user_name==target){
                $scope.newstaffdata[4]=$scope.model3[i].name;     
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
        $scope.cust_search.SALE_CODE = null;
    }
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        params = {};        
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/manager_otherwork_day?export=1";
       
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            if(params[key] instanceof moment)params['DATE_ID']=params['DATE_ID'].format("YYYYMMDD");
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        console.log(params)
        SqsReportService.info('manager_otherwork_day',params).success(function(resp) {
            $scope.data = resp;
         console.log(resp)
        if(resp.rows[0]=='未'){
            alert("未到月末,不能查看")
            resp.rows=''
            $scope.tableMessage = "未查到数据";
            return;
        }
	    if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查到数据";
            }
        });
    }
    var add_element=angular.element('#manager_otherwork_day__modal');
    var add_button_element=angular.element('#manager_otherwork_day_new_add_button')
    var edit_button_element=angular.element('#manager_otherwork_day_save_edit_button')
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/manager_otherwork_day?export=1"+"&DATE_ID="+moment().format('YYYYMMDD');

    $scope.add = function(){
    $scope.edit_flag=false
    $scope.show_flag = 1
    $scope.newstaffdata={};
    $scope.newstaffdata[0] = moment();
    add_element.modal('show');
    add_button_element.show();
    edit_button_element.hide();
    };
    
    $scope.save = function(){
        console.log($scope.newstaffdata)
        var nsd ={};
        nsd["date_id"]=$scope.newstaffdata[0].format('YYYYMMDD');
        if($scope.newstaffdata[1]==null || $scope.newstaffdata[1]=="")
        {
            alert("请填写机构号")
            return
        }
        if($scope.newstaffdata[3]==null || $scope.newstaffdata[3]=="")
        {
          alert("请填写员工号")
          return
        }
        if ($scope.newstaffdata[5]==null || $scope.newstaffdata[5]==""){
         $scope.newstaffdata[5]=null
         alert("请将大堂经理的工作日信息补充完整")
         return
        }
        if (Number($scope.newstaffdata[5])<0){
         $scope.newstaffdata[5]=null
         alert("大堂经理的工作日不能为负数")
         return
        }
        if (Number($scope.newstaffdata[5]).toString()=='NaN'){
         $scope.newstaffdata[5]=null
         alert("大堂经理的工作日存在非法字符")
         return
        }
         if ($scope.newstaffdata[6]==null || $scope.newstaffdata[6]==""){
         $scope.newstaffdata[6]=null
         alert("请将大唐经理的担任天数信息补充完整")
         return
        }
         if (Number($scope.newstaffdata[6])<0){
         $scope.newstaffdata[6]=null
         alert("大堂经理的担任天数不能为负数")
         return
        }
         if (Number($scope.newstaffdata[6]).toString()=='NaN'){
         $scope.newstaffdata[6]=null
         alert("大堂经理的担任天数存在非法字符")
         return
        }
 
        nsd["org_code"]=$scope.newstaffdata[1];
        nsd["org_name"]=$scope.newstaffdata[2];
        nsd["sale_code"]=$scope.newstaffdata[3];
        nsd["sale_name"]=$scope.newstaffdata[4];
        nsd["work_days"]=$scope.newstaffdata[5];
        nsd["server_days"]=$scope.newstaffdata[6];
        console.log(nsd)
        var nd = {"newdata":nsd};
        hallManagerHanderServer.other_save(nd).success(function (reps){
        $scope.cust_search.DATE_ID=$scope.newstaffdata[0].format('YYYYMMDD');
        alert(reps.data)
        $scope.search(); 
        add_element.modal('hide');
        });
    };
    $scope.to_edit = function(row){
    $scope.edit_flag=true
    $scope.show_flag = 2
    add_element.modal('show');
    add_button_element.hide();
    edit_button_element.show();
    $scope.change_name(row[1]);
    a = String(row[0]);
    str = a.substr(0,4)+'-'+a.substr(4,2)+'-'+a.substr(6,2);
    console.log('qwe'+row[3])
    $scope.newstaffdata[0] = moment(str);
    $scope.newstaffdata[1] = row[1];
    $scope.newstaffdata[2] = row[2];
    $scope.newstaffdata[3] = row[3];
    $scope.newstaffdata[4] = row[4];
    $scope.newstaffdata[5] = row[5];
    $scope.newstaffdata[6] = row[6];
    $scope.newstaffdata[7]=row[7]
    };
    $scope.edit_save = function(){
        alert('dddddddddddd')
        var nsd ={};
        if ($scope.newstaffdata[5]==null || $scope.newstaffdata[5]==""){
         $scope.newstaffdata[5]=null
         alert("请将大堂经理的工作日信息补充完整")
         return
        }
        if (Number($scope.newstaffdata[5]).toString()=='NaN'){
         $scope.newstaffdata[5]=null
         alert("大堂经理的工作日存在非法字符")
         return
        }
        if (Number($scope.newstaffdata[5])<0){
            alert(Number($scope.newstaffdata[5]))
         $scope.newstaffdata[5]=null
         alert("大堂经理的工作日不能为负数")
         return
        }

         if ($scope.newstaffdata[6]==null || $scope.newstaffdata[6]==""){
         $scope.newstaffdata[6]=null
         alert("请将大堂经理的担任天数信息补充完整")
         return
        }
         if (Number($scope.newstaffdata[6]).toString()=='NaN'){
         $scope.newstaffdata[6]=null
         alert("大堂经理的担任天数存在非法字符")
         return
        }
         if (Number($scope.newstaffdata[6])<0){
         $scope.newstaffdata[6]=null
         alert("大堂经理的担任天数不能为负数")
         return
        }

        nsd["org_code"]=$scope.newstaffdata[1];
        nsd["org_name"]=$scope.newstaffdata[2];
        nsd["sale_code"]=$scope.newstaffdata[3];
        nsd["sale_name"]=$scope.newstaffdata[4];
        nsd["work_days"]=$scope.newstaffdata[5];
        nsd["server_days"]=$scope.newstaffdata[6];
        console.log(nsd)
        var nd = {"newdata":nsd};
        hallManagerHanderServer.other_save(nd).success(function (reps){
        $scope.cust_search.DATE_ID=$scope.newstaffdata[0].format('YYYYMMDD');
        alert(reps.data)
        $scope.search(); 
        add_element.modal('hide');
        });
    };
    $scope.to_edit = function(row){
    $scope.edit_flag=true
    add_element.modal('show');
    add_button_element.hide();
    edit_button_element.show();
    $scope.change_name(row[1]);
    a = String(row[0]);
    str = a.substr(0,4)+'-'+a.substr(4,2)+'-'+a.substr(6,2);
    console.log('qwe'+row[3])
    $scope.newstaffdata[0] = moment(str);
    $scope.newstaffdata[1] = row[1];
    $scope.newstaffdata[2] = row[2];
    $scope.newstaffdata[3] = row[3];
    $scope.newstaffdata[4] = row[4];
    $scope.newstaffdata[5] = row[5];
    $scope.newstaffdata[6] = row[6];
    $scope.newstaffdata[7]=row[7]
    };
    $scope.edit_save = function(){
        var nsd ={};
        if ($scope.newstaffdata[5]==null || $scope.newstaffdata[5]==""){
         $scope.newstaffdata[5]=null
         alert("请将大堂经理的工作日信息补充完整")
         return
        }
        if (Number($scope.newstaffdata[5])<0||Number($scope.newstaffdata[5]).toString()=='NaN'){
         $scope.newstaffdata[5]=null
         alert("大堂经理的工作日不能为负数或非法字符")
         return
        }
         if ($scope.newstaffdata[6]==null || $scope.newstaffdata[6]==""){
         $scope.newstaffdata[6]=null
         alert("请将大唐经理的担任天数信息补充完整")
         return
        }
         if (Number($scope.newstaffdata[6])<0||Number($scope.newstaffdata[6]).toString()=='NaN'){
         $scope.newstaffdata[6]=null
         alert("大堂经理的担任天数不能为负数或非法字符")
         return
        }
       console.log($scope.newstaffdata)
        nsd["date_id"]=moment($scope.newstaffdata[0]).format('YYYYMMDD');
        nsd["org_code"]=$scope.newstaffdata[1];
        nsd["org_name"]=$scope.newstaffdata[2];
        nsd["sale_code"]=$scope.newstaffdata[3];
        nsd["sale_name"]=$scope.newstaffdata[4];
        nsd["work_days"]=$scope.newstaffdata[5];
        nsd["server_days"]=$scope.newstaffdata[6];
        nsd["id"]=$scope.newstaffdata[7];
        var nd = {"newdata":nsd};
        hallManagerHanderServer.other_update(nd).success(function (reps){
        $scope.cust_search.DATE_ID=moment($scope.newstaffdata[0]).format('YYYYMMDD');
        alert(reps.data)
        $scope.search(); 
        add_element.modal('hide');
        });
        
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
    var nsd={};
    nsd["id"]=row[6];
    var nd = {"newdata":nsd};
        hallManagerHanderServer.delete(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        add_element.modal('hide');
        });
        }
    };

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
        console.log('aaaaaaa',form)
        form.append('application_id',$scope.applicationId)
        form.append('about','elec_arch')
        console.log('sssssssss',form)
        $.ajax({
        type: "POST",
        url : base_url+"/hall_manager_hander/other_upload/",
        data: form,
        processData: false,
        contentType: false,
        beforeSend: function(request) {
        request.setRequestHeader("x-session-token", token);
        },
        success: function(msg){
        $("div[name='loading']").modal("hide");
        alert(msg.data);
        }
        });
    }

    $scope.find_users_by_branches = function(){
        branchmanageService.find_users_by_branches({'branch_id':$scope.cust_search.ORG_CODE}).success(function(reps){
            $scope.model2 =reps.data;
       });
    };

    $scope.show_lt_modal = function(trigger_elem){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal']").modal("show");
    }

    var element = angular.element('#cust_hookSearchModal');
    //查找对应页面
    $scope.choose_branch_type = function(branch_code, branch_name, branch_level){
        $scope.cust_search.ORG_CODE= branch_code.replace(/(^\s*)|(\s*$)/g, "");
        $scope.cust_search.branch_name = branch_name.replace(/(^\s*)|(\s*$)/g, "");
        $scope.cust_search.branch_level = branch_level.replace(/(^\s*)|(\s*$)/g, "");
        $scope.ltSelected = false;
        console.log($scope.cust_search.ORG_CODE); 
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

    $scope.isManager = function() {
        $scope.flag=false;
        branchmanageService.get_user_permission({'user_id':$rootScope.user_session.user_id}).success(function(reps){
            if(reps.data>0)$scope.flag=true;
        });    
    }
    $scope.isManager();



};

managerOtherWorkDayController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','branchmanageService','hallManagerHanderServer'];

angular.module('YSP').service('managerOtherWorkDayController', managerOtherWorkDayController);
