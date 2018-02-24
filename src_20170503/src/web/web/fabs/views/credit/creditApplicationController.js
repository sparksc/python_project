ysp.controller('creditApplicationController', function($scope,store, $rootScope, creditService, CustomerSearchService, PledgeService ){
    $scope.guaranteeType = ['新发生', '展期', '借旧还新', '资产重组'];
    $scope.lendType = ['个人住房贷款'];
    $scope.tableMessage = '请点击查询';
    $scope.applicationStatus='新增申请';
    /* Table Operating Flag */
    /* Query Application */
    $scope.tableHead=['申请书号','客户名称', '业务品种', '主要担保方式', '申请状态', '币种', '金额', '申请人', '申请机构', '操作'];
    $scope.queryCond = [];
    $scope.tableData = [];
    $scope.queryApplication = function(){
        if($scope.applicationStatus_=='个人业务申请'){
               $scope.cust_type='person';
        }else{
               $scope.cust_type='company';
        }
        creditService.query(
                $scope.applicationStatus,
                $scope.cust_type,
                $scope.queryCond.cust_name,
                $scope.queryCond.guarantee_type,
                $scope.queryCond.lend_type,
                $scope.queryCond.ld_ratio,
                $scope.queryCond.start_date,
                $scope.queryCond.end_date
            ).success(function(resp){
                $scope.tableData = resp.data;
                if($scope.tableData.length > 0){
                    $scope.tableMessage=''; 
                }else{
                    $scope.tableMessage='未查询到数据'; 
                }
            }
        );
    };
    $scope.init = function(){
        $scope.queryApplication();
    };
    $scope.tableHead1=['抵质押物编号','抵质押物类型', '权利人名称', '登记人', '登记时机', '登记机构', '更新时间', '操作'];
    // 担保合同申请
    $scope.loca_index = "新增担保信息";

    $scope.guarantee_add = function(applicationStatus, $event){
        angular.element("#accordion").children(".collapse.in").find(".active").removeClass('active');
        angular.element(event.srcElement).addClass('active');
        var tabName = '新增担保信息';
        var eventObj = {
            'close':{
                'changeNav': "TODO:根据显示页面来显示Nav的active",
                'on':function(){
                    angular.element("#accordion").children(".collapse.in").find(".active").removeClass('active');
                    return true;
                }
            }
        };
        var htmlContent = '<div ng-include="'+'\'views/credit/GuaranteeInformation/guaranty/guarantee_add.html' +'\'"></div>';
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'applicationStatus':applicationStatus});
    };
    // 担保合同申请
    $scope.loca_index = "新增抵质押物信息";

    $scope.limits_add = function(applicationStatus, $event){
        angular.element("#accordion").children(".collapse.in").find(".active").removeClass('active');
        angular.element(event.srcElement).addClass('active');
        var tabName = '新增抵质押物信息';
        var eventObj = {
            'close':{
                'changeNav': "TODO:根据显示页面来显示Nav的active",
                'on':function(){
                    angular.element("#accordion").children(".collapse.in").find(".active").removeClass('active');
                    return true;
                }
            }
        };
        var htmlContent = '<div ng-include="'+'\'views/credit/GuaranteeInformation/guaranty/limits_add.html' +'\'"></div>';
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'applicationStatus':applicationStatus});
    };
     // 合同登记
   $scope.tableHead3=['最终审批意见流水号','客户名称', '业务品种', '币种', '批复金额', '主要担保方式', '最终审批意见类型', '操作'];
    $scope.loca_index = "新增合同信息";
    $scope.contract_add = function(){
        $scope.confirmBtnDisabled = true;
        if($scope.chosenCust == null){alert('请先选择客户');};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal('hide');

        var cust_id = $scope.chosenCust.cust_info.role_id;
        var cust_name = $scope.chosenCust.party.name;
        var tabName = cust_name+'的合同信息';
        var htmlContent = '<div ng-include="'+'\'views/credit/CreditManage/contract_add.html' +'\'"></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':$scope.chosenCust.party});
    };
	// 审查审批
   $scope.tableHead4=['申请流水号','客户名称', '业务品种', '发生类型', '币种', '金额', '当前流程', '操作'];
    $scope.loca_index = "新增审查审批";
    $scope.check_add = function(){
        $scope.confirmBtnDisabled = true;
        if($scope.chosenCust == null){alert('请先选择客户');};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal('hide');

        var cust_id = $scope.chosenCust.cust_info.role_id;
        var cust_name = $scope.chosenCust.party.name;
        var tabName = cust_name+'的审查审批信息';
        var htmlContent = '<div ng-include="'+'\'views/credit/CreditManage/check_add.html' +'\'"></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':$scope.chosenCust.party});
    };

    /* Application Detail */
    $scope.applicationDetail = function(applicationId,application_status){
        creditService.detail(applicationId).success(function(resp){
            var data = resp.data;
            var cust_name = resp.data.customer_name;
            var tabName = cust_name+'的贷款申请';
            var htmlContent = '<div ng-include="'+'\'views/credit/index.html' +'\'" ></div>';
            var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':data.party,'appli_status':application_status,'applicationId':applicationId,'product_page':data.product.product_page});                       
            var applicationScope = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).scope();
            //applicationScope['appli_status'] = application_status;
            //applicationScope['base_info_display'] = true;
            //applicationScope['applicationId'] = applicationId;
        });

    };

    /* New Application */
    $scope.newApplication = function(){
        var d = new Date();
        $scope.curr_date = d.getFullYear() + '-' + d.getMonth() + '-' + d.getDay();
        $scope.confirmBtnDisabled = false;
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal({backdrop: 'static',});
    };

    // Customer Search
    $scope.customerListTH = ['客户编号', '客户名称', '证件类型', '证件号码', '客户类型'];
    $scope.cust_search = { 'cust_name':'',};
    $scope.chosenCust = null;
    $scope.searchCustomer = function(){
        if($scope.applicationStatus_ == '个人业务申请'){

            CustomerSearchService.query('', $scope.cust_search.cust_name).success(function(resp){
                $scope.custTableData =  resp.data;
            });
        }
        else{
            CustomerSearchService.query_company('', $scope.cust_search.cust_name).success(function(resp){
                $scope.custTableData =  resp.data;
            });
        
        }
    };
    $scope.choseCustomer = function(cust, $event){
        $scope.chosenCust = cust;
        var obj = event.srcElement;
        var oTr = obj.parentNode;
        var tableObj = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content'))
                        .find("table[name='custListTable']")[0];
        for(var i=1; i<tableObj.rows.length; i++){ 
            tableObj.rows[i].style.backgroundColor = "";   
            tableObj.rows[i].tag = false;   
        }
        oTr.style.backgroundColor = "#87CEFA";   
    };

    $scope.custSearchConfirm = function(){
        $scope.confirmBtnDisabled = true;
        if($scope.chosenCust == null){alert('请先选择申请的客户');};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal('hide');

        var cust_id = $scope.chosenCust.cust_info.role_id;
        var cust_name = $scope.chosenCust.party.name;
        var tabName = cust_name+'的贷款申请';
        var htmlContent = '<div ng-include="'+'\'views/credit/index.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':$scope.chosenCust.party,'apply_type':$scope.applicationStatus_});
    };

    // 授信申请
    $scope.tableHead2=['授信编号','客户编号', '客户名称', '授信金额', '币种', '生效日', '金额', '申请人', '申请机构', '操作'];
    $scope.loca_index = "新增授信信息";
    $scope.credit_add = function(){
        $scope.confirmBtnDisabled = true;
        if($scope.chosenCust == null){alert('请先选择要授信的客户');};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal('hide');

        var cust_id = $scope.chosenCust.cust_info.role_id;
        var cust_name = $scope.chosenCust.party.name;
        var tabName = cust_name+'的授信信息';
        var htmlContent = '<div ng-include="'+'\'views/credit/CreditManage/credit_add.html' +'\'"></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':$scope.chosenCust.party});
    };
    //授信额度调整
    $scope.loca_index = "授信额度调整";

    $scope.credit_update = function(applicationStatus, $event){
        angular.element("#accordion").children(".collapse.in").find(".active").removeClass('active');
        angular.element(event.srcElement).addClass('active');
        var tabName = '授信额度调整';
        var eventObj = {
            'close':{
                'changeNav': "TODO:根据显示页面来显示Nav的active",
                'on':function(){
                    angular.element("#accordion").children(".collapse.in").find(".active").removeClass('active');
                    return true;
                }
            }
        };
        var htmlContent = '<div ng-include="'+'\'views/credit/CreditManage/credit_update.html' +'\'"></div>';
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'applicationStatus':applicationStatus});
    };


    $scope.custSearchCancel = function(){
        $scope.chosenCust = null;
        $scope.custTableData = {};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal('hide');
    };
    $scope.filter={};
