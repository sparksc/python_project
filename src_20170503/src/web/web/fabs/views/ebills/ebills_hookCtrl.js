/**
 * Mandep Controller
 */
function ebills_hookController($scope, $rootScope, $filter, SqsReportService, permissionService,branchmanageService,ebills_managerService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "点击查询";
    $scope.cust_search = {};
    $scope.custinfo_ebills={}
    $scope.org_fen_row={}//原来的数据,用作分配历史
    $scope.original_row={}//待分配数据
    $scope.new_row={}//要分配的数据
    $scope.add_row={}//新增数据
    $scope.cust_search.login_branch_no = $rootScope.user_session.branch_code;
    $scope.cust_search.login_teller_no = $rootScope.user_session.user_code;
    $scope.cust_search.DATE_ID = moment();
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
        console.log($scope.model1)
        });
    };
    find_branchs();
    $scope.find_users = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.org){role_id=$scope.model1[i].role_id;}
        }
        
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
        $scope.cust_search.id = null;
    }
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
    var move_element =angular.element(document.getElementById($scope.subTabId)).find('#ebills_hook_distribution');
    $scope.search = function() {
        $("div[name='loading']").modal("show");
        params = {};        
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/ebills_hook?export=1"+"&DATE_ID="+ $scope.cust_search.DATE_ID.format("YYYYMMDD") + "&login_branch_no=" + $rootScope.user_session.branch_code+"&login_teller_no=" + $rootScope.user_session.user_code
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            if(key=='DATE_ID')params['DATE_ID']=params['DATE_ID'].format("YYYYMMDD");
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        SqsReportService.info('ebills_hook',params).success(function(resp) {
            $("div[name='loading']").modal("hide");
            $scope.data = resp;
        console.log(resp)
        if(resp.rows[0]=='未'){
        alert("未到月末,不能查看")
        resp.rows=''
        $scope.tableMessage = "未查到数据";
        return;
        }
	    if (($scope.data.rows || []).length > 0) {
                console.log($scope.data.actions)
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查到数据";
            }
        });
    }

    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/ebills_hook?export=1"+"&DATE_ID="+ $scope.cust_search.DATE_ID.format("YYYYMMDD") + "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code;

    $scope.find_users_by_branches = function(){
        branchmanageService.find_users_by_branches({'branch_id':$scope.cust_search.org}).success(function(reps){
            $scope.model2 =reps.data;
       });
    };

    $scope.find_users_by_branches1 = function(){
        branchmanageService.find_users_by_branches({'branch_id':$scope.new_row.ORG_CODE}).success(function(reps){
            $scope.model5 =reps.data;
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

    $scope.show_lt_modal1 = function(trigger_elem){
        var modal=$("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal1']")
        modal.modal({backdrop:"static",keybord:false});
        move_element.modal('hide')
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
        $scope.new_row.ORG_CODE= res_msg;
        $("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal1']").modal("hide");
        move_element.modal('show')

        $scope.find_users_by_branches1();
        $scope.new_row.SALE_CODE= null;
        console.log(res_msg);
    }

    $scope.ztreeBtmClose1 = function(){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal1']").modal("hide");

        move_element.modal('show')
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
	    branchmanageService.get_branch_list({'branch_code':'966000'}).success(function (resp) {
            data = resp.data;
            show_branches(data)
            $.fn.zTree.init($("#loan_type_tree"+$scope.tabId), setting, Nodes);
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
	    branchmanageService.get_branch_list({'branch_code':'966000'}).success(function (resp) {
            data = resp.data;
            show_branches(data)
            $.fn.zTree.init($("#loan_type_tree1"+$scope.tabId), setting, Nodes);
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

        $scope.choose_branch_type1 = function(branch_code, branch_name, branch_level){
        console.log(branch_code,branch_name,branch_level)
        $scope.new_row.ORG_CODE= branch_code.replace(/(^\s*)|(\s*$)/g, "");
                        //$scope.ltSelected = false;
         }


    $scope.isManager = function() {
        $scope.flag=false;
        branchmanageService.get_user_permission({'user_id':$rootScope.user_session.user_id}).success(function(reps){
            if(reps.data>0)$scope.flag=true;
        });    
    }
    $scope.isManager();
    var internation_modal=angular.element('#internation_modal');
    $scope.internat_modal=function(){
        internation_modal.modal('show');
        $scope.internation_date_id=moment()
    }

    $scope.inter_count=function(){
        internation_modal.modal('hide');
        var nsd={'internation_date': $scope.internation_date_id.format('YYYYMMDD')} 
        $("div[name='loading']").modal("show");
        ebills_managerService.internation_count(nsd).success(function (reps){
            alert(reps.data)
            $("div[name='loading']").modal("hide");
            console.log(reps.data)
            $scope.cust_search.DATE_ID=$scope.internation_date_id
        }).error(function (reps){
            $("div[name='loading']").modal("hide");
        })
    }
    var element_edit=angular.element('#ebills_hook_edit_modal_11')
    var element_org_info =angular.element('#ebills_hook_distribution')
    var element_distri_list=angular.element('#ebills_distri_list')
    $scope.edit_org_code=""
    $scope.edit_org_name=""
    $scope.edit_sale_code=""
    $scope.edit_sale_name=""
    
    $scope.org_name=function(aa){
      if(aa!=$scope.edit_org_code){
        var nd={}    
        nd={'ORG_CODE':aa}
        ebills_managerService.total_cust_info(nd).success(function (reps){
        console.log(reps)
        $scope.custinfo_ebills.ORG_NAME=reps.data.ORG_NAME
        alert('请同步修改员工号和员工名')
       // $scope.custinfo_ebills.SALE_NAME=""
       // $scope.custinfo_ebills.SALE_CODE=""
      })
       }
       if(aa==$scope.edit_org_code){
        $scope.custinfo_ebills.ORG_NAME=$scope.edit_org_name
       }
    }
     $scope.sale_name=function(aa){
      if(aa!=$scope.edit_sale_code){
       var nd={}
        nd={'SALE_CODE':aa}
        ebills_managerService.total_cust_info(nd).success(function (reps){
        console.log(reps)
        $scope.custinfo_ebills.SALE_NAME=reps.data.SALE_NAME
      })
     }
     if(aa==$scope.edit_sale_code){
        $scope.custinfo_ebills.SALE_NAME=$scope.edit_sale_name
     }
    }
 
    $scope.edit = function(item){
        element_edit.modal('show');
        $scope.custinfo_ebills.MONTH              = item[0]
        $scope.custinfo_ebills.ORG_CODE           = item[1]
        $scope.custinfo_ebills.ORG_NAME           = item[2]
        $scope.edit_org_code= item[1]    
        $scope.edit_org_name=item[2]
        $scope.custinfo_ebills.CORPNAME           = item[3]
        $scope.custinfo_ebills.SALE_CODE          = item[4]
        $scope.edit_sale_code=item[4]
        $scope.custinfo_ebills.SALE_NAME          = item[5]
        $scope.edit_sale_name=item[5]
        $scope.custinfo_ebills.EXBPAMT            = item[6]
        $scope.custinfo_ebills.EXAGENTAMT         = item[7]
        $scope.custinfo_ebills.EXCLEANAMT         = item[8]
        $scope.custinfo_ebills.NTCLEANAMT         = item[9]
        $scope.custinfo_ebills.EXINREMITAMT       = item[11]
        $scope.custinfo_ebills.NTINREMITAMT       = item[12]
        $scope.custinfo_ebills.IMOUTREMTIAMT      = item[14]
        $scope.custinfo_ebills.NTOUTREMITAMT      = item[15]
        $scope.custinfo_ebills.IMLCAMT            = item[17]
        $scope.custinfo_ebills.IMICAMT            = item[18]
        $scope.custinfo_ebills.FIINREMITAMT       = item[19]
        $scope.custinfo_ebills.FIOUTREMITAMT      = item[20]
        $scope.custinfo_ebills.LGAMT              = item[21]
        $scope.custinfo_ebills.IMLGAMT            = item[22]
        $scope.custinfo_ebills.USANCEAMT          = item[24]
        $scope.custinfo_ebills.SIGHTAMT           = item[25]
        $scope.custinfo_ebills.CROSSBORDERAMT     = item[26]
        $scope.custinfo_ebills.MONTHAMT           = item[28]
        $scope.custinfo_ebills.DAYAMT             = item[29]
        $scope.custinfo_ebills.BALANCE            = item[30]
        $scope.custinfo_ebills.IS_OPEN_NEW_WH     = item[31]
        $scope.custinfo_ebills.ID                 = item[32]
        $scope.custinfo_ebills.CUST_IN_NO         = item[33]
    }
    $scope.is_new_open=false
    $scope.custinfo_ebills.THATYEAR_INTERACCT=false
    $scope.custinfo_ebills.LASTYEAR_FIRSTACCT=false
    $scope.custinfo_ebills.ONEYEAR_AGAINACCT=false

    $('#ebills_hook_edit_modal_11').on('hide.bs.modal',function(){
        $scope.is_new_open=false
        $scope.custinfo_ebills.THATYEAR_INTERACCT=false
        $scope.custinfo_ebills.LASTYEAR_FIRSTACCT=false
        $scope.custinfo_ebills.ONEYEAR_AGAINACCT=false
    })
    $scope.is_open=function(aa){
        console.log(aa)
        if(aa=='是'){
            $scope.is_new_open=true
        }
    }
    $scope.hook_edit_save = function (){
        var nd={}
        if($scope.custinfo_ebills.IS_OPEN_NEW_WH!='是'&&$scope.custinfo_ebills.IS_OPEN_NEW_WH!='否')
        {
            alert("请选择新开有效外汇账户的状态")
            return
        }
        if($scope.custinfo_ebills.IS_OPEN_NEW_WH=='是')
        {
            if($scope.custinfo_ebills.IS_OPEN_NEW_WH=='是'&& $scope.custinfo_ebills.THATYEAR_INTERACCT==false&&$scope.custinfo_ebills.LASTYEAR_FIRSTACCT==false&&$scope.custinfo_ebills.ONEYEAR_AGAINACCT==false)
            {
                alert('请选择新开外汇账户的类型')
                return
            }
            else if(($scope.custinfo_ebills.IS_OPEN_NEW_WH=='是'&& $scope.custinfo_ebills.THATYEAR_INTERACCT==true&&$scope.custinfo_ebills.LASTYEAR_FIRSTACCT==false&&$scope.custinfo_ebills.ONEYEAR_AGAINACCT==false)){
                    $scope.custinfo_ebills.THATYEAR_INTERACCT='1'       
            }
            else if(($scope.custinfo_ebills.IS_OPEN_NEW_WH=='是'&& $scope.custinfo_ebills.THATYEAR_INTERACCT==false&&$scope.custinfo_ebills.LASTYEAR_FIRSTACCT==true&&$scope.custinfo_ebills.ONEYEAR_AGAINACCT==false)){
                $scope.custinfo_ebills.LASTYEAR_FIRSTACCT='1'
            }
            else if(($scope.custinfo_ebills.IS_OPEN_NEW_WH=='是'&& $scope.custinfo_ebills.THATYEAR_INTERACCT==false&&$scope.custinfo_ebills.LASTYEAR_FIRSTACCT==false&&$scope.custinfo_ebills.ONEYEAR_AGAINACCT==true))
            {
                $scope.custinfo_ebills.ONEYEAR_AGAINACCT='1'
            }
            else{
                alert('有且只能选择一个新开有效外汇类型')
                return
            }
        }
        nd={'custinfo':$scope.custinfo_ebills}
        console.log($scope.custinfo_ebills.IS_OPEN_NEW_WH,$scope.custinfo_ebills.THATYEAR_INTERACCT,$scope.custinfo_ebills.LASTYEAR_FIRSTACCT,$scope.custinfo_ebills.ONEYEAR_AGAINACCT)
        ebills_managerService.hook_edit_save(nd).success(function (reps){
            alert(reps.data);
            $scope.search();
            $scope.is_new_open=false
            $scope.custinfo_ebills.THATYEAR_INTERACCT=false
            $scope.custinfo_ebills.LASTYEAR_FIRSTACCT=false
            $scope.custinfo_ebills.ONEYEAR_AGAINACCT=false
            element_edit.modal('hide');
        })
    }

   $scope.distribution=function(item){
        $scope.new_row.ORG_CODE=null
        $scope.new_row.SALE_CODE=null
        $scope.init_branches1()
        element_org_info.modal('show')
        $scope.original_row.MONTH              = item[0]
        $scope.original_row.ORG_CODE           = item[1]
        $scope.original_row.ORG_NAME           = item[2]
        $scope.original_row.CORPNAME           = item[3]
        $scope.original_row.SALE_CODE          = item[4]
        $scope.original_row.SALE_NAME          = item[5]
        $scope.original_row.EXBPAMT            = item[6]
        $scope.original_row.EXAGENTAMT         = item[7]
        $scope.original_row.EXCLEANAMT         = item[8]
        $scope.original_row.NTCLEANAMT         = item[9]
        $scope.original_row.EXINREMITAMT       = item[11]
        $scope.original_row.NTINREMITAMT       = item[12]
        $scope.original_row.IMOUTREMTIAMT      = item[14]
        $scope.original_row.NTOUTREMITAMT      = item[15]
        $scope.original_row.IMLCAMT            = item[17]
        $scope.original_row.IMICAMT            = item[18]
        $scope.original_row.FIINREMITAMT       = item[19]
        $scope.original_row.FIOUTREMITAMT      = item[20]
        $scope.original_row.LGAMT              = item[21]
        $scope.original_row.IMLGAMT            = item[22]
        $scope.original_row.USANCEAMT          = item[24]
        $scope.original_row.SIGHTAMT           = item[25]
        $scope.original_row.CROSSBORDERAMT     = item[26]
        $scope.original_row.MONTHAMT           = item[28]
        $scope.original_row.DAYAMT             = item[29]
        $scope.original_row.BALANCE            = item[30]
        $scope.original_row.IS_OPEN_NEW_WH     = item[31]
        $scope.original_row.ID                 = item[32]
        $scope.original_row.CUST_IN_NO         = item[33]
        $scope.new_row.MONTH=item[0] //月份
        $scope.new_row.CORPNAME= item[3]//客户名称
        $scope.new_row.CUST_IN_NO=item[33]//客户内码
        $scope.add_row.ORIG_MONTH     = item[0]//原始月
        $scope.add_row.ORIG_ORG_CODE  = item[1]//原始机构
        $scope.add_row.ORIG_ORG_NAME  = item[2]//原始机构名
        $scope.add_row.ORIG_CORPNAME  = item[3]//原始客户名称
        $scope.add_row.ORIG_SALE_CODE = item[4]//原始员工号
        $scope.add_row.ORIG_SALE_NAME = item[5]//原始员工名
        $scope.add_row.ORIG_CUST_IN_NO= item[33]//原始客户内码

        $scope.org_fen_row.EXBPAMT       = item[6]
        $scope.org_fen_row.EXAGENTAMT    = item[7]
        $scope.org_fen_row.EXCLEANAMT    = item[8]
        $scope.org_fen_row.NTCLEANAMT    = item[9]
        $scope.org_fen_row.EXINREMITAMT  = item[11]
        $scope.org_fen_row.NTINREMITAMT  = item[12]
        $scope.org_fen_row.IMOUTREMTIAMT = item[14]
        $scope.org_fen_row.NTOUTREMITAMT = item[15]
        $scope.org_fen_row.IMLCAMT       = item[17]
        $scope.org_fen_row.IMICAMT       = item[18]
        $scope.org_fen_row.FIINREMITAMT  = item[19]
        $scope.org_fen_row.FIOUTREMITAMT = item[20]
        $scope.org_fen_row.LGAMT         = item[21]
        $scope.org_fen_row.IMLGAMT       = item[22]
        $scope.org_fen_row.USANCEAMT     = item[24]
        $scope.org_fen_row.SIGHTAMT      = item[25]
        $scope.org_fen_row.CROSSBORDERAMT= item[26]
        $scope.org_fen_row.MONTHAMT      = item[28]
        $scope.org_fen_row.DAYAMT        = item[29]
        $scope.org_fen_row.BALANCE       = item[30]
 
     }
     
     $scope.info_mantch=function(){
        if($scope.new_row.ORG_CODE==""||$scope.new_row.ORG_CODE==null||$scope.new_row.SALE_CODE==null||$scope.new_row.SALE_CODE==""||$scope.new_row.ORG_CODE.split(',').length>1)
        {
          alert("机构号和员工号必填,且只能有1个")
          return;
        }
        $scope.new_row.SALE_NAME=$scope.new_row.SALE_CODE.name
        $scope.new_row.SALE_CODE=$scope.new_row.SALE_CODE.user_name
        var nd={}
        nd={'ORG_CODE':$scope.new_row.ORG_CODE,'SALE_CODE':$scope.new_row.SALE_CODE}
        ebills_managerService.total_cust_info(nd).success(function (reps){
            console.log(reps)
            $scope.new_row.ORG_NAME=reps.data.ORG_NAME
            $scope.add_row.NEW_ORG_CODE           = $scope.new_row.ORG_CODE//新机构
            $scope.add_row.NEW_ORG_NAME           = $scope.new_row.ORG_NAME//新机构名
            $scope.add_row.NEW_SALE_CODE          = $scope.new_row.SALE_CODE//新员工号
            $scope.add_row.NEW_SALE_NAME          = $scope.new_row.SALE_NAME//新员工名
            $scope.init_addrow()
            $scope.init_newrow()
            element_distri_list.modal('show')
        })
   };
    $scope.init_newrow=function(){
        $scope.new_row.EXBPAMT       =0 
        $scope.new_row.EXAGENTAMT    =0 
        $scope.new_row.EXCLEANAMT    =0 
        $scope.new_row.NTCLEANAMT    =0 
        $scope.new_row.EXINREMITAMT  =0 
        $scope.new_row.NTINREMITAMT  =0 
        $scope.new_row.IMOUTREMTIAMT =0 
        $scope.new_row.NTOUTREMITAMT =0 
        $scope.new_row.IMLCAMT       =0 
        $scope.new_row.IMICAMT       =0 
        $scope.new_row.FIINREMITAMT  =0 
        $scope.new_row.FIOUTREMITAMT =0 
        $scope.new_row.LGAMT         =0 
        $scope.new_row.IMLGAMT       =0 
        $scope.new_row.USANCEAMT     =0 
        $scope.new_row.SIGHTAMT      =0 
        $scope.new_row.CROSSBORDERAMT=0 
        $scope.new_row.MONTHAMT      =0 
        $scope.new_row.DAYAMT        =0 
        $scope.new_row.BALANCE       =0 

        //记得把新开有效外汇置成否,标志位都置成否
    }

    $scope.init_addrow=function(){
        $scope.add_row.EXBPAMT       =0 
        $scope.add_row.EXAGENTAMT    =0 
        $scope.add_row.EXCLEANAMT    =0 
        $scope.add_row.NTCLEANAMT    =0 
        $scope.add_row.EXINREMITAMT  =0 
        $scope.add_row.NTINREMITAMT  =0 
        $scope.add_row.IMOUTREMTIAMT =0 
        $scope.add_row.NTOUTREMITAMT =0 
        $scope.add_row.IMLCAMT       =0 
        $scope.add_row.IMICAMT       =0 
        $scope.add_row.FIINREMITAMT  =0 
        $scope.add_row.FIOUTREMITAMT =0 
        $scope.add_row.LGAMT         =0 
        $scope.add_row.IMLGAMT       =0 
        $scope.add_row.USANCEAMT     =0 
        $scope.add_row.SIGHTAMT      =0 
        $scope.add_row.CROSSBORDERAMT=0 
        $scope.add_row.MONTHAMT      =0 
        $scope.add_row.DAYAMT        =0 
        $scope.add_row.BALANCE       =0 
        //要建历史表,要原始月份,原始机构号,机构名,员工名,员工号,客户名,客户内码,转移的机构号,机构名,转移的员工号,员工名//以下还没开始做
    }
    $('#ebills_distri_list').on('hide.bs.modal',function(){
        element_org_info.modal('hide')
    })
    $scope.total_sum_save= function (){
        var nd={}
        $scope.new_row.IS_OPEN_NEW_WH='否'
        $scope.new_row.THATYEAR_INTERACCT='0'
        $scope.new_row.LASTYEAR_FIRSTACCT='0'
        $scope.new_row.ONEYEAR_AGAINACCT='0'
        $scope.add_row.EXBPAMT=(Number($scope.org_fen_row.EXBPAMT||0)*1000-Number($scope.original_row.EXBPAMT||0)*1000)/1000
        $scope.add_row.EXAGENTAMT=(Number($scope.org_fen_row.EXAGENTAMT||0)*1000-Number($scope.original_row.EXAGENTAMT||0)*1000)/1000
        $scope.add_row.EXCLEANAMT=(Number($scope.org_fen_row.EXCLEANAMT||0)*1000-Number($scope.original_row.EXCLEANAMT||0)*1000)/1000
        $scope.add_row.NTCLEANAMT=(Number($scope.org_fen_row.NTCLEANAMT||0)*1000-Number($scope.original_row.NTCLEANAMT||0)*1000)/1000
        $scope.add_row.EXINREMITAMT=(Number($scope.org_fen_row.EXINREMITAMT||0)*1000-Number($scope.original_row.EXINREMITAMT||0)*1000)/1000
        $scope.add_row.NTINREMITAMT=(Number($scope.org_fen_row.NTINREMITAMT||0)*1000-Number($scope.original_row.NTINREMITAMT||0)*1000)/1000
        $scope.add_row.IMOUTREMTIAMT=(Number($scope.org_fen_row.IMOUTREMTIAMT||0)*1000-Number($scope.original_row.IMOUTREMTIAMT||0)*1000)/1000
        $scope.add_row.NTOUTREMITAMT=(Number($scope.org_fen_row.NTOUTREMITAMT||0)*1000-Number($scope.original_row.NTOUTREMITAMT||0)*1000)/1000
        $scope.add_row.IMLCAMT=(Number($scope.org_fen_row.IMLCAMT||0)*1000-Number($scope.original_row.IMLCAMT||0)*1000)/1000
        $scope.add_row.IMICAMT=(Number($scope.org_fen_row.IMICAMT||0)*1000-Number($scope.original_row.IMICAMT||0)*1000)/1000
        $scope.add_row.FIINREMITAMT=(Number($scope.org_fen_row.FIINREMITAMT||0)*1000-Number($scope.original_row.FIINREMITAMT||0)*1000)/1000
        $scope.add_row.FIOUTREMITAMT=(Number($scope.org_fen_row.FIOUTREMITAMT||0)*1000-Number($scope.original_row.FIOUTREMITAMT||0)*1000)/1000
        $scope.add_row.LGAMT=(Number($scope.org_fen_row.LGAMT||0)*1000-Number($scope.original_row.LGAMT||0)*1000)/1000
        $scope.add_row.IMLGAMT=(Number($scope.org_fen_row.IMLGAMT||0)*1000-Number($scope.original_row.IMLGAMT||0)*1000)/1000
        $scope.add_row.USANCEAMT=(Number($scope.org_fen_row.USANCEAMT||0)*1000-Number($scope.original_row.USANCEAMT||0)*1000)/1000
        $scope.add_row.SIGHTAMT=(Number($scope.org_fen_row.SIGHTAMT||0)*1000-Number($scope.original_row.SIGHTAMT||0)*1000)/1000
        $scope.add_row.CROSSBORDERAMT=(Number($scope.org_fen_row.CROSSBORDERAMT||0)*1000-Number($scope.original_row.CROSSBORDERAMT||0)*1000)/1000
        $scope.add_row.MONTHAMT=(Number($scope.org_fen_row.MONTHAMT||0)*1000-Number($scope.original_row.MONTHAMT||0)*1000)/1000
        $scope.add_row.DAYAMT=(Number($scope.org_fen_row.DAYAMT||0)*1000-Number($scope.original_row.DAYAMT||0)*1000)/1000
        $scope.add_row.BALANCE=(Number($scope.org_fen_row.BALANCE||0)*1000-Number($scope.original_row.BALANCE||0)*1000)/1000
        nd={"original_row":$scope.original_row,'new_row':$scope.new_row,'add_row':$scope.add_row}
        ebills_managerService.total_sum_save(nd).success(function(reps){
            alert(reps.data);
            element_org_info.modal('hide')
            element_distri_list.modal('hide');
            $scope.add_row={}
            $scope.init_addrow()
            $scope.new_row={}
            $scope.init_newrow()
            $scope.search()
        }).error(function (reps){
            element_org_info.modal('hide')
            element_distri_list.modal('hide');
            $scope.search()
        })
    }

    $scope.total_sum=function(flag){
       if (flag=='6'){
         if($scope.add_row.EXBPAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.EXBPAMT=0
            return
        }
       if(Number($scope.original_row.EXBPAMT||0)<Number($scope.add_row.EXBPAMT||0)||Number($scope.new_row.EXBPAMT||0)<-Number($scope.add_row.EXBPAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.EXBPAMT=0
       }
      else{
            $scope.original_row.EXBPAMT=(Number($scope.original_row.EXBPAMT||0)*1000-Number($scope.add_row.EXBPAMT||0)*1000)/1000 
            $scope.new_row.EXBPAMT=(Number($scope.new_row.EXBPAMT||0)*1000+Number($scope.add_row.EXBPAMT||0)*1000)/1000
        }
       }

       if (flag=='7'){
         if($scope.add_row.EXAGENTAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.EXAGENTAMT=0
            return
        }
       if(Number($scope.original_row.EXAGENTAMT||0)<Number($scope.add_row.EXAGENTAMT||0)||Number($scope.new_row.EXAGENTAMT||0)<-Number($scope.add_row.EXAGENTAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.EXAGENTAMT=0
       }
      else{
            $scope.original_row.EXAGENTAMT=(Number($scope.original_row.EXAGENTAMT||0)*1000-Number($scope.add_row.EXAGENTAMT||0)*1000)/1000 
            $scope.new_row.EXAGENTAMT=(Number($scope.new_row.EXAGENTAMT||0)*1000+Number($scope.add_row.EXAGENTAMT||0)*1000)/1000
        }
       }
 
       if (flag=='8'){
          if($scope.add_row.EXCLEANAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.EXCLEANAMT=0
            return
        }
      if(Number($scope.original_row.EXCLEANAMT||0)<Number($scope.add_row.EXCLEANAMT||0)||Number($scope.new_row.EXCLEANAMT||0)<-Number($scope.add_row.EXCLEANAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.EXCLEANAMT=0
       }
      else{
            $scope.original_row.EXCLEANAMT=(Number($scope.original_row.EXCLEANAMT||0)*1000-Number($scope.add_row.EXCLEANAMT||0)*1000)/1000 
            $scope.new_row.EXCLEANAMT=(Number($scope.new_row.EXCLEANAMT||0)*1000+Number($scope.add_row.EXCLEANAMT||0)*1000)/1000
        }
       }
 
       if (flag=='9'){
         if($scope.add_row.NTCLEANAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.NTCLEANAMT=0
            return
        }
       if(Number($scope.original_row.NTCLEANAMT||0)<Number($scope.add_row.NTCLEANAMT||0)||Number($scope.new_row.NTCLEANAMT||0)<-Number($scope.add_row.NTCLEANAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.NTCLEANAMT=0
       }
      else{
            $scope.original_row.NTCLEANAMT=(Number($scope.original_row.NTCLEANAMT||0)*1000-Number($scope.add_row.NTCLEANAMT||0)*1000)/1000 
            $scope.new_row.NTCLEANAMT=(Number($scope.new_row.NTCLEANAMT||0)*1000+Number($scope.add_row.NTCLEANAMT||0)*1000)/1000
        }
       }
 
       if (flag=='11'){
         if($scope.add_row.EXINREMITAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.EXINREMITAMT=0
            return
        }
       if(Number($scope.original_row.EXINREMITAMT||0)<Number($scope.add_row.EXINREMITAMT||0)||Number($scope.new_row.EXINREMITAMT||0)<-Number($scope.add_row.EXINREMITAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.EXINREMITAMT=0
       }
      else{
            $scope.original_row.EXINREMITAMT=(Number($scope.original_row.EXINREMITAMT||0)*1000-Number($scope.add_row.EXINREMITAMT||0)*1000)/1000 
            $scope.new_row.EXINREMITAMT=(Number($scope.new_row.EXINREMITAMT||0)*1000+Number($scope.add_row.EXINREMITAMT||0)*1000)/1000
        }
       }
 
       if (flag=='12'){
         if($scope.add_row.NTINREMITAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.NTINREMITAMT=0
            return
        }
       if(Number($scope.original_row.NTINREMITAMT||0)<Number($scope.add_row.NTINREMITAMT||0)||Number($scope.new_row.NTINREMITAMT||0)<-Number($scope.add_row.NTINREMITAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.NTINREMITAMT=0
       }
      else{
            $scope.original_row.NTINREMITAMT=(Number($scope.original_row.NTINREMITAMT||0)*1000-Number($scope.add_row.NTINREMITAMT||0)*1000)/1000 
            $scope.new_row.NTINREMITAMT=(Number($scope.new_row.NTINREMITAMT||0)*1000+Number($scope.add_row.NTINREMITAMT||0)*1000)/1000
        }
       }
 
       if (flag=='14'){
         if($scope.add_row.IMOUTREMTIAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.IMOUTREMTIAMT=0
            return
        }
       if(Number($scope.original_row.IMOUTREMTIAMT||0)<Number($scope.add_row.IMOUTREMTIAMT||0)||Number($scope.new_row.IMOUTREMTIAMT||0)<-Number($scope.add_row.IMOUTREMTIAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.IMOUTREMTIAMT=0
       }
      else{
            $scope.original_row.IMOUTREMTIAMT=(Number($scope.original_row.IMOUTREMTIAMT||0)*1000-Number($scope.add_row.IMOUTREMTIAMT||0)*1000)/1000 
            $scope.new_row.IMOUTREMTIAMT=(Number($scope.new_row.IMOUTREMTIAMT||0)*1000+Number($scope.add_row.IMOUTREMTIAMT||0)*1000)/1000
        }
       }
 
       if (flag=='15'){
         if($scope.add_row.NTOUTREMITAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.NTOUTREMITAMT=0
            return
        }
       if(Number($scope.original_row.NTOUTREMITAMT||0)<Number($scope.add_row.NTOUTREMITAMT||0)||Number($scope.new_row.NTOUTREMITAMT||0)<-Number($scope.add_row.NTOUTREMITAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.NTOUTREMITAMT=0
       }
      else{
            $scope.original_row.NTOUTREMITAMT=(Number($scope.original_row.NTOUTREMITAMT||0)*1000-Number($scope.add_row.NTOUTREMITAMT||0)*1000)/1000 
            $scope.new_row.NTOUTREMITAMT=(Number($scope.new_row.NTOUTREMITAMT||0)*1000+Number($scope.add_row.NTOUTREMITAMT||0)*1000)/1000
        }
       }
 
       if (flag=='17'){
         if($scope.add_row.IMLCAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.IMLCAMT=0
            return
        }
       if(Number($scope.original_row.IMLCAMT||0)<Number($scope.add_row.IMLCAMT||0)||Number($scope.new_row.IMLCAMT||0)<-Number($scope.add_row.IMLCAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.IMLCAMT=0
       }
      else{
            $scope.original_row.IMLCAMT=(Number($scope.original_row.IMLCAMT||0)*1000-Number($scope.add_row.IMLCAMT||0)*1000)/1000 
            $scope.new_row.IMLCAMT=(Number($scope.new_row.IMLCAMT||0)*1000+Number($scope.add_row.IMLCAMT||0)*1000)/1000
        }
       }
 
       if (flag=='18'){
         if($scope.add_row.IMICAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.IMICAMT=0
            return
        }
       if(Number($scope.original_row.IMICAMT||0)<Number($scope.add_row.IMICAMT||0)||Number($scope.new_row.IMICAMT||0)<-Number($scope.add_row.IMICAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.IMICAMT=0
       }
      else{
            $scope.original_row.IMICAMT=(Number($scope.original_row.IMICAMT||0)*1000-Number($scope.add_row.IMICAMT||0)*1000)/1000 
            $scope.new_row.IMICAMT=(Number($scope.new_row.IMICAMT||0)*1000+Number($scope.add_row.IMICAMT||0)*1000)/1000
        }
       }
 
       if (flag=='19'){
         if($scope.add_row.FIINREMITAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.FIINREMITAMT=0
            return
        }
       if(Number($scope.original_row.FIINREMITAMT||0)<Number($scope.add_row.FIINREMITAMT||0)||Number($scope.new_row.FIINREMITAMT||0)<-Number($scope.add_row.FIINREMITAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.FIINREMITAMT=0
       }
      else{
            $scope.original_row.FIINREMITAMT=(Number($scope.original_row.FIINREMITAMT||0)*1000-Number($scope.add_row.FIINREMITAMT||0)*1000)/1000 
            $scope.new_row.FIINREMITAMT=(Number($scope.new_row.FIINREMITAMT||0)*1000+Number($scope.add_row.FIINREMITAMT||0)*1000)/1000
        }
       }
 
       if (flag=='20'){
         if($scope.add_row.FIOUTREMITAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.FIOUTREMITAMT=0
            return
        }
       if(Number($scope.original_row.FIOUTREMITAMT||0)<Number($scope.add_row.FIOUTREMITAMT||0)||Number($scope.new_row.FIOUTREMITAMT||0)<-Number($scope.add_row.FIOUTREMITAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.FIOUTREMITAMT=0
       }
      else{
            $scope.original_row.FIOUTREMITAMT=(Number($scope.original_row.FIOUTREMITAMT||0)*1000-Number($scope.add_row.FIOUTREMITAMT||0)*1000)/1000 
            $scope.new_row.FIOUTREMITAMT=(Number($scope.new_row.FIOUTREMITAMT||0)*1000+Number($scope.add_row.FIOUTREMITAMT||0)*1000)/1000
        }
       }
 
       if (flag=='21'){
         if($scope.add_row.LGAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.LGAMT=0
            return
        }
       if(Number($scope.original_row.LGAMT||0)<Number($scope.add_row.LGAMT||0)||Number($scope.new_row.LGAMT||0)<-Number($scope.add_row.LGAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.LGAMT=0
       }
      else{
            $scope.original_row.LGAMT=(Number($scope.original_row.LGAMT||0)*1000-Number($scope.add_row.LGAMT||0)*1000)/1000 
            $scope.new_row.LGAMT=(Number($scope.new_row.LGAMT||0)*1000+Number($scope.add_row.LGAMT||0)*1000)/1000
        }
       }
 
       if (flag=='22'){
         if($scope.add_row.IMLGAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.IMLGAMT=0
            return
        }
       if(Number($scope.original_row.IMLGAMT||0)<Number($scope.add_row.IMLGAMT||0)||Number($scope.new_row.IMLGAMT||0)<-Number($scope.add_row.IMLGAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.IMLGAMT=0
       }
      else{
            $scope.original_row.IMLGAMT=(Number($scope.original_row.IMLGAMT||0)*1000-Number($scope.add_row.IMLGAMT||0)*1000)/1000 
            $scope.new_row.IMLGAMT=(Number($scope.new_row.IMLGAMT||0)*1000+Number($scope.add_row.IMLGAMT||0)*1000)/1000
        }
       }
 
       if (flag=='24'){
         if($scope.add_row.USANCEAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.USANCEAMT=0
            return
        }
       if(Number($scope.original_row.USANCEAMT||0)<Number($scope.add_row.USANCEAMT||0)||Number($scope.new_row.USANCEAMT||0)<-Number($scope.add_row.USANCEAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.USANCEAMT=0
       }
      else{
            $scope.original_row.USANCEAMT=(Number($scope.original_row.USANCEAMT||0)*1000-Number($scope.add_row.USANCEAMT||0)*1000)/1000 
            $scope.new_row.USANCEAMT=(Number($scope.new_row.USANCEAMT||0)*1000+Number($scope.add_row.USANCEAMT||0)*1000)/1000
        }
       }
 
       if (flag=='25'){
         if($scope.add_row.SIGHTAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.SIGHTAMT=0
            return
        }
       if(Number($scope.original_row.SIGHTAMT||0)<Number($scope.add_row.SIGHTAMT||0)||Number($scope.new_row.SIGHTAMT||0)<-Number($scope.add_row.SIGHTAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.SIGHTAMT=0
       }
      else{
            $scope.original_row.SIGHTAMT=(Number($scope.original_row.SIGHTAMT||0)*1000-Number($scope.add_row.SIGHTAMT||0)*1000)/1000 
            $scope.new_row.SIGHTAMT=(Number($scope.new_row.SIGHTAMT||0)*1000+Number($scope.add_row.SIGHTAMT||0)*1000)/1000
        }
       }
 
       if (flag=='26'){
         if($scope.add_row.CROSSBORDERAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.CROSSBORDERAMT=0
            return
        }
       if(Number($scope.original_row.CROSSBORDERAMT||0)<Number($scope.add_row.CROSSBORDERAMT||0)||Number($scope.new_row.CROSSBORDERAMT||0)<-Number($scope.add_row.CROSSBORDERAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.CROSSBORDERAMT=0
       }
      else{
            $scope.original_row.CROSSBORDERAMT=(Number($scope.original_row.CROSSBORDERAMT||0)*1000-Number($scope.add_row.CROSSBORDERAMT||0)*1000)/1000 
            $scope.new_row.CROSSBORDERAMT=(Number($scope.new_row.CROSSBORDERAMT||0)*1000+Number($scope.add_row.CROSSBORDERAMT||0)*1000)/1000
        }
       }
 
       if (flag=='28'){
         if($scope.add_row.MONTHAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.MONTHAMT=0
            return
        }
       if(Number($scope.original_row.MONTHAMT||0)<Number($scope.add_row.MONTHAMT||0)||Number($scope.new_row.MONTHAMT||0)<-Number($scope.add_row.MONTHAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.MONTHAMT=0
       }
      else{
            $scope.original_row.MONTHAMT=(Number($scope.original_row.MONTHAMT||0)*1000-Number($scope.add_row.MONTHAMT||0)*1000)/1000 
            $scope.new_row.MONTHAMT=(Number($scope.new_row.MONTHAMT||0)*1000+Number($scope.add_row.MONTHAMT||0)*1000)/1000
        }
       }
 
       if (flag=='29'){
         if($scope.add_row.DAYAMT.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.DAYAMT=0
            return
        }
       if(Number($scope.original_row.DAYAMT||0)<Number($scope.add_row.DAYAMT||0)||Number($scope.new_row.DAYAMT||0)<-Number($scope.add_row.DAYAMT||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.DAYAMT=0
       }
      else{
            $scope.original_row.DAYAMT=(Number($scope.original_row.DAYAMT||0)*1000-Number($scope.add_row.DAYAMT||0)*1000)/1000 
            $scope.new_row.DAYAMT=(Number($scope.new_row.DAYAMT||0)*1000+Number($scope.add_row.DAYAMT||0)*1000)/1000
        }
       }
 
       if (flag=='30'){
         if($scope.add_row.BALANCE.substr(0,1)=='N'){
            alert('分配额度有误,请检查')
            $scope.add_row.BALANCE=0
            return
        }
       if(Number($scope.original_row.BALANCE||0)<Number($scope.add_row.BALANCE||0)||Number($scope.new_row.BALANCE||0)<-Number($scope.add_row.BALANCE||0))
       {
            alert('分配额度超出,请检查')
            $scope.add_row.BALANCE=0
       }
      else{
            $scope.original_row.BALANCE=(Number($scope.original_row.BALANCE||0)*1000-Number($scope.add_row.BALANCE||0)*1000)/1000 
            $scope.new_row.BALANCE=(Number($scope.new_row.BALANCE||0)*1000+Number($scope.add_row.BALANCE||0)*1000)/1000
        }
       }
   

    }

};

ebills_hookController.$inject = ['$scope', '$rootScope', '$filter', 'SqsReportService', 'permissionService','branchmanageService','ebills_managerService'];

angular.module('YSP').service('ebills_hookController', ebills_hookController); 
