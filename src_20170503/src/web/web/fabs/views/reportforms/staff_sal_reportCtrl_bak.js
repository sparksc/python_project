/**
 * Mandep Controller
 */
function StaffSalReportController($scope, $rootScope, store,$filter,SqsReportService, permissionService,branchmanageService,StaffSalNewService) {
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
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/staff_sal_rep?export=1"+"&DATE_ID="+ $scope.cust_search.DATE_ID.format("YYYYMMDD") + "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            if(key=='DATE_ID')params['DATE_ID']=params['DATE_ID'].format("YYYYMMDD");
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }

        SqsReportService.info('staff_sal_rep',params).success(function(resp) {
            $("div[name='loading']").modal("hide");
            $scope.data = resp;
         console.log(resp)
	    if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查到数据";
            }
        });
    }
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/staff_sal_rep?export=1a"+"&DATE_ID="+ $scope.cust_search.DATE_ID.format("YYYYMMDD") + "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code;

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
    var element_edit = angular.element('#staffSal_input_edit_modal');
    var element_add = angular.element('#staffSal_input_add_modal');
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
                url : base_url+"/staff_sal_input/upload/",
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
            console.log(nsd);
            console.log(StaffSalNewService.ssdelete)
            var nd = {"newdata":nsd};
            StaffSalNewService.ssdelete(nd).success(function (reps){
                alert(reps.data)

                $scope.search();
            });
        }
        };
        var LAST_AVG_SAL_flag=""
        $scope.edit = function(item){
            element_edit.modal('show');
            $scope.custinfo.DATE_ID=item[0];
            $scope.custinfo.ORG_CODE=item[1];
            $scope.custinfo.ORG_NAME=item[2]
            $scope.custinfo.SALE_CODE=item[3]
            $scope.custinfo.SALE_NAME=item[4]
            $scope.dep.LAST_AVG_SAL=item[7] //存款,贷款等下记得*100000000,而信用卡不用任何操作
            LAST_AVG_SAL_flag=item[7]
            $scope.dep.ADD_AVG_SAL=item[8]
            $scope.loan.TOTAL_NUM_SAL =item[9]
            $scope.loan.AVG_SAL=item[10]
            $scope.loan.PRI_ADD_NUM_SAL=item[11]
            $scope.loan.PUB_ADD_NUM_SAL=item[12]
            $scope.loan.ADD_AVG_ASL=item[13]
            $scope.loan.TWO_CARD_LOANRATE_SAL=item[14]
            $scope.loan.ELEC_FILE_INFO_SAL=item[15]
            $scope.card.SALARY=item[16]
            $scope.ebank.MB_ADD_NUM_SAL=item[17]
            $scope.ebank.CB_ADD_NUM_SAL=item[18]
            $scope.ebank.EPAY_ADD_NUM_SAL=item[19]
            $scope.ebank.ADD_HIGH_POS_SAL=item[20]
            $scope.ebank.ADD_LOW_POS_SAL=item[21]
            $scope.ebank.FARM_SERV_SAL=item[22]
            $scope.ebank.ADD_THIRD_DEPO_SAL=item[23]
            $scope.ebank.ADD_ETC_NUM_SAL=item[24]
            $scope.ebank.BASE_PAY=item[25]
            $scope.ebank.POSITION_PAY=item[26]
            $scope.ebank.BRANCH_NET_SAL=item[27]
            $scope.ebank.MANAGE_BUS_SAL=item[28]
            $scope.ebank.WORK_QUALITY_SAL=item[29]
            $scope.ebank.HIG_CIV_QUAL_SAL=item[30]
            $scope.ebank.JOB_SAT_SAL=item[31]
            $scope.ebank.DAY_DEP_COMP_PER=item[32]
            $scope.ebank.DAY_DEP_SAL=item[33]
            $scope.ebank.DAY_DEP_SEC_FEN=item[34]
            $scope.ebank.CREDIT_POOL=item[35]
            $scope.ebank.INTER_SET_SAL=item[36]
            $scope.ebank.SALE_VOC_SAL=item[37]
            $scope.ebank.ADD_EFC_CURSAL=item[38]
            $scope.ebank.ADD_FUNON_SAL=item[39]
            $scope.ebank.PER_CAR_DANERSAL=item[40]
            $scope.ebank.BUM_HOM_SAL=item[41]
            $scope.ebank.OTHER_ACHI_SAL=item[42]
            $scope.ebank.COMPRE_SAL=item[43]
            $scope.ebank.LABOR_COMP_SAL=item[44]
            $scope.ebank.PROV_FUND_SAL=item[45]
            $scope.ebank.SAFE_FAN_SAL=item[46]
            $scope.ebank.ALL_RISK_SAL=item[47]
            $scope.ebank.BAD_LOAN_PERSAL=item[48]
            $scope.ebank.FTP_ACH_SAL=item[49]
            $scope.ebank.COUNT_COMPLE_SAL=item[50]
            $scope.ebank.COUNT_COP_SSAL=item[51]
            $scope.ebank.HP_FINA_SAL=item[52]
            $scope.ebank.OTHER_SPEC_SAL1=item[53]
            $scope.ebank.OTHER_SPEC_SAL2=item[54]
            $scope.ebank.OTHER_SPEC_SAL3=item[55]
            $scope.ebank.OTHER_SPEC_SAL4=item[56]
            $scope.ebank.OTHER_SPEC_SAL5=item[57]
            $scope.ebank.BRANCH_SECO_FEN1=item[58]
            $scope.ebank.BRANCH_SECO_FEN2=item[59]
            $scope.ebank.BRANCH_SECO_FEN3=item[60]
            $scope.ebank.BRANCH_SECO_FEN4=item[61]
            $scope.ebank.OTHER_ACH_WAGES=item[62]
            $scope.ebank.OVER_WORK_SAL=item[63]
            $scope.ebank.OTHER_SAL1_DUAN=item[64]
            $scope.ebank.OTHER_SAL2=item[65]
            $scope.ebank.OTHER_SAL3_WEI=item[66]
            $scope.ebank.OTHER_SAL4_KE=item[67]
            $scope.ebank.OTHER_SAL5_GE=item[68]
            $scope.ebank.OTHER_SAL6=item[60]
            $scope.ebank.OTHER_SAL7=item[70]
            $scope.ebank.OTHER_SAL8=item[71]
            $scope.ebank.QJ_BAD_LOAN_SAL=item[72]
        }


        $scope.edit_save = function (){
            element_edit.modal('hide');
            if(LAST_AVG_SAL_flag==$scope.dep.LAST_AVG_SAL){
               $scope.dep.LAST_AVG_SAL=Number(LAST_AVG_SAL_flag)*12
               $scope.dep.LAST_AVG_SAL=$scope.dep.LAST_AVG_SAL.toString()
            var nd={}
            nd={'custinfo':$scope.custinfo,'loan':$scope.loan,'ebank':$scope.ebank,'card':$scope.card,'dep':$scope.dep}
            StaffSalNewService.edit_save(nd).success(function (reps){
            alert(reps.data);
            $scope.search();
            })
            }
            else{
                var nd={}
                nd={'custinfo':$scope.custinfo,'loan':$scope.loan,'ebank':$scope.ebank,'card':$scope.card,'dep':$scope.dep}
                StaffSalNewService.edit_save(nd).success(function (reps){
                alert(reps.data);
                $scope.search();
                })
            
            }

        }

        $scope.add = function(){
            element_add.modal('show');
            $scope.custinfo_add.DATE_ID=moment();
            $scope.custinfo_add.ORG_CODE=''
            $scope.custinfo_add.ORG_NAME=''
            $scope.custinfo_add.SALE_CODE=''
            $scope.custinfo_add.SALE_NAME=''
            $scope.dep_add.LAST_AVG_SAL=''
            $scope.dep_add.ADD_AVG_SAL=''
            $scope.loan_add.TOTAL_NUM_SAL =''
            $scope.loan_add.AVG_SAL=''
            $scope.loan_add.PRI_ADD_NUM_SAL=''
            $scope.loan_add.PUB_ADD_NUM_SAL=''
            $scope.loan_add.ADD_AVG_ASL=''
            $scope.loan_add.TWO_CARD_LOANRATE_SAL=''
            $scope.loan_add.ELEC_FILE_INFO_SAL=''
            $scope.card_add.SALARY=''
            $scope.ebank_add.MB_ADD_NUM_SAL=''
            $scope.ebank_add.CB_ADD_NUM_SAL=''
            $scope.ebank_add.EPAY_ADD_NUM_SAL=''
            $scope.ebank_add.ADD_HIGH_POS_SAL=''
            $scope.ebank_add.ADD_LOW_POS_SAL=''
            $scope.ebank_add.FARM_SERV_SAL=''
            $scope.ebank_add.ADD_THIRD_DEPO_SAL=''
            $scope.ebank_add.ADD_ETC_NUM_SAL=''
            $scope.ebank_add.BASE_PAY=''
            $scope.ebank_add.POSITION_PAY=''
            $scope.ebank_add.BRANCH_NET_SAL=''
            $scope.ebank_add.MANAGE_BUS_SAL=''
            $scope.ebank_add.WORK_QUALITY_SAL=''
            $scope.ebank_add.HIG_CIV_QUAL_SAL=''
            $scope.ebank_add.JOB_SAT_SAL=''
            $scope.ebank_add.DAY_DEP_COMP_PER=''
            $scope.ebank_add.DAY_DEP_SAL=''
            $scope.ebank_add.DAY_DEP_SEC_FEN=''
            $scope.ebank_add.CREDIT_POOL=''
            $scope.ebank_add.INTER_SET_SAL=''
            $scope.ebank_add.SALE_VOC_SAL=''
            $scope.ebank_add.ADD_EFC_CURSAL=''
            $scope.ebank_add.ADD_FUNON_SAL=''
            $scope.ebank_add.PER_CAR_DANERSAL=''
            $scope.ebank_add.BUM_HOM_SAL=''
            $scope.ebank_add.OTHER_ACHI_SAL=''
            $scope.ebank_add.COMPRE_SAL=''
            $scope.ebank_add.LABOR_COMP_SAL=''
            $scope.ebank_add.PROV_FUND_SAL=''
            $scope.ebank_add.SAFE_FAN_SAL=''
            $scope.ebank_add.ALL_RISK_SAL=''
            $scope.ebank_add.BAD_LOAN_PERSAL=''
            $scope.ebank_add.FTP_ACH_SAL=''
            $scope.ebank_add.COUNT_COMPLE_SAL=''
            $scope.ebank_add.COUNT_COP_SSAL=''
            $scope.ebank_add.HP_FINA_SAL=''
            $scope.ebank_add.OTHER_SPEC_SAL1=''
            $scope.ebank_add.OTHER_SPEC_SAL2=''
            $scope.ebank_add.OTHER_SPEC_SAL3=''
            $scope.ebank_add.OTHER_SPEC_SAL4=''
            $scope.ebank_add.OTHER_SPEC_SAL5=''
            $scope.ebank_add.BRANCH_SECO_FEN1=''
            $scope.ebank_add.BRANCH_SECO_FEN2=''
            $scope.ebank_add.BRANCH_SECO_FEN3=''
            $scope.ebank_add.BRANCH_SECO_FEN4=''
            $scope.ebank_add.OTHER_ACH_WAGES=''
            $scope.ebank_add.OVER_WORK_SAL=''
            $scope.ebank_add.OTHER_SAL1_DUAN=''
            $scope.ebank_add.OTHER_SAL2=''
            $scope.ebank_add.OTHER_SAL3_WEI=''
            $scope.ebank_add.OTHER_SAL4_KE=''
            $scope.ebank_add.OTHER_SAL5_GE=''
            $scope.ebank_add.OTHER_SAL6=''
            $scope.ebank_add.OTHER_SAL7=''
            $scope.ebank_add.OTHER_SAL8=''
            $scope.ebank_add.QJ_BAD_LOAN_SAL=''
 
        }



    $scope.add_save = function (){
      element_add.modal('hide');
      $scope.custinfo_add.DATE_ID=$scope.custinfo_add.DATE_ID.format('YYYYMMDD')
      var nd={}
      nd={'custinfo_add':$scope.custinfo_add,'loan_add':$scope.loan_add,'ebank_add':$scope.ebank_add,'card_add':$scope.card_add,'dep_add':$scope.dep_add}
      console.log($scope.card_add)

     StaffSalNewService.add_save(nd).success(function (reps){
        alert(reps.data);
        $scope.search();
     })
    }


};





StaffSalReportController.$inject = ['$scope', '$rootScope', 'store','$filter', 'SqsReportService', 'permissionService','branchmanageService','StaffSalNewService'];

angular.module('YSP').service('StaffSalReportController', StaffSalReportController); 