/* 担保物管理 */
/*查询*/
    $scope.queryGuarantee = function(){
                    console.log($scope.filter);
          PledgeService.otherquery($scope.filter.gty_id,$scope.filter.pledge_type,$scope.filter.gty_cus_name).success(function(resp){
                  $scope.tableData = resp.data;
                  if($scope.tableData.length > 0){
                      $scope.tableMessage='';
                  }else{
                      $scope.tableMessage='未查询到数据';
                  }
              }
          );
    };
/*上传清单按钮*/
    $scope.showInfo = function(info){
        var infos = ['抵押-动产','抵押-设备','抵押-设备+动产','质押-银行承兑汇票'];
        return infos.indexOf(info) != -1;
    }
/*删除*/
    $scope.delGuarantee = function(gty_id){
       if(confirm("确定删除吗？")){
           PledgeService.deleteGTY(gty_id).success(function(){
               $scope.queryGuarantee();
        });
       }
    };
/*详情*/    
    $scope.detailsGuarantee = function(pledge_type,gty_id){
        PledgeService.otherquery(gty_id).success(function(resp){
        resp.data[0].ins_due_date = new Date(resp.data[0].ins_due_date);
        var data = resp.data;
        var tabName = pledge_type;
        var url = 'index.html';
         if (pledge_type == '质押-其他'){ url='pawn_other_a.html'}
         if (pledge_type == '质押-单位定期存单'){ url='pawn_stub_a.html'}
         if (pledge_type == '质押-本行理财产品'){ url='pawn_finance_a.html'}
         if (pledge_type == '质押-账户资金'){ url='pawn_saving_a.html'}
         if (pledge_type == '质押-银行承兑汇票'){ url='pawn_accp_a.html'}
         if (pledge_type == '质押-应收账款'){ url='pawn_acc_rec_a.html'}
         if (pledge_type == '抵押-动产'){ url='mrge_movable_a.html'}
         if (pledge_type == '抵押-房屋所有权'){ url='mrge_building_a.html'}
         if (pledge_type == '抵押-土地使用权'){ url='mrge_land_a.html'}
         if (pledge_type == '抵押-设备'){ url='mrge_eqp_a.html'}
         if (pledge_type == '抵押-设备+动产'){ url='mrge_eqp_movable_a.html'}
         if (pledge_type == '抵押-交通工具'){ url='mrge_vch_a.html'}
         if (pledge_type == '抵押-其他'){ url='mrge_other_a.html'}	
         if (pledge_type == '质押-个人定期存单'){ url='pawn_per_stub_a.html'}		 
        var divName = 'otherForm'
        var controller='guarantyController'
        var htmlContent = '<div  ng-include="'+'\'views/credit/GuaranteeInformation/pledge/'+url+'\'" ng-controller="pledgeUpController"></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'modal_data':data[0]});
        });
    };
