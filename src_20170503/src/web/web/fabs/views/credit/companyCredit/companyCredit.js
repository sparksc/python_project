ysp.controller('companyCreditController', function($scope, $rootScope, creditService,companyInformationService, PledgeService,CustomerSearchService ){
    $scope.guaranteeType = ['新发生', '展期', '借旧还新', '资产重组'];
    $scope.lendType = ['个人住房贷款'];
    $scope.tableMessage = '请点击查询';
    $scope.applicationStatus='新增申请';
    /* Table Operating Flag */
    /* Query Application */
    $scope.tableHead=['申请书号','客户名称', '业务品种', '主要担保方式', '申请状态', '币种', '金额', '申请人', '申请机构', '操作'];
    $scope.queryCond = {};
    $scope.tableData = [];
    $scope.queryApplication = function(){
        $scope.cust_type='company';
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
    /* Application Detail */
    $scope.applicationDetail = function(data){
        var cust_name = data.party.name;
        var tabName = cust_name+'的贷款申请';
        var htmlContent = '<div ng-include="'+'\'views/credit/pageDistribute/index.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':data.party,'application_status':data.application_status,'activity_status':data.activity_status,'applicationId':data.id,'product_page':data.product.product_page,'activity_page':data.activity_page});                       
        var applicationScope = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).scope();

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
    $scope.cust_search.cust_type='company'; 
    $scope.searchCustomer = function(){
        CustomerSearchService.queryroleparty($rootScope.user_session).success(function(resp){
            $scope.custTableData =  resp.data.party;

        });
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

        var cust_id = $scope.chosenCust.no;
        var cust_name = $scope.chosenCust.name;
        var tabName = cust_name+'的贷款申请';
        var htmlContent = '<div ng-include="'+'\'views/credit/companyCredit/companyCreditInfo.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':$scope.chosenCust});
    };

    $scope.custSearchCancel = function(){
        $scope.chosenCust = null;
        $scope.custTableData = {};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal('hide');
    };

   /*转入大表*/ 
    $scope.addToComm = function(code,applicationId){
        codes = ['330','330_1','331','331_1','332','332_1','333','333_1','523','523_1','525','525_1','527','527_1','529','540','540_1','541','541_1','369_1','368_1','370_1','341','341_1','342','343','536','117'];
        if(codes.indexOf(code) != -1 ){
             creditService.add_comm(applicationId).success(function(resp){
                  data = eval('(' + resp.data + ')');
                  alert(data.msg);
             });
        }else{
            alert('该笔贷款不属于转贷贷款，不能加入大表');
        }
    }    
})
ysp.controller('companyApplicationController', function($scope, store,$rootScope, creditService){
     $scope.pre_apply={};
     $scope.pre_apply.party_id=$scope.customer.id
     $scope.pre_apply.no=$scope.customer.no;
     $scope.pre_apply.name=$scope.customer.name;
     $scope.onSubmit = function(){
          creditService.save($scope.pre_apply).then(function(resp){
               var data = resp.data.data
               if(data.success){
                   alert('新增成功');
               }else{
                   alert(data.error)
               }  
          });
     }
    $scope.ltSelected = false;
    $scope.show_lt_modal = function(trigger_elem){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal']").modal("show");
    }
    $scope.choose_business_type = function(typeCode, typeName,typePage,guaType){
        $scope.pre_apply.loan_type_code = typeCode.replace(/(^\s*)|(\s*$)/g, "");
        $scope.pre_apply.loan_type = typeName.replace(/(^\s*)|(\s*$)/g, "");
        $scope.pre_apply.main_gua = guaType;
    }; 
    $scope.init_business_type = function(){
        var tree_html = '<ul id="loan_type_tree'+$scope.tabId+'" class="ztree"> </ul>';
        angular.element($('#tab_'+ $scope.tabId + '_content').find("div[name='for_lt_tree']")).append(tree_html);
        var setting = {};
        var Nodes=[];
        creditService.products('对公业务').success(function(resp){
            var data = resp.data;
            show_product(data)
            $.fn.zTree.init($("#loan_type_tree"+$scope.tabId), setting, Nodes);
        });
        function show_product(data){
            for(var i = 0 ; i < data.length ; ++i){
                var One = new Object();
                One.name = data[i].product_type.name;
                pro_arr = data[i].products;
                One.children=new Array();
                if(pro_arr.length>0){
                    for (var j = 0 ; j < pro_arr.length; ++j){
                        var Two = new Object();
                        Two.name=pro_arr[j].name;
                        Two.click="choose_business_type(this, '"+pro_arr[j].product_code+"', '"+Two.name+"','"+pro_arr[j].product_page+"', '"+pro_arr[j].main_gua_type+"')";
                        One.children.push(Two);
                    }
                }else{
                    One.click="choose_business_type(this, '"+data[i].product_code+"', '"+One.name+"','"+data[i].product_page+"')";
                }
                Nodes.push(One);
            }
        } 
    }
    $scope.init_business_type();
})
