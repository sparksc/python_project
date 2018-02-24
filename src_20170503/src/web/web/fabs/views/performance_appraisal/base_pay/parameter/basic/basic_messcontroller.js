/**
 * basic_mess Controller
 */
function basic_messController($scope, $rootScope, $filter, SqsReportService, staffrelationService, staff_statusService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    
    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.his_cust_ifno={};
    $scope.cust_search.login_branch_no = $rootScope.user_session.branch_code;
    $scope.cust_search.S_DATE=moment();
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
    $scope.onAction1 = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.detail_data = resp;
        });
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
            $scope.jycd=["研究生及以上","本科","大专","中等教育"]
        });       
    };
    get_group_type();
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name, 'parent_branch_no':$scope.cust_search.login_branch_no}).success(function (reps) {
        $scope.model1=reps.data;
        });
    };
    $scope.find_users = function(target){
        $scope.cust_search.SALE_CODE=null;
        $scope.cust_search.STAFF_NAME=null;
        $scope.cust_search.POSITION=null;
        $scope.cust_search.DEPARTMENT=null;
        //$scope.his_flag(); TBD clliu del 20161223
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
    var element_add = angular.element('#myModaladd');
    $scope.add = function(){
        $scope.add_date={};
        $scope.add_date.x1 = moment();
        $scope.add_date.x2 = null;
        $scope.add_date.x3 = null;
        $scope.add_date.x4 = null;
        $scope.add_date.x5 = null;
        $scope.add_date.x6 = null;
        $scope.add_date.x7 = null;
        $scope.add_date.x8 = null;
        $scope.add_date.x9 = null;
        $scope.add_date.x10 = null;
        $scope.add_date.x11 = null;
        $scope.add_date.x12 = null;
        $scope.add_date.x13 = null;
        $scope.add_date.x14 = null;
        $scope.add_date.x15 = '本科';
        $scope.add_date.x16 = '否';
        element_add.modal('show');
    };
    $scope.add_save = function (valid){
        if($scope.add_date.x1 instanceof moment){
            $scope.add_date.x1 = $scope.add_date.x1.format('YYYYMMDD');
        }else {
            $scope.add_date.x1 = '0000';
        };
        $scope.add_date.x2=$scope.add_date.x2.role_id;
        if($scope.add_date.x8=='无'||$scope.add_date.x8=='0'||$scope.add_date.x8==0){
        $scope.add_date.x8=null
        }
        staffrelationService.tsave({'add_date':$scope.add_date}).success(function (resp){
            alert(resp.data);
            $scope.search();
            element_add.modal('hide');
         });
    };
    $scope.to_del = function(item){
        var r=confirm("确定删除？");
        if(r==true){
            staffrelationService.tdelt({'del_date':item}).success(function(resp){
                alert(resp.data);
                $scope.search();
            });
        }
        else{alert("取消删除");}
    };


    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/basicmess?export=1&ORG_NO="+$rootScope.user_session.branch_code+"&MANAGER_NO"+$rootScope.user_session.user_code; 
    $scope.search = function() {

        params = {};
        params=$scope.cust_search;
        if($scope.cust_search.org!=''){
            params.org = $scope.cust_search.org;
        }else{
            params.org = null;
        }
        if($scope.cust_search.DEPARTMENT!=''){
            params.DEPARTMENT = $scope.cust_search.DEPARTMENT;
        }else{
            params.DEPARTMENT = null;
        }
        if($scope.cust_search.SALE_CODE!=''){
            params.SALE_CODE = $scope.cust_search.SALE_CODE;
        }else{
            params.SALE_CODE = null;
        }
        if($scope.cust_search.STAFF_NAME!=''){
            params.STAFF_NAME = $scope.cust_search.STAFF_NAME;
        }else{
            params.STAFF_NAME = null;
        }
        if($scope.cust_search.POSITION!=''){
            params.POSITION = $scope.cust_search.POSITION;
        }else{
            params.POSITION = null;
        }
        if($scope.cust_search.MANAGE_TYPE!=''){
            params.MANAGE_TYPE = $scope.cust_search.MANAGE_TYPE;
        }else{
            params.MANAGE_TYPE = null;
        }
        if($scope.cust_search.WORK_STATUS!=''){
            params.WORK_STATUS = $scope.cust_search.WORK_STATUS;
        }else{
            params.WORK_STATUS = null;
        }
        if($scope.cust_search.IS_VIRTUAL!=''){
            params.IS_VIRTUAL = $scope.cust_search.IS_VIRTUAL;
        }else{
            params.IS_VIRTUAL = null;
        }
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/basicmess?export=1"+ "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        
        SqsReportService.info('basicmess',params).success(function(resp) {
            $scope.data = resp;
	        if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    /**
     *点击编辑
     **/
    $scope.bb=[];
    $scope.to_edit = function(row) {
    $scope.flag=false;
    $scope.target =[];
    $scope.his_row=row;
    console.log("aaaa")
    console.log($scope.his_row)
    for(var i =0 ;i<row.length;i++){
        $scope.target[i] = row[i];//把要编辑那一行数据作为list对象取得
        if(i == 0){
            if(row[i]==null)$scope.target[i] = moment();
            else $scope.target[i]=moment(row[0]);
            }
        }
        $scope.LevelMatch=[$scope.target[8]]
        for(i in $scope.model1){
        if($scope.model1[i].branch_name==$scope.target[5]){
            $scope.target[5]=$scope.model1[i];
            }   
        }
        //$scope.find_users($scope.target[5]);
        branchmanageService.branchgroup({'branch_id':$scope.target[5].role_id}).success(function(reps){
            $scope.bb = reps.data;
        for(i in $scope.bb){
            if($scope.bb[i].group_name==$scope.target[6]){
                $scope.target[6]=$scope.bb[i].group_id;
            }
        }
        });
	$('#myModal').modal('show');
    };

    /**
     *编辑界面保存
     **/
    $scope.newupdate = function(target,valid) {//target表示待编辑的那行数据
        var new_data = {};
        new_data['newdata']=target;//把list对象放到key为newdata的字典里
        new_data['newdata'][5]=target[5].role_id;
        new_data['newdata'][0]=moment(target[0]).format("YYYYMMDD")
        if(new_data['newdata'][0].substring(6)!='01'){
            alert('修改员工职位只能是月初')
            return;
        
        }
        if(moment(target[0]).format('YYYYMMDD')<moment($scope.his_row[0]).format('YYYYMMDD')){
            alert('员工新上任时间不能小于员工在旧机构的开始时间');
            return;
        }
 
        
       /* if($scope.flag){
            $scope.update_his($scope.his_row);
            new_data['newdata'][0]=moment().format("YYYYMMDD")
        };*/
        // alert(target);
        var old_jg=$scope.his_row[21];
        var new_jg=target[5];
        var old_bm=$scope.his_row[6];
        var new_bm;
        var old_zw=$scope.his_row[7];
        var new_zw=target[7];

        for(i in $scope.bb){
            if($scope.bb[i].group_id==$scope.target[6]){
                 new_bm=$scope.bb[i].group_name;
                }
        }
        
        if(new_data['newdata'][8]=='无'||new_data['newdata'][8]=='0'||new_data['newdata'][8]==0)
        {
            new_data['newdata'][8]=null
        }
        /*console.log(old_jg); 
        console.log(new_jg); 
        console.log(old_bm); 
        console.log(new_bm); 
        console.log(old_zw); 
        console.log(new_zw);*/ 
        //if(old_jg!=new_jg || old_bm!=new_bm || old_zw!=new_zw)
          // new_data['newdata'][0]=moment().format("YYYYMMDD");


	    staffrelationService.newupdate(new_data).success(function(resp) {
            alert(resp.data);//resp是个object对象，对象的属性data，成功更新这条记录就返回data值更新成功。
            $scope.update_his($scope.his_row,target);
            if(old_jg!=new_jg || old_bm!=new_bm || old_zw!=new_zw){
               // $scope.update_his($scope.his_row);
                $scope.search();
                $('#myModal').modal('hide');
            }
            else
            {
               
                $scope.search();
                $('#myModal').modal('hide');
            }
        }).error(function(resp){
         // $scope.to_edit($scope.his_row);                 
       
        for(j in $scope.model1){
        if($scope.model1[j].role_id==target[5]){
            $scope.target[5]=$scope.model1[j];
            }   
          }
        });    
    };
   
    
    $scope.his_flag = function(){                                                                                     
            if($scope.target[7]=='委派会计主管(副股级)' || $scope.target[7]=='委派会计主管'||$scope.target[7]=='助理会计'){
             $scope.LevelMatch=['一级','二级','三级'];
            }
            else if($scope.target[7]=='客户经理'){
                $scope.LevelMatch=['资深客户经理','高级客户经理','中级客户经理','初级客户经理','助理客户经理'];
            }
            else if($scope.target[7]=='综合柜员'||$scope.target[7]=='一般员工')
            {
                $scope.LevelMatch=['资深柜员','高级柜员','中级柜员','初级柜员','助理柜员'];
            }

            else{
                $scope.LevelMatch='无'
            }
    };                                                                                                                
    $scope.his_flag_1 = function(){                                                                                     
            if($scope.his_cust_ifno.position_his=='委派会计主管(副股级)' || $scope.his_cust_ifno.position_his=='委派会计主管'||$scope.his_cust_ifno.position_his=='助理会计'){
             $scope.LevelMatch1=['一级','二级','三级'];
            }
            else if($scope.his_cust_ifno.position_his=='客户经理'){
                $scope.LevelMatch1=['资深客户经理','高级客户经理','中级客户经理','初级客户经理','助理客户经理'];
            }
            else if($scope.his_cust_ifno.position_his=='综合柜员'||$scope.his_cust_ifno.position_his=='一般员工')
            {
                $scope.LevelMatch1=['资深柜员','高级柜员','中级柜员','初级柜员','助理柜员'];
            }

            else{
                $scope.LevelMatch1='无'
            }
    }; 
    $scope.his_flag_2 = function(){                                                                                     
            if($scope.add_date.x8=='委派会计主管(副股级)' || $scope.add_date.x8=='委派会计主管'||$scope.add_date.x8=='助理会计'){
             $scope.LevelMatch2=['一级','二级','三级'];
            }
            else if($scope.add_date.x8=='客户经理'){
                $scope.LevelMatch2=['资深客户经理','高级客户经理','中级客户经理','初级客户经理','助理客户经理'];
            }
            else if($scope.add_date.x8=='综合柜员'||$scope.add_date.x8=='一般员工')
            {
                $scope.LevelMatch2=['资深柜员','高级柜员','中级柜员','初级柜员','助理柜员'];
            }

            else{
                $scope.LevelMatch2='无'
            }
    }; 

    $scope.update_his = function(old_target,new_target){
            olddata = {};
            if(moment(old_target[0]).format('YYYYMMDD')==moment(new_target[0]).format('YYYYMMDD')){
                return;
            }
            else{
            olddata['start_date']=moment(old_target[0]).format('YYYYMMDD');
            olddata['end_date']=(moment(new_target[0]).add('days',-1)).format('YYYYMMDD');
            }
            olddata['sale_code']=old_target[1];
            olddata['org_code']=old_target[5];
            olddata['group_his']=old_target[6];
            olddata['position_his']=old_target[7];
            olddata['SALE_NAME']=old_target[2]
            olddata['PROPERTY']=old_target[3]
            if(old_target[8]=='0' || old_target[8]==0 ||old_target[8]=='无')
            {
                old_target[8]=null
            }
            olddata['DEG_LEVEL']=old_target[8]

            olddata['POSITION_TYPE']=old_target[9]
            olddata['SALE_FALG']=old_target[10]
            olddata['WORKSTATUS']=old_target[11]
            olddata['IS_TEST']=old_target[20]
            olddata['IS_VIRIUAL']=old_target[21]
            var nd = {"olddata":olddata};
            if(olddata['org_code']!='0'&&olddata['group_his']!='0'&&olddata['position_his']!='0')staffrelationService.update_his(nd);
    };

    //历史详情按钮
    $scope.detail = function(row){
        params ={'sale_code':row[1]}
        SqsReportService.info('bgu', params).success(function(resp) {
            $scope.detail_data = resp;
	        if ((resp.rows || []).length > 0) {
                $scope.tableMessage2 = "";
            } else {
                $scope.tableMessage2 = "未查询到历史数据";
            }
        });
        $('#history_modal').modal('show').css({
        width:'auto',
        'margin-left':function(){
            return -($(this).width()/3)
        }
        });
    };
    

    $scope.his_to_edit=function(row){
        console.log('---------------aaa-----------')
        console.log(row)
        $('#history_modal').modal('hide')
        $('#his_myModal').modal('show') 
        $scope.his_cust_ifno.id=row[0]
        $scope.his_cust_ifno.start_date= row[1]
        $scope.his_cust_ifno.end_date= row[2]
        $scope.his_cust_ifno.sale_code=row[3]
        $scope.his_cust_ifno.SALE_NAME=row[4]
        $scope.his_cust_ifno.PROPERTY=row[5]
        $scope.his_cust_ifno.org_code=row[6]
        $scope.his_cust_ifno.group_his=row[7]
        $scope.his_cust_ifno.position_his=row[8]
        $scope.his_cust_ifno.DEG_LEVEL=row[9]
        $scope.LevelMatch1=[$scope.his_cust_ifno.DEG_LEVEL]
        $scope.his_cust_ifno.POSITION_TYPE=row[10]
        $scope.his_cust_ifno.SALE_FALG=row[11]
        $scope.his_cust_ifno.WORKSTATUS=row[12]
        $scope.his_cust_ifno.IS_TEST=row[13]
        $scope.his_cust_ifno.IS_VIRIUAL=row[14]
        for(i in $scope.model1){
        if($scope.model1[i].branch_name==$scope.his_cust_ifno.org_code){
        $scope.his_cust_ifno.org_code=$scope.model1[i];
        }
        }

        branchmanageService.branchgroup({'branch_id':$scope.his_cust_ifno.org_code.role_id}).success(function(reps){
        $scope.bb = reps.data;
        for(i in $scope.bb){
        if($scope.bb[i].group_name==$scope.his_cust_ifno.group_his){
        $scope.his_cust_ifno.group_his=$scope.bb[i].group_id;
        }
        }
        });

        console.log($scope.his_cust_ifno)

    }
    $scope.his_edit=function(){
        var nd={}
        $('#his_myModal').modal('hide')
        console.log('--------v---------v----------')
        console.log($scope.his_cust_ifno)
        $scope.his_cust_ifno.start_date=moment($scope.his_cust_ifno.start_date).format("YYYYMMDD")
       $scope.his_cust_ifno.end_date=moment($scope.his_cust_ifno.end_date).format("YYYYMMDD")
    
        $scope.his_cust_ifno.group_his=$scope.his_cust_ifno.org_code.branch_level
        $scope.his_cust_ifno.org_code=$scope.his_cust_ifno.org_code.branch_name
        if($scope.his_cust_ifno.DEG_LEVEL=='0'||$scope.his_cust_ifno.DEG_LEVEL=='无'||$scope.his_cust_ifno.DEG_LEVEL==0){
            $scope.his_cust_ifno.DEG_LEVEL=null
        }
        console.log($scope.his_cust_ifno)
        var nd={'his_data':$scope.his_cust_ifno}
        staffrelationService.edit_his(nd).success(function(resp) {
            alert(resp.data)

        })

    }
    $scope.his_to_del=function(row){
        var nd={}
        $('#history_modal').modal('hide')
        if(confirm("确认删除?")){
        var nd={'his_data':{'id':row[0]}}
        staffrelationService.delete_his(nd).success(function(resp) {
        alert(resp.data)
        })
        return;
        }
    }

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
        //console.log($scope.cust_search.org); 
        //console.log($scope.cust_search.branch_name); 
        //console.log($scope.cust_search.branch_level); 
    }

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
        //console.log(res_msg);
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
        //console.log(data); 
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

basic_messController.$inject = ['$scope', '$rootScope', '$filter', 'SqsReportService' ,'staffrelationService','staff_statusService','branchmanageService'];

angular.module('YSP').service('basic_messController', basic_messController);