//清单上传
    $scope.addlist = function(gty_id){
            var token = store.getSession("token");
            var file = $('#myForm').find('input[name="file"]').prop('files');
             console.log(file);
            var form = new FormData();
            if(file[0] == undefined){
                alert('请选择上传文件');
                return;
            }
            form.append('file',file[0]);
            form.append('gty_id',gty_id );
        $.ajax({
            type: "POST",
            url : base_url+"/pledge/upload/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("x-session-token", token);
            },
            success: function(msg){
                if(msg.data == 'err'){
                    alert('文件格式有误，上传失败')
                }else{
                    alert("导入成功");
                }
            }
        });
    };
/*质押-其他 修改*/
    $scope.otherUpdate = function(){
    PledgeService.otherupdate($scope.modal_data);
    };
 /*质押-存单 修改*/
     $scope.stubUpdate = function(){
     PledgeService.stubupdate($scope.modal_data);
     };
 /*质押-saving 修改*/
     $scope.savingUpdate = function(){
     PledgeService.savingupdate($scope.modal_data);
     };
 /*质押-nd 修改*/
     $scope.ndUpdate = function(){
     PledgeService.ndupdate($scope.modal_data);
     };
 /*质押-ins 修改*/
     $scope.insUpdate = function(){
     PledgeService.insupdate($scope.modal_data);
     };
 /*质押-crd 修改*/
     $scope.crdUpdate = function(){
     PledgeService.crdupdate($scope.modal_data);
     };
 /*质押-fe_saving 修改*/
     $scope.fe_savingUpdate = function(){
     PledgeService.fe_savingupdate($scope.modal_data);
     };
 /*质押-ware_lst 修改*/
     $scope.ware_lstUpdate = function(){
     PledgeService.ware_lstupdate($scope.modal_data);
     };
 /*质押-do 修改*/
     $scope.doUpdate = function(){
     PledgeService.doupdate($scope.modal_data);
     };
 /*质押-vch 修改*/
     $scope.vchUpdate = function(){
     PledgeService.vchupdate($scope.modal_data);
     };
 /*质押-vch_qlf 修改*/
     $scope.vch_qlfUpdate = function(){
     PledgeService.vch_qlfupdate($scope.modal_data);
     };
 /*质押-bond 修改*/
     $scope.bondUpdate = function(){
     PledgeService.bondupdate($scope.modal_data);
     };
 /*质押-ipo_int 修改*/
     $scope.ipo_intUpdate = function(){
     PledgeService.ipo_intupdate($scope.modal_data);
     };
 /*质押-non_ipo_int 修改*/
     $scope.non_ipo_intUpdate = function(){
     PledgeService.non_ipo_intupdate($scope.modal_data);
     };
 /*质押-acc_rec 修改*/
     $scope.acc_recUpdate = function(){
     PledgeService.acc_recupdate($scope.modal_data);
     };
 /*质押-cvrg 修改*/
     $scope.cvrgUpdate = function(){
     PledgeService.cvrgupdate($scope.modal_data);
     };
 /*质押-accp 修改*/
     $scope.accpUpdate = function(){
     PledgeService.accpupdate($scope.modal_data);
     };
 /*质押-bill 修改*/
     $scope.billUpdate = function(){
     PledgeService.billupdate($scope.modal_data);
     };
     
	 
})

