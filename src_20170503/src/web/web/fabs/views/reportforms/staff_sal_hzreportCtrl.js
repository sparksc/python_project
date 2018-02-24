/**
 * Mandep Controller
 */
function StaffSalHZReportController($scope, $rootScope, store,$filter,SqsReportService, permissionService,branchmanageService,StaffSalHzService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "点击查询";
    $scope.cust_search = {};
    $scope.custinfo={};
    $scope.dep={};
    $scope.loan={};
    $scope.ebank={};
    $scope.card={};
    $scope.custinfo_add={};
    $scope.dep_add={};
    $scope.loan_add={};
    $scope.ebank_add={};
    $scope.card_add={};

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
    $scope.search = function() {
        $("div[name='loading']").modal("show");
        params = {};        
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/staff_sal_hzrep?export=1"+"&DATE_ID="+ $scope.cust_search.DATE_ID.format("YYYYMMDD") + "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            if(key=='DATE_ID')params['DATE_ID']=params['DATE_ID'].format("YYYYMMDD");
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }

        SqsReportService.info('staff_sal_hzrep',params).success(function(resp) {
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
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查到数据";
            }
        });
    }
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/staff_sal_hzrep?export=1a"+"&DATE_ID="+ $scope.cust_search.DATE_ID.format("YYYYMMDD") + "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code;

    $scope.find_users_by_branches = function(){
        branchmanageService.find_users_by_branches({'branch_id':$scope.cust_search.org}).success(function(reps){
            $scope.model2 =reps.data;
       });
    };

    $scope.show_lt_modal1 = function(trigger_elem){
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
           // if (nodes[i].id.charAt(0) == 'M')
           // {
           //     continue
           // }
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
    var element_edit = angular.element('#staffSal_hzinput_edit_modal');
    var element_add = angular.element('#staffSal_hzinput_add_modal');
   $scope.upload_excel = function(){
    var files = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#elec_arch").prop('files');
    console.log('bbbbb',files)
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
                url : base_url+"/staff_sal_hzinput/upload/",
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

        $scope.sdelete = function(row){
        if(confirm("确认删除？")){
            var nsd={};
            nsd["DATE_ID"]=row[0];
            nsd["ORG_CODE"]=row[1];
            nsd["SALE_CODE"]=row[3];
            var nd = {"newdata":nsd};
            StaffSalHzService.ssdelete(nd).success(function (reps){
                alert(reps.data)
                $scope.search();
            });
        }

        };

        $scope.edit = function(item){
        element_edit.modal('show');
        $scope.custinfo.DATE_ID=item[0];
        $scope.custinfo.ORG_CODE=item[1];
        $scope.custinfo.ORG_NAME=item[2]
        $scope.custinfo.SALE_CODE=item[3]
        $scope.custinfo.SALE_NAME=item[4]
        $scope.custinfo.HZ_BASE_PAY  =item[7]
        $scope.custinfo.HZ_POSITION_PAY  =item[8]
        $scope.custinfo.HZ_NET_BUS_SAL  =item[9]
        $scope.custinfo.HZ_COMPRE_SAL  =item[10]
        $scope.custinfo.HZ_LABOR_COMP_SAL  =item[11]
        $scope.custinfo.HZ_PROV_FUND_SAL  =item[12]
        $scope.custinfo.HZ_SAFE_FAN_SAL  =item[13]
        $scope.custinfo.HZ_ALL_RISK_SAL  =item[14]
        $scope.custinfo.HZ_BAD_LOAN_PERSAL  =item[15]
        $scope.custinfo.HZ_FTP_ACH_SAL  =item[16]
        $scope.custinfo.HZ_COUNT_COMPLE_SAL  =item[17]
        $scope.custinfo.HZ_OTHER_SPEC_SAL1  =item[18]
        $scope.custinfo.HZ_OTHER_SPEC_SAL2  =item[19]
        $scope.custinfo.HZ_OTHER_SPEC_SAL3  =item[20]
        $scope.custinfo.HZ_OTHER_SPEC_SAL4  =item[21]
        $scope.custinfo.HZ_OTHER_SPEC_SAL5  =item[22]
        $scope.custinfo.HZ_OTHER_SAL1  =item[23]
        $scope.custinfo.HZ_OTHER_SAL2  =item[24]
        $scope.custinfo.HZ_OTHER_SAL3  =item[25]
        $scope.custinfo.HZ_OTHER_SAL4  =item[26]
        $scope.custinfo.HZ_OTHER_SAL5  =item[27]

    }
    $scope.edit_save = function (){
        element_edit.modal('hide');
        var nd={}
        nd={'custinfo':$scope.custinfo}
        StaffSalHzService.edit_save(nd).success(function (reps){
            alert(reps.data);
            $scope.search();
        })
    }


        $scope.add = function(){
        element_add.modal('show');
        $scope.custinfo_add.DATE_ID=moment();
        $scope.custinfo_add.ORG_CODE=""
        $scope.custinfo_add.ORG_NAME=""
        $scope.custinfo_add.SALE_CODE=""
        $scope.custinfo_add.SALE_NAME=""
        $scope.custinfo_add.HZ_BASE_PAY  =""
        $scope.custinfo_add.HZ_POSITION_PAY  =""
        $scope.custinfo_add.HZ_NET_BUS_SAL  =""
        $scope.custinfo_add.HZ_COMPRE_SAL  =""
        $scope.custinfo_add.HZ_LABOR_COMP_SAL  =""
        $scope.custinfo_add.HZ_PROV_FUND_SAL  =""
        $scope.custinfo_add.HZ_SAFE_FAN_SAL  =""
        $scope.custinfo_add.HZ_ALL_RISK_SAL  =""
        $scope.custinfo_add.HZ_BAD_LOAN_PERSAL  =""
        $scope.custinfo_add.HZ_FTP_ACH_SAL  =""
        $scope.custinfo_add.HZ_COUNT_COMPLE_SAL  =""
        $scope.custinfo_add.HZ_OTHER_SPEC_SAL1  =""
        $scope.custinfo_add.HZ_OTHER_SPEC_SAL2  =""
        $scope.custinfo_add.HZ_OTHER_SPEC_SAL3  =""
        $scope.custinfo_add.HZ_OTHER_SPEC_SAL4  =""
        $scope.custinfo_add.HZ_OTHER_SPEC_SAL5  =""
        $scope.custinfo_add.HZ_OTHER_SAL1  =""
        $scope.custinfo_add.HZ_OTHER_SAL2  =""
        $scope.custinfo_add.HZ_OTHER_SAL3  =""
        $scope.custinfo_add.HZ_OTHER_SAL4  =""
        $scope.custinfo_add.HZ_OTHER_SAL5  =""

    }

    $scope.add_save = function (){
    element_add.modal('hide');
    $scope.custinfo_add.DATE_ID=$scope.custinfo_add.DATE_ID.format('YYYYMMDD')
    var nd={}
    nd={'custinfo_add':$scope.custinfo_add}
    StaffSalHzService.add_save(nd).success(function (reps){
        alert(reps.data);
        $scope.search();
        $scope.custinfo_add.DATE_ID=""
    })
    }


};





StaffSalHZReportController.$inject = ['$scope', '$rootScope', 'store','$filter', 'SqsReportService', 'permissionService','branchmanageService','StaffSalHzService'];

angular.module('YSP').service('StaffSalHZReportController', StaffSalHZReportController); 
